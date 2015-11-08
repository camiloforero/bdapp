from django.conf import settings
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^login/$', 'django.contrib.auth.views.login', name='login'),
    url(
        '^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/app/'},
        name='logout' ),
    url('^password_change/$', 'django.contrib.auth.views.password_change',
        {'post_change_redirect':'/app/', 'template_name': 'scheduler/change_password.html',}, name='password_change'),
    url(r'^seleccion/$', views.seleccion, name='seleccion'),
    url(r'^ver_aceptados/$', views.ver_aceptados, name='ver_aceptados'),
    url(r'^ver_cartas/$', views.ver_cartas, name='ver_cartas'),
    url(r'^ver_legalizados/$', views.ver_legalizados, name='ver_legalizados'),
    url(r'^seleccionar/(?P<trainee>\d+)/(?P<aprobado>.*)/$', views.seleccionar, name='seleccionar'),
    url(r'^subir_cartas/(?P<trainee>\d+)$', views.subir_cartas, name='subir_cartas'),
    url(r'^confirmation$', views.confirmation, name='confirmation'),
    url(r'^test$', views.crearEscarapelas, name='testTemplate'),
    url(r'^test2$', views.crearBookletsAfuera, name='booklets'),
    url(r'^media\/(?P<path>.*)$', views.media_xsendfile, {
        'document_root': settings.MEDIA_ROOT,
         }),


]
