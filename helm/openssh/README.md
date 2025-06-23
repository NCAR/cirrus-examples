# openssh-helm
A chart for deploying OpenSSH Server containers to the CISL cloud with Helm

This example uses secrets store in [bao.k8s.ucar.edu](https://bao.k8s.ucar.edu)

```{note}
Information required to create a Helm chart for your OpenSSH server:
1. A Name for your SSH application, this is the name of the k8s objects created (deployment, service, external secret)
2. A Secret Store name that references your External Secrets Operator store configuration
3. An OpenBao secret path where your SSH credentials are stored
4. Username and password secret keys that correspond to the keys in your OpenBao secret store
5. Optional: Custom SSH port if you don't want to use the default 2222
6. Optional: Custom container image if you want to use a different OpenSSH server image
```

## Update values.yaml file
In the `openssh-helm/` directory is a file named `values.yaml` which contains all the specific details for your SSH server deployment. You need to update the following values to be unique for your deployment:

- `ssh.enabled: true` : Controls whether the SSH deployment and service are active. Set to `false` to disable SSH resources when not needed
- `ssh.name: #SSH_APP_NAME` : The name to give your SSH application and associated Kubernetes objects (deployment, service, external secret)
- `ssh.secret.secretStoreName: #SECRET_STORE_NAME` : The name of your External Secrets Operator SecretStore that connects to your OpenBao instance
- `ssh.secret.path: #BAO_SECRET_PATH` : The path in OpenBao where your SSH credentials are stored (e.g., `secret/data/ssh/myapp`)
- `ssh.secret.usernameKey: #BAO_USERNAME_SECRET_KEY` : The key name in your OpenBao secret that contains the SSH username (typically `username`)
- `ssh.secret.passwordKey: #BAO_PASSWORD_SECRET_KEY` : The key name in your OpenBao secret that contains the SSH password (typically `password`)

```{note}
The default configuration uses:
- **Container Image**: `lscr.io/linuxserver/openssh-server:latest` (LinuxServer.io's OpenSSH container)
- **SSH Port**: `2222` (container port that SSH server listens on)
- **External Secret**: Automatically syncs credentials from OpenBao to Kubernetes secrets (always active)
- **Service Type**: LoadBalancer with external DNS annotation for `<app-name>.k8s.ucar.edu` access
- **Resource Limits**: 200m CPU / 128Mi memory limits, 100m CPU / 64Mi memory requests
```

## Secret Management
This Helm chart uses External Secrets Operator to securely manage SSH credentials:

1. **External Secret**: Creates a Kubernetes secret by pulling credentials from OpenBao (always active)
2. **Secret Store**: Must be pre-configured to connect to your OpenBao instance
3. **Credential Mapping**: OpenBao secret properties `username` and `password` are mapped to Kubernetes secret keys `<app-name>-username` and `<app-name>-password`
4. **Refresh Interval**: Credentials are refreshed from OpenBao every hour

Make sure your OpenBao secret contains `username` and `password` properties before deploying the chart. The External Secret remains synchronized regardless of whether the SSH deployment is enabled.

## Network Access
The SSH service will be accessible within the Kubernetes cluster on port 2222. For external access, you may need to:
- Configure a NodePort or LoadBalancer service
- Set up port forwarding
- Configure ingress (though this is uncommon for SSH services)

## Update Chart.yaml
The Chart.yaml file is used to describe your SSH application and track versions. Update the following fields:
- `name`: Should match your SSH application name
- `description`: Brief description of your SSH server deployment
- `version`: Chart version for tracking changes
- `appVersion`: Version of the OpenSSH server image being used

## Deployment Management
**Important**: This SSH deployment should only be enabled when you need to SSH to the container, and it should be disabled when you are done. This follows security best practices by minimizing the attack surface.

You can control deployment using the `enabled` flag in your values.yaml:
```yaml
app:
  enabled: true  # Set to false to disable the entire SSH deployment
```

The Helm templates should include conditional logic (`{{- if .Values.app.enabled }}`) to only deploy resources when explicitly enabled.

## Security Considerations
- SSH credentials are managed through External Secrets Operator for enhanced security
- Enable the deployment only when SSH access is needed, disable when finished
- Ensure your OpenBao secret path has appropriate access controls
- Review container security settings and consider running as non-root user where possible