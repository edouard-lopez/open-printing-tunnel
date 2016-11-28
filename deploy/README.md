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
    # Password: <admin@akema.fr + Akema LessPass Password coaxis.com>

## Release

Run the script with the version to release:

    cd deploy/
    ./release.sh v1.5.11
    ./release.sh  # the 'latest' tag

It is the same as:

1. rebuild `daemon/frontend/` ;
1. rebuild `frontend/` ;
1. tag and push the release ;
1. update the `docker-compose` and deploy script.

## Deploy

Connect to production server using the `optbox` forwarding rule (cf. [optbox's section](#optbox)):

        ssh -p 2222 coaxis@optbox-forward
        cd coaxisopt/
        ./deploy.sh ens192 v1.5.10
        ./deploy.sh