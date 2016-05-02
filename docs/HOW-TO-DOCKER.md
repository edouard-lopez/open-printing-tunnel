## Installation

* [Docker Install on Linux](https://docs.docker.com/linux/step_one/) ;
* [Docker Compose](https://docs.docker.com/compose/install/).

```bash
    # sudo apt-get update
    # sudo apt-get install -y apt-transport-https ca-certificates docker linux-image-extra-$(uname -r)
    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee -a /etc/apt/sources.list.d/docker.list
    sudo apt-get update
    # sudo apt-get purge lxc-docker
    # sudo apt-cache policy docker-engine
    sudo apt-get install -y docker docker-engine
    sudo usermod -aG docker coaxis
    sudo apt-get autoremove
    sudo wget https://github.com/docker/compose/releases/download/1.7.0/docker-compose-`uname -s`-`uname -m` -O /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
```

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
