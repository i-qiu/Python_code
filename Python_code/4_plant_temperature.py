import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 

file_path = ""
sheet_names = ['2021冠层温度', '2021冠层中部温度', '2022冠层温度', '2022冠层中部温度']

key_dates_2021 = pd.to_datetime([
    ('2021-06-20'),
    ('2021-07-05'),
    ('2021-07-20'),
    ('2021-08-04'),
    ('2021-08-19'),
    ('2021-09-03'),
    ('2021-09-18'),
    ('2021-10-03'),
    ('2021-10-18')
])

key_dates_2022 = pd.to_datetime([
    ('2022-06-20'),
    ('2022-07-05'),
    ('2022-07-20'),
    ('2022-08-04'),
    ('2022-08-19'),
    ('2022-09-03'),
    ('2022-09-18'),
    ('2022-10-03'),
    ('2022-10-18')
])
y_labels = ['Canopy temperature(°C)', 'Middle canopy temperature(°C)', 'Canopy temperature(°C)', 'Middle canopy temperature(°C)']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, sheet in enumerate(sheet_names):
    df = pd.read_excel(file_path, sheet_name=sheet)
    df['日期'] = pd.to_datetime(df['日期'])

    ax = axes[i]
    ax.plot(df['日期'], df['CK'], label='CK', color='blue')
    ax.plot(df['日期'], df['W'], label='W', color='red')

    ax.set_xlabel("Date",fontsize=20)
    ax.set_ylabel(y_labels[i],fontsize=17)
    ax.legend(loc='best',frameon=False,fontsize=22)
    if i < 2:
        key_dates = key_dates_2021
    else:
        key_dates = key_dates_2022
    ax.set_xticks(key_dates)
    ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in key_dates], rotation=45, ha='right',fontsize=20)
    ax.set_ylim(0,40)
    ax.tick_params(axis='y',labelsize=20)
plt.tight_layout()
fig = plt.gcf()
plt.show()
