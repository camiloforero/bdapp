# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User, Group
from models import Empresa, Perfil, Trainee, Empresario
from fileManager import admin_views


class MyAdminSite(AdminSite):
    site_header = 'Administración de la aplicación de BD'
    index_template = "admin/my_index.html"

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        my_urls = [
            url(r'^crear_memodeals/$', self.admin_view(admin_views.crear_memodeals), name="crear_memodeals"),
            url(r'^subir_trainees/$', self.admin_view(admin_views.subir_trainees), name="subir_trainees"),
        ]
        return my_urls + urls

admin_site = MyAdminSite()

class EmpresarioInline(admin.StackedInline):
    model = Empresario
    can_delete = False

@admin.register(User, site=admin_site)
class UserAdmin(AuthUserAdmin):
    inlines = [EmpresarioInline]

admin_site.register(Empresa)
admin_site.register(Trainee)

# Register your models here.
