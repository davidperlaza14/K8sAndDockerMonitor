# Docker and Kubernetes Container Monitoring and Logging System

This project is a real-time monitoring and alert generation application for Docker and Kubernetes containers. The application allows real-time visualization of key metrics (such as CPU and memory usage), generates alerts when certain thresholds are reached, and stores logs for later analysis. It also supports monitoring multiple Kubernetes clusters.

## Main Features

- **Real-Time Visualization:** Real-time monitoring of CPU and memory usage for Docker containers and Kubernetes pods.
- **Alert Generation:** Automatic alerts based on predefined thresholds for CPU and memory usage.
- **Log Storage:** Events and alerts are logged in files for later analysis.
- **Support for Multiple Clusters:** The application allows selecting and monitoring different Kubernetes clusters using kubeconfig files.
- **Report Generation:** Ability to generate detailed reports with recorded metrics and incidents.

## Prerequisites

Before installing and running the application, ensure you meet the following requirements:

- **Python 3.8 or higher**
- **Docker** installed on your system
- **Kubernetes** (optional, if you will be monitoring Kubernetes clusters)
- **Kubeconfig** of the Kubernetes clusters you want to monitor
- **Python Libraries** listed in the `requirements.txt` file

## Installation

Follow these steps to install and run the application in your local environment:

1. **Clone the Repository**

```bash
git clone https://github.com/your_username/container-monitoring.git
cd container-monitoring

   ```


## Usage
Once the dependencies are installed and Docker and Kubernetes are configured, you can run the application as follows:
 
1. **Run the Application**
    ```bash
     python3 gui_monitor.py
    ```
   The graphical interface will appear on the screen, displaying container metrics and allowing the configuration of thresholds for alerts.

2. **Monitoring Docker**
    1. Select the Docker tab in the application.
    2. The application will display a list of running containers along with their real-time metrics (CPU, memory, etc.).
    3. Adjust the alert thresholds as needed. Alerts will be generated automatically if the defined thresholds are reached.


2.  **Monitoring Kubernetes**
    1. Select the Kubernetes tab in the application.
    2. Load a kubeconfig file to access the available clusters.
    3. The application will display the pods and their real-time metrics.
    4. Configure thresholds to generate alerts if the pods exceed certain resource usage limits.

## Log Analysis
The generated events and alerts are recorded in log files. These files can be manually reviewed for later analysis. The logs are stored in the logs/ directory within the project.


## Report Generation
We will soon implement the functionality to generate detailed reports with all the recorded metrics and alerts. These reports can be exported in formats such as CSV or PDF.


## Contributing

If you want to contribute to this project:
    
    1. Fork the repository.
    2. Create a new branch for your feature (git checkout -b feature/new-feature).
    3. Make the necessary changes and commit them with descriptive messages.
    4. Submit a pull request for review.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
