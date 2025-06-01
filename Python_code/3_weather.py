import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 
import matplotlib.dates as mdates

df_2021 = pd.read_excel()
df_2022 = pd.read_excel()

df_2021['日期'] = pd.to_datetime(df_2021['日期'])
df_2022['日期'] = pd.to_datetime(df_2022['日期'])

key_dates_2021 = [
    ('2021-06-20'),
    ('2021-07-05'),
    ('2021-07-20'),
    ('2021-08-04'),
    ('2021-08-19'),
    ('2021-09-03'),
    ('2021-09-18'),
    ('2021-10-03'),
    ('2021-10-18')
]

key_dates_2022 = [
    ('2022-06-20'),
    ('2022-07-05'),
    ('2022-07-20'),
    ('2022-08-04'),
    ('2022-08-19'),
    ('2022-09-03'),
    ('2022-09-18'),
    ('2022-10-03'),
    ('2022-10-18')
]


def plot_weather(ax, df,key_dates):
    
    ax.plot(df['日期'], df['平均温度'], color='tab:orange', label='Average temperature')
    ax.plot(df['日期'], df['最高温度'], color='tab:red', linestyle='--', label='Maximum temperature')
    ax.set_ylabel('Temperature (°C)', color='tab:red',fontsize=20)
    ax.tick_params(axis='y', labelcolor='tab:red',labelsize=20)
    
    
    ax_rain = ax.twinx()
    ax_rain.bar(df['日期'], df['降水量'], width=0.8, color='tab:blue', alpha=0.3, label='Precipitation')
    ax_rain.set_ylabel('Precipitation (mm)', color='tab:blue',fontsize=20)
    ax_rain.tick_params(axis='y', labelcolor='tab:blue',labelsize=20)

    
    dates = [pd.to_datetime(d) for d in key_dates]
    ax.set_xticks(dates)
    ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in dates], rotation=45, ha='right',fontsize=20)
    
    
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_rain.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(1.05, 1.0),fontsize=20,frameon=False)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14))
plot_weather(ax1, df_2021,  key_dates_2021)
plot_weather(ax2, df_2022,  key_dates_2022)

plt.tight_layout(rect=[0, 0, 1.0, 1])
fig = plt.gcf()
plt.show()
