import json
import uuid

from django.contrib.auth import login, authenticate
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from docker import Client

from api import models, serializers
from api.permissions import IsAdmin

docker_api = Client(base_url='unix://var/run/docker.sock')


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def list(request, format=None):
        if request.user.is_authenticated():
            user = {
                'id': request.user.id,
                'email': request.user.email,
                'is_admin': request.user.is_staff,
                'is_authenticated': True
            }
        else:
            user = {
                'id': None,
                'email': None,
                'is_admin': False,
                'is_authenticated': False
            }

        return Response({
            'user': user
        })

    @staticmethod
    def post(request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user and user.is_active:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def get_queryset(self):
        return models.Company.objects.all()


class RemoteNodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RemoteNodeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def get_queryset(self):
        # print(cli.containers())
        for container in docker_api.containers():
            print(container['Image'])
        # return models.RemoteNode.objects.filter(company=self.request.user.company)
        return models.RemoteNode.objects.all()


class MastContainerViewSet(viewsets.ModelViewSet):
    queryset = models.MastContainer.objects.all()
    serializer_class = serializers.MastContainerSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        containers = []
        for container in self.queryset:
            container.append({'config': docker_api.containers(id=container['Id'])})
            containers.append(container)
        print(containers)
        return Response(containers)

    def post(self, request, pk=None):
        image_name = 'busybox:latest'
        docker_api.pull(image_name)
        container = docker_api.create_container(
            image=image_name,
            name='mast_{}'.format(uuid.uuid4()),
            command='tail -f /dev/null'
        )
        container_id = container.get('Id')
        docker_api.start(container=container_id)
        print(container)

        container_obj = models.MastContainer.objects.create(
            id=container_id,
            config=json.dumps(container),
            company=None
        )
        if container_obj:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        print(docker_api.containers(id=id))
        return Response(status=status.HTTP_400_BAD_REQUEST)
