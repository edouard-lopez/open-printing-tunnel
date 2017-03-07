import json
import logging

import docker
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api import container_services
from api import models, serializers
from api import permissions as app_permissions
from api import services

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


class UserMeViewSet(viewsets.ViewSet):
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


class ClientsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    permission_classes = (app_permissions.IsTechnician,)
    search_fields = ('id', 'name',)

    def list(self, request, *args, **kwargs):
        self.queryset = services.get_clients(self.request.user)

        return super(ClientsViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        creator = services.get_employee(self.request.user)
        serializer.save(employees=[creator.id])


class NetworksViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAdminUser,)

    @staticmethod
    def list(request, format=None):
        return Response(container_services.filter_opt_networks(docker_api.networks()))

    def destroy(self, request, pk=None):
        docker_api.remove_network(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DaemonsViewSet(viewsets.ModelViewSet):
    queryset = models.Daemon.objects.all()
    serializer_class = serializers.DaemonSerializer
    permission_classes = (app_permissions.IsTechnician,)

    def create(self, request, *args, **kwargs):
        data = {
            "ip": request.data.get('ip'),
            "subnet": request.data.get('subnet'),
            "gateway": request.data.get('gateway'),
            "vlan": request.data.get('vlan'),
            "hostname": request.data.get('hostname'),
            "client_id": request.data.get('client_id')
        }
        data_without_empty_value = dict((k, v) for k, v in data.items() if v)
        try:
            container = container_services.pop_new_container(data_without_empty_value, docker_api)
            data_without_empty_value['container_id'] = container.get('Id')
            models.Daemon.objects.create(**data_without_empty_value)
        except Exception as e:
            logger.exception(e)
            raise ValidationError(str(e))
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        new_data = serializer.data
        new_data['container_info'] = docker_api.inspect_container(instance.container_id)
        return Response(new_data)

    def perform_destroy(self, instance):
        container_services.destroy(instance.container_id)
        instance.delete()


class Container(APIView):
    permission_classes = (app_permissions.IsTechnician,)

    def get(self, request, container_id, action=None):
        try:
            container = models.Daemon.objects.get(id=container_id)
            data = serializers.DaemonSerializer(container).data
            return Response(data=data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, container_id, action):
        try:
            container = models.Daemon.objects.get(id=container_id)
            data = serializers.DaemonSerializer(container).data
            if action == 'restart':
                container_services.restart(container.container_id, docker_api)
                return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except ObjectDoesNotExist:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)