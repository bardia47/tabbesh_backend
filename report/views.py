from django.shortcuts import render, redirect, get_object_or_404
import datetime
from accounts.models import *
from accounts.enums import RoleCodes
from django.db.models import Q
from operator import or_
from functools import reduce
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, \
    BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from dashboard.serializers import *
from rest_framework import status
from django.http import response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework import generics
import base64
from django.core.files.base import ContentFile
from accounts.utils import  Utils
# for load or dump jsons


class ClassList(generics.RetrieveAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    queryset = Course.objects.all()
    serializer_class = FilesSerializer
    lookup_field = 'code'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        students = instance.user_set.all()
        listSerializer = ClassListSerializer(instance={'students': students, 'course': instance},context={'course_id': instance.id})
        return Response(listSerializer.data)
