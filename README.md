# CIRRUS Example Applications

Example Helm charts and deployment templates for CIRRUS, NSF NCAR's cloud-native platform for scientific computing.

## About CIRRUS

CIRRUS (Cloud Infrastructure for Remote Research, Universities, and Scientists) is NSF NCAR's Kubernetes-based platform. For complete documentation, see [CIRRUS Documentation](https://ncar-hpc-docs.readthedocs.io/en/latest/compute-systems/cirrus/).

## What's a Helm Chart?

Helm charts are packages that define Kubernetes applications. They contain templates for Kubernetes objects (Deployments, Services, ConfigMaps, etc.) and make it easy to deploy, version, and manage applications on Kubernetes clusters like CIRRUS.

## Examples

### Getting Started
- **[web-app-helm](./web-app-helm/)** - Deploy a containerized application as a website with a URL accessible internally or externally
- **[service-helm](./service-helm/)** - Deploy a containerized application as an internal cluster service without external access

### Storage
- **[cirrus-vol-helm](./cirrus-vol-helm/)** - Web application with persistent Ceph storage volumes (RBD for single-pod or CephFS for multi-pod access)
- **[nfs-vol-helm](./nfs-vol-helm/)** - Web application with NFS volume mounts (e.g., read-only access to GLADE)

### Databases
- **[postgres-helm](./postgres-helm/)** - CloudNativePG database cluster with TLS certificates, load balancer service, and credentials managed via OpenBao external secrets

### Compute Workloads
- **[dask-helm](./dask-helm/)** - Dedicated Dask distributed computing cluster (scheduler + workers) alongside a web application

### Security
- **[external-secret-helm](./external-secret-helm/)** - Web application with secrets injected from OpenBao (`bao.k8s.ucar.edu`) as environment variables

## Helm Chart Structure

Each Helm chart in this repository is contained in its own directory with the required structure:
```
chart-name/
├── Chart.yaml
├── values.yaml
└── templates/
```

`values.yaml` defines configurable parameters that are injected into template placeholders at deploy time. Override these with your own values to customize each deployment.

## Usage

Clone this repository and use the relevant example as a starting point for your application. Each example directory contains its own README with prerequisites, configuration options, and template descriptions.

## Questions?

Contact the CIRRUS team or see the [CIRRUS documentation](https://ncar-hpc-docs.readthedocs.io/en/latest/compute-systems/cirrus/) for support resources.