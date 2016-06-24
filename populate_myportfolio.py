import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invest.settings')

import django
django.setup()

from myportfolio.models import Investor, Portfolio, AssetClass, STOCKS, BONDS,\
    ALTERNATIVES, Security, Transaction, Account

def populate():
    investor1 = add_investor(name='David Lim', 
                 username='Dave', 
                 email='dave@gmail.com')

    p1 = add_portfolio(owner=investor1, 
                  name='Retirement', 
                  obj='Save for retirement', 
                  risk_tolerance='I am comfortable with 80/20 stock bond ratio', 
                  time_frame=30, 
                  stock_bond_ratio=4, 
                  asset_allocation={})

    a1 = add_assetclass(owner=investor1, 
                        name='US', 
                        asset_type=STOCKS)
    
    a2 = add_assetclass(owner=investor1, 
                        name='EU', 
                        asset_type=STOCKS)

    a3 = add_assetclass(owner=investor1, 
                        name='Global Bonds', 
                        asset_type=BONDS)
    
    p1.target_asset_allocation[a1.id] = 0.3
    p1.target_asset_allocation[a2.id] = 0.3
    p1.target_asset_allocation[a3.id] = 0.4
    p1.save()
    
    s1 = add_security(asset_class=a1, 
                      name='Vanguard total Stock ETF', 
                      symbol='VTI', 
                      isin='QW1234456', 
                      currency='USD', 
                      exchange='NYSE', 
                      expense_ratio_percent=0.1, 
                      last_trade_price=100.05)

    investor2 = add_investor(name='Diana', 
                 username='Rose', 
                 email='rose@gmail.com')

    p2 = add_portfolio(owner=investor2, 
                  name='New house', 
                  obj='Save for new house', 
                  risk_tolerance='I am comfortable with 50/50 stock bond ratio', 
                  time_frame=15, 
                  stock_bond_ratio=1, 
                  asset_allocation={})

    add_assetclass(owner=investor2, 
                   name='World', 
                   asset_type=STOCKS)
    
    add_assetclass(owner=investor2, 
                   name='REIT', 
                   asset_type=ALTERNATIVES)

    add_assetclass(owner=investor2, 
                   name='Global Bonds', 
                   asset_type=BONDS)
    
    for i in Investor.objects.all():
        print ('{} - {} - {}'.format(i.name, i.username, i.email))
        for p in Portfolio.objects.filter(owner=i):
            print ('  {} - {} - {} - {}'.format(p.name, p.objective, p.time_frame, p.target_asset_allocation))
            for a in AssetClass.objects.filter(owner=i):
                print ('  {}. {} - {}'.format(a.id, a.name, a.type))
                for s in Security.objects.filter(asset_class=a):
                    print ('    {} {}'.format(s.name, s.symbol))
    
    ac1 = Account.objects.get_or_create(owner=investor1,
                                        name='AC1',
                                        description='AC1'
                                        )[0]
    ac1.save()
    t = Transaction.objects.get_or_create(portfolio=p1,
                                          security=s1,
                                          account=ac1,
                                          date=datetime.datetime.now(),
                                          price=1,
                                          quantity=1)[0]
    t.save()
    print (p1.transaction_set.all())
    
    
def add_investor(name, username, email):
    i=Investor.objects.get_or_create(name=name, 
                                     username=username,
                                     email=email)[0]
    return i
    
def add_portfolio(owner, name, obj, risk_tolerance, time_frame, stock_bond_ratio, asset_allocation):
    p = Portfolio.objects.get_or_create(owner=owner,
                                        time_frame=time_frame, 
                                        target_stock_bond_ratio=stock_bond_ratio,
                                        )[0]
    p.owner = owner
    p.name = name
    p.objective = obj
    p.risk_tolerance = risk_tolerance
    p.target_asset_allocation = asset_allocation
    p.save()
    return p

def add_assetclass(owner, name, asset_type):
    a = AssetClass.objects.get_or_create(owner=owner, 
                                         name=name, 
                                         type=asset_type,
                                         )[0]
    return a

def add_security(asset_class, 
                name,
                symbol,
                isin,
                currency,
                exchange,
                expense_ratio_percent,
                last_trade_price):
    
    s = Security.objects.get_or_create(asset_class=asset_class,
                                    name=name,
                                    symbol=symbol,
                                    isin=isin,
                                    currency=currency,
                                    exchange=exchange,
                                    expense_ratio_percent=expense_ratio_percent,
                                    #last_trade_price=last_trade_price,
                                    )[0]
    
    return s

if __name__ == '__main__':
    populate()
    