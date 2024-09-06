from kubernetes import client, config
import logging

# Configuración del registro de logs
logging.basicConfig(filename='kubernetes_metrics.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_kubernetes_pods():
    config.load_kube_config()  # Carga la configuración del clúster
    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        pod_info = (f"Pod Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}, "
                    f"Status: {pod.status.phase}")
        print(pod_info)
        logging.info(pod_info)

if __name__ == "__main__":
    monitor_kubernetes_pods()
