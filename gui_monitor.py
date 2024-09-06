import tkinter as tk
from tkinter import messagebox, filedialog  # Para alertas y diálogos de selección de archivos
import docker
from kubernetes import client, config
import time
import logging

# Configuración inicial de Docker
docker_client = docker.from_env()

# Configuración del sistema de logs
logging.basicConfig(
    filename='monitoring_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Contenedores")

        # Variables para los umbrales
        self.memory_threshold_var = tk.DoubleVar(value=80)
        self.cpu_threshold_var = tk.DoubleVar(value=80)

        # Crear una etiqueta para el título
        self.title_label = tk.Label(root, text="Monitoreo de Contenedores Docker y Kubernetes", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Crear una etiqueta y campo para el umbral de memoria
        self.memory_threshold_label = tk.Label(root, text="Umbral de Memoria (%):")
        self.memory_threshold_label.pack()
        self.memory_threshold_entry = tk.Entry(root, textvariable=self.memory_threshold_var)
        self.memory_threshold_entry.pack(pady=5)

        # Crear una etiqueta y campo para el umbral de CPU
        self.cpu_threshold_label = tk.Label(root, text="Umbral de CPU (%):")
        self.cpu_threshold_label.pack()
        self.cpu_threshold_entry = tk.Entry(root, textvariable=self.cpu_threshold_var)
        self.cpu_threshold_entry.pack(pady=5)

        # Selección del clúster de Kubernetes
        self.cluster_label = tk.Label(root, text="Seleccione el Clúster de Kubernetes:")
        self.cluster_label.pack(pady=5)
        self.cluster_button = tk.Button(root, text="Cargar Kubeconfig", command=self.load_kubeconfig)
        self.cluster_button.pack(pady=5)

        # Crear un área de texto para mostrar los datos
        self.text_area = tk.Text(root, height=20, width=80)
        self.text_area.pack(pady=10)

        # Crear un botón para actualizar los datos manualmente
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_data)
        self.update_button.pack(pady=10)

        # Variable para almacenar la configuración de Kubernetes
        self.k8s_client = None

        # Iniciar el hilo para la actualización automática
        self.auto_update()

    def load_kubeconfig(self):
        # Función para seleccionar un archivo kubeconfig y cargar la configuración del clúster
        kubeconfig_path = filedialog.askopenfilename(title="Seleccione el archivo kubeconfig")
        if kubeconfig_path:
            try:
                config.load_kube_config(config_file=kubeconfig_path)
                self.k8s_client = client.CoreV1Api()
                messagebox.showinfo("Éxito", f"Kubeconfig cargado exitosamente: {kubeconfig_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el kubeconfig: {str(e)}")
    
    def update_data(self):
        # Limpiar el área de texto
        self.text_area.delete(1.0, tk.END)

        # Obtener los umbrales definidos por el usuario
        memory_threshold = self.memory_threshold_var.get()
        cpu_threshold = self.cpu_threshold_var.get()

        # Obtener las métricas de Docker
        self.text_area.insert(tk.END, "Métricas de Contenedores Docker:\n")
        containers = docker_client.containers.list()
        for container in containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percentage = (memory_usage / memory_limit) * 100

            if memory_percentage > memory_threshold:
                alert_message = f"Alerta: El contenedor {container.name} ha superado el umbral de memoria.\n"
                alert_message += f"Uso de Memoria: {memory_percentage:.2f}% (Umbral: {memory_threshold}%)"
                self.show_alert(alert_message)
                logging.warning(alert_message)

            container_info = (f"Contenedor: {container.name} (ID: {container.short_id})\n"
                              f"  Uso de CPU: {cpu_usage} | Uso de Memoria: {memory_usage} bytes "
                              f"({memory_percentage:.2f}%)\n\n")
            self.text_area.insert(tk.END, container_info)

        # Verificar si se ha cargado un clúster Kubernetes
        if self.k8s_client:
            self.text_area.insert(tk.END, "Métricas de Pods de Kubernetes:\n")
            pods = self.k8s_client.list_pod_for_all_namespaces()
            for pod in pods.items:
                pod_info = (f"Pod Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}, "
                            f"Status: {pod.status.phase}\n")

                if pod.status.phase != "Running":
                    alert_message = f"Alerta: El Pod {pod.metadata.name} está en estado {pod.status.phase}."
                    self.show_alert(alert_message)
                    logging.warning(alert_message)

                self.text_area.insert(tk.END, pod_info)
        else:
            self.text_area.insert(tk.END, "No se ha cargado ningún clúster de Kubernetes.\n")

    def show_alert(self, message):
        # Función para mostrar una alerta emergente
        messagebox.showwarning("Alerta del Sistema de Monitoreo", message)

    def auto_update(self):
        # Actualizar los datos cada 5 segundos automáticamente
        self.update_data()
        self.root.after(5000, self.auto_update)


def start_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()




































""" import tkinter as tk
import docker
from kubernetes import client, config
import time

# Umbrales de alerta
MEMORY_THRESHOLD = 80  # 80% de uso de memoria
CPU_THRESHOLD = 80  # 80% de uso de CPU (esto puede ajustarse según sea necesario)

# Configuración inicial de Docker
docker_client = docker.from_env()

# Cargar configuración del clúster de Kubernetes
config.load_kube_config()
k8s_client = client.CoreV1Api()

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Contenedores")

        # Crear una etiqueta para el título
        self.title_label = tk.Label(root, text="Monitoreo de Contenedores Docker y Kubernetes", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Crear un área de texto para mostrar los datos
        self.text_area = tk.Text(root, height=20, width=80)
        self.text_area.pack(pady=10)

        # Crear un botón para actualizar los datos manualmente
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_data)
        self.update_button.pack(pady=10)

        # Iniciar el hilo para la actualización automática
        self.auto_update()

    def update_data(self):
        # Limpiar el área de texto
        self.text_area.delete(1.0, tk.END)

        # Obtener las métricas de Docker
        self.text_area.insert(tk.END, "Métricas de Contenedores Docker:\n")
        containers = docker_client.containers.list()
        for container in containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percentage = (memory_usage / memory_limit) * 100

            alert_color = "black"  # Color predeterminado
            if memory_percentage > MEMORY_THRESHOLD:
                alert_color = "red"
            elif memory_percentage > 50:
                alert_color = "yellow"

            container_info = (f"Contenedor: {container.name} (ID: {container.short_id})\n"
                              f"  Uso de CPU: {cpu_usage} | Uso de Memoria: {memory_usage} bytes "
                              f"({memory_percentage:.2f}%)\n\n")

            # Insertar el texto y aplicar color si es necesario
            self.text_area.insert(tk.END, container_info)
            self.text_area.tag_add("alert", "end-2c linestart", "end-2c")
            self.text_area.tag_config("alert", foreground=alert_color)

        # Obtener las métricas de Kubernetes
        self.text_area.insert(tk.END, "Métricas de Pods de Kubernetes:\n")
        pods = k8s_client.list_pod_for_all_namespaces()
        for pod in pods.items:
            pod_info = (f"Pod Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}, "
                        f"Status: {pod.status.phase}\n")

            alert_color = "black"  # Color predeterminado para pods
            if pod.status.phase != "Running":
                alert_color = "red"

            # Insertar el texto y aplicar color si es necesario
            self.text_area.insert(tk.END, pod_info)
            self.text_area.tag_add("alert", "end-2c linestart", "end-2c")
            self.text_area.tag_config("alert", foreground=alert_color)

    def auto_update(self):
        # Actualizar los datos cada 5 segundos automáticamente
        self.update_data()
        self.root.after(5000, self.auto_update)  # Actualización cada 5 segundos


def start_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()


"""






"""
import tkinter as tk
import docker
from kubernetes import client, config
import time
import threading

# Configuración inicial de Docker
docker_client = docker.from_env()

# Cargar configuración del clúster de Kubernetes
config.load_kube_config()
k8s_client = client.CoreV1Api()

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Contenedores")

        # Crear una etiqueta para el título
        self.title_label = tk.Label(root, text="Monitoreo de Contenedores Docker y Kubernetes", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Crear un área de texto para mostrar los datos
        self.text_area = tk.Text(root, height=20, width=80)
        self.text_area.pack(pady=10)

        # Crear un botón para actualizar los datos manualmente
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_data)
        self.update_button.pack(pady=10)

        # Iniciar el hilo para la actualización automática
        self.auto_update()

    def update_data(self):
        # Limpiar el área de texto
        self.text_area.delete(1.0, tk.END)

        # Obtener las métricas de Docker
        self.text_area.insert(tk.END, "Métricas de Contenedores Docker:\n")
        containers = docker_client.containers.list()
        for container in containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percentage = (memory_usage / memory_limit) * 100

            container_info = (f"Contenedor: {container.name} (ID: {container.short_id})\n"
                              f"  Uso de CPU: {cpu_usage} | Uso de Memoria: {memory_usage} bytes "
                              f"({memory_percentage:.2f}%)\n\n")
            self.text_area.insert(tk.END, container_info)

        # Obtener las métricas de Kubernetes
        self.text_area.insert(tk.END, "Métricas de Pods de Kubernetes:\n")
        pods = k8s_client.list_pod_for_all_namespaces()
        for pod in pods.items:
            pod_info = (f"Pod Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}, "
                        f"Status: {pod.status.phase}\n")
            self.text_area.insert(tk.END, pod_info)

    def auto_update(self):
        # Actualizar los datos cada 5 segundos automáticamente
        self.update_data()
        self.root.after(5000, self.auto_update)  # Actualización cada 5 segundos


def start_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
"""