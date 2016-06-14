from django.db import models
import jsonfield

STOCKS = 'STK'
BONDS = 'BND'
CASH = 'CSH'
ALTERNATIVES = 'ALT'

TYPE_OF_ASSET_CLASSES = (
    (STOCKS, 'Stocks'),
    (BONDS, 'Bonds'),
    (CASH, 'Cash Equivalents'),
    (ALTERNATIVES, 'Alternatives'),
)

class Investor(models.Model):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    owner = models.ForeignKey(Investor) 
    name = models.CharField(max_length=128)
    objective = models.CharField(max_length=128)
    risk_tolerance = models.TextField()
    time_frame = models.PositiveSmallIntegerField()
    stock_bond_ratio = models.DecimalField(max_digits=4, decimal_places=2)  # Stock percentage divided by bond percentage
    asset_allocation = jsonfield.JSONField()  # Key = AssetClass id. Value = percentage in decimal format, ranges from 0.0 to 1.0. 
    
    def __str__(self):
        return "{}'s {}".format(self.owner.name, self.name)
    
class AssetClass(models.Model):
    owner = models.ForeignKey(Investor)
    name = models.CharField(max_length=128)
    type = models.CharField(
            max_length=3,
            choices=TYPE_OF_ASSET_CLASSES,
            default=STOCKS,
            )
    
    def __str__(self):
        return self.name

class Account(models.Model):
    owner = models.ForeignKey(Investor)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Security(models.Model):
    asset_class = models.ForeignKey(AssetClass)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=16)
    isin = models.CharField(max_length=16)
    currency =  models.CharField(max_length=3)  # TODO: use choices
    exchange = models.CharField(max_length=64)  # TODO: use choices
    expense_ratio_percent = models.DecimalField(max_digits=4, decimal_places=2)  # 0.40 means 0.40%
    last_trade_price = models.DecimalField(max_digits=11, decimal_places=4)  # One million
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    security = models.ForeignKey(Security)
    account = models.ForeignKey(Account)
    date = models.DateField()
    price = models.DecimalField(max_digits=11, decimal_places=4)  # One million
    quantity = models.DecimalField(max_digits=11, decimal_places=4)  # One million 
    
    def __str__(self):
        return "{} - {}".format(self.date, self.security.name)
