from django.contrib.auth.models import User
from django.db import models

from django.contrib import admin

# Create your models here.
class Player(models.Model):
    class Meta(object):
        db_table = 'player'

    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)

class Stock(models.Model):
    class Meta(object):
        db_table = 'stock'

    name = models.CharField(max_length=255)

class PlayerToStock(models.Model):
    class Meta(object):
        db_table = 'playertostock'

    player = models.ForeignKey(Player)
    stock = models.ForeignKey(Stock)
    quantity = models.IntegerField(default=0)
    
admin.site.register(Player)