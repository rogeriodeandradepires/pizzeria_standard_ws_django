import uuid
from datetime import datetime

from django.core import serializers
from django.forms import models, model_to_dict
from django.utils import timezone

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from imagekit.admin import AdminThumbnail

from standard_backend_app.forms import DropdownModelForm, ItemForm
from standard_backend_app.models import Categoria, Produto, Tamanho, Valore, Pedido, Item
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib import admin


class StandardAdminCategoria(admin.ModelAdmin):
    # class Meta:
    #     model = Categoria
    #     fields = ['image']

    exclude = ('image_img',)
    # list_display = ('description', 'name', 'image_img')
    list_display = ('description', 'name', 'image_img',)
    list_filter = ('title',)
    # readonly_fields = ('image_img',)
    readonly_fields = ('admin_thumbnail', )
    change_form_template = 'admin/custom/change_form.html'

    admin_thumbnail = AdminThumbnail(image_field='image_60x60', template='category_image.html')
    admin_thumbnail.short_description = 'Ícone'

    # A handy constant for the name of the alternate database.
    using = 'standard'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.

        if obj.id == '':
            obj.id = uuid.uuid1()

        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class SizePricesInline(admin.TabularInline):
    # model = Produto.size_prices.through
    verbose_name = "Valor"
    verbose_name_plural = "Valores"
    model = Valore
    extra = 1
    insert_after = 'size'
    # fields = ['description']

    # A handy constant for the name of the alternate database.
    using = 'standard'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        if obj.id == '':
            obj.id = uuid.uuid1()

        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class StandardAdminTamanho(admin.ModelAdmin):
    # exclude = ('image',)
    list_display = ('description', 'price', 'flavors_quantity')
    list_filter = ('description', 'flavors_quantity')
    # readonly_fields = ('image_img', 'dateRegister')

    # A handy constant for the name of the alternate database.
    using = 'standard'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        if obj.id == '':
            obj.id = uuid.uuid1()

        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# class AdminImageWidget(AdminFileWidget):
#     def render(self, name, value, attrs=None, renderer=None):
#         output = []
#         if value and getattr(value, "url", None):
#             image_url = value.url
#             file_name = str(value)
#             output.append(u' <a href="%s" target="_blank"><img src="%s" width="150" alt="%s" /></a> %s ' % \
#                           (image_url, image_url, file_name, _('Change:')))
#         output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
#         return mark_safe(u''.join(output))


