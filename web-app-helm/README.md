# web-app-helm
A chart for deploying web applications to the CISL cloud with Helm

```{note}
Information required to create a Helm chart for your web application:
1. A Name for your application, this is not the URL that will be deployed but the name of the k8s objects created
2. A URL path. This also is not the full URL, just the suffix you'd like to use after `.edu`. This is typically just `/` but may be things like `/api` that correspond to endpoints on your application.
3. An FQDN. This is the full URL for your application. Currently in the CISL cloud environment we only can create names under the `.k8s.ucar.edu` domain and your FQDN should end with `.k8s.ucar.edu`. Please make sure this is unique, try to browse to it before applying, and descriptive for your application. 
4. Container image to use. This should be an image that is already built and has been pushed to a container registry that the application can pull from. By default it is set to look at docker.io so if you are using something different you need to specify that before your container registry and image name:tag
5. Container port to expose. Your containerized application will expose a port to the network in order to communicate. More often than not there is a default for the application you are using and you also have the ability to provide a specific port if you wanted. If you have run your container image locally it is usually in the URL you used to access it locally, ie. `http://127.0.0.1:8888` is running on port 8888 and would be the appropriate value to put in the Helm chart. 
```

## Update values.yaml file
In the `web-app-helm/` directory is a file named `values.yaml` which contains all the specific details for your application. You need to update the following values to be unique for your deployment:

    - `#APP_NAME` : The name, and group name, to give your application.
    - `#URL_PATH` : This is the URL suffix to route to. For most applications this will just be `/` unless your applications launches on a different default path
    - `#FQDN` : ***This must end in .k8s.ucar.edu*** The fully Fully Qualified Domain Name to use for your application. This needs to be unique and has to live under the sub domain `*.k8s.ucar.edu`
    - `secretName: incommon-cert-#HOST` : This is a secret that gets stored in kubernetes that contains the certificate for your application. This needs to be unique for the FQDN that is going to be in use as the SSL certificate and URL are coupled. 
    - `#IMAGE_NAME` : This is the name and path to your image. By default Helm will look to Docker Hub. If you use something else please provide the full path to your image
    - `#CONTAINER_PORT` : This is the network path that your container application opens and listens on. We need to map this to k8s in order to communicate in to your container. 
    - `memory:` & `cpu:` is the amount of memory and cpus to allocate to your application. By default this is set low and it should be adjusted to fine tune your applications performance. 

```{note}
replicaCount: defines how many instances of your container you want to run. This is a static value that will run at all times and not a number that scales. Autoscaling is possible but requires additions to the Helm chart. 
```

## Update Chart.yaml
The Chart.yaml file is mostly used to describe your application and keep track of what versions you are on and running. 