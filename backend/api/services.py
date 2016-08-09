# -*- coding: utf-8 -*-

from django import shortcuts

from api import models


def get_employee(user):
    return shortcuts.get_object_or_404(models.Employee, pk=user.employee.id)


def get_company(employee):
    return employee.companies.first()