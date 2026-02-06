# service-helm

A Helm chart for deploying a containerized application as an internal service on CIRRUS, accessible only within the cluster without an external URL.

## Prerequisites

Before deploying, you'll need the following information:

| Parameter | Description |
|-----------|-------------|
| **Application name** | Name for your Kubernetes objects |
| **Container image** | A pre-built image available in a container registry that CIRRUS can pull from |
| **Container port** | The port your application listens on inside the container |
| **Resource requirements** | How much memory and CPU your application needs. Set both guaranteed minimums (`requests`) and upper bounds (`limits`) |

## Configuration

Update `values.yaml` with your application details:

```yaml
replicaCount: 2                           # Number of identical pods to run

service:
  name: my-service                        # Name for k8s objects
  group: my-service                       # Group label for related resources
  container:
    image: my-registry/my-image:tag       # Full image path
    port: 8080                            # Port your container listens on
    requests:
      memory: 512M                        # Guaranteed memory allocation
      cpu: 1                              # Guaranteed CPU allocation
    limits:
      memory: 1G                          # Maximum memory allowed
      cpu: 2                              # Maximum CPU allowed
```

> `replicaCount` defines how many identical copies (pods) of your container to run. This is a static value — autoscaling requires additional chart components. We recommend 2+ for zero-downtime deployments during server maintenance.

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Deployment** — runs your container with the specified resource limits and replica count
- **Service** — exposes your container port within the cluster