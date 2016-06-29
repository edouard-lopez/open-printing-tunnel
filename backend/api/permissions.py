from rest_framework import permissions

from api import services


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return services.get_employee(request.user).is_technician
