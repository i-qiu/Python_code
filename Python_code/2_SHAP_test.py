import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial' 
from sklearn.preprocessing import StandardScaler
import shap

file_path = ''  
data = pd.read_excel(file_path)

features = [
    "CPR", "DMA","NU", "DMT","NT"
]
target = "Yield"
for col in features + [target]:
    data[col] = pd.to_numeric(data[col], errors="coerce")
data_clean = data.dropna(subset=features + [target])
X = data_clean[features]
y = data_clean[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
print(rf.predict(X_test_scaled))

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test_scaled)

mean_abs_shap = np.abs(shap_values).mean(axis=0)
importance_df = pd.DataFrame({
    'feature': features,
    'mean_abs_shap': mean_abs_shap
}).sort_values(by='mean_abs_shap', ascending=False)
print(importance_df)

plt.figure(figsize=(8, 6), dpi=300)  
shap.summary_plot(shap_values, X_test_scaled, feature_names=features, plot_type="bar", color='#1f77b4',show=False)
ax = plt.gca() 
ax.set_xlabel('') 
ax.spines['top'].set_visible(True)  
ax.spines['right'].set_visible(True) 
ax.spines['left'].set_visible(True)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
fig = plt.gcf()
plt.show()
fig.savefig()
