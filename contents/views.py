from .models import Content
from courses.models import Course
from .serializers import ContentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrReadOnlyForCoursesCreate, IsAdminForCourseDetailView, IsAdminForCourseForContents
from drf_spectacular.utils import extend_schema


class ContentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminForCourseDetailView]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        return serializer.save(course_id=self.kwargs["pk"])
    
    @extend_schema(operation_id="content_create", summary="Criação de conteúdos do curso", description="Rota de criação dos conteúdos do curso (apenas admin podem ter acesso).", tags=["Content"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    @extend_schema(operation_id="content_get", exclude=True)
    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class ContentDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminForCourseForContents]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @extend_schema(operation_id="content_list_id", summary="Lista um conteúdo do curso pelo id do curso e do contéudo.", description="Rota para listar um conteúdo do curso pelo id (apenas admin tem acesso a todos os conteúdos dos cursos, usuário comum só tem acesso ao conteúdo do curso que ele foi adicionado).", tags=["Content"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @extend_schema(operation_id="content_update", summary="Atualiza um conteúdo do curso pelo id do curso e do contéudo.", description="Rota para atualizção de conteúdo da aplicação(apenas admin tem acesso).", tags=["Content"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    @extend_schema(operation_id="content_delete", summary="Deleta um conteúdo do curso pelo id do curso e do contéudo.", description="Rota para deleção de conteúdo do curso (apenas admin tem acesso).", tags=["Content"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    @extend_schema(operation_id="content_put", exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
     
