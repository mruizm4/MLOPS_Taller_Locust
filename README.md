# Taller Locust - Inference API con FastAPI y MLflow

## Descripción del proyecto
Este repositorio contiene una API de inferencia construida con FastAPI que consume un modelo previamente entrenado desde MLflow. La API se despliega en Docker y se prueba con Locust para evaluar su comportamiento bajo cargas altas.

## Componentes
- `docker-compose.yaml`: Orquesta la API de inferencia publicada en Docker Hub y ejecuta el servicio de pruebas de carga con Locust.
- `locustfile.py`: Define el escenario de carga para generar usuarios concurrentes y medir el rendimiento de la API.
- `Dockerfile.locust`: Construye la imagen de Locust para el test de carga.

## Imagen de Docker publicada
- Imagen de inferencia: `karabaharesu/apirepo:inference`
- Esta imagen levanta la API FastAPI que realiza inferencia usando el modelo alojado en MLflow.

## Configuración usada en `docker-compose.yaml`
El servicio `api` se configura con:
- 3 réplicas
- Límite de CPU: `4`
- Límite de memoria: `10000M`
- Reserva de CPU: `2`
- Reserva de memoria: `5000M`

El servicio `locust` se conecta a la API en `http://api:8000` y expone la interfaz web en `http://localhost:8089`.

## Resultados de la prueba de carga
1. Recursos mínimos para soportar 10.000 usuarios:
   - En las pruebas se usó la configuración de `4 CPUs` y `10 GB` de memoria como límite, con reservas de `2 CPUs` y `5 GB`.
   - La API fue capaz de atender el aumento progresivo hasta 10.000 usuarios concurrentes.
   - Sin embargo, al mantener la carga por varios minutos comenzaron a aparecer errores de `timeout` y `ConnectionResetError`.
   - Esto sugiere que la saturación no fue por falta de recursos del host, sino por la capacidad de mantener colas de solicitudes prolongadas en un único contenedor.

2. Incremento de réplicas en Docker Compose:
   - Una instancia única tiende a saturarse y generar errores de tiempo de espera cuando se sostiene una carga de 10.000 usuarios.
   - Múltiples réplicas permiten distribuir la carga entre contenedores, reduciendo la cola de peticiones en cada uno.
   - El comportamiento mejora notablemente con escalado horizontal, ya que cada réplica atiende menos solicitudes simultáneas.

3. ¿Es posible reducir más los recursos?
   - Sí, es posible disminuir los recursos asignados por contenedor si se incrementa el número de réplicas.
   - Pero si se reducen demasiado, cada réplica puede volverse inestable y aumentar los errores de conexión.
   - El balance adecuado es asignar recursos mínimos suficientes por réplica y compensar la carga con más instancias.

4. Mayor cantidad de peticiones soportadas:
   - Con una sola réplica, la API alcanzó 10.000 usuarios concurrentes, pero no pudo mantener esa carga de forma estable durante mucho tiempo.
   - Con múltiples réplicas, la capacidad aumentó y la estabilidad mejoró, acercándose más al objetivo de 10.000 usuarios sostenidos.
   - La mayor cantidad soportada depende directamente del número de réplicas y del balanceo de carga.

5. Diferencia entre una instancia y múltiples instancias:
   - Una instancia: funciona inicialmente, pero se satura con cargas altas y genera timeouts y errores de conexión.
   - Múltiples instancias: distribuyen mejor la carga, mejoran la estabilidad y permiten escalar de forma más efectiva.

## Conclusión general (MLOps)
El experimento muestra que el verdadero límite no está en los recursos físicos del host, sino en la arquitectura de despliegue. Para cargas sostenidas de 10.000 usuarios, escalar horizontalmente con múltiples réplicas es más efectivo que simplemente aumentar CPU o memoria en una sola instancia.

## Uso
1. Levantar la aplicación y el test de carga:
```bash
docker compose up --build
```
2. Acceder a Locust en `http://localhost:8089`.
3. Configurar el host de prueba como `http://api:8000` y ejecutar el escenario.

## Notas
- Asegúrate de que MLflow y el backend de almacenamiento S3 estén disponibles en los endpoints configurados por el contenedor.
- La prueba de carga se realiza con Locust y permite observar el comportamiento de la API bajo incremento progresivo de usuarios.

