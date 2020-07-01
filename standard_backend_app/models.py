from datetime import datetime, date
from datetime import datetime, date
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.utils import timezone
from imagekit.admin import AdminThumbnail
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Categoria(models.Model):
    class Meta:
        ordering = ['description']

    description = models.CharField(max_length=250, verbose_name='Descrição')
    # icon = models.CharField(max_length=250, verbose_name='Url do Ícone')
    # image = models.CharField(max_length=250, verbose_name='Url da Imagem')
    id = models.CharField(primary_key=True, max_length=100, editable=False)
    name = models.CharField(max_length=100, verbose_name='Endereço para a API')
    title = models.CharField(max_length=100, verbose_name='Título')
    shouldShow = models.BooleanField(default=True, verbose_name='Mostrar categoria ao cliente?')
    image = models.ImageField(upload_to='images/standard_pizzeria/categories', verbose_name='Url do Ícone',
                              max_length=250, )
    # image = models.CharField(max_length=250, verbose_name='Url da Imagem')
    image_60x60 = ImageSpecField(
        source='image',
        processors=[ResizeToFill(60, 60)],
        format='PNG',
        options={'quality': 85}
    )

    def __str__(self):
        return self.title

    def show_desc(self):
        return self.description

    def image_img(self):
        from django.utils.html import mark_safe
        # return u'<img src="%s" />' % escape(self.icon)
        return mark_safe(
            '<div style="padding: 5px;width: 60px; height: 60px;background-color: #280000"><img src=' + self.image.url + ' style="height: 100%; width: 100%; object-fit: scale-down;"/></div>')

    image_img.short_description = 'Ícone'
    image_img.allow_tags = True

    # def image_img(self):
    #     from django.utils.html import mark_safe
    #     if 'http' in self.image:
    #         return mark_safe(
    #             '<img src="%s" width="30" height="30" style="background-color:#280000;padding:5px;" />' % (self.icon))
    #     else:
    #         image = models.ImageField(upload_to='images/', verbose_name='Url da Imagem', max_length=250, )
    #         return image
    #
    # image.short_description = 'Url da Imagem'
    # image.allow_tags = True


class Tamanho(models.Model):
    description = models.CharField(max_length=100, verbose_name='Descrição do tamanho')
    flavors_quantity = models.IntegerField(verbose_name='Quantidade de Sabores', default=1)
    price = models.DecimalField(validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Preço', max_digits=10,
                                decimal_places=2, default=0.00)

    def __str__(self):
        return self.description + ' - ' + 'R$ ' + str(self.price) + ' - ' + str(self.flavors_quantity) + ' sabor(es)'


