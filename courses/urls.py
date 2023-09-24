from django.urls import path
from .views import CourseView, CourseDetailView
from contents import views
from students_courses import views as students_views

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<str:pk>/", CourseDetailView.as_view()),
    path("courses/<str:pk>/contents/", views.ContentView.as_view()),
    path("courses/<uuid:course_id>/students/", students_views.StudentCourseView.as_view()),
    path("courses/<uuid:id>/contents/<str:pk>/", views.ContentDetailView.as_view()),
    path("courses/<uuid:course_id>/students/<str:student_id>/", students_views.StudentCourseDetailView.as_view())
]
