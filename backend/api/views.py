import logging

import docker
from django.contrib.auth import login, authenticate
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from api import models, serializers, services, container_services
from api.permissions import IsTechnician
from api.services import get_company, get_employee

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def list(request, format=None):
        if request.user.is_authenticated():
            employee = get_employee(request.user)
            user = {
                'id': request.user.id,
                'email': request.user.email,
                'is_admin': request.user.is_staff,
                'is_technician': employee.is_technician,
                'is_authenticated': True
            }
        else:
            user = {
                'id': None,
                'email': None,
                'is_admin': False,
                'is_authenticated': False
            }

        return Response(user)

    @staticmethod
    def post(request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user and user.is_active:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return models.Company.objects.all()


class RemoteNodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RemoteNodeSerializer
    permission_classes = (permissions.IsAuthenticated, IsTechnician,)

    def get_queryset(self):
        for container in docker_api.containers():
            print(container['Image'])
        return models.RemoteNode.objects.filter(company__in=self.request.user.employee.companies.all())


class MastContainerViewSet(viewsets.ModelViewSet):
    queryset = models.MastContainer.objects.all()
    serializer_class = serializers.MastContainerSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        employee = services.get_employee(request.user)

        container = container_services.pop_new_container({
            'company_id': request.data.get('company_id'),
            'subnet': request.data.get('subnet'),
            'gateway': request.data.get('gateway'),
            'ip': request.data.get('ip'),
            'hostname': request.data.get('hostname'),
            'labels': request.data.get('labels')
        }, docker_api)

        container_obj = container_services.save_infos({
            'user': employee,
            'container': container,
            'company_id': request.data.get('company_id'),
            'description': request.data.get('description'),
        })

        if container_obj:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        container_services.destroy(instance.container_id)
        instance.delete()
