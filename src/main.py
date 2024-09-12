import os
import subprocess


def update_paths(project_root):
    # Liste des fichiers à mettre à jour
    files_to_update = [
        "src/airflow/docker-compose.yaml",
        "src/prometheus-grafana/docker-compose.yml",
        "src/airflow/dags/DAG_prod.py"
        # Ajoutez ici tous les fichiers nécessitant une mise à jour des chemins
    ]

    for file_path in files_to_update:
        with open(file_path, 'r') as file:
            content = file.read()

        updated_content = content.replace('/home/jo/PycharmProjects/projet_DST_satisfaction_client', project_root)

        with open(file_path, 'w') as file:
            file.write(updated_content)


def install_dependencies():
    subprocess.check_call([os.sys.executable, "setup.py", "install"])


def is_service_running(service_name):
    result = subprocess.run(["docker", "compose", "ps", "-q", service_name], capture_output=True, text=True)
    return bool(result.stdout.strip())


def stop_services():
    subprocess.run(["docker", "compose", "down"], cwd="src/airflow")
    subprocess.run(["docker", "compose", "down"], cwd="src/prometheus-grafana")


def start_services():
    # Appliquer les permissions nécessaires pour Docker et PostgreSQL
    subprocess.run(["sudo", "chmod", "666", "/var/run/docker.sock"])
    subprocess.run(["sudo", "chmod", "666", "/var/run/postgresql/.s.PGSQL.5432"])

    subprocess.run(["docker", "compose", "up", "-d"], cwd="src/airflow")
    subprocess.run(["docker", "compose", "-f", "docker-compose.yml", "up", "-d"], cwd="src/prometheus-grafana")


if __name__ == "__main__":
    project_root = os.getcwd()
    update_paths(project_root)
    install_dependencies()

    if is_service_running("airflow") or is_service_running("prometheus-grafana"):
        stop_services()

    start_services()
