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


## Código fuente de la aplicación demo (Python/Flask)

La aplicación utilizada en este workshop está escrita en Python usando el microframework Flask. Es extremadamente simple y está pensada para que cualquier persona pueda entenderla y modificarla rápidamente.

### Estructura de archivos

```text
app/
	├── app.py
	├── requirements.txt
	└── Dockerfile
```

### Descripción rápida del código

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

### Ciclo de vida CI/CD

No es necesario construir ni compilar la imagen Docker en local. Todo el proceso de construcción y publicación de la imagen se realiza automáticamente mediante GitHub Actions:

1. Al hacer push de cambios al repositorio, GitHub Actions construye la imagen Docker y la publica en Docker Hub.
2. Así, los participantes solo deben actualizar el manifiesto de Kubernetes para desplegar la última versión, sin preocuparse por la construcción manual.

#### Autenticación con Docker Hub

Para que GitHub Actions pueda publicar la imagen, es necesario crear dos secretos en el repositorio:
- `DOCKERHUB_USERNAME`: tu usuario de Docker Hub.
- `DOCKERHUB_TOKEN`: un token de acceso generado en Docker Hub.

> **Nota:** No es necesario modificar la imagen base para experimentar con las estrategias de despliegue; la imagen publicada funciona tal cual para todos los ejercicios.

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

## Validar que el clúster está correctamente configurado

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

