from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para manejar usuarios sin 'username'.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que usa 'email' en lugar de 'username'.
    """
    username = None  # Eliminamos el campo 'username'
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    documento = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'documento']

    objects = CustomUserManager()  # Usamos nuestro manager personalizado

    def __str__(self):
        return self.email
