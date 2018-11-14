# Deployment

## Optbox

In developmenet we use the `optbox` device as a reverse proxy to access customer's infrastructure.

    Host optbox-forward
    Port 2222
    HostName <your-optbox-ip>
    IdentityFile ~/.ssh/id_rsa.pub 

## Connect to docker registry

    docker login docker.akema.fr:5000
    # User: coaxis 
    # Password: on LessPass v1: coaxis.com + admin@akema.fr + v1>

## Release

Run the script with the version to release:

    make release

It is the same as:

1. rebuild `daemon/frontend/` ;
1. rebuild `frontend/` ;
1. tag and push the release ;
1. update the `docker-compose` and deploy script.

## Deploy

Connect to production server using the `optbox` forwarding rule (cf. [optbox's section](#optbox)):

    ssh -p 2222 coaxis@optbox-forward
    cd coaxisopt/
    ./deploy.sh ens192 v1.7.4
