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

    def __str__(self):
        return self.email 

