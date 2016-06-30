import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from api import models, container_services


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company


class RemoteNodeSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)

    class Meta:
        model = models.RemoteNode
        read_only_fields = ('company ', 'created', 'modified')


class MastContainerSerializer(serializers.ModelSerializer):
    infos = serializers.ReadOnlyField()

    class Meta:
        model = models.MastContainer
        fields = ('id', 'description', 'company', 'container_id', 'infos',)
        read_only_fields = ('company', 'container_id', 'infos',)
