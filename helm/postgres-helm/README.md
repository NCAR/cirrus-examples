# postgres-helm
A chart for deploying a PostgreSQL database cluster to the CISL cloud with Helm. This requires a superuser and regular user username and password to access the PostgreSQL database to be stored in bao.k8s.ucar.edu so it can be injected in to the required containers appropriately. 

```{note}
Information required to create a Helm chart for your web application:
1. A Name for the database. This will be used as a hostname to connect to via <db_name>.k8s.ucar.edu
2. The number of PostgreSQL servers to run in the database cluster
3. The size of the volume to mount to the database and a unique name for the volume. 
4. Secret information to access the database. This should be stored in bao.k8s.ucar.edu. An example of what a path would look like is, <email>/database01. Under that path use the keys postgresuser and postgrespass to store the username and password for the DB securely.   
```

## Update values.yaml file
In the `postgres-helm/` directory is a file named `values.yaml` which contains all the specific details for your application. You need to update the following values to be unique for your deployment:

    - `#DATABASE_NAME` : The name of the database.
    - `#DATABASE_APP_GROUP` : The group of applications to run the database with. If it's a standalone DB this can just be the DB name. 
    - `#DATABASE_CLUSTER_MEMBERS` : The number of PostgreSQL database servers running for the cluster
    - `#DATABASE_SIZE` : How large to make the database in Gi. 
    - `#SU_USERNAME_SECRET_KEY` : The superuser username key as designated in bao.k8s.ucar.edu.
    - `#SU_PASSWORD_SECRET_KEY` : The superuser password key as designated in bao.k8s.ucar.edu. 
    - `#SU_SECRET_PATH` : The superuser secret path designated in bao.k8s.ucar.edu. 
    - `#APP_USERNAME_SECRET_KEY` : The database username key to query in bao.k8s.ucar.edu in order to get the username value.
    - `#APP_PASSWORD_SECRET_KEY` : The database password key to query in bao.k8s.ucar.edu in order to get the password value.
    - `#APP_USER_SECRET_PATH` : The path in bao.k8s.ucar.edu where the DB secrets are stored.


## Update Chart.yaml
The Chart.yaml file is mostly used to describe your application and keep track of what versions you are on and running. 