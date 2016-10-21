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

## Prepare the release

1. It is assumed that your `frontend` applications are **up-to-date and build**.

        cd daemon/frontend/ ; 
        npm run build
   
1. Tag and push the new docker image to the repository:

        cd ../../deploy/ ; 
        ./tag_and_push.sh

## Send files to server

You need to send the latest recipe and deployment script:
 
    ./send_archive.sh
    
## Deploy

1. connect to production server using the `optbox` forwarding rule (cf. [optbox's section](#optbox)):

        ssh -p 2222 coaxis@optbox-forward
    
1. move to coaxisopt folder:

        cd coaxisopt/
    
1. launch the deployment:    

        ./deploy.sh