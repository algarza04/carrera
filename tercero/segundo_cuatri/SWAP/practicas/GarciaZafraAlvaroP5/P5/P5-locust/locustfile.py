# Importa las siguientes librerías de Locust
#   -HttpUser servirá para definir un usuario que realizará las peticiones
#   -TaskSet servirá para definir un conjunto de tareas que realizará el usuario
#   -task servirá para definir una tarea que realizará el usuario   
#   -between servirá para definir el tiempo de espera entre tareas
from locust import HttpUser, TaskSet, task, between

# Simula un usuario realizando tareas en el CMS y desactiva la verificación del certificado SSL
from locust import HttpUser, TaskSet, task, between

class P5_algarza04(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        # Hacer login en index.php?action=login
        response = self.client.post(
            "index.php?action=login",
            json={"username": "testuser", "password": "testpass"},
            verify=False
        )
        if response.status_code == 200:
            token = response.json().get("token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task
    def load_index(self):
        # Cargar la página principal
        self.client.get("index.php", verify=False)

# Se definen dos tipos de usuarios:
#   -P5_usuarios_https: usuario que realiza peticiones a través de HTTPS
#   -P5_usuarios_http: usuario que realiza peticiones a través de HTTP
# Ambos usuarios tienen un tiempo de espera entre 1 y 5 segundos entre tareas e indica las tareas que debe realizar
class P5_usuarios_https(HttpUser):
    host = "https://192.168.10.50:443"
    tasks = [P5_algarza04]
    wait_time = between(1, 5)
    
class P5_usuarios_http(HttpUser):
    host = "http://192.168.10.50:80"
    tasks = [P5_algarza04]
    wait_time = between(1, 5)