class Produto(models.Model):
    # today = datetime.now()
    # today = today.strftime("%d-%m-%Y-%H:%M:%S")
    class Meta:
        ordering = ['description']

    today = timezone.localtime(timezone.now()).isoformat()

    dateRegister = models.DateTimeField(default=today, blank=True, null=True, verbose_name='Data do Último Registro')
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, default='gYOBtzVcIFN01Z7R9Utx',
                                 verbose_name='Categoria')
    description = models.CharField(max_length=250, verbose_name='Descrição')
    ingredients = models.CharField(max_length=250, verbose_name='Ingredientes', blank=True, null=True)
    notes = models.CharField(max_length=250, verbose_name='Observações', blank=True, null=True)
    price = models.DecimalField(validators=[MinValueValidator(Decimal('0.01'))],
                                help_text='Deixar em branco se for Pizza', verbose_name='Preço (Explícito)',
                                max_digits=10, decimal_places=2, blank=True,
                                null=True)
    size = models.CharField(help_text='Deixar em branco se for Pizza', max_length=50,
                            verbose_name='Tamanho (Explícito)', blank=True, null=True)
    shouldShow = models.BooleanField(default=True, verbose_name='Mostrar produto ao cliente?')

    id = models.CharField(primary_key=True, max_length=100, editable=False)
    # image = models.CharField(max_length=250, verbose_name='Url da Imagem')
    image = models.ImageField(upload_to='images/standard_pizzeria/products', verbose_name='Url da Imagem', )

    size_prices = models.ManyToManyField(Tamanho, related_name='size', verbose_name='Tamanho-Preço',
                                         help_text='Preço por tamanho', through='Valore')

    image_160x160 = ImageSpecField(
        source='image',
        processors=[ResizeToFill(160, 160)],
        format='PNG',
        options={'quality': 85}
    )

    def to_describe(self):
        retorno = self.description
        tempRetorno = ''
        relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()

        for relation in relationQuerySet:
            tamanho = Tamanho.objects.get(id=relation['tamanho_id'])
            tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(
                tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.', ',')

        retorno = retorno + tempRetorno
        return retorno

    def __str__(self):

        retorno = self.description

        if self.size != None:
            retorno = retorno + ' ' + self.size;

        # tempRetorno = ''
        # relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()
        #
        # for relation in relationQuerySet:
        #     tamanho = Tamanho.objects.get(id=relation['tamanho_id'])
        #     tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(
        #         tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.', ',')
        #
        # retorno = retorno + tempRetorno
        # return retorno
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

    # def newDateRegister(self):
    #     today = datetime.now()
    #     today = today.strftime("%d de %B de %Y às %H:%M:%S %Z")
    #
    #     return today
    #
    # newDateRegister.short_description = 'Data do Registro Atual'
    # newDateRegister.allow_tags = True

    def image_img(self):
        from django.utils.html import mark_safe
        # return u'<img src="%s" />' % escape(self.icon)
        # return mark_safe('<img src="%s" width="160" height="160" style="" />' % (self.image.url))
        return mark_safe(
            '<div style="padding: 5px;width: 60px; height: 60px;"><img src=' + self.image.url + ' style="height: 100%; width: 100%; object-fit: scale-down;"/></div>')

    image_img.short_description = 'Imagem'
    image_img.allow_tags = True


class Pedido(models.Model):
    PAYMENT_METHOD = (('credit_card', 'Cartão'), ('money', 'Dinheiro'))
    DELIVERY_OPTION = (('withdraw', 'Retirada'), ('delivery', 'Entrega'))
    # class PaymentMethod(models.TextChoices):
    #     CREDIT_CARD = "Cartão"
    #     MONEY = "Dinheiro"

    # class DeliveryOptions(models.TextChoices):
    #     WITHDRAW = "Retirada"
    #     DELIVERY = "Entrega"

    today = timezone.localtime(timezone.now()).isoformat()
    # today = timezone.now()
    # today = today.strftime("YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")

    # today = datetime.now()
    # today = today.strftime("%d-%m-%Y-%H:%M:%S")
    # today = today.strptime(str(today), "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")

    name = models.CharField(max_length=250, verbose_name='Nome do Cliente')
    phone = models.CharField(max_length=250, verbose_name='Telefone do Cliente')
    dateTime = models.DateTimeField(default=today, blank=True, null=True, verbose_name='Data do Registro')
    coupon_id = models.CharField(max_length=100, verbose_name='Cupom de Desconto')
    delivery = models.CharField(choices=DELIVERY_OPTION, default='withdraw', max_length=100,
                                verbose_name='Forma de Entrega')
    delivery_address = models.CharField(max_length=100, verbose_name='Endereço de Entrega')
    id = models.CharField(primary_key=True, max_length=100, editable=False)
    total = models.DecimalField(validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Total', max_digits=10,
                                decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='credit_card', max_length=100,
                                      verbose_name='Forma de Pagamento')
    payment_change = models.DecimalField(validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Troco para',
                                         max_digits=10, decimal_places=2, blank=True, null=True)
    picture = models.ImageField(upload_to='images/standard_pizzeria/users_pictures', verbose_name='Url da Foto', )
    product_list = models.ManyToManyField(Produto, related_name='product_list', verbose_name='Lista de Produtos',
                                          help_text='Itens do Pedido', through='Item',
                                          through_fields=('pedido', 'produto'), )
    # help_text='Itens do Pedido', through='Valore')

    image_100x100 = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 85}
    )

    def __str__(self):
        return self.name + ' - ' + self.phone + ' - ' + str(self.total)

    def show_desc(self):
        return self.name + ' - ' + self.phone + ' - ' + str(self.total)


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


