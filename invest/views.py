import requests
import json
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

URL = 'https://query.yahooapis.com/v1/public/yql'
QUERY_STR = 'q=select Name,Symbol,LastTradePriceOnly from yahoo.finance.quote \
where symbol in (%s)&format=json&env=store://datatables.org/alltableswithkeys\
&callback='

def quote(request, symbol):
    results = json.loads(_query_yql(symbol))
    quote = results['query']['results']['quote']['LastTradePriceOnly']
    return HttpResponse(quote if quote else -1)


def quotes(request, symbols):
    quotes = []
    data = dict()
    data['title'] = 'Stock Quotes | The Mamak Stall Investor'

    results = json.loads(_query_yql(symbols))

    for q in results['query']['results']['quote']:
        quote = q['LastTradePriceOnly']
        quotes.append(quote if quote else -1)
    data['quotes'] = quotes

    html = get_template('liststockprice.html').render(Context(data))
    return HttpResponse(html)


def _query_yql(symbols):
    # Another way to process symbols:
    #symbol_str = str(tuple(symbols.split(',')))
    #symbol_list = symbol_str.replace("'", '"')[1:len(symbol_str)-1]

    symbol_list = ",".join(tuple(map(lambda x:'"'+ x +'"', symbols.split(','))))
    r = requests.get(URL, QUERY_STR % symbol_list)
    return r.content.decode('utf-8')  # return string


def _scrape_yahoo(symbol):
    symbol = symbol.lower()

    if symbol.endswith(('.hk', 's.si')):
        html_id = 'yfs_l10_' + symbol
    else:
        html_id = 'yfs_l84_' + symbol

    r = requests.get('https://sg.finance.yahoo.com/q?s=%s&ql=1' % symbol)
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
