from django.urls import path, include
from dashboard.views.view_public_courses import PublicCourseSugesstionsView, PublicCourseView
from dashboard.views.view_public_teachers import PublicTecherView, TeacherCursesView
from dashboard.views.view_shopping import ShoppingCourseViewSet
from dashboard.views.view_courses import UserCoursesView
from dashboard.views.view_course_panel import PanelCoursesView, CourseCalenderView, OfflineVideoView
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('courses', PublicCourseView)
suggestions_router = routers.NestedSimpleRouter(router, 'courses', lookup='pk')
suggestions_router.register('sugesstion', PublicCourseSugesstionsView, basename='suggestion')

router.register('teachers', PublicTecherView)
teacher_courses_router = routers.NestedSimpleRouter(router,'teachers', lookup='slug')
teacher_courses_router.register('course', TeacherCursesView, basename='course')

# dashboard router urls
dashboard_router = routers.SimpleRouter()
dashboard_router.register('shopping', ShoppingCourseViewSet, basename='shopping')
dashboard_router.register('panel/courses/', UserCoursesView, basename='courses')
dashboard_router.register('course', PanelCoursesView, basename='course')
course_nested_router = routers.NestedSimpleRouter(dashboard_router, 'course', lookup='pk')
course_nested_router.register('calender', CourseCalenderView, basename='calender')
course_nested_router.register('offlines', OfflineVideoView, basename='offlines')


urlpatterns = [
    path('public/', include([
        path('', include(router.urls)),
        path('', include(suggestions_router.urls)),
        path('',include(teacher_courses_router.urls))]
    )),
    path('', include(dashboard_router.urls)),
    path('', include(course_nested_router.urls))
]
