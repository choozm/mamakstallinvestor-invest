import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context


def price(request, symbol):
    return HttpResponse(from_yahoo(symbol))


def prices(request, symbols):
    data = dict()
    data['title'] = "Stock Prices"

    pricelist = []
    for symbol in symbols.split(','):
        pricelist.append(from_yahoo(symbol))

    data['prices'] = pricelist

    html = get_template('liststockprice.html').render(Context(data))
    return HttpResponse(html)


def from_yahoo(symbol):
    symbol = symbol.lower()

    if symbol.endswith(('.hk', 's.si')):
        html_id = 'yfs_l10_' + symbol
    else:
        html_id = 'yfs_l84_' + symbol

    r=requests.get('https://sg.finance.yahoo.com/q?s=%s&ql=1' % symbol)
    soup = BeautifulSoup(r.content, 'html.parser')
    price = soup.find(id=html_id)
    return -1 if price is None else price.text


def home(request):
    html = '''
<html><head><title>The Mamak Stall Investor</title></head>
<body>
<h3>
<a href="https://mamakstallinvestor.wordpress.com/">The Mamak Stall Investor</a>
</h3>
</body></html>'''
    return HttpResponse(html)
