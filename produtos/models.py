from django.db import models
import uuid
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.
class Produto(models.Model):
    
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nome = models.CharField(max_length=60, verbose_name='Nome do Produto')
    marca = models.CharField(max_length=21, verbose_name='Marca do Produto')
    descricao = models.TextField(verbose_name='Descrição do Produto')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço do Produto')
    comparacao_preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Preço de Comparação (Valor anterior antes do desconto)')
    estoque = models.IntegerField(verbose_name='Quantidade em Estoque')
    imagem_principal = models.ImageField(upload_to='images_produts', default='images_produts/default.jpg', blank=True, verbose_name='Imagem Principal do Produto')
    Imagem_2 = models.ImageField(upload_to='images_produts', default='images_produts/default.jpg', blank=True, verbose_name='Imagem 2 do Produto')
    Imagem_3 = models.ImageField(upload_to='images_produts', default='images_produts/default.jpg', blank=True, verbose_name='Imagem 3 do Produto')
    Imagem_4 = models.ImageField(upload_to='images_produts', default='images_produts/default.jpg', blank=True, verbose_name='Imagem 4 do Produto')

    def __str__(self):
        return self.nome
    
    def tem_desconto(self):
        if self.comparacao_preco == None:
            return False
        else:
            return True
    
    def desconto(self):
        if self.tem_desconto():
            if self.comparacao_preco > 0:
                return (self.comparacao_preco - self.preco) / self.comparacao_preco * 100
            else:
                return 0
        else:
            return 0

@receiver(post_delete, sender=Produto)
def apagar_arquivos_produto_deletado(sender, instance, **kwargs):
    
    nomes_campos_imagem = [
        'imagem_principal',
        'Imagem_2',
        'Imagem_3',
        'Imagem_4',
    ]
    
    default_image_path = 'images_produts/default.jpg' # Caminho da imagem padrão

    for nome_campo in nomes_campos_imagem:
        campo_imagem = getattr(instance, nome_campo, None)
        
        if campo_imagem and campo_imagem.name and campo_imagem.name != default_image_path:
            if hasattr(campo_imagem, 'path') and os.path.isfile(campo_imagem.path):
                os.remove(campo_imagem.path)
