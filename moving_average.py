import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

#crude oil
oil = yf.Ticker("CL=F")
stock =  oil.history(start='2010-01-01',  end='2020-07-21')
stock.head()

stock = stock.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      stock[i]  =  stock[i].astype('float64')
print(stock)

fig = go.Figure(data=[go.Candlestick(x=stock['Date'], 
									open=stock['Open'], 
									high=stock['High'],
									low=stock['Low'],
									close=stock['Close'])])
		
#fig.show()

ewm20=np.asarray(stock['Open'].ewm(span=20, adjust=False).mean())
ewm100=np.asarray(stock['Open'].ewm(span=100, adjust=False).mean())

sell,buy=list(),list()
signalbuy=list()
signalsell=list()
flag=-1


for i in range(len(stock['Open'])):
  if ewm20[i] < ewm100[i]:
    if flag != 1:
      buy.append(stock['Open'][i])
      sell.append(np.nan)
      signalbuy.append(stock['Date'][i])
      signalsell.append(np.nan)
      flag=1
    else:
      buy.append(np.nan)
      sell.append(np.nan)
      signalbuy.append(np.nan)
      signalsell.append(np.nan)
    
  elif ewm20[i] > ewm100[i]:
    if flag!=0:
      sell.append(stock['Open'][i])
      buy.append(np.nan)
      signalbuy.append(np.nan)
      signalsell.append(stock['Date'][i])
      flag=0
    else:
      buy.append(np.nan)
      sell.append(np.nan)
      signalbuy.append(np.nan)
      signalsell.append(np.nan)

print(sell)

ewm=[]
ewm.append(go.Scatter(x=stock['Date'], y=ewm20))
ewm.append(go.Scatter(x=stock['Date'], y=ewm100))
ewm.append(go.Scatter(mode="markers", x=signalsell, y=sell, marker_symbol='triangle-down',
                          marker_color="red", marker_size=15, name='sell'))
ewm.append(go.Scatter(mode="markers", x=signalbuy, y=buy, marker_symbol='triangle-up',
                          marker_color="green", marker_size=15, name='buy'))
ewm=go.Figure(ewm)
ewm.show()

