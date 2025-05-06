# cirrus-helm-examples
A repository that contains example Helm charts that can be used as templates to deploy custom applications to CIRRUS.

For more information on CIRRUS, please see [CIRRUS, NSF NCAR Cloud Infrastructure for Remote Research, Universities, and Scientists](https://ncar-hpc-docs.readthedocs.io/en/latest/compute-systems/cirrus/). 

There are a number of different directories in this repository that have more details README files with specific instructions

  - autoscale-helm : An example Helm chart for a simple web app that can autoscale the number of containers running based on resource utilization metrics
  - cirrus-vol-helm : An example Helm chart for a simple web app that allocates storage to mount to the webapp that persists when the underlying container changes. 
  - dask-helm : An example Helm chart that creates a Dask cluster, a scheduler and workers, to run alongside a webapp.
  - external-secret-helm : An example Helm chart that retrieves a secret from bao.k8s.ucar.edu and injects it in to a container as an environment variable.
  - nfs-vol-helm : An example Helm chart that mounts an existing NFS volume inside a container at a specific mount path.
  - postgres-helm : An example Helm chart that creates a webapp with a dedicated PostgreSQL container with an associated persistent volume.
  - web-app-helm : An example Helm chart for a simple web app that does not require any additional objects outside the web app container. 