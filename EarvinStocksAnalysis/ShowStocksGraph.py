import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 使用你確定存在的字體檔案
font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
font_prop = fm.FontProperties(fname=font_path)

# 讓 matplotlib 使用這個字體
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 讓 mplfinance 也使用同一字體
mpf_style = mpf.make_mpf_style(
    base_mpf_style='yahoo',
    rc={'font.family': font_prop.get_name()}
)

def plot_kline_with_volume(csv_file):
    df = pd.read_csv(csv_file)

    df.columns = ["日期", "股票代號", "股票名稱", "開盤價", "最高價", "最低價", "收盤價", "成交量"]

    df["日期"] = pd.to_datetime(df["日期"])
    df.set_index("日期", inplace=True)

    df.rename(columns={
        "開盤價": "Open",
        "最高價": "High",
        "最低價": "Low",
        "收盤價": "Close",
        "成交量": "Volume"
    }, inplace=True)

    mpf.plot(
        df,
        type="candle",
        volume=True,
        style=mpf_style,
        title=f"{df['股票名稱'].iloc[0]} ({df['股票代號'].iloc[0]}) K 線圖",
        ylabel="價格",
        ylabel_lower="成交量",
        figratio=(16, 9),
        figscale=1.2
    )

plot_kline_with_volume("1101.csv")
