from rest_framework import viewsets
from dashboard.serializers.serializer_user_courses import UserCoursesSerializer
from accounts.models.user import User
from dashboard.models.course import Course
from rest_framework.permissions import IsAuthenticated


class UserCoursesView(viewsets.ModelViewSet):
    serializer_class = UserCoursesSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    lookup_field = None

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).courses()

