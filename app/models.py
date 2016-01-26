from django.contrib.auth.models import User
from django.db import models

from django.contrib import admin

# Create your models here.
class Player(models.Model):
    class Meta(object):
        db_table = 'player'

    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,default="")
    cash = models.FloatField(default=500000)
    value_in_stocks = models.FloatField(default=0)
    def __str__(self):
        return self.user.username

class Stock(models.Model):
    class Meta(object):
        db_table = 'stock'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, db_index=True)
    price = models.FloatField()
    diff = models.FloatField(default=0)
    def __str__(self):
        return str(self.code)

class PlayerToStock(models.Model):
    class Meta(object):
        db_table = 'playertostock'

    player = models.ForeignKey(Player)
    stock = models.ForeignKey(Stock)
    quantity = models.IntegerField(default=0)
    #price_bought_at = models.FloatField()
    
admin.site.register(Player)
admin.site.register(Stock)
admin.site.register(PlayerToStock)