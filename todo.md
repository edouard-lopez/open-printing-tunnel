* grab site SSH port to customize telnet command
* ~~PV recette~~

* fixes
    * [ ] unicode caractere in description?

## Sprint #8

* [ ] ajouter l'info de la limite de débit du site → déplacer dans _future_
    
## Sprint #7

* [x] fix status #50
* [x] fix modal #52

### Features 

* [x] Récupération des infos d'une/des imprimante-s [#36](https://gitlab.akema.fr/coaxis/discussions/issues/36)
* [x] Scripts d'installation supplémentaires [#35](https://gitlab.akema.fr/coaxis/discussions/issues/35)
* [x] Detection des imprimantes [#12](https://gitlab.akema.fr/coaxis/discussions/issues/12) 


## Sprint #5

* refonte architecture logiciel (clentsdeaemon)
* Plug sites ;
* Plug printer ;

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