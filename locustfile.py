from locust import HttpUser, task, between

class UsuarioDeCarga(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hacer_inferencia(self):
        # Los parámetros deben ir en la query string porque tu endpoint usa Query(...)
        params = {
            "models": ["TREE", "KNN", "SVM"],
            "culmen_length_mm": 39,
            "culmen_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3700,
            "island": "Dream",
            "sex": "Male"
        }

        # Enviar la petición POST al endpoint /predict_endpoint
        response = self.client.post("/predic", params=params)

        # Validación opcional de la respuesta
        if response.status_code != 200:
            print("❌ Error en la inferencia:", response.text)
        else:
            print("✅ Respuesta:", response.text)
