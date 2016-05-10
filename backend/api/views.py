from django.contrib.auth import login, authenticate
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from api import models, serializers
from api.permissions import IsAdmin


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
        return models.RemoteNode.objects.filter(company=self.request.user.company)
