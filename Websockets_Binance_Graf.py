import websockets
import asyncio
import json
from datetime import datetime
import matplotlib.pyplot as plt


xdata = []
ydata = []


fig = plt.figure()
ax = fig.add_subplot(111)

# необязательные параметры
plt.xlabel('Time')
plt.ylabel('Price')
fig.show()


def update_graph():
    ax.plot(xdata, ydata, color='g')
    ax.legend([f"Last price: {ydata[-1]}$"])
    fig.canvas.draw()
    plt.pause(0.1)


async def main():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    # w - web
    # s - socket, ws = http
    # s - secure, wss = https
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']
            timestamp = data['E'] // 1000  # 0 = 1970-01-01
            date_time = datetime.strftime(
                datetime.fromtimestamp(timestamp), '%Y-%m-%d %H:%M:%S')
            coin_price = round(float(data['c']), 2)
            print(date_time, '->', coin_price)

            xdata.append(date_time)
            ydata.append(coin_price)
            update_graph()
        # print(await client.send('xxxxxxxxxxxxxxxxxxxx'.encode('utf-8')))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
