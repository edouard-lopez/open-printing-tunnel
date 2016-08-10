from api import models
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client


class DaemonSerializer(serializers.ModelSerializer):
    container_info = serializers.ReadOnlyField()
    company = ClientSerializer()

    class Meta:
        model = models.Daemon
        fields = ('id', 'ip', 'subnet', 'gateway', 'vlan', 'hostname', 'company', 'container_id', 'container_info',)
        read_only_fields = ('id', 'company', 'container_id', 'container_info',)
