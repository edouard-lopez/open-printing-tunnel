# deployment

## connect to docker registry

    docker login docker.akema.fr:5000
    # User: coaxis 
    # Password: <Akema LessPass Password coaxis.com>

## send files to server

    ./send_archive.sh [USER@HOSTNAME] [SSH_PORT]
    
example
    
    ./send_archive.sh coaxis@192.168.2.231 2222
    
## deploy

connect to server

    ssh -p 2222 coaxis@192.168.2.231
    
move to coaxisopt folder

    cd coaxisopt
    
run `./deploy.sh`    

    ./deploy.sh [DEFAULT_INTERFACE]