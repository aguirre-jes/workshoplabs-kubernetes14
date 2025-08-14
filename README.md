# Workshop de Orquestación con Kubernetes (Minikube)

## Introducción

Este repositorio contiene un workshop práctico de orquestación de contenedores usando Kubernetes, empleando Minikube como entorno de laboratorio. El objetivo principal es que los participantes comprendan a fondo el ciclo de desarrollo y las estrategias de despliegue disponibles en Kubernetes, desde el entorno local hasta ambientes productivos.

## Uso de Devcontainer

Para facilitar la experiencia y asegurar la compatibilidad entre usuarios de Windows, Linux y macOS, este workshop utiliza un entorno de desarrollo basado en Devcontainer. Esto permite que todos los participantes trabajen en un entorno homogéneo, sin importar su sistema operativo.

### Requerimientos para ejecutar Devcontainer

- Tener instalado [Docker](https://docs.docker.com/get-docker/) en tu sistema.
- Tener instalado [Visual Studio Code](https://code.visualstudio.com/).
- Instalar la extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) en VS Code.

### Instrucciones para levantar el Devcontainer con VS Code

1. Clona este repositorio:

```shell
git clone https://github.com/aguirre-jes/workshoplabs-kubernetes14.git
```

2. Abre la carpeta del repositorio en VS Code.
3. Si tienes la extensión Dev Containers instalada, VS Code te sugerirá abrir el proyecto en un contenedor. Acepta la sugerencia o usa el comando:
	 - `F1` → `Dev Containers: Reopen in Container`
4. Espera a que se construya y levante el entorno. Tendrás todas las herramientas necesarias preinstaladas.

### Features utilizadas en el Devcontainer

- **docker-in-docker:** Permite ejecutar Docker dentro del contenedor, necesario para Minikube.
- **kubectl-helm-minikube:** Instala las herramientas de Kubernetes (kubectl), Helm y Minikube.

### Estructura de archivos

```text
app/
	├── app.py
	├── requirements.txt
	└── Dockerfile
```

### Descripción rápida del código

La aplicación utilizada en este workshop está escrita en Python usando el microframework Flask. Es extremadamente simple y está pensada para que cualquier persona pueda entenderla y modificarla rápidamente.

- **app.py:** expone dos endpoints:

	- `/` muestra un mensaje y la versión de la app (definida por la variable de entorno `VERSION`).
	- `/health` responde "OK" para pruebas de salud.

- **requirements.txt:** solo requiere `flask` como dependencia.
- **Dockerfile:** usa multi-stage build y ejecuta la app como usuario sin privilegios para máxima seguridad.

### Dependencias

La única dependencia es Flask, definida en `requirements.txt`:

```text
flask
```

### Ciclo de vida CI/CD y manejo de versiones

No es necesario construir ni compilar la imagen Docker en local. Todo el proceso de construcción y publicación de la imagen se realiza automáticamente mediante GitHub Actions.

#### ¿Cómo funciona el workflow?

Al hacer push de cambios al repositorio, GitHub Actions ejecuta un workflow automatizado que realiza los siguientes pasos:

1. **Checkout del código:** Descarga el código fuente del repositorio para que esté disponible en el runner.
2. **Configuración de Docker Buildx:** Prepara el entorno para construir imágenes Docker de manera eficiente y multiplataforma.
3. **Login en Docker Hub:** Utiliza los secretos configurados (`DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN`) para autenticarse y poder subir imágenes al repositorio de Docker Hub.
4. **Lectura de la versión:** Lee el valor de la versión desde el archivo `app/version.properties` (por ejemplo, `VERSION=1.0.0`) y lo guarda como una variable de salida para usarlo en los siguientes pasos.
5. **Construcción y push de la imagen:** Construye la imagen Docker usando el código fuente de la carpeta `app/` y la etiqueta con la versión obtenida. Luego, sube la imagen a Docker Hub con el tag correspondiente (por ejemplo, `:1.0.0`).
6. **(Opcional) Escaneo de seguridad:** Utiliza Trivy para analizar la imagen publicada y detectar posibles vulnerabilidades.

> **Importante:** Así, los participantes solo deben actualizar el archivo `version.properties` para definir una nueva versión antes de hacer push, y luego usar esa versión en los manifiestos de Kubernetes. No es necesario construir la imagen manualmente ni preocuparse por el versionado de la imagen, ya que todo el proceso es automático y transparente.

#### Autenticación con Docker Hub

Para que GitHub Actions pueda publicar la imagen, es necesario crear dos secretos en el repositorio:

- `DOCKERHUB_USERNAME`: tu usuario de Docker Hub.
- `DOCKERHUB_TOKEN`: un token de acceso generado en Docker Hub.

> **Nota:** No es necesario modificar la imagen base para experimentar con las estrategias de despliegue; la imagen publicada funciona tal cual para todos los ejercicios. El manejo de versiones facilita la gestión de despliegues y pruebas en Kubernetes.

Minikube es una herramienta que permite ejecutar un clúster de Kubernetes localmente, ideal para desarrollo, pruebas y aprendizaje. Facilita la experimentación con recursos y despliegues de Kubernetes sin requerir infraestructura en la nube.

### Importancia de Minikube

- Permite simular entornos de producción en local.
- Es multiplataforma (Windows, Linux, macOS).
- Facilita la práctica de despliegues, actualizaciones y pruebas de aplicaciones en Kubernetes.

## Determinar recursos disponibles en tu sistema

Antes de levantar el clúster, es importante conocer los recursos disponibles (RAM y CPU) para asignarlos adecuadamente a Minikube.

### Comandos para verificar recursos

#### Linux/macOS

- Ver memoria disponible:

```bash
free -h
```

- Ver CPUs disponibles:

```bash
nproc
```

#### Windows (PowerShell)

- Ver memoria disponible:
	
 ```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory
```

- Ver CPUs disponibles:

```powershell
Get-WmiObject -Class Win32_Processor | Select-Object NumberOfLogicalProcessors
```

## Levantar el clúster de Minikube

Una vez identificados los recursos, puedes iniciar un clúster de 3 nodos con la versión 1.33 de Kubernetes, asignando 2 GiB de RAM y 2 CPUs por nodo (ajusta según tus recursos):

```bash
minikube start --nodes=3 --kubernetes-version=v1.33.0 --memory=2048 --cpus=2
```

Esto creará un clúster listo para practicar el ciclo de desarrollo y despliegue en Kubernetes.

### Validar que el clúster está correctamente configurado

Al ejecutar el comando para iniciar Minikube, deberías ver una salida similar a la siguiente:

```text
😄  minikube v1.36.0 on Ubuntu 24.04 (docker/arm64)
🆕  Kubernetes 1.33.1 is now available. If you would like to upgrade, specify: --kubernetes-version=v1.33.1
✨  Using the docker driver based on existing profile
❗  You cannot change the number of nodes for an existing minikube cluster. Please use 'minikube node add' to add nodes to an existing cluster.
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.47 ...
🏃  Updating the running docker "minikube" container ...
🐳  Preparing Kubernetes v1.33.0 on Docker 28.1.1 ...
🔎  Verifying Kubernetes components...
	▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner

👍  Starting "minikube-m02" worker node in "minikube" cluster
🚜  Pulling base image v0.0.47 ...
🏃  Updating the running docker "minikube-m02" container ...
🌐  Found network options:
	▪ NO_PROXY=192.168.49.2
🐳  Preparing Kubernetes v1.33.0 on Docker 28.1.1 ...
	▪ env NO_PROXY=192.168.49.2
🔎  Verifying Kubernetes components...
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default.
```

### Comandos para validar el clúster con kubectl

Puedes usar los siguientes comandos para verificar que el clúster y los nodos están funcionando correctamente:

```bash
# Ver el estado de los nodos
kubectl get nodes

# Ver los pods en todos los namespaces
kubectl get pods -A

# Ver el estado general del clúster
kubectl cluster-info
```

Si los nodos aparecen en estado `Ready` y los pods del sistema están en estado `Running` o `Completed`, tu clúster está correctamente configurado y listo para usarse.

## Manifiestos de Kubernetes: deployment.yaml y service.yaml

Para desplegar la aplicación en Kubernetes, utilizamos dos archivos de manifiesto YAML:

- **deployment.yaml:** Define cómo se debe ejecutar la aplicación, cuántas réplicas (pods) se desean, qué imagen Docker usar, variables de entorno, probes de salud y la política para siempre descargar la imagen más reciente (`imagePullPolicy: Always`). Esto permite que la aplicación esté disponible en alta disponibilidad y que los cambios de versión sean automáticos.
- **service.yaml:** Expone la aplicación dentro del clúster y hacia el exterior usando un Service de tipo NodePort. Esto permite acceder a la app desde tu máquina local usando una URL y puerto asignado por Minikube.

## Guía paso a paso: Estrategias de despliegue en Kubernetes

### 1. Despliegue inicial

**Aplica los manifiestos:**

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Verifica los pods y su distribución:**

```bash
kubectl get pods -o wide
kubectl get nodes
```

Observa que hay 3 pods distribuidos en los 3 nodos del clúster.

**Obtén el NodePort y prueba la app:**

```bash
kubectl get service k8s-orchestrator-demo
minikube service k8s-orchestrator-demo --url
```

Accede a la URL mostrada o usa curl para ver la versión y el pod que responde:

```bash
curl <URL-QUE-TE-DA-MINIKUBE>
```

---

### 2. Rolling Update

1. Edita el `k8s/deployment.yaml`:
	- Cambia la variable de entorno VERSION a la nueva versión.
2. Aplica el cambio:

```bash
kubectl apply -f k8s/deployment.yaml
```

3. Observa el rolling update:

```bash
kubectl rollout status deployment/k8s-orchestrator-demo
kubectl get pods -w
```

### Validación de la aplicación desde la consola

Como estarás trabajando en un devcontainer, es recomendable validar el funcionamiento de la aplicación usando la terminal y no el navegador. Para esto puedes usar los comandos `watch` y `curl`.

#### Obtener la IP y puerto del Service

Primero, obtén la URL del servicio con:

```bash
minikube service k8s-orchestrator-demo --url
```

Esto te dará una dirección IP y puerto, por ejemplo: `http://192.168.49.2:32711/`.

#### Validar la respuesta de la app

Para ver la respuesta de la app y el pod que responde, ejecuta en la terminal:

```bash
watch -n 1 curl -s http://192.168.49.2:32711/
```

Verás una salida similar a:

```text
Every 1.0s: curl -s http://192.168.49.2:32711/  aa6805d90aa7: Thu Aug 14 03:34:39 2025

Hello, Kubernetes Folks, this is the final version! Version: 1.2.0 | Host: k8s-orchestrator-demo-55485d6848-czjw7
```

#### Validar el endpoint de salud

Para validar el endpoint de salud (`/health`):

```bash
watch -n 1 curl -s http://192.168.49.2:32711/health
```

La salida será:

```text
Every 1.0s: curl -s http://192.168.49.2:32711/health  aa6805d90aa7: Thu Aug 14 03:35:00 2025

OK
```

> **Importante:** Debes usar la IP y puerto que te da el comando `minikube service ... --url` para que funcione correctamente.

---

### 3. Rollback

Si algo sale mal (por ejemplo, colocas una versión no soportada por el app.py en el deployment), puedes volver a la versión anterior fácilmente:

```bash
kubectl rollout undo deployment/k8s-orchestrator-demo
```

Esto restaurará la configuración previa y los pods volverán a la versión anterior que funcionaba correctamente.

## Estrategia Canary Deployment (manual, simple)

El canary deployment te permite probar una nueva versión de la aplicación con solo una pequeña parte del tráfico, mientras el resto sigue usando la versión estable. Así puedes validar la nueva versión antes de hacer el cambio completo.

### ¿Cómo hacerlo?

1. Aplica el deployment canary:

```bash
kubectl apply -f k8s/deployment-canary.yaml
```

2. Ahora tendrás 3 pods de la versión estable y 1 pod canary. El Service balanceará el tráfico entre todos los pods.

3. Haz varias peticiones (usando `watch` y `curl` como antes) y verás que ocasionalmente recibirás la respuesta de la nueva versión (canary), lo que demuestra el despliegue progresivo.

> **Tip:** Puedes aumentar el número de réplicas canary para ajustar el porcentaje de tráfico que recibe la nueva versión.

## Estrategia Blue/Green Deployment (manual, simple)

El blue/green deployment te permite tener dos versiones de la aplicación corriendo al mismo tiempo (blue = actual, green = nueva). El Service controla a cuál versión se dirige el tráfico. Cuando estés listo, cambias el selector del Service y todo el tráfico va a la nueva versión de golpe.

### ¿Cómo realizarlo?

1. Modifica el Service para que su selector apunte a los pods blue (por ejemplo, color: blue). Ejemplo de fragmento en `k8s/service.yaml`:

```yaml
selector:
   app: k8s-orchestrator-demo
   color: blue
```

2. Aplica los manifiestos:

```bash
kubectl apply -f k8s/deployment-green.yaml
kubectl apply -f k8s/service.yaml
```

3. Cuando estés listo para el cambio, edita el Service y cambia el selector a color: green

```yaml
selector:
   app: k8s-orchestrator-demo
   color: green
```

4. Aplica el cambio:

```bash
kubectl apply -f k8s/service.yaml
```

4. Todo el tráfico irá a los pods de la nueva versión de golpe. Puedes validar con curl y watch como antes.

> **Tip:** Puedes mantener ambos deployments activos para pruebas, y solo cambiar el selector del Service cuando decidas hacer el switch.

## Limpieza del Workshop: Detener y eliminar recursos

Cuando termines el workshop, puedes limpiar tu entorno siguiendo estos pasos sencillos:

### 1. Detener el clúster de Minikube

```bash
minikube stop
```

Esto detiene todos los nodos y recursos del clúster local.

### 2. Eliminar el clúster de Minikube

```bash
minikube delete
```

Esto borra completamente el clúster y libera los recursos usados por Minikube.

### 3. Detener y salir del Devcontainer

1. Guarda tus cambios y cierra cualquier terminal activa dentro del devcontainer.
2. Haz clic en la esquina inferior izquierda de VS Code donde dice "Dev Container" y selecciona `Close Remote Connection` o simplemente cierra la ventana de VS Code.

¡Listo! Así de fácil limpias tu entorno después de practicar con Kubernetes y Minikube.
