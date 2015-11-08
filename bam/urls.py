from django.conf.urls import url, include
import views

urlpatterns = [
     url(r'^ranking/(?P<area>[OI]G(?:CD|I)P)/(?P<semana>\d+)/$', views.ranking, name='ranking'),
     url(r'^coins/(?P<nombre_lc>.+)/(?P<semana>\d+)$', views.millas_lc, name='millas_lc'),
     ]
