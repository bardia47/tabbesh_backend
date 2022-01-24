from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views.view_counter import CounterView
from .views.view_new_course import NewCourseHome
from .views.view_search import SearchHome

router = DefaultRouter()
# router.register('teachers', TeacherViewset)
# router.register('blog', WeblogViewSet)
# router.register('slides', SlideViewSet)

urlpatterns = [
    path('counter/', cache_page(60 * 60 * 2)(CounterView.as_view()), name='counter'),
    # path('most-discounted-courses/', cache_page(60 * 60 * 2)(MostDiscountedCourses.as_view()),
    #      name='most-discounted-courses'),
   # path('best-selling-courses/', cache_page(60 * 60 * 2)(BestSellingCourses.as_view()), name='best-selling-courses'),
    path('search-home/', SearchHome.as_view(), name='search-home'),
    path('new-course-home/', cache_page(60 * 60 * 2)(NewCourseHome.as_view()), name='new-course-home'),
  #  path('support/',(Support.as_view()), name='support'),

]

urlpatterns += router.urls
