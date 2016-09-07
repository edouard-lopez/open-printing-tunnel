# -*- coding: utf-8 -*-

from django import shortcuts

from api import models


def get_employee(user):
    return shortcuts.get_object_or_404(models.Employee, pk=user.employee.id)


def get_clients(user):
    employee = get_employee(user)
    return employee.clients.all()


def is_technician(user):
    return get_employee(user).is_technician


def get_daemons(user):
    clients = get_clients(user)

    return models.Daemon.objects.filter(client__in=clients)
