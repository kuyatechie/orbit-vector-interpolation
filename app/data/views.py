from django.shortcuts import render
from rest_framework import generics

from .serializers import OrbitVectorSerializer, DateTimeSerializer
from .models import OrbitVector
from .utils import Interpolator

from rest_framework import status
from rest_framework.response import Response
from django.http import Http404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class OrbitVectorCreateView(generics.CreateAPIView):
    serializer_class = OrbitVectorSerializer


class OrbitVectorInterpolateView(generics.RetrieveAPIView):
    serializer_class = DateTimeSerializer
    queryset = OrbitVector.objects.all()

    time = openapi.Parameter("time", openapi.IN_QUERY,
                                description="Time used to interpolate values",
                                type=openapi.FORMAT_DATETIME)

    def interpolate(self, time):
        interpolator = Interpolator(time)
        return interpolator.generate()

    @swagger_auto_schema(manual_parameters=[time])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def get_object(self, time):
        return self.interpolate(time)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object(request.GET.get('time'))
            serializer = self.get_serializer(instance)
        except Http404:
            return Response({"Error" : "Insufficient data."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"Error" : "Invalid datetime format. Please use %Y-%m-%dT%H:%M:%S."}, status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response({"Error" : "Invalid datetime format for parameter time."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

