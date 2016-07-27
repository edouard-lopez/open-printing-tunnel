## Installation

* [Docker Install on Linux](https://docs.docker.com/linux/step_one/) ;
* [Docker Compose](https://docs.docker.com/compose/install/).

```bash
sudo apt-key adv \
    --keyserver hkp://p80.pool.sks-keyservers.net:80 \
    --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" \
    | sudo tee -a /etc/apt/sources.list.d/docker.list
sudo apt-get purge lxc-docker
sudo apt-get update && sudo apt-get install --yes \
    apt-transport-https \
    ca-certificates \
    docker-engine \
    linux-image-extra-"$(uname -r)"
sudo apt-get autoremove
sudo usermod -aG docker coaxis
sudo wget \
    --output-document=/usr/local/bin/docker-compose \
    https://github.com/docker/compose/releases/download/1.7.0/docker-compose-"$(uname -s)"-"$(uname -m)" 
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Usage

### Configure DNS

You need to edit [docker-compose.yml](../docker-compose.yml) file to change the value of the [`extra_hosts`](https://docs.docker.com/compose/compose-file/#extra-hosts) directive. Only the domain name should change and target the local loop (e.g. `127.0.0.1`): 

    extra_hosts:
      - "mon-client.opt:127.0.0.1"

    
### Entering in a `docker`

You can enter in a `docker` container to explore it live:

    docker exec -it coaxisopt_daemon_1 bash
    
Where _`coaxisopt_daemon_1`_ is the name of the container (see [`docker ps -a`](https://docs.docker.com/engine/reference/commandline/ps/))

#### Reading the logs

We can use the above method to watch apache logs:

    docker exec -it coaxisopt_daemon_1 bash -c 'tail -f /var/log/apache2/*'
