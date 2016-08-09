import requests


def get_sites(container_ip, site_id=None):
    if not site_id:
        resource = 'https://{}/sites/'.format(container_ip)
    else:
        resource = 'https://{}/sites/{}'.format(container_ip, site_id)

    return requests.get(resource)
