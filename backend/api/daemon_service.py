import requests


def get_sites(container_ip, site_id=None):
    if not site_id:
        resource = 'http://{}:5000/sites/'.format(container_ip)
    else:
        resource = 'http://{}:5000/sites/{}'.format(container_ip, site_id)

    return requests.get(resource)
