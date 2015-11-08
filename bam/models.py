from django.db import models


class Cluster(models.Model):
    nombre = models.CharField(max_length=16, primary_key=True)
    def __unicode__(self):
        return self.nombre

class Semana(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    def __unicode__(self):
        return "Semana %i" % self.id
    
class LC(models.Model):
    nombre = models.CharField(max_length=32, primary_key=True)
    logo = models.ImageField(null=True)
    cluster = models.ForeignKey(Cluster, related_name="lcs", null=True)
    semana = models.ManyToManyField(Semana, through="Puntajes", related_name="lcs")
    def __unicode__(self):
        return self.nombre

class Puntajes(models.Model):
    lc = models.ForeignKey(LC)
    semana = models.ForeignKey(Semana)
    OGCDP = models.PositiveSmallIntegerField(default=0)
    ip_OGCDP = models.PositiveSmallIntegerField(default=0)
    ma_OGCDP = models.PositiveSmallIntegerField(default=0)
    bonus_OGCDP = models.PositiveSmallIntegerField(default=0)
    IGCDP = models.PositiveSmallIntegerField(default=0)
    ip_IGCDP = models.PositiveSmallIntegerField(default=0)
    ma_IGCDP = models.PositiveSmallIntegerField(default=0)
    bonus_IGCDP = models.PositiveSmallIntegerField(default=0)
    OGIP = models.PositiveSmallIntegerField(default=0)
    ip_OGIP = models.PositiveSmallIntegerField(default=0)
    ma_OGIP = models.PositiveSmallIntegerField(default=0)
    bonus_OGIP = models.PositiveSmallIntegerField(default=0)
    IGIP = models.PositiveSmallIntegerField(default=0)
    ip_IGIP = models.PositiveSmallIntegerField(default=0)
    ma_IGIP = models.PositiveSmallIntegerField(default=0)
    bonus_IGIP = models.PositiveSmallIntegerField(default=0)
    class Meta:
        unique_together = ("lc", "semana")
    
# Create your models here.
