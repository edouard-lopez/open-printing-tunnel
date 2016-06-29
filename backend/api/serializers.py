from rest_framework import serializers

from api import models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company


class RemoteNodeSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)

    class Meta:
        model = models.RemoteNode
        read_only_fields = ('company ', 'created', 'modified')


class MastContainerSerializer(serializers.ModelSerializer):
    # company = CompanySerializer(read_only=True)

    class Meta:
        model = models.MastContainer
        fields = ('id', 'description', 'company', 'config')
        read_only_fields = ('company', 'config')
