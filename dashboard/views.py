from django.shortcuts import render, redirect
from operator import or_
from functools import reduce
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, \
    BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework import status
from rest_framework import generics
from core.utils import Utils
from rest_framework.decorators import permission_classes
from core.utils import TextUtils
# for load or dump jsons
from django.db.models import Case, Value, When, IntegerField
from .permission import EditDocumentPermission
from .enums import DashboardMessages
from zarinpal.serializers import CartInstallmentSerializer


# TODO clean this  after using react
class Dashboard(generics.RetrieveAPIView):
    """
                    ### swagger of this is incorrect !
          """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'dashboard/dashboard.html'
    serializer_class = DashboardSerializer

    def retrieve(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        need_buy_titles = None
        if self.request.user.is_student():
            courses = request.user.courses().filter(end_date__gt=now)
            value = jdatetime.datetime.fromgregorian(datetime=now).day
            if (value >= 20):
                need_buys = Installment.objects.filter(
                    start_date__gt=now, start_date__lt=now + datetime.timedelta(30), course__in=courses).exclude(
                    user=request.user)
                if (need_buys.exists()):
                    # need_buy_ids = list(need_buys.values_list('id', flat=True))
                    need_buy_titles = TextUtils.convert_list_to_string(
                        list(need_buys.values_list('course__title', flat=True)))
        elif self.request.user.is_teacher():
            courses = Course.objects.filter(teacher__id=self.request.user.id, end_date__gt=now)
        else:
            courses = Course.objects.filter(end_date__gt=now)
        classes = Course_Calendar.objects.filter(
            Q(start_date__day=now.day) | Q(start_date__day=now.day + 1), course__in=courses)
        if classes.count() > 0:
            calendar_time = classes.first().start_date - now
        else:
            calendar_time = None
        if request.accepted_renderer.format == 'html':
            resp = {'now': now, 'classes': classes, 'calendar_time': calendar_time}
            if need_buy_titles:
                resp.update({'need_buy': {'need_buy_text': TextUtils.replacer(DashboardMessages.needBuyMassage.value,
                                                                              [need_buy_titles])}})
            return Response(resp)
        # ser = DashboardSerializer(instance={'course_calendars': classes, 'now': now, 'calendar_time': calendar_time})
        # return Response(ser.data)


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
            serializer = UserProfileSerializer(instance, data=request.data, partial=False)
            haveError = True
            if serializer.is_valid():
                serializer.save()
                haveError = False

            showSer = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
            if haveError:
                newdict = {'errors': serializer.errors}
                newdict.update(showSer.data)
                return Response(newdict, status=status.HTTP_406_NOT_ACCEPTABLE)
            Utils.cleanMenuCache(request)
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
                    if request.session.get('new_login'):
                        del request.session['new_login']
                    return redirect('signin')
                return Response()
        # if request sent from app, use base64
        if method == 'changeAvatar':
            # this is for  flutter
            # try:
            #     file = request.data['file']
            #     file_name = request.data['file_name']
            #     format, imgstr = file.split(';base64,')
            #     ext = format.split('/')[-1]
            #     avatar = ContentFile(base64.b64decode(imgstr), name=file_name + "." + ext)
            # except:
            avatar = Utils.compressImage(request.FILES.get("file"), width=200)

            if avatar:
                if not request.user.avatar.url.startswith("/media/defaults"):
                    request.user.avatar.delete()
                request.user.avatar = avatar
                request.user.save()
                showSer = UserProfileShowSerializer(instance={'grades': grades, 'cities': cities, "user": request.user})
                Utils.cleanMenuCache(request)
                return Response(showSer.data)


# Lessons Page
class Lessons(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        now = datetime.datetime.now()
        if request.accepted_renderer.format == 'html':
            return Response({"have_class": self.request.user.courses().count() != 0},
                            template_name='dashboard/lessons.html')


class GetLessonsViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseLessonsSerializer
    http_method_names = ['get', ]
    search_fields = ('title',)
    ordering_fields = ('title',)
    pagination_class = None

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     if queryset.count()==0:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     if 'text/javascript' in request.headers['Accept']:
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        query = Q()
        # it was for app and now is depricated
        # if self.request.GET.get("lesson"):
        #     query &= getAllLessons(self.request.GET.get("lesson"))

        if self.request.user.is_student():
            courses = self.request.user.courses().filter(query)
        elif self.request.user.is_teacher():
            query &= Q(teacher__id=self.request.user.id)
            courses = Course.objects.filter(query)
        else:
            now = datetime.datetime.now()
            query &= Q(end_date__gt=now)
            courses = Course.objects.filter(query)

        courses = courses.order_by('-end_date')
        return courses


# get child lessons of parent (using tree)
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


# Shopping Page
class Shopping(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        grades = Grade.objects.all()
        lessons = Lesson.objects.filter(parent__id=None)
        teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        ser = ShoppingSerializer(instance={'grades': grades, 'lessons': lessons, 'teachers': teachers})
        return Response(ser.data, template_name='dashboard/shopping.html')


class GetShoppingViewSet(viewsets.ModelViewSet):
    # thats fake :/ because its Mandatory
    queryset = Course.objects.filter(is_active=True)
    serializer_class = ShoppingCourseSerializer
    http_method_names = ['get', ]

    # default show all active courses
    def get_queryset(self):
        now = datetime.datetime.now()
        queryset = super(GetShoppingViewSet, self).get_queryset()
        query = Q(end_date__gt=now + datetime.timedelta(days=InstallmentModelEnum.installmentDateBefore.value))
        if self.request.user.courses().all():
            queryNot = reduce(or_, (Q(id=course.id)
                                    for course in self.request.user.courses().all()))
            query = query & ~queryNot

        if self.request.GET.get("teacher") or self.request.GET.get("lesson") or self.request.GET.get("grade"):
            if self.request.GET.get("lesson"):
                query &= getAllLessons(self.request.GET.get("lesson"))
            if self.request.GET.get("grade"):
                query &= (Q(grade__id=self.request.GET.get("grade")) | Q(grade__id=None))
            if self.request.GET.get("teacher"):
                query &= Q(teacher__id=self.request.GET.get("teacher"))
            queryset = queryset.filter(query)
        else:
            queryset = queryset.filter(query)
            if self.request.user.grades.count() > 0:
                query1 = (Q(grade__id=self.request.user.grades.first().id) | Q(grade__id=None))
                query2 = ~(Q(grade__id=self.request.user.grades.first().id) | Q(grade__id=None))
                queryset = (queryset
                            .filter(query1 | query2).annotate(
                    search_type_ordering=Case(
                        When(query1, then=Value(2)),
                        When(query2, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()))
                            .order_by('-search_type_ordering'))

        return queryset


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


class FileManager(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    queryset = Course.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'code'

    def get_permissions(self):
        if self.action != 'retrieve':  # this not is not for student
            self.permission_classes = [EditDocumentPermission, ]
        return super(FileManager, self).get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            if request.user.is_student():
                request.user.courses().get(id=instance.id)
        except:
            if request.accepted_renderer.format == 'html':
                return redirect('/dashboard/shopping/')
        documents = instance.document_set.all()
        fileSerializer = FilesSerializer(instance={'documents': documents, 'course': instance})
        return Response(fileSerializer.data, template_name='dashboard/filemanager.html')
        # return Response(template_name='dashboard/test.html')

    def create(self, request, *args, **kwargs):
        # request and the course should be for a same teacher
        course = Course.objects.get(code=self.kwargs['code'])
        request.data.update({"sender": request.user.id, "course": course.id})  # change because we handle course with id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": "yes"}, status=status.HTTP_200_OK)


# this permission is not for student
@permission_classes((EditDocumentPermission,))
class UpdateFile(viewsets.ModelViewSet):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class = DocumentSerializer
    # code for get course
    lookup_field = ('document_id', 'code',)

    def get_queryset(self):
        queryset = Document.objects.get(pk=self.kwargs['document_id'])
        return queryset

    def update(self, request, *args, **kwargs):
        # we can set course and sender here
        instance = self.get_queryset()
        # make comment !
        # if request.data['upload_document'] == '':
        #     request.data['upload_document'] = instance.upload_document
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({"success": "yes"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response({"success": "yes"}, status=status.HTTP_204_NO_CONTENT)


class ClassList(generics.RetrieveAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    queryset = Course.objects.all()
    serializer_class = FilesSerializer
    lookup_field = 'code'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        students = instance.students().all()
        listSerializer = ClassListSerializer(instance={'students': students, 'course': instance},
                                             context={'course_id': instance.id})
        return Response(listSerializer.data)


def teacher_course_panel(request, code):
    return render(request, 'dashboard/teacher_course_panel.html', {"code": code})


def student_course_panel(request, code):
    return render(request, 'dashboard/student_course_panel.html', {"code": code})


class UserInstallmentsViewSet(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = UserCourseInsalmentSerializer

    lookup_field = 'code'
    pagination_class = None
