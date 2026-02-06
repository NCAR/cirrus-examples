# external-secret-helm

A Helm chart for deploying a containerized application as a website on CIRRUS with secrets injected from [OpenBao](https://openbao.org/) (`bao.k8s.ucar.edu`) via ExternalSecrets. Secrets are mounted as environment variables inside the container.

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
| **Secret path** | The path in `bao.k8s.ucar.edu` where your secret is stored |
| **Secret key** | The key under that path to retrieve the secret value |

### OpenBao Secret Setup

Your secret must be stored in `bao.k8s.ucar.edu` before deploying. For example, if your path is `my-sso/mywebapp` with a key of `api-token`, the value stored at that key will be injected as an environment variable in your container.

> **Note:** A `SecretStore` must be configured in your namespace to access OpenBao. Contact [cirrus-admin@ucar.edu](mailto:cirrus-admin@ucar.edu) to have this set up.

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
  container:
    image: my-registry/my-image:tag       # Full image path
    port: 8080                            # Port your container listens on
    requests:
      memory: 512M                        # Guaranteed memory allocation
      cpu: 1                              # Guaranteed CPU allocation
    limits:
      memory: 1G                          # Maximum memory allowed
      cpu: 2                              # Maximum CPU allowed
  secret:
    secretPath: my-sso/mywebapp           # Path in OpenBao where the secret is stored
    secretKey: api-token                  # Key to retrieve from OpenBao
    envVar: API_TOKEN                     # Environment variable name inside the container
```

> This example injects a single secret as an environment variable. To add more secrets, add additional entries to the `secret` section in `values.yaml` and corresponding `data` entries in the ExternalSecret and `env` entries in the Deployment templates.

## Non-web usage

This example deploys a full web application with a URL. If you only need an internal service with secrets, omit the `ingress.yaml` template and the `tls` and `ingress` sections from `values.yaml`. See [service-helm](../service-helm/) for a standalone service example.

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Deployment** — runs your container with the specified resource limits, replica count, and secret environment variables
- **Service** — exposes your container port within the cluster
- **Ingress** — configures external access via your FQDN with TLS termination using an InCommon certificate
- **ExternalSecret** — pulls secret values from OpenBao and creates a Kubernetes secret