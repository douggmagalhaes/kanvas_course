from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from accounts.permissions import IsAdminOrReadOnlyForCoursesCreate, IsAdminForCourseDetailView, IsAdminOrReadOnlyForCoursesCreateTeste
from drf_spectacular.utils import extend_schema


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnlyForCoursesCreate]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @extend_schema(operation_id="courses_list", summary="Listagem de cursos.", description="Rota para listar todos os cursos (somente usuários autenticados tem acesso).", tags=["Courses"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @extend_schema(operation_id="courses_create", summary="Criação de cursos.", description="Rota de criação de cursos da aplicação (apenas admin podem criar cursos).", tags=["Courses"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminForCourseDetailView] 

    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        return Course.objects.filter(students=self.request.user)
    
    @extend_schema(operation_id="courses_list_id", summary="Lista um curso pelo id do curso.", description="Rota para listar um curso pelo id (apenas admin tem acesso a todos os cursos, usuários comuns só tem acesso ao curso que foi adicionado).", tags=["Courses"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @extend_schema(operation_id="courses_update", summary="Atualiza um curso pelo id do curso", description="Rota para atualizção de cursos (apenas admin tem acesso).", tags=["Courses"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    @extend_schema(operation_id="courses_delete", summary="Deleta um curso pelo id do curso", description="Rota para deleção de cursos (apenas admin tem acesso).", tags=["Courses"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    @extend_schema(operation_id="courses_patch", exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs) 
