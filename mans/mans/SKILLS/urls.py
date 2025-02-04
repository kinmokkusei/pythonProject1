from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('main', views.main, name='main'),
    path('', views.main2, name='main2'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_details, name='course_details'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('my-courses/', views.my_courses, name='mycourses'),

]



