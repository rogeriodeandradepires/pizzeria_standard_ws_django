from datetime import datetime, date

from django import forms
from django.db import models


# Create your models here.
from imagekit.admin import AdminThumbnail
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Categoria(models.Model):
    class Meta:
        ordering = ['description']

    description = models.CharField(max_length=250, verbose_name='Descrição')
    icon = models.CharField(max_length=250, verbose_name='Url do Ícone')
    image = models.CharField(max_length=250, verbose_name='Url da Imagem')
    id = models.CharField(primary_key=True, max_length=100, editable=False)
    name = models.CharField(max_length=100, verbose_name='Endereço para a API')
    title = models.CharField(max_length=100, verbose_name='Título')

    def __str__(self):
        return self.title

    def show_desc(self):
        return self.description

    def image_img(self):
        from django.utils.html import mark_safe
        # return u'<img src="%s" />' % escape(self.icon)
        return mark_safe('<img src="%s" width="30" height="30" style="background-color:#280000;padding:5px;" />' % (self.icon))

    image_img.short_description = 'Ícone'
    image_img.allow_tags = True


class Tamanho(models.Model):
    description = models.CharField(max_length=100, verbose_name='Descrição do tamanho')
    flavors_quantity = models.IntegerField(verbose_name='Quantidade de Sabores', default=1)
    price = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.description + ' - ' + 'R$ ' + str(self.price) + ' - ' + str(self.flavors_quantity) + ' sabor(es)'


class Produto(models.Model):
    today = datetime.now()
    today = today.strftime("%Y-%m-%d %H:%M:%S")

    dateRegister = models.DateTimeField(default=today, blank=True, null=True, verbose_name='Data de Registro')
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, default='gYOBtzVcIFN01Z7R9Utx',
                                 verbose_name='Categoria')
    description = models.CharField(max_length=250, verbose_name='Descrição')
    ingredients = models.CharField(max_length=250, verbose_name='Ingredientes', blank=True, null=True)
    notes = models.CharField(max_length=250, verbose_name='Observações', blank=True, null=True)
    price = models.DecimalField(help_text='Deixar em branco se for Pizza', verbose_name='Preço (Explícito)', max_digits=10, decimal_places=2, blank=True,
                                null=True)
    size = models.CharField(help_text='Deixar em branco se for Pizza', max_length=50, verbose_name='Tamanho (Explícito)', blank=True, null=True)

    id = models.CharField(primary_key=True, max_length=100, editable=False)
    # image = models.CharField(max_length=250, verbose_name='Url da Imagem')
    image = models.ImageField(upload_to='images/', verbose_name='Url da Imagem',)

    size_prices = models.ManyToManyField(Tamanho, related_name='size', verbose_name='Tamanho-Preço', help_text='Preço por tamanho', through='Valore')

    image_160x160 = ImageSpecField(
        source='image',
        processors=[ResizeToFill(160, 160)],
        format='PNG',
        options={'quality': 85}
    )

    def __str__(self):

        retorno = self.description
        tempRetorno = ''
        relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()

        for relation in relationQuerySet:
            tamanho = Tamanho.objects.get(id=relation['tamanho_id'])
            tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.',',')

        retorno = retorno + tempRetorno
        return retorno

    def show_desc(self):
        retorno = self.description
        tempRetorno = ''
        relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()

        for relation in relationQuerySet:
            tamanho = Tamanho.objects.get(id=relation['tamanho_id'])
            tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(
                tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.', ',')

        retorno = retorno + tempRetorno
        return retorno

    show_desc.short_description = 'Produto'

    # def dateRegister(self):
    #     today = datetime.now()
    #     today = today.strftime("%Y-%m-%d %H:%M:%S")
    #
    #     return today
    #
    # dateRegister.short_description = 'Data de Registro'
    # dateRegister.allow_tags = True

    def image_img(self):
        from django.utils.html import mark_safe
        # return u'<img src="%s" />' % escape(self.icon)
        return mark_safe('<img src="%s" width="150" style="" />' % (self.image.url))

    image_img.short_description = 'Imagem'
    image_img.allow_tags = True


# class ProductImageForm(forms.ModelForm):
#     class Meta:
#         model = Produto
#         fields = ['description', 'image']


class Valore(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)

    def __str__(self):
        # return ' Tamanho ' + str(self.tamanho_id)
        return "Tamanho %s" % self.tamanho_id

