# dask-helm

A Helm chart for deploying a dedicated [Dask](https://www.dask.org/) distributed computing cluster on CIRRUS alongside a web application. This deploys a Dask scheduler, a configurable number of workers, and a web application that connects to the cluster.

## Dask Gateway

CIRRUS also has [Dask Gateway](https://gateway.dask.org/) installed and accessible to applications in the cluster. Dask Gateway uses JupyterHub authentication and requires an API key, typically stored in OpenBao via ExternalSecrets (see [external-secret-helm](../external-secret-helm/)). This chart is for deploying a dedicated Dask cluster for an application or set of applications that need their own scheduler and workers.

## Prerequisites

Before deploying, you'll need the following information:

| Parameter | Description |
|-----------|-------------|
| **Application name** | Name for your web application Kubernetes objects (not the URL) |
| **FQDN** | Full URL for your app, must end in `.k8s.ucar.edu` and be unique |
| **URL path** | The path suffix after your FQDN, typically `/` unless your app serves on a subpath like `/api` |
| **Visibility** | Whether your application URL is accessible to the public (`external`) or only the UCAR network/VPN (`internal`) |
| **Web app image** | Container image for your web application |
| **Web app port** | The port your web application listens on |
| **Dask image** | Container image for the Dask scheduler and workers (must have Dask installed) |
| **Worker count** | Number of Dask workers to run |
| **Resource requirements** | Memory and CPU for the web app, scheduler, and workers |

## Connecting to the Dask Cluster

Your web application connects to the Dask scheduler using the Kubernetes service name. In your Python code:

```python
from dask.distributed import Client

client = Client("tcp://scheduler:8786")
```

The Dask dashboard is accessible at the scheduler service on port `8787` and is exposed via the ingress at the `/dask-dashboard` path.

## Non-web usage

This chart can also be used without the web application to run a standalone Dask cluster as a service. Remove the `webapp_deployment.yaml`, `ingress.yaml`, and `webapp_service.yaml` templates, and the `webapp` section from `values.yaml`. Other applications in the cluster can connect to the scheduler service directly.

## Configuration

Update `values.yaml` with your application details:

```yaml
webapp:
  name: my-app                            # Name for web app k8s objects
  group: my-app                           # Group label for related resources
  replicaCount: 2                         # Number of web app pods to run
  path: /                                 # URL path suffix for the web app
  tls:
    fqdn: my-app.k8s.ucar.edu            # Must be unique and end in .k8s.ucar.edu
    secretName: incommon-cert-my-app      # Unique TLS secret name for your FQDN
  ingress:
    visibility: internal                  # internal or external
  container:
    image: my-registry/my-webapp:tag      # Web application image
    port: 8080                            # Port your web app listens on
    requests:
      memory: 512M                        # Guaranteed memory allocation
      cpu: 1                              # Guaranteed CPU allocation
    limits:
      memory: 1G                          # Maximum memory allowed
      cpu: 2                              # Maximum CPU allowed

scheduler:
  name: scheduler                         # Name for scheduler k8s objects
  path: /dask-dashboard                   # URL path for the Dask dashboard
  container:
    image: my-registry/my-dask:tag        # Dask image (used by scheduler and workers)
    dashboardPort: 8787                   # Dask dashboard port
    workerPort: 8786                      # Dask scheduler-worker communication port
    requests:
      memory: 512M                        # Guaranteed memory allocation
      cpu: 1                              # Guaranteed CPU allocation
    limits:
      memory: 1G                          # Maximum memory allowed
      cpu: 2                              # Maximum CPU allowed

worker:
  name: dask-worker                       # Name for worker k8s objects
  replicaCount: 4                         # Number of Dask workers to run
  container:
    requests:
      memory: 1G                          # Guaranteed memory allocation
      cpu: 1                              # Guaranteed CPU allocation
    limits:
      memory: 2G                          # Maximum memory allowed
      cpu: 4                              # Maximum CPU allowed
```

> Workers typically need more resources than the scheduler or web app since they perform the actual computation. Adjust worker resources based on your workload requirements.

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Deployment (web app)** — runs your web application container
- **Deployment (scheduler)** — runs the Dask scheduler
- **Deployment (workers)** — runs Dask workers that connect to the scheduler
- **Service (web app)** — exposes your web app port within the cluster
- **Service (scheduler)** — exposes the scheduler ports for worker communication and the dashboard
- **Ingress (web app)** — configures external access to the web app via your FQDN with TLS termination using an InCommon certificate
- **Ingress (scheduler)** — exposes the Dask dashboard at your FQDN under the `/dask-dashboard` path with regex rewriting