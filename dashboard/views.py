from django.shortcuts import render, redirect, get_object_or_404
import datetime
from accounts.models import *
from accounts.enums import RoleCodes
from django.db.models import Q
from operator import or_
from functools import reduce
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, \
    BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework import status
from django.http import response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework import generics
import base64
from django.core.files.base import ContentFile

# for load or dump jsons
import json


class Dashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        now = datetime.datetime.now()
        user = get_object_or_404(User, pk=request.user.id)
        courses = user.courses.filter(end_date__gt=now)
        classes = Course_Calendar.objects.filter(
            Q(start_date__day=now.day) | Q(start_date__day=now.day + 1), course__in=courses)
        if classes.count() > 0:
            calendar_time = classes.first().start_date - now
        else:
            calendar_time = None
        if request.accepted_renderer.format == 'html':
            return Response({'now': now, 'classes': classes, 'calendar_time': calendar_time},
                            template_name='dashboard/dashboard.html')
        ser = DashboardSerializer(instance={'course_calendars': classes, 'now': now, 'calendar_time': calendar_time})
        return Response(ser.data)


class AppProfile(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        ser = UserProfileSerializer(request.user)
        return Response(ser.data)


# Edit Profile Page
class EditProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'dashboard/profile_page.html'

    def get(self, request):
        grades = Grade.objects.all()
        cities = City.objects.all()
        ser = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
        return Response(ser.data)

    def post(self, request):
        grades = Grade.objects.all()
        cities = City.objects.all()
        method = request.GET.get('method')
        if method is None:
            instance = request.user
            serializer = UserSaveProfileSerializer(instance, data=request.data, partial=False)
            haveError = True
            if serializer.is_valid():
                serializer.save()
                haveError = False

            showSer = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
            if haveError:
                newdict = {'errors': serializer.errors}
                newdict.update(showSer.data)
                return Response(newdict, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(showSer.data)

        if method == 'changePassword':
            showSer = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
            if not request.user.check_password(request.data['old_password']):
                # define dict this type for same concept like serializer.errors
                newdict = {'errors': {
                    'password': ['رمز وارد شده اشتباه است']
                }}
                newdict.update(showSer.data)
                return Response(newdict, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                request.user.password = make_password(request.data['password'])
                request.user.save()
                if request.accepted_renderer.format == 'html':
                    return redirect('signin')
                return Response()

        if method == 'changeAvatar':
            try:
                file=request.data['file']
                file_name=request.data['file_name']
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                avatar = ContentFile(base64.b64decode(imgstr), name=file_name +"."+ ext)
            except:
                avatar = request.user.compressImage(request.FILES.get("file"))

            if avatar:
                if not request.user.avatar.url.startswith("/media/defaults"):
                    request.user.avatar.delete()
                request.user.avatar = avatar
                request.user.save()
                showSer = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
                return Response(showSer.data)


# # Edit profile page --> change avatar form
# @login_required
# def change_avatar(request):
#     if request.method == 'POST':
#         form = ProfileForm()
#         avatar = request.user.compressImage(request.FILES.get("file"))
#         if avatar:
#             if not request.user.avatar.url.startswith("/media/defaults"):
#                 request.user.avatar.delete()
#             request.user.avatar = avatar
#             request.user.save()
#         return redirect('dashboard')
#     else:
#         error = 'تغییر پروفایل با مشکل رو به رو شد'
#         return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})
#
#
# # Edit profile page --> change field except avatar field
# @login_required
# def change_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#         else:
#             return render(request, 'dashboard/profile_page.html', {'form': form})


# # Edit profile page --> change password
# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = ProfileForm()
#         if not request.user.check_password(request.POST['old_password']):
#             error = 'رمز وارد شده اشتباه است'
#             return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})
#         else:
#             error = 'تغییر رمز با موفقیت انجام شد'
#             request.user.password = make_password(request.POST['password'])
#             request.user.save()
#             return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})


# Lessons Page
class Lessons(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        now = datetime.datetime.now()
        if request.accepted_renderer.format == 'html':
            return Response({"have_class" : request.user.courses.filter(end_date__gt=now).count()!=0} ,template_name='dashboard/lessons.html')
# Shopping Page
class Shopping(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        grades = Grade.objects.all()
        lessons = Lesson.objects.filter(parent__id=None)
        teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        ser = ShoppingSerializer(instance={'grades': grades, 'lessons': lessons, 'teachers': teachers})
        return Response(ser.data, template_name='dashboard/shopping.html')


def getAllLessons(lesson_id):
    lessons = Lesson.objects.filter(id=lesson_id)
    whilelessons = lessons
    while True:
        extend_lesson = []
        query = reduce(or_, (Q(parent__id=lesson.id)
                             for lesson in whilelessons))
        extend_lesson = Lesson.objects.filter(query)
        if len(extend_lesson) == 0:
            break
        else:
            whilelessons = extend_lesson
            lessons = lessons | whilelessons
    query = reduce(or_, (Q(lesson__id=lesson.id) for lesson in lessons))
    return query



class GetLessonsViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseLessonsSerializer
    http_method_names = ['get', ]

    search_fields = ('title',)
    ordering_fields = ('title',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.count()==0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'text/javascript' in request.headers['Accept']:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_queryset(self):
         query = Q()
         if self.request.GET.get("lesson"):
             query &= getAllLessons(self.request.GET.get("lesson"))
         courses = self.request.user.courses.filter(query).order_by('-end_date')
         return courses


class GetShoppingViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ShoppingCourseSerializer
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'text/javascript' in request.headers['Accept']:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        now = datetime.datetime.now()
        query = Q(end_date__gt=now)
        if self.request.GET.get("teacher") or self.request.GET.get("lesson") or  self.request.GET.get("grade"):
            if  self.request.GET.get("lesson"):
                query &= getAllLessons( self.request.GET.get("lesson"))
            if  self.request.GET.get("grade"):
                query &= (Q(grade__id= self.request.GET.get("grade")) | Q(grade__id=None))
            if  self.request.GET.get("teacher"):
                query &= Q(teacher__id= self.request.GET.get("teacher"))
        else:
            if ( self.request.user.grades.count() > 0):
                query &= (Q(grade__id= self.request.user.grades.first().id) | Q(grade__id=None))

        if self.request.user.courses.all():
            queryNot = reduce(or_, (Q(id=course.id)
                                    for course in self.request.user.courses.all()))
            query = query & ~queryNot
        courses = Course.objects.filter(query)
        return courses

# @api_view(['GET', ])
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
# def filemanager(request, code):
#         course = Course.objects.get(code=code)
#         try:
#             request.user.courses.get(id=course.id)
#         except:
#             if request.accepted_renderer.format == 'html':
#                 return redirect('/dashboard/shopping/')
#             return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
#


class FileManager(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    queryset = Course.objects.all()
    serializer_class = FilesSerializer
    lookup_field = 'code'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            request.user.courses.get(id=instance.id)
        except:
            if request.accepted_renderer.format == 'html':
                return redirect('/dashboard/shopping/')
        documents = instance.document_set.all()
        fileSerializer = FilesSerializer(instance={'documents': documents, 'course': instance})
        return Response(fileSerializer.data, template_name='dashboard/filemanager.html')


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

