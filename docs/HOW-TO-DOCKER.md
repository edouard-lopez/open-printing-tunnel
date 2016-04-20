## Installation

* [Docker Install on Linux](https://docs.docker.com/linux/step_one/) ;
* [Docker Compose](https://docs.docker.com/compose/install/).

## Usage

### Start OPT

We are using a `docker-compose` to manage the various containers: 

    cd coaxis-opt/  # project root directory
    docker-compose build  # create the containers images 
    docker-compose up  # start project
    
### Entering in a `docker`

You can enter in a `docker` container to explore it live:

    docker exec -it coaxisopt_daemon_1 bash
    
Where _`coaxisopt_daemon_1`_ is the name of the container (see [`docker ps -a`](https://docs.docker.com/engine/reference/commandline/ps/))

#### Reading the logs

We can use the above method to watch apache logs:

    docker exec -it coaxisopt_daemon_1 bash -c 'tail -f /var/log/apache2/*'
