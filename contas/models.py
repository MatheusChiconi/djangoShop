from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioCustomizado(AbstractUser):
    # --- Seus campos adicionais começam aqui ---
    telefone = models.CharField(
        max_length=20,
        null=True, 
        blank=True
    )
    cpf = models.CharField(
        max_length=14,
        unique=True
    )
    cep = models.CharField(
        max_length=10,
        null=True, 
        blank=True
    )
    endereco = models.CharField(
        max_length=255,
        null=True, 
        blank=True
    )
    cidade = models.CharField(
        max_length=100,
        null=True, 
        blank=True
    )
    estado = models.CharField(
        max_length=2,
        null=True, 
        blank=True
    )
    data_nascimento = models.DateField(
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.email
    

