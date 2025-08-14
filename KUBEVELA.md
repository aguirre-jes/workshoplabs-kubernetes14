
# BONUS: Despliegue sencillo con KubeVela y OAM

¿Quieres ir un paso más allá? Puedes experimentar con [KubeVela](https://kubevela.io/) y el estándar OAM (Open Application Model) para desplegar la misma app con un solo manifiesto YAML, en vez de dos (Deployment y Service).

## ¿Qué es KubeVela?

KubeVela es una plataforma de entrega de aplicaciones sobre Kubernetes que simplifica el despliegue usando el modelo OAM. Permite definir aplicaciones de manera declarativa y más sencilla, ideal para quienes buscan abstraer detalles de bajo nivel de Kubernetes.

## 1. Instalar KubeVela CLI y Core

Primero, instala la CLI de KubeVela (esto solo es necesario una vez por máquina):

```bash
curl -fsSl https://kubevela.io/script/install.sh | bash
```

Luego, instala el core de KubeVela en tu clúster Minikube:

```bash
vela install
```

Espera unos segundos a que los pods de KubeVela estén en estado `Running`:

```bash
kubectl get pods -n vela-system
```

## 2. Desplegar la app con KubeVela

Usa la CLI de KubeVela para aplicar el manifiesto:

```bash
vela up -f kubevela/vela-app.yaml
```

Deberas tener una salida asi:

```text
Applying an application in vela K8s object format...
✅ App has been deployed 🚀🚀🚀
    Port forward: vela port-forward k8s-orchestrator-demo-vela
             SSH: vela exec k8s-orchestrator-demo-vela
         Logging: vela logs k8s-orchestrator-demo-vela
      App status: vela status k8s-orchestrator-demo-vela
        Endpoint: vela status k8s-orchestrator-demo-vela --endpoint
Application /k8s-orchestrator-demo-vela applied.
```

Esto creará automáticamente el Deployment y el Service necesarios, ¡todo desde un solo archivo!

## 3. Validar y operar la aplicación con KubeVela

Puedes ver el estado y detalles de la aplicación con:

```bash
vela ls
vela status k8s-orchestrator-demo-vela
```

Para ver los endpoints expuestos por la app:

```bash
vela port-forward k8s-orchestrator-demo-vela --component demo-web
```

> También puedes seguir usando `vela logs` para ver los logs de la app:

```bash
vela logs k8s-orchestrator-demo-vela --component demo-web
```

> Si necesitas eliminar la app:

```bash
vela delete k8s-orchestrator-demo-vela -n default
```

> Si quieres ver los recursos nativos generados, puedes usar `kubectl get deployment,svc` como referencia.

## 5. ¿Qué aprendiste?

- Con OAM y KubeVela puedes definir una app completa en un solo manifiesto YAML.
- KubeVela se encarga de crear los recursos nativos de Kubernetes por ti.
- Es ideal para simplificar despliegues y abstraer detalles para equipos de desarrollo.

> **Tip:** Puedes modificar el manifiesto OAM para experimentar con variables de entorno, puertos, réplicas, etc., igual que harías con los manifiestos nativos.
