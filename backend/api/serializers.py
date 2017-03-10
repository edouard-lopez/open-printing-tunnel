from api import models
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'

class DaemonSerializer(serializers.ModelSerializer):
    container_info = serializers.ReadOnlyField()
    client = ClientSerializer(read_only=True)

    class Meta:
        model = models.Daemon
        fields = ('id', 'ip', 'subnet', 'gateway', 'vlan', 'hostname', 'client', 'container_id', 'container_info',)
        read_only_fields = ('id', 'container_id', 'container_info',)
