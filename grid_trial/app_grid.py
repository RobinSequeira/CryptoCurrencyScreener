import flask
import requests
# from markupsafe import Markup

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

@app.route('/')
def index():
    symbol = topN()
    elements = []
    for i in range(len(symbol)):
        elements.append(f"""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_6c7af"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/{symbol[i]}/?exchange=BINANCE" rel="noopener" target="_blank"><span class="blue-text">{symbol[i]} Chart</span></a> by TradingView</div>
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
  "hide_side_toolbar": false,
  "allow_symbol_change": true,
  "studies": [
    "BB@tv-basicstudies",
    "IchimokuCloud@tv-basicstudies",
    "MACD@tv-basicstudies",
    "StochasticRSI@tv-basicstudies",
    "TripleEMA@tv-basicstudies",
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

if __name__ == "__main__":
    app.run(use_reloader=True)
    app.run(host= '127.0.0.1', port = 3500)