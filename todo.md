## Sprint #5

* Flask API
* configurer une IP arbitraire sur chaque conteneur (via docker-py)
    * IP, mask, passerlle

Sur l'infra coaxis pour un conteneur, il faut rajouter:

    sous_reseau=172.16.0.0
    masque=255.255.0.0
    hote_docker=192.168.2.156
    sudo route add -net $sous_reseau netmask $masque gw $hote_docker

Coté hôte docker, il faut:

* ajouter un conteneur `IPtable` ;
    * pour chaque nouveau conteneur OPT, rajouter une règle



## Sprint #4

* mastContainer.container_id
* traduction (fr, en)
* validez ip assignation


## Sprint #3

* validez container can access docker API ? vs. backend at same level as docker engine
* validez ip assignation
* front-end vueJS with JWT authentication

## Sprint #2

### Glossaire

* **interface admin** (ou `opt.coaxis.com`):
    * interface d'administration pour les techniciens Coaxis et pour les admins clients ;
    * l'indentification se fait pas email/mot de passe et donne accès au `back-office` et `front-office`.
* **back-office**:
    * accès restreint aux techniciens Coaxis ;
    * permet la création des nouveaux clients (`docker`) ;
    * accès `read-write` sur les fichiers de configuration SSH ;
* **front-office**:
    * accès restreint aux administrateurs client ;
    * permet de gérer les imprimantes et les sites géographiques ;
    * il est responsable de la gestion des _configurations SSH_ ;
    * actions tunnels (`status`, `start`, etc.) ;
    * infos état (serice, `telnet`, `ping`) ;
* **configurations SSH** :
    * elles sont stockées dans des volumes nommées accessible au `front-office`.
* **docker-opt** contient :
    * le daemon `mast` qui gère les tunnels (`restart`, `status`) ;
    * trickle pour la compression ;
    * un `nginx` qui proxy-pass les clients vers l'_interface admin_ ;
    * accès `read-only` sur les fichiers de _configurations SSH_ ;
    * accès `read-write` sur les logs (e.g. `apache`).
* **volume partage**
    * via un partage réseau (Samba, NFS, etc.) ;
    * contient les configurations SSH (une part site).

### Scénario d'Usage

* l'admin coaxis se connecte à la `opt.coaxis.com` ;
* il ajoute un nouveau client (cela pop un nouveau container docker) ;
* le client consulte `ma-societe.coaxis.com` qui le proxy-pass vers l'interface d'admin

### Questions

* IP des dockers configurable (ex. `10.128.x.x`) ;
* le nom des interfaces réseaux doit de préférence configurable (nommées par _Coaxis_) ;
* s'assurer d'avoir un volume par client
    * ~~quid des logs ? Avoir des volumes dédiés~~ (cf. ci-dessous) ;
* chiffrement du mot de passe dans le docker/makefile.