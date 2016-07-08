from django.db import models

class TransactionQuerySet(models.QuerySet):
    def transactions(self, portfolio_id):
        p = self.filter(id=portfolio_id)
        if (p):
            return p[0].transaction_set.all()
        else:
            return []
    
class PortfolioManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)
    
    def transactions(self, portfolio_id):
        return self.get_queryset().transactions(portfolio_id)

class SecurityManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)
    
    def transactions(self, portfolio_id):
        return self.get_queryset().transactions(portfolio_id)
