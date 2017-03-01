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

## Let's Encrypt
    
SSH on to `docker.akema.fr`
    

### Checks certificate is valid

check certificate is valid in a linux terminal

    $ echo | openssl s_client -connect "$yourdomain":5000 2>/dev/null | openssl x509 -noout -dates
    notBefore=Nov 21 14:07:00 2016 GMT
    notAfter=Feb 19 14:07:00 2017 GMT

### Renew certificate

It's done by a script `/root/registry/renew-certificate.sh`on the host we run with `cron`:

    #!/usr/bin/env bash
    # Usage:
    #       ./renew-certificate.sh [your.domain.org]
    
    yourdomain="${1:-docker.akema.fr}"
    
    printf "Renew certificate for: %s\n" "$yourdomain"
    printf "\n--\n%s\n" "$(date '+%Y-%m-%dT%H:%M:%S')" >> /var/log/lets-encrypt-renewal.log
    /root/certbot-auto renew --force-renewal --no-self-upgrade 1>&2 | tee --append /var/log/lets-encrypt-renewal.log
    
    printf "Copy certificate to docker registry\n"
    cp /etc/letsencrypt/live/"$yourdomain"/privkey.pem /root/registry/certs/"$yourdomain".key
    cp /etc/letsencrypt/live/"$yourdomain"/fullchain.pem /root/registry/certs/"$yourdomain".crt
    
    # Restart registry container
    cd /root/registry
    docker-compose restart

Re-check the certificate to see if date have been updated.