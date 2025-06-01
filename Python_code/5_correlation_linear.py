import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 
from statsmodels.tools.tools import add_constant

file_path = ''  
df = pd.read_excel(file_path)

df = df[["Yield", "NU", "NT", "GNDR","Treament","DMA","DMT","CPR","DMTE",'year']]
df['Warming'] = df['Treament'].apply(lambda x: 1 if 'W' in x else 0)  
df['Nitrogen'] = df['Treament'].apply(lambda x: 1 if 'N' in x else 0)  


def plot_with_stats(x, y, data, xlabel, ylabel, title, filename=None):
    
    X = sm.add_constant(data[x])  
    y_data = data[y]

    
    model = sm.OLS(y_data, X).fit()
    r_squared = model.rsquared
    p_value = model.pvalues[1]  
    coef = model.params[1]
    intercept = model.params[0]
    if intercept >= 0:
        equation = f"$Y = {coef:.2f}X + {abs(intercept):.2f}$"
    else:
        equation = f"$Y = {coef:.2f}X - {abs(intercept):.2f}$"
    
    if p_value < 0.001:
        p_str = "$\\it{P}$<0.001"
    elif p_value < 0.01:
        p_str = "$\\it{P}$<0.01"
    elif p_value < 0.05:
        p_str = "$\\it{P}$<0.05"
    else:
        p_str = f"$\\it{{P}}$ = {p_value:.3f}"
    
    sns.lmplot(x=x, y=y, data=data, aspect=1.0, ci=95,scatter_kws={'s': 70}, line_kws={'linewidth': 6})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    text_position_x = 0.05
    text_position_y = 0.95
    plt.gca().text(
        text_position_x, text_position_y, 
        f"R² = {r_squared:.3f}\n{p_str}\n{equation}", 
        transform=plt.gca().transAxes, 
        fontsize=20, 
        verticalalignment="top", 
    )
    
    ax = plt.gca()  
    ax.spines['top'].set_visible(True)  
    ax.spines['right'].set_visible(True) 
    fig=plt.gcf()
    plt.show()   
    if filename:
        fig.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close() 

variables = [
    {"name": "CPR", "xlabel": "CPR (µmol CO$_2$ m$^{-2}$ s$^{-1}$)"},
    {"name": "NT", "xlabel": "NT (g m$^{-2}$)"},
    {"name": "DMA", "xlabel": "DMA (g m$^{-2}$)"},
    {"name": "DMT", "xlabel": "DMT (g m$^{-2}$)"},
    {"name": "NU", "xlabel": "NU (g m$^{-2}$)"}
]

for var in variables:
    save_path = f""
    plot_with_stats(
        x=var["name"], 
        y="Yield", 
        data=df, 
        xlabel=var["xlabel"], 
        ylabel="Yield (g m$^{-2}$)", 
        title=f"Relationship between {var['name']} and Yield",
        filename=save_path
    )