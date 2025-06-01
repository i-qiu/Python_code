import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

file_path = ''  
data = pd.read_excel(file_path)

data['Warming'] = data['Treament'].apply(lambda x: 1 if 'W' in x else 0)  
data['Nitrogen'] = data['Treament'].apply(lambda x: 1 if 'N' in x else 0)  

variable = 'Pn30'

formula = f'{variable} ~ C(Warming) + C(Nitrogen) + C(year) + C(Warming):C(Nitrogen)'
model = ols(formula, data=data).fit()
anova_results = anova_lm(model, typ=2)

p_warming = anova_results.loc['C(Warming)', 'PR(>F)']
p_nitrogen = anova_results.loc['C(Nitrogen)', 'PR(>F)']
p_interaction = anova_results.loc['C(Warming):C(Nitrogen)', 'PR(>F)']

print("ANCOVA Results:")
print(anova_results)


grouped = data.groupby(['Warming', 'Nitrogen'])[variable].agg(['mean', 'std']).reset_index()


plot_data = data.copy()
plot_data['Nitrogen_label'] = plot_data['Nitrogen'].apply(lambda x: '+N' if x == 1 else '-N')
plot_data['Warming_label'] = plot_data['Warming'].apply(lambda x: '+W' if x == 1 else '-W')

sns.set(style="white")
plt.figure(figsize=(4, 6))

ax = sns.barplot(
    data=plot_data,
    x="Nitrogen_label",
    y="Pn30",
    hue="Warming_label",
    ci=None,
    width=0.6,
    palette=['#FFB3B3','#A41313' ]    
)

def significance_label(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'
# （-N，W=0 vs W=1）
subset1 = data[data['Nitrogen'] == 0]  
formula1 = f'{variable} ~ C(Warming) + C(year)'
model1 = ols(formula1, data=subset1).fit()
anova_results1 = anova_lm(model1, typ=2)
p_value1 = anova_results1.loc['C(Warming)', 'PR(>F)']

# （+N，W=0 vs W=1）
subset2 = data[data['Nitrogen'] == 1]  
formula2 = f'{variable} ~ C(Warming)+ C(year)'
model2 = ols(formula2, data=subset2).fit()
anova_results2 = anova_lm(model2, typ=2)
p_value2 = anova_results2.loc['C(Warming)', 'PR(>F)']


label1 = significance_label(p_value1)
label2 = significance_label(p_value2)

bar_positions = []  
for bar in ax.patches:
    bar_positions.append((bar.get_x() + bar.get_width() / 2, bar.get_height()))

y_offset = 1.0  
line_width = 0.2  

center_x1 = 0  
y1 = 14.5  
ax.plot([center_x1 - line_width, center_x1 + line_width], [y1, y1], color="black", lw=1.5)  
ax.text(center_x1, y1 + 0.2, label1, ha='center', va='bottom', fontsize=16)  

ax.plot([center_x1 - line_width, center_x1 - line_width], [y1 - 1, y1], color='black', lw=1.5)
ax.plot([center_x1 + line_width, center_x1 + line_width], [y1 - 1, y1], color='black', lw=1.5)


center_x2 = 1  
y2 = 17  
ax.plot([center_x2 - line_width, center_x2 + line_width], [y2, y2], color="black", lw=1.5)  
ax.text(center_x2, y2 + 0.2, label2, ha='center', va='bottom', fontsize=16)  

ax.plot([center_x2 - line_width, center_x2 - line_width], [y2 - 1, y2], color='black', lw=1.5)
ax.plot([center_x2 + line_width, center_x2 + line_width], [y2 - 1, y2], color='black', lw=1.5)


ax.text(0.02, 0.98, f"W: $\\it{{P}}$={p_warming:.3f}", transform=ax.transAxes, fontsize=14, va='top', ha='left')
ax.text(0.02, 0.93, f"N: $\\it{{P}}$={p_nitrogen:.3f}", transform=ax.transAxes, fontsize=14, va='top', ha='left')
ax.text(0.02, 0.88, f"W*N: $\\it{{P}}$={p_interaction:.3f}", transform=ax.transAxes, fontsize=14, va='top', ha='left')


ax.set_ylim(0, 30)
plt.ylabel(f"{variable} ($\mu$mol CO$_2$ m$^{-2}$ s$^{-1}$)",fontsize=16)
plt.legend(loc="upper right",fontsize=14 ,frameon=False)
plt.tick_params(axis='x', labelsize=16)  
plt.tick_params(axis='y', labelsize=16)
ax.set_xlabel('') 
plt.tight_layout()
fig = plt.gcf()  
plt.show()
fig.savefig()