class Item(models.Model):
    # def size_option(self):
    #     SIZE_OPTIONS = (('withdraw', 'Retirada'), ('delivery', 'Entrega'))
    #     # SIZE_OPTIONS = ()
    #
    #     relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()
    #     # SIZE_OPTIONS = [[(t.id, str(t)) for t in tamanhos] for tamanhos in relationQuerySet]
    #     # print(SIZE_OPTIONS)
    #     # SIZE_OPTIONS = []
    #
    #     for relation in relationQuerySet:
    #         tamanhos = Tamanho.objects.filter(id=relation['tamanho_id'])
    #         # SIZE_OPTIONS = [(t.id, str(t)) for t in tamanhos]
    #         SIZE_OPTIONS.append((t.id, str(t)) for t in tamanhos)
    #         # tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(
    #         #     tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.', ',')
    #
    #     return models.CharField(choices=SIZE_OPTIONS, default='withdraw', max_length=100,
    #                             verbose_name='Tamanho-Preço')
    #     # return models.CharField(widget=models.CharField(attrs={'size': 100, }), choices=SIZE_OPTIONS,
    #     #                         default='withdraw', max_length=100,
    #     #                         verbose_name='Tamanho-Preço')
    #     # print(SIZE_OPTIONS)
    #     # return SIZE_OPTIONS

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    # size_option.short_description = 'Tamanho'
    # size_option.allow_tags = True
    # size_option = property(__size_option2)

    # SIZE_OPTIONS = (('', ''), )

    # size_option = models.CharField(null=True, blank=True, choices=SIZE_OPTIONS, default='withdraw', max_length=100,
    #                             verbose_name='Tamanho-Preço')

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        # self.helper = FormHelper(self)
        # self.helper.form_show_errors = True
        # self.helper.error_text_inline = False
        # if self.produto_id is not None:
        #     print("entrou")
        #     valores = Valore.objects.filter(produto_id=self.produto_id).all().values()
        #     tamanhos = Tamanho.objects.filter(valores__in=valores)
        #
        #     self.fields['size_option'] = forms.ModelChoiceField(
        #         queryset=tamanhos, required=False)

    def __str__(self):
        # return "Tamanho %s" % self.tamanho_id
        return "Produto %s" % self.produto.description

    # def size_option2(self):
    #     # SIZE_OPTIONS = (('withdraw', 'Retirada'), ('delivery', 'Entrega'))
    #     SIZE_OPTIONS = ()
    #
    #     relationQuerySet = Valore.objects.filter(produto_id=self.id).all().values()
    #     SIZE_OPTIONS = [[(t.id, str(t)) for t in tamanhos] for tamanhos in relationQuerySet]

    # for relation in relationQuerySet:
    #     tamanhos = Tamanho.objects.filter(id=relation['tamanho_id'])
    #     SIZE_OPTIONS = [(t.id, str(t)) for t in tamanhos]
    #     # tempRetorno = tempRetorno + ' / ' + tamanho.description + ' - ' + str(
    #     #     tamanho.flavors_quantity) + ' sabor(es)' + ' - R$ ' + str(tamanho.price).replace('.', ',')

    #     self.size_option = models.CharField(choices=SIZE_OPTIONS, default='withdraw', max_length=100,
    #                             verbose_name='Tamanho-Preço')
    #
    # size_option2.short_description = 'Ícone'
    # size_option2.allow_tags = True
    # size_option = size_option2
