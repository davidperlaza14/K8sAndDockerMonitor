import docker
import time
import logging

# Configuración del registro de logs
logging.basicConfig(filename='container_metrics.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Definimos los umbrales para las alertas
CPU_THRESHOLD = 50000000  # Ejemplo: Umbral de CPU en nanosegundos
MEMORY_THRESHOLD = 50  # Umbral de memoria en porcentaje

def monitor_container_metrics():
    client = docker.from_env()
    containers = client.containers.list()

    for container in containers:
        logging.info(f"Monitoreando contenedor: {container.name} (ID: {container.short_id})")
        
        # Monitoreamos las métricas del contenedor en tiempo real
        for stats in container.stats(stream=True):
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            
            # Convertimos el uso de memoria en porcentaje
            memory_percentage = (memory_usage / memory_limit) * 100
            
            # Imprimimos y registramos las métricas
            log_message = (f"Uso de CPU: {cpu_usage} | Uso de Memoria: {memory_usage} bytes "
                           f"({memory_percentage:.2f}%)")
            print(log_message)
            logging.info(log_message)
            
            # Comprobamos si las métricas superan los umbrales
            if cpu_usage > CPU_THRESHOLD:
                alert_message = (f"ALERTA: El contenedor {container.name} ha excedido el umbral de CPU.")
                print(alert_message)
                logging.warning(alert_message)
            
            if memory_percentage > MEMORY_THRESHOLD:
                alert_message = (f"ALERTA: El contenedor {container.name} ha excedido el umbral de memoria "
                                 f"({MEMORY_THRESHOLD}%).")
                print(alert_message)
                logging.warning(alert_message)

            # Dormimos un poco para no sobrecargar el sistema
            time.sleep(2)

if __name__ == "__main__":
    monitor_container_metrics()
