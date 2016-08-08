import jinja2


def render(filename, data):
    package_name = 'scripts'
    env = jinja2.Environment(loader=jinja2.PackageLoader(package_name, 'templates'))

    template = env.get_template(filename)

    return template.render(data)
