from django.db import models

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
    nickname = models.CharField(max_length=30)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    owner = models.ForeignKey(Investor) 
    name = models.CharField(max_length=128)
    objective = models.CharField(max_length=128)
    risk_tolerance = models.TextField()
    time_frame = models.PositiveSmallIntegerField()
    stock_bond_ratio = models.DecimalField(max_digits=4, decimal_places=2)  # Stock percentage divided by bond percentage
    
    def __str__(self):
        return "{}'s {}".format(self.owner.name, self.name)
    
class AssetClass(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    name = models.CharField(max_length=128)
    type = models.CharField(
            max_length=3,
            choices=TYPE_OF_ASSET_CLASSES,
            default=STOCKS,
            )
    percentage = models.DecimalField(max_digits=3, decimal_places=2)  # Range: 0.00 to 1.00
    
    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Security(models.Model):
    asset_class = models.ForeignKey(AssetClass)
    asset_location = models.ForeignKey(Account)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=16)
    isin = models.CharField(max_length=16)
    currency =  models.CharField(max_length=3)
    exchange = models.CharField(max_length=64)
    expense_ratio_percent = models.DecimalField(max_digits=4, decimal_places=2)  # 0.40 means 0.40%
    last_trade_price = models.DecimalField(max_digits=18, decimal_places=6)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    security = models.ForeignKey(Security)
    account = models.ForeignKey(Account)
    date = models.DateField()
    price = models.DecimalField(max_digits=17, decimal_places=4)  # One trillion
    quantity = models.DecimalField(max_digits=10, decimal_places=4) # One hundred thousand 
    
    def __str__(self):
        return self.name
