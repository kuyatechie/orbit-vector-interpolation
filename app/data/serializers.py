from rest_framework import serializers
from data.models import OrbitVector


class OrbitVectorSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(required=True, allow_null=False)
    posx = serializers.FloatField(required=True, allow_null=False)
    posy = serializers.FloatField(required=True, allow_null=False)
    posz = serializers.FloatField(required=True, allow_null=False)
    velx = serializers.FloatField(required=True, allow_null=False)
    vely = serializers.FloatField(required=True, allow_null=False)
    velz = serializers.FloatField(required=True, allow_null=False)

    class Meta:
        model = OrbitVector
        fields = ('time', 'posx', 'posy', 'posz', 'velx', 'vely', 'velz')
        

class DateTimeSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(required=True, allow_null=False)

    class Meta:
        model = OrbitVector
        fields = ('time', 'posx', 'posy', 'posz', 'velx', 'vely', 'velz')
