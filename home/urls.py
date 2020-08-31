from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('404-page-not-found/', page_not_found, name='page-not-found'),
    path('all-teacher/', cache_page(60 * 60 * 2)(AllTeacher.as_view()), name='all-teacher'),
    path('counter/', cache_page(60 * 60 * 2)(Counter.as_view()), name='counter'),
    path('most-discounted-courses/', cache_page(60 * 60 * 2)(MostDiscountedCourses.as_view()),
         name='most-discounted-courses'),
    path('best-selling-courses/', cache_page(60 * 60 * 2)(BestSellingCourses.as_view()), name='best-selling-courses'),
    path('search-home/', SearchHome.as_view(), name='search-home'),
    path('support/', cache_page(60 * 60 * 2)(Support.as_view()), name='support')

]