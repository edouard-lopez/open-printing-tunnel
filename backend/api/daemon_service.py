import requests


def get_sites(container_ip):
    return requests.get('http://{}:5000/sites/'.format(container_ip))


def get_site(container_ip, site_id):
    resource = 'http://{}:5000/sites/{}'.format(container_ip, site_id)
    return requests.get(resource)
