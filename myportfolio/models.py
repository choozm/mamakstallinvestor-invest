from django.db import models

class AssetClass(models.Model):
    def __str__(self):
        return None

class Portfolio(models.Model):
    name = models.CharField(max_length=128)
    objective = models.TextField()
    asset_classes = models.ManyToManyField(AssetClass)
    
    def __str__(self):
        return None
    
class Security(models.Model):
    asset_class = models.ForeignKey(AssetClass)
    last_trade_price = models.DecimalField(max_digits=18, decimal_places=6)
    
    def __str__(self):
        return None
    
class Account(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    
    def __str__(self):
        return None
    
class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    security = models.ForeignKey(Security)
    account = models.ForeignKey(Account)
    date = models.DateField()
    price = models.DecimalField(max_digits=18, decimal_places=6)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return None
