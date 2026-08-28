from tools import (
    get_pod_logs,
    get_pod_status,
    get_pod_metrics,
)


pod_name = "call-processing-84c75748-9m4db"
namespace = "911-platform"

print("POD STATUS")
print(get_pod_status(namespace, pod_name))

print("\nPOD METRICS")
print(get_pod_metrics(namespace, pod_name))

print("\nPOD LOGS")
print(get_pod_logs(
    namespace,
    pod_name,
    tail_lines=20,
))