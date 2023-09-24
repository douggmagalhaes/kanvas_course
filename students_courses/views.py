from .models import StudentCourse
from courses.models import Course
from accounts.models import Account
from .serializers import StudentCourseSerializer, CourseStudentsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from accounts.permissions import IsAdminForStudentsCourse
from drf_spectacular.utils import extend_schema


class StudentCourseView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminForStudentsCourse]

    queryset = Course.objects.all()
    serializer_class = CourseStudentsSerializer

    lookup_url_kwarg = "course_id"

    @extend_schema(operation_id="students_list", summary="Listagem de estudantes do curso.", description="Rota para listar todos os estudantes do curso pelo id do curso (apenas admin tem acesso a essa rota).", tags=["Students"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @extend_schema(operation_id="students_put", exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(operation_id="students_patch", exclude=True)
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)    


class StudentCourseDetailView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminForStudentsCourse]

    queryset = Course.objects.all()
    serializer_class = StudentCourseSerializer

    lookup_url_kwarg = "course_id"

    def perform_destroy(self, instance):
        
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(Account, id=student_id)
        students_course = instance.students.all()
        if student not in students_course:
            raise NotFound({"detail": "this id is not associated with this course."})
        
        instance.students.remove(student)

    @extend_schema(operation_id="students_update", summary="Adiciona um estudante ao curso pelo id do curso.", description="Rota para adição de estudante ao curso (apenas admin tem acesso a essa rota).", tags=["Students"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs) 

    @extend_schema(operation_id="students_delete", summary="Remove um estudante do curso pelo id do curso e do estudante.", description="Rota para remover um estudante do curso (apenas admin tem acesso a essa rota).", tags=["Students"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 

    @extend_schema(operation_id="students_put", exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)  

