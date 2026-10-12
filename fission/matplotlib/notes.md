# Fission Plot Example

This example demonstrates a Fission Function-as-a-Service that generates soil moisture plots from CYGNSS satellite data.

## Quick Start

```bash
# Build the container
docker build -t hub.k8s.ucar.edu/khrpcek/fission-plot-example:3.13 -f container/Containerfile .

# Push to registry
docker push hub.k8s.ucar.edu/khrpcek/fission-plot-example:3.13

# Deploy to Fission
fission env create --name plot-example --image hub.k8s.ucar.edu/khrpcek/fission-plot-example:3.13 --builder hub.k8s.ucar.edu/khrpcek/fission-plot-example:3.13 --poolsize 1
fission fn create --name plot-example --env plot-example --entrypoint plot_cygnss_sm --code sm.py

# Create route
fission route create --function plot-example --route-provider gateway --name plot-example --route-path='/plot-example' --route-host fn.k8s.ucar.edu --url /plot-example --gateway traefik/traefik-gateway
```

## Usage

```bash
curl "https://fn.k8s.ucar.edu/plot-example?fileurl=https://example.com/data/soil_moisture.nc.gz" --output plot.png
```

## Documentation

For a detailed guide covering architecture, code explanation, and troubleshooting, see [GUIDE.md](GUIDE.md).