# pip install mplfinance pandas
import pandas as pd
import mplfinance as mpf

def plot_kline_mpf(
    dates, opens, highs, lows, closes,
    title="K線圖", ma=(5, 10, 20), volume=None, save_path=None, style="yahoo"
):
    """
    dates: 可為字串(yyyy-mm-dd等)或 pd.Timestamp
    opens/highs/lows/closes: 數值序列(長度需一致)
    ma: (5,10,20) 代表畫移動平均線；設為 None 可關閉
    volume: 可選，成交量序列
    save_path: 可選，像 'kline.png'，不傳則直接顯示
    style: 'yahoo', 'charles', 'binance', 'classic', 'blueskies'...等
    """
    df = pd.DataFrame({
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
    }, index=pd.to_datetime(dates))

    # 顏色設定：上漲紅、下跌綠（台股慣例）
    mc = mpf.make_marketcolors(
        up='red', down='green',
        edge='inherit', wick='inherit', volume='inherit'
    )
    s  = mpf.make_mpf_style(marketcolors=mc, base_mpf_style=style, mavcolors=['#d62728','#1f77b4','#2ca02c'])

    addplots = []
    kwargs = {
        'type': 'candle',
        'style': s,
        'title': title,
        'ylabel': 'Price',
        'tight_layout': True,
        'xrotation': 15,
    }

    if ma:
        kwargs['mav'] = ma

    if volume is not None:
        df['Volume'] = volume
        kwargs['volume'] = True
        kwargs['ylabel_lower'] = 'Volume'

    if save_path:
        mpf.plot(df, **kwargs, savefig=save_path)
    else:
        mpf.plot(df, **kwargs)

if __name__ == "__main__":
    """
    # 範例資料
    dates  = ["2025-09-01","2025-09-02","2025-09-03","2025-09-04","2025-09-05"]
    opens  = [100, 103, 102, 104, 106]
    highs  = [105, 106, 107, 108, 110]
    lows   = [ 98, 101, 100, 102, 105]
    closes = [103, 102, 105, 107, 109]
    vols   = [5000, 4800, 6200, 7000, 6800]
    """

    df = pd.read_csv('1101.csv')
    print(df.head())
    dates  = df['trade_date'].tolist()
    opens  = df['start_price'].tolist()
    highs  = df['high_price'].tolist()
    lows   = df['low_price'].tolist()
    closes = df['end_price'].tolist()
    vols   = df['volume'].tolist()

    print("start\n")

    plot_kline_mpf(dates, opens, highs, lows, closes, title="示例K線", ma=(5,10), volume=vols)
    
    print("end")