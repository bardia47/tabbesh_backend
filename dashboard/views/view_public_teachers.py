from rest_framework import viewsets
from dashboard.serializers.serializer_public_teacher import TeacherSerializer
from dashboard.serializers.serializer_public_course import CourseSerializer
from accounts.enums.enum_role_code import RoleCodeEnum
from accounts.models.user import TeacherUser
from core.pagination import Pagination
from dashboard.models import Course


class PublicTecherView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    queryset = TeacherUser.objects.filter(role__exact=RoleCodeEnum.TEACHER.value)
    http_method_names = ['get']

class TeacherCursesView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    lookup_field = 'slug'
    http_method_names = ['get']
    pagination_class = Pagination

    def get_queryset(self):
        return Course.objects.filter(teacher_id=self.kwargs['slug_id'])
