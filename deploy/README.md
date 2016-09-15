# Deployment

## Connect to docker registry

    docker login docker.akema.fr:5000
    # User: coaxis 
    # Password: <Akema LessPass Password coaxis.com>

## Prepare the release

1. It is assumed that your `frontend` applications are **up-to-date and build**.

        cd daemon/frontend/ ; npm run build
   
1. Tag and push the new docker image to the repository:

        cd deploy/ ; ./tag_and_push.sh

## Send files to server

You need to send the latest recipe and deployment script:
 
    ./send_archive.sh
    
## Deploy

1. connect to production server:

        ssh -p 2222 coaxis@192.168.2.231
    
1. move to coaxisopt folder:

        cd coaxisopt/
    
1. launch the deployment:    

        ./deploy.sh