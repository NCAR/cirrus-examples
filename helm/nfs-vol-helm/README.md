# nfs-vol-helm

A Helm chart for deploying a containerized application as a website on CIRRUS with NFS volume mounts. This allows your application to access data from existing NFS servers rather than provisioning new storage.

## GLADE Access

A common use case is mounting [GLADE](https://arc.ucar.edu/knowledge_base/70549550) storage inside your container. If you need the GLADE NFS server FQDN, contact [cirrus-admin@ucar.edu](mailto:cirrus-admin@ucar.edu).

> **Note:** The Glade NFS export policy for CIRRUS hosts is read-only. GLADE access can only be read-only, so if mounting Glade the `readOnly` value must be set to `true`.

## Non-web usage

This example deploys a full web application with a URL. If you only need an internal service without external access, omit the `ingress.yaml` template and the `tls` and `ingress` sections from `values.yaml`. See [service-helm](../service-helm/) for a standalone service example.

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
| **NFS server** | The FQDN or IP address of the NFS server |
| **NFS path** | The export path on the NFS server to mount (must exist on the server) |
| **Mount path** | The path inside the container where the NFS share will be mounted |

## Configuration

Update `values.yaml` with your application details:

```yaml
replicaCount: 2                           # Number of identical pods to run

webapp:
  name: my-app                            # Name for k8s objects
  group: my-app                           # Group label for related resources
  path: /                                 # URL path suffix
  tls:
    fqdn: my-app.k8s.ucar.edu            # Must be unique and end in .k8s.ucar.edu
    secretName: incommon-cert-my-app      # Unique TLS secret name for your FQDN
  ingress:
    visibility: internal                  # internal or external
  nfs:
    name: glade-campaign                  # Unique name for the volume
    server: nfs.example.ucar.edu          # NFS server FQDN or IP
    path: /campaign                       # Export path on the NFS server
    mountPath: /glade/campaign            # Path inside the container to mount to
    readOnly: true                        # GLADE access is read-only
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

- **Deployment** — runs your container with the specified resource limits, replica count, and NFS volume mount
- **Service** — exposes your container port within the cluster
- **Ingress** — configures external access via your FQDN with TLS termination using an InCommon certificate