from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=128)
    objectivce = models.TextField()
    
    
    def __str__(self):
        return None

class Asset(models.Model):
    def __str__(self):
        return None

class Security(models.Model):
    def __str__(self):
        return None

class Transaction(models.Model):
    def __str__(self):
        return None

class Account(models.Model):
    def __str__(self):
        return None

class Price(models.Model):
    def __str__(self):
        return None
