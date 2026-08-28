from kubernetes import client, config
from kubernetes.stream import stream

def load_kubernetes():
    config.load_kube_config()


def get_pod_logs(namespace: str, pod_name: str, tail_lines: int = 20):

    load_kubernetes()

    v1 = client.CoreV1Api()

    logs = v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace,
        tail_lines=tail_lines,
    )

    if isinstance(logs, bytes):
        return logs.decode("utf-8")

    if isinstance(logs, str) and logs.startswith("b'"):
        return bytes(logs[2:-1], "utf-8").decode("unicode_escape")

    return logs

def get_pod_status(namespace: str, pod_name: str):
    load_kubernetes()

    v1 = client.CoreV1Api()

    pod = v1.read_namespaced_pod(
        name=pod_name,
        namespace=namespace,
    )

    return {
        "pod": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "phase": pod.status.phase,
        "ready": all(
            condition.status == "True"
            for condition in (pod.status.conditions or [])
            if condition.type == "Ready"
        ),
        "restart_count": sum(
            container.restart_count or 0
            for container in (pod.status.container_statuses or [])
        ),
    }


def get_pod_metrics(namespace: str, pod_name: str):
    load_kubernetes()

    custom_api = client.CustomObjectsApi()

    metrics = custom_api.get_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods",
        name=pod_name,
    )

    return {
        "pod": pod_name,
        "namespace": namespace,
        "containers": [
            {
                "name": container["name"],
                "cpu": container["usage"].get("cpu"),
                "memory": container["usage"].get("memory"),
            }
            for container in metrics.get("containers", [])
        ],
    }


# ---------------------------------------------------------
# Diagnostic tools
# ---------------------------------------------------------

def get_service(namespace: str, service_name: str):
    """
    Get Kubernetes Service configuration.
    """

    load_kubernetes()

    v1 = client.CoreV1Api()

    service = v1.read_namespaced_service(
        name=service_name,
        namespace=namespace,
    )

    return {
        "service": service.metadata.name,
        "namespace": service.metadata.namespace,
        "type": service.spec.type,
        "cluster_ip": service.spec.cluster_ip,
        "ports": [
            {
                "port": port.port,
                "target_port": str(port.target_port),
                "protocol": port.protocol,
            }
            for port in (service.spec.ports or [])
        ],
        "selector": service.spec.selector,
    }


def get_service_endpoints(namespace: str, service_name: str):
    """
    Get the current endpoints behind a Kubernetes Service.
    """

    load_kubernetes()

    v1 = client.CoreV1Api()

    endpoints = v1.read_namespaced_endpoints(
        name=service_name,
        namespace=namespace,
    )

    addresses = []

    for subset in endpoints.subsets or []:

        for address in subset.addresses or []:

            for port in subset.ports or []:

                addresses.append({
                    "ip": address.ip,
                    "port": port.port,
                    "protocol": port.protocol,
                })

    return {
        "service": service_name,
        "namespace": namespace,
        "endpoints": addresses,
    }

def check_tcp_connectivity(
    namespace: str,
    pod_name: str,
    host: str,
    port: int,
):
    load_kubernetes()

    v1 = client.CoreV1Api()

    command = [
        "python",
        "-c",
        (
            "import socket; "
            "s=socket.socket(); "
            "s.settimeout(3); "
            f"s.connect(('{host}', {port})); "
            "print('TCP connection successful'); "
            "s.close()"
        ),
    ]

    result = stream(
        v1.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        container="call-processing",
        command=command,
        stderr=True,
        stdin=False,
        stdout=True,
        tty=False,
    )

    result = result.strip()

    if "ConnectionRefusedError" in result:
        return {
            "host": host,
            "port": port,
            "reachable": False,
            "error": "Connection refused",
        }

    if "TimeoutError" in result or "timed out" in result.lower():
        return {
            "host": host,
            "port": port,
            "reachable": False,
            "error": "Connection timeout",
        }

    if "socket.gaierror" in result:
        return {
            "host": host,
            "port": port,
            "reachable": False,
            "error": "DNS resolution failure",
        }

    if "TCP connection successful" in result:
        return {
            "host": host,
            "port": port,
            "reachable": True,
            "result": "TCP connection successful",
        }

    return {
        "host": host,
        "port": port,
        "reachable": False,
        "error": "Unknown TCP connectivity failure",
        "details": result,
    }