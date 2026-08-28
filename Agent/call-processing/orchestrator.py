from tools import (
    get_pod_status,
    get_pod_logs,
    get_pod_metrics,
)

from llm_client import analyze_incident


NAMESPACE = "911-platform"
POD_NAME = "call-processing-84c75748-9m4db"


def investigate(namespace=NAMESPACE, pod_name=POD_NAME):

    print("=== INCIDENT INVESTIGATION ===")

    # 1. Service health
    status = get_pod_status(
        namespace=namespace,
        pod_name=pod_name,
    )

    print("\n[1] SERVICE HEALTH")
    print(status)

    # 2. Application logs
    logs = get_pod_logs(
        namespace=namespace,
        pod_name=pod_name,
        tail_lines=20,
    )

    print("\n[2] APPLICATION ACTIVITY")
    print(logs)

    # 3. Resource metrics
    metrics = get_pod_metrics(
        namespace=namespace,
        pod_name=pod_name,
    )

    print("\n[3] RESOURCE HEALTH")
    print(metrics)

    # 4. AI analysis
    print("\n[4] AI ANALYSIS")

    analysis = analyze_incident(
        status=status,
        logs=logs,
        metrics=metrics,
    )

    print(analysis)

    return {
        "namespace": namespace,
        "pod": pod_name,
        "status": status,
        "logs": logs,
        "metrics": metrics,
        "analysis": analysis,
    }


if __name__ == "__main__":
    investigate()