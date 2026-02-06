# web-app-helm

A Helm chart for deploying a containerized application as a website on CIRRUS, accessible via a URL on the UCAR network or the public internet.

## Prerequisites

Before deploying, you'll need the following information:

| Parameter | Description |
|-----------|-------------|
| **Application name** | Name for your Kubernetes objects (not the URL) |
| **FQDN** | Full URL for your app, must end in `.k8s.ucar.edu` and be unique |
| **URL path** | The path suffix after your FQDN, typically `/` unless your app serves on a subpath like `/api` |
| **Container image** | A pre-built image available in a container registry that CIRRUS can pull from |
| **Container port** | The port your application listens on inside the container. If you run it locally at `http://127.0.0.1:8888`, the port is `8888` |
| **Visibility** | Whether your application URL is accessible to the public (`external`) or only the UCAR network/VPN (`internal`) |
| **Resource requirements** | How much memory and CPU your application needs. Set both guaranteed minimums (`requests`) and upper bounds (`limits`) |

## Configuration

Update `values.yaml` with your application details:

```yaml
replicaCount: 2                          # Number of identical pods to run

webapp:
  name: my-app                          # Name for k8s objects
  group: my-app                         # Group label for related resources
  path: /                               # URL path suffix
  tls:
    fqdn: my-app.k8s.ucar.edu          # Must be unique and end in .k8s.ucar.edu
    secretName: incommon-cert-my-app    # Unique TLS secret name for your FQDN
  ingress:
    visibility: internal                # internal or external
  container:
    image: my-registry/my-image:tag     # Full image path if not on Docker Hub
    port: 8080                          # Port your container listens on
    memory: 1G                          # Memory limit
    cpu: 2                              # CPU limit
```

> `replicaCount` defines how many identical copies (pods) of your container to run. This is a static value — autoscaling requires additional chart components. We recommend 2+ for zero-downtime deployments during server maintenance.

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Deployment** — runs your container with the specified resource limits and replica count
- **Service** — exposes your container port within the cluster
- **Ingress** — configures external access via your FQDN with TLS termination using an InCommon certificate