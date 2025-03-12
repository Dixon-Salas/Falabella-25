from rest_framework import generics, status, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .serializers import ForgotPasswordSerializer, ChangePasswordSerializer, ResetPasswordSerializer


User  = get_user_model()

class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all() #Vista de usuarios y registros
    serializer_class = UserSerializer

    def get_permissions(self):#Permite registro de usuario pero GET requiere permisos
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):#Vista para actualizar o eliminar usuario esp.
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ChangePasswordView(generics.UpdateAPIView):#Vista para cambiar contraseña
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user #Devuelve usuario que hizo solicitud
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #Verifica contraseña actual incorrecta
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Contraseña incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)
        
        #Estable nueva contraseña y la guarda
        user.set_password(serializer.data.get("new_password"))
        user.save()
        
        return Response({"detail": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)



class ForgotPasswordView(APIView):
    #Permite solicitar restablecimiento
    permission_classes = [permissions.AllowAny]

    def post (self,requet, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=requet.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "El usuario con este correo electrónico no existe."}, status=status.HTTP_400_BAD_REQUEST)
        #Se devuelve el mismo mensaje para email no encontrado
        
        #Genera token y codifica el id de usuario
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        #Construye enlace para restablecer contraseña
        reset_link = f"{requet.scheme}://{requet.get_host()}/api/users/reset_password/?uid={uid}&token={token}"
        #Envia correo con enlace
        print("Enlace de restablecimiento de contraseña:", reset_link)

        return Response({"detail": "Se ha enviado un enlace de restablecimiento de contraseña a su correo electrónico."}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    #Permite restablecer contraseña
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response ({"detaiil": "ID de usuario valido."}, status=status.HTTP_400_BAD_REQUEST)
        
        #Verificar el token
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token no válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        #Establecer nueva contraseña y guardar
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)