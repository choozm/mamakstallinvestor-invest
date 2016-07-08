from django.shortcuts import render
from myportfolio.models import Investor, Portfolio

def investor(request):
    investors = Investor.objects.all()
    context = {'investors': investors}
    
    return render(request, 'myportfolio/investor.html', context)

def portfolio(request, investor_id):
    context = {}
    investor = Investor.objects.filter(id=investor_id)[0]
    portfolios = Portfolio.objects.filter(owner=investor)
    
    context['investor']= investor
    context['portfolios'] = portfolios
    return render(request, 'myportfolio/portfolio.html', context)

def transaction(request, portfolio_id):
    context = {}
    portfolio = Portfolio.objects.get(id=portfolio_id)
    transactions = portfolio.transaction_set.all()
    
    context['portfolio'] = portfolio
    context['transactions']= transactions

    return render(request, 'myportfolio/transaction.html', context)
