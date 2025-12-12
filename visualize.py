import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

np.random.seed(42)
n_samples = 200

tenure = np.random.randint(1, 72, n_samples)
charges = np.random.uniform(30, 120, n_samples)

churn_prob = (charges / 120) * 0.6 - (tenure / 72) * 0.5 + 0.4
churn_prob += np.random.normal(0, 0.05, n_samples) 
churn_prob = np.clip(churn_prob, 0, 1)

df = pd.DataFrame({'Tenure': tenure, 'Charges': charges, 'Churn': churn_prob})
X = df[['Tenure', 'Charges']]
y = df['Churn']

tree_model = DecisionTreeRegressor(max_depth=5)
tree_model.fit(X, y)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

x_min, x_max = X['Tenure'].min(), X['Tenure'].max()
y_min, y_max = X['Charges'].min(), X['Charges'].max()
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 30), np.linspace(y_min, y_max, 30))

Z_tree = tree_model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
Z_rf = rf_model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

fig = plt.figure(figsize=(16, 7))
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(tenure, charges, churn_prob, c='r', marker='o', s=20, alpha=0.3, label='Actual Data')
ax1.plot_surface(xx, yy, Z_tree, cmap='viridis', alpha=0.8, edgecolor='none')
ax1.set_title("Single Decision Tree\n('Staircase' Decisions)", fontsize=14)
ax1.set_xlabel('Tenure (Months)')
ax1.set_ylabel('Monthly Charges ($)')
ax1.set_zlabel('Churn Probability')

ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(tenure, charges, churn_prob, c='r', marker='o', s=20, alpha=0.3, label='Actual Data')
ax2.plot_surface(xx, yy, Z_rf, cmap='plasma', alpha=0.8, edgecolor='none')
ax2.set_title("Random Forest (100 Trees)\n(Smoothed 'Averaged' Decisions)", fontsize=14)
ax2.set_xlabel('Tenure (Months)')
ax2.set_ylabel('Monthly Charges ($)')
ax2.set_zlabel('Churn Probability')

plt.tight_layout()
plt.show()