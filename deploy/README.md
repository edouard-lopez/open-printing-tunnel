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

## Release Version

First, we create a feature/patch tag:

    make tag-as-feature
    # or tag-as-patch

Then we will build new container images, tagged as `latest` and the latest `git` tag. Then we push them to [DockerHub](hub.docker.com/r/coaxisasp/):

    make release

## Deploy

Connect to production server using the `optbox` forwarding rule (cf. [optbox's section](#optbox)):

    ssh -p 2222 coaxis@optbox-forward
    cd coaxisopt/
    ./deploy.sh ens192 v1.7.4
