import flask
from flask import request
import requests
# from markupsafe import Markup
print(request.__module__)
app = flask.Flask(__name__)



def topN():
    r = requests.get("https://api.binance.com/api/v3/ticker/24hr")

    symbol_24hrPercent_volume = [[i.get('symbol'), i.get('priceChangePercent'), i.get('volume')] for i in r.json()]

    symbol_24hrPercent_volume = sorted(symbol_24hrPercent_volume, key=lambda x: abs(float(x[1])), reverse=True)

    volume_threshold = 1_000_000
    symbol_24hrPercent_volume = [i for i in symbol_24hrPercent_volume if float(i[2])>volume_threshold]

    topN = 20
    symbol_24hrPercent_volume = symbol_24hrPercent_volume[:topN]

    top_symbols =[i[0] for i in symbol_24hrPercent_volume]
    return top_symbols

def MACD():
  pass

@app.route('/')
def index():
    symbol = topN()
    elements = []
    for i in range(len(symbol)):
        elements.append(f"""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_6c7af"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
  "width": 490,
  "height": 305,
  "symbol": "BINANCE:{symbol[i]}",
  "interval": "15",
  "timezone": "Asia/Kolkata",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "hide_side_toolbar": true,
  "allow_symbol_change": true,
  "studies": [
    "Volume@tv-basicstudies"
  ],
  "container_id": "{i}"
}}
  );
  </script>
</div>
<!-- TradingView Widget END -->""")
    print(len(elements))
    return flask.render_template('creating_grid.html', elements=elements)


@app.route('/top',methods = ['GET' , 'POST'])
def tooop():
  if request.method == 'GET':
    # import ipdb
    # ipdb.set_trace()
    # print(request.form['Interval'])
    # import ipdb
    # ipdb.set_trace()
    interval = request.args.get('Interval')
    interval = interval if interval else '15' 
  # else:
  #   interval = '15'

  symbol = topN()
  elements = []
  for i in range(len(symbol)):
    elements.append(f"""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_6c7af"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
  "width": 490,
  "height": 305,
  "symbol": "BINANCE:{symbol[i]}",
  "interval": "{interval}",
  "timezone": "Asia/Kolkata",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "hide_side_toolbar": true,
  "allow_symbol_change": true,
  "studies": [
    "Volume@tv-basicstudies"
  ],
  "container_id": "{i}"
}}
  );
  </script>
</div>
<!-- TradingView Widget END -->""")
  print(len(elements))
  return flask.render_template('top.html',elements=elements)

@app.route('/pinned')
def pinned():
  return flask.render_template('pinned.html')

@app.route('/buy_sell')
def buy_sell():
  return flask.render_template('buy_sell.html')

@app.route('/positions')
def positions():
  return flask.render_template('positions.html')

if __name__ == "__main__":
    app.run(use_reloader=True)
    # app.run(host= '127.0.0.1', port = 3500)
