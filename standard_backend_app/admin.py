import uuid

from django.contrib import admin
from django.contrib.auth.models import User, Group
from imagekit.admin import AdminThumbnail

from standard_backend_app.models import Categoria, Produto, Tamanho, Valore
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib import admin


class StandardAdminCategoria(admin.ModelAdmin):
    # class Meta:
    #     model = Categoria
    #     fields = ['image']

    exclude = ('image',)
    list_display = ('description', 'name', 'image_img',)
    list_filter = ('title',)
    readonly_fields = ('image_img',)

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


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" width="150" alt="%s" /></a> %s ' % \
                          (image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class StandardAdminProduto(admin.ModelAdmin):
    exclude = ('image_img',)
    list_display = ('show_desc', 'price', 'admin_thumbnail',)
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


admin.site.register(Categoria, StandardAdminCategoria)
admin.site.register(Produto, StandardAdminProduto)
admin.site.register(Tamanho, StandardAdminTamanho)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Pizzeria Admin"
admin.site.title = "Pizzeria Admin Portal"
admin.site.index_title = "Bem-vindo ao Portal de Administração do app Pizzeria Standard"
