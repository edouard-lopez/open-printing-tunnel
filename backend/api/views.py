import docker
from django import dispatch
from django.contrib.auth import login, authenticate
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from api import models, serializers, services, container_services
from api.models import MastContainer
from api.permissions import IsAdmin

docker_api = docker.Client(base_url='unix://var/run/docker.sock')


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
        for container in docker_api.containers():
            print(container['Image'])
        return models.RemoteNode.objects.filter(company=self.request.user.company)


class MastContainerViewSet(viewsets.ModelViewSet):
    queryset = models.MastContainer.objects.all()
    serializer_class = serializers.MastContainerSerializer
    permission_classes = (permissions.AllowAny,)

    # def get_queryset(self):
    #     return self.queryset

    def create(self, request, *args, **kwargs):
        container = container_services.pop_new_container()
        user = services.get_employee(request.user)

        container_obj = container_services.save_infos({
            'user': user,
            'container': container,
            'description': request.data.get('description')
        })

        if container_obj:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    container_destroyed = dispatch.Signal(providing_args=[])
    def perform_destroy(self, instance):
        self.container_destroyed.send(sender=self.__class__)
        # container_services.destroy(instance.container_id)
        # instance.delete()

    @receiver(post_delete, sender=MastContainer)
    def destroy_container(sender, **kwargs):
        print('signal received!')
        # container_services.destroy(instance.container_id)