from rest_framework.generics import ListCreateAPIView
from .models import Account
from .serializers import AccountSerializer
from drf_spectacular.utils import extend_schema


class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(operation_id="account_create", summary="Criação das contas dos usuários.", description="Rota de criação das contas dos usuários.", tags=["Account"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    @extend_schema(operation_id="account_put", exclude=True)
    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
