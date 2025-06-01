import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 
from scipy.stats import pearsonr
file_path = ''  
data = pd.read_excel(file_path)
numeric_columns = [
    "Yield",
    "CPR",
    "Pn10",
    "Pn20",
    "Pn30",
    "DMA",
    "DMT",
    "DMTE",
    "NU",
    "NT",
    "GNDR"  
]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")
correlation_matrix = data[numeric_columns].corr(method='pearson')
print(correlation_matrix)


pval_matrix = pd.DataFrame(np.ones((len(numeric_columns), len(numeric_columns))),
                            columns=numeric_columns, index=numeric_columns)
for i in numeric_columns:
    for j in numeric_columns:
        if i != j:
            corr, pval = pearsonr(data[i].dropna(), data[j].dropna())
            pval_matrix.loc[i, j] = pval


def significance_stars(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return ""

annot = correlation_matrix.round(2).astype(str)
for i in numeric_columns:
    for j in numeric_columns:
        if i != j:
            annot.loc[i, j] += significance_stars(pval_matrix.loc[i, j])
        else:
            annot.loc[i, j] = "1.00"

plt.figure(figsize=(12, 10))
ax=sns.heatmap(correlation_matrix, annot=annot, fmt="", cmap="coolwarm", cbar=True,annot_kws={"fontsize": 14})
ax.collections[0].colorbar.ax.tick_params(labelsize=16)
plt.xticks(rotation=45, ha='right',fontsize=16)   
plt.yticks(rotation=0,fontsize=16)               
plt.tight_layout()
fig = plt.gcf()
plt.show()
fig.savefig()