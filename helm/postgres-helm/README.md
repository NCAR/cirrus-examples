# postgres-helm

A Helm chart for deploying a [CloudNativePG](https://cloudnative-pg.io/) database cluster on CIRRUS. Database credentials are stored in [OpenBao](https://openbao.org/) (`bao.k8s.ucar.edu`) and injected via ExternalSecrets.

## Prerequisites

Before deploying, you'll need the following:

| Parameter | Description |
|-----------|-------------|
| **Database name** | Name for your database cluster. This is also used as the hostname: `<name>.k8s.ucar.edu` |
| **Instances** | Number of PostgreSQL servers in the cluster. We recommend 2+ for high availability |
| **Storage size** | Disk space for the database (e.g., `10Gi`) |
| **Application database name** | Name of the database to create during bootstrap |
| **Secrets in OpenBao** | Superuser and application user credentials stored in `bao.k8s.ucar.edu` (see below) |

### OpenBao Secret Setup

Both the superuser and application user credentials must be stored in `bao.k8s.ucar.edu` before deploying. Each secret path should contain key-value pairs for the username and password.

Example structure:
```
<your-path>/superuser
  ├── username: postgres
  └── password: <secure-password>

<your-path>/appuser
  ├── username: myappuser
  └── password: <secure-password>
```

> **Note:** A `SecretStore` must be configured in your namespace to access OpenBao. Contact [cirrus-admin@ucar.edu](mailto:cirrus-admin@ucar.edu) to have this set up.

## Configuration

Update `values.yaml` with your database details:

```yaml
db:
  name: my-database                       # Database cluster name, also used as hostname
  group: my-database                      # Group label for related resources
  instances: 2                            # Number of PostgreSQL servers in the cluster
  size: 10Gi                              # Storage size for the database
  superUser:
    enabled: false                         # Enable superuser access to the database
    usernameKey: username                  # Key in OpenBao for superuser username
    passwordKey: password                  # Key in OpenBao for superuser password
    secretPath: my-path/superuser          # Path in OpenBao where superuser credentials are stored
  app:
    name: my-app-db                       # Database name to create during bootstrap
    usernameKey: username                  # Key in OpenBao for app user username
    passwordKey: password                  # Key in OpenBao for app user password
    secretPath: my-path/appuser            # Path in OpenBao where app user credentials are stored
```

## Chart.yaml

Update `Chart.yaml` with your application's name, description, and version information. This metadata is used by Helm to identify and track your chart.

## Templates

This chart creates the following Kubernetes resources:

- **Cluster** — CloudNativePG cluster with the specified number of instances and storage
- **Service (LoadBalancer)** — exposes the primary database instance at `<name>.k8s.ucar.edu:5432` via an internal load balancer with DNS managed by external-dns
- **Certificate** — self-signed TLS certificate for encrypted database connections, covering all CloudNativePG service endpoints
- **Issuer** — cert-manager self-signed issuer for the TLS certificate
- **ExternalSecret (superuser)** — pulls superuser credentials from OpenBao
- **ExternalSecret (app user)** — pulls application user credentials from OpenBao