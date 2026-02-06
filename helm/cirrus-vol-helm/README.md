# cirrus-vol-helm

A Helm chart for deploying a containerized application as a website on CIRRUS with persistent storage volumes. Volumes persist across container restarts and image updates, so data written to them is not lost when pods are recreated.

## Storage Classes

CIRRUS uses [Ceph](https://docs.ceph.com/en/reef/) to provision persistent storage. Two storage classes are available:

| Storage Class | Access Mode | Use Case |
|---------------|-------------|----------|
| **Ceph RBD** (`ceph-kubepv`) | ReadWriteOnce (RWO) | Single pod access only. No other pods can mount this volume. |
| **Ceph FS** (`cephfs`) | ReadWriteMany (RWX) | Multiple pods can read and write simultaneously. Required when `replicaCount` > 1 and pods need shared storage. |

This example includes both volume types. Use the one(s) appropriate for your application — if only your single pod needs the storage, RWO is sufficient. If multiple pods need to read and write to the same volume, use RWX.

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
| **Volume name** | A unique name for each persistent volume |
| **Volume size** | Storage capacity to provision (e.g., `10Gi` for 10 gigabytes) |
| **Mount path** | The path inside the container where the volume will be mounted |

> **Which storage type do you need?** If only a single pod needs access to the volume, use Ceph RBD (`rdb`). If multiple pods need to read and write to the same volume — for example, when running multiple replicas — use Ceph FS (`fs`). See the [Storage Classes](#storage-classes) table above for details.

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
  volume:
    rdb:
      enabled: false                        # Enable Ceph RBD (ReadWriteOnce) volume
      name: my-app-rdb                      # Unique name for the RWO volume
      size: 10Gi                            # Volume size
      mountPath: /data/rdb                  # Path inside the container to mount to
    fs:
      enabled: false                        # Enable Ceph FS (ReadWriteMany) volume
      name: my-app-fs                       # Unique name for the RWX volume
      size: 10Gi                            # Volume size
      mountPath: /data/fs                   # Path inside the container to mount to
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

> `replicaCount` defines how many identical copies (pods) of your container to run. This is a static value — autoscaling requires additional chart components. We recommend 2+ for zero-downtime deployments during server maintenance. Note that if using multiple replicas, any shared storage must use the Ceph FS (RWX) volume — Ceph RBD (RWO) can only be mounted by a single pod.

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Deployment** — runs your container with the specified resource limits, replica count, and volume mounts
- **Service** — exposes your container port within the cluster
- **Ingress** — configures external access via your FQDN with TLS termination using an InCommon certificate
- **PersistentVolumeClaim (RBD)** — provisions a Ceph RBD volume with ReadWriteOnce access (If enabled)
- **PersistentVolumeClaim (FS)** — provisions a Ceph FS volume with ReadWriteMany access (If enabled)