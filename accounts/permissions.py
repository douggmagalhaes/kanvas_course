from rest_framework import permissions
from rest_framework.views import Request
from .models import Account
from contents.models import Content


class IsAdminOrReadOnlyForCoursesCreate(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
  
        if request.method == "POST" and request.user.is_superuser:
            return True
        return False


class IsAdminOrReadOnlyForCoursesCreateTeste(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.method in permissions.SAFE_METHODS or request.user.is_superuser):
            return True


class IsAdminForCourseDetailView(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        
        if request.user.is_superuser:
            return True
        return False


class IsAdminForCourseForContents(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj: Content):
        return (
            request.method in permissions.SAFE_METHODS and request.user in obj.course.students.all() or request.user.is_superuser
        )
  
    
class IsAdminForStudentsCourse(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj: Content):
        if request.user.is_superuser:
            return True
        return False  
