# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User, Group
from models import Empresa, Perfil, Trainee, Empresario
from fileManager import admin_views
from fileManager.admin_views import SubirPapeles, MostrarSubirPapeles


class MyAdminSite(AdminSite):
    site_header = 'Administración de la aplicación de BD'
    index_template = "admin/my_index.html"

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        my_urls = [
            url(r'^crear_documentos/$', self.admin_view(admin_views.crear_documentos), name="crear_documentos"),
            url(r'^subir_trainees/$', self.admin_view(admin_views.subir_trainees), name="subir_trainees"),
            url(r'^subir_papeles/$', self.admin_view(MostrarSubirPapeles.as_view()), name="mostrar_subir_papeles"),
            url(r'^subir_papeles/(?P<pk>\d+)/$', self.admin_view(SubirPapeles.as_view()), name="subir_papeles"),
        ]
        return my_urls + urls

admin_site = MyAdminSite()

class EmpresarioInline(admin.StackedInline):
    model = Empresario
    can_delete = False

@admin.register(User, site=admin_site)
class UserAdmin(AuthUserAdmin):
    inlines = [EmpresarioInline]

@admin.register(Trainee, site=admin_site)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'estado')

admin_site.register(Empresa)

# Register your models here.
