import requests
import json
from django.http import HttpResponse
from django.template.loader import get_template

API_KEY= "<enter your API key>"
URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey={}&symbol={}"

def _query_source(symbol):
    r = requests.get(URL.format(API_KEY, symbol))
    return json.loads(r.content.decode('utf-8'))

def _retrieve_quote(result):
    try:
        last_refreshed = result["Meta Data"]["3. Last Refreshed"]
        quote = result["Time Series (Daily)"][last_refreshed]["4. close"]
    except:
        print("ERROR: Setting 'quote' to -1")
        quote = -1

    return quote

def quote(request, symbol):
    result = _query_source(symbol)
    quote = _retrieve_quote(result)
    return HttpResponse(quote)

def quotes(request, symbols):
    quotes = []
    data = dict()
    data['title'] = 'Stock Quotes | The Mamak Stall Investor'

    symbol_list = list(filter(None,(symbols.split(','))))
    for s in symbol_list:
        result = _query_source(s)
        quote = _retrieve_quote(result)
        quotes.append(quote)

    data['quotes'] = quotes
    html = get_template('liststockprice.html').render(data)
    return HttpResponse(html)

def home(request):
    html = '''
<html><head><title>The Mamak Stall Investor</title></head>
<body>
<h3>
<a href="https://mamakstallinvestor.wordpress.com/">The Mamak Stall Investor</a>
</h3>
</body></html>'''
    return HttpResponse(html)