class StandardAdminProduto(admin.ModelAdmin):
    exclude = ('image_img',)
    list_display = ('show_desc', 'price', 'image_img', 'dateRegister',)
    list_filter = ('category',)
    readonly_fields = ('admin_thumbnail', 'dateRegister',)
    inlines = (SizePricesInline,)
    change_form_template = 'admin/custom/change_form.html'
    # change_form_template = "fieldset.html"

    admin_thumbnail = AdminThumbnail(image_field='image_160x160', template='product_image.html')
    admin_thumbnail.short_description = 'Imagem'
    # fields = ('category', 'description', 'ingredients', 'notes', 'price', 'size', 'admin_thumbnail', 'image')

    # A handy constant for the name of the alternate database.
    using = 'standard'

    # image_fields = ['image']

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name in self.image_fields:
    #         request = kwargs.pop("request", None)
    #         kwargs['widget'] = AdminImageWidget
    #         return db_field.formfield(**kwargs)
    #     return super(StandardAdminProduto, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        if obj.id == '':
            obj.id = uuid.uuid1()

        today = timezone.localtime(timezone.now()).isoformat()
        # today = today.strftime("YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")

        obj.dateRegister = today

        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class SizeOptionsForOrderInline(admin.TabularInline):
    # model = Produto.size_prices.through
    verbose_name = "Item"
    verbose_name_plural = "Itens"
    model = Item
    extra = 1
    insert_after = 'phone'

    form = ItemForm

    # json_serializer = serializers.get_serializer("json")()
    # teste = json_serializer.serialize(Valore.objects.all(), ensure_ascii=False)
    # fields = ['produto', 'size_option']
    readonly_fields = ['preco', ]
    # template = 'admin/custom/order_product_add_change_form.html'
    # template = 'admin/custom/order_product_change_form.html'

    # A handy constant for the name of the alternate database.
    using = 'standard'

    # def get_readonly_fields(self, request, obj=None):
    #     if obj is not None:  # You may have to check some other attrs as well
    #         # Editing an object
    #         return ('field_name',)
    #     else:
    #         # Creating a new object
    #         return ()

    def preco(self, obj):
        return '---'
    preco.short_description = 'Preço'
    preco.allow_tags = True


    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        if obj.id == '':
            obj.id = uuid.uuid1()

        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class StandardAdminPedido(admin.ModelAdmin):
    filter_horizontal = ('product_list',)
    # template = 'myapp/templates/myapp/admin/tabular.html'
    # class Meta:
    #     model = Categoria
    #     fields = ['image']

    inlines = (SizeOptionsForOrderInline,)

    # fieldsets = (
    #     ('Dados do Cliente', {
    #         'fields': ('name', 'phone'),
    #     }),
    #     ('Forma de Entrega', {
    #         'fields': ('delivery',),
    #         'classes': ('delivery',)
    #     }),
    #     (None, {
    #         'fields': ('delivery_address',),
    #         'classes': ('abcdefg',)
    #     }),
    #     ('Pagamento', {
    #         'fields': ('total', 'payment_method'),
    #     }),
    #     (None, {
    #         'fields': ('payment_change',),
    #         # 'classes': ('abcdefg',)
    #     }),
    #     ('Registro', {
    #         'fields': ('time_to_show',),
    #         # 'classes': ('abcdefg',)
    #     }),
    # )
    #
    # form = DropdownModelForm
    # form = DropdownModelForm(attrs={'size': 10, 'id': 'date_field', })

    # class Media:
    #     js = ('standard_backend_app/dropdown/js/base.js',)

    exclude = ('coupon_id', 'picture', 'dateTime')
    # list_display = ('description', 'name', 'image_img')
    list_display = ('dateTime', 'name', 'phone', 'get_products', 'total',)
    list_filter = ('name',)
    # readonly_fields = ('image_img',)
    readonly_fields = ('time_to_show', )

    admin_thumbnail = AdminThumbnail(image_field='image_100x100', template='category_image.html')
    admin_thumbnail.short_description = 'Foto'


    # A handy constant for the name of the alternate database.
    using = 'standard'

    # some_variable = 'teste'

    change_form_template = 'admin/custom/order_deliverytype_change_form.html'
    # change_form_template = 'admin/custom/change_form.html'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['some_var'] = self.get_osm_info()
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )
    #
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['some_var'] = 'This is what I want to show'
    #     return super(StandardAdminPedido, self).changeform_view(request, extra_context=extra_context)
    #
    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['some_var'] = 'This is what I want to show'
    #     return super(StandardAdminPedido, self).changelist_view(request, extra_context=extra_context)

    def get_products(self, obj):

        lista = ''

        for p in obj.product_list.all():
            preco = 'R$ ' + str(p.price)
            # print(preco)
            item = Item.objects.using('standard').get(pedido_id=obj.id, produto_id=p.id)

            if item.tamanho:
                lista = lista + p.description + ' / ' + str(item.tamanho) + '<br>'
            else:
                lista = lista + p.description + ' / ' + preco + '<br>'

        return format_html(lista)
        # return format_html("<br>".join([p.description for p in obj.product_list.all()]))
    get_products.allow_tags = True
    get_products.short_description = 'Itens'

    def time_to_show(self, obj):
        from django.utils.translation import activate
        activate('pt-br')

        month_name = _(datetime.now().strftime("%B"))
        date = datetime.now().strftime("%d de {month} de %Y às %H:%M:%S").format(month=month_name)

        return date

    time_to_show.short_description = 'Data do Registro'
    time_to_show.allow_tags = True

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.

        if obj.id == '':
            obj.id = uuid.uuid1()

        today = timezone.localtime(timezone.now()).isoformat()
        # today = today.strftime("YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")

        obj.dateTime = today

        # print(model_to_dict(obj))

        # if obj.delivery == 'withdraw':
        #     obj.delivery_address == 'Retirada'


        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

# pandras_admin_site = PandrasAdminSite(name='pandras_admin')
admin.site.register(Categoria, StandardAdminCategoria)
admin.site.register(Produto, StandardAdminProduto)
admin.site.register(Tamanho, StandardAdminTamanho)
admin.site.register(Pedido, StandardAdminPedido)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Pizzeria Admin"
admin.site.title = "Pizzeria Admin Portal"
admin.site.index_title = "Bem-vindo ao Portal de Administração do app Pizzeria Standard"
