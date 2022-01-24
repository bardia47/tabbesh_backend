from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from dashboard.models.course import Course
from accounts.models.user import User
from rest_framework.response import Response
from accounts.enums.enum_role_code import RoleCodeEnum

class CounterView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        course_counter = Course.objects.all().count()
        student_counter = User.objects.filter(role__code=RoleCodeEnum.STUDENT.value).count()
        teacher_counter = User.objects.filter(role__code=RoleCodeEnum.TEACHER.value).count()
        data = {"course_counter": course_counter, "student_counter": student_counter,
                "teacher_counter": teacher_counter}
        return Response(data)

