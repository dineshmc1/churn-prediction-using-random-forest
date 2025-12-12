import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report


df = pd.read_csv('customer_churn_data.csv')
X = df.drop(['CustomerID', 'Churn'], axis=1)
y = df['Churn'] 

categorical_cols = ['Gender', 'Contract_Type', 'Payment_Method']
numerical_cols = [col for col in X.columns if col not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])


rf_regressor = RandomForestRegressor(random_state=42)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', rf_regressor)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {
    'regressor__n_estimators': [50, 100, 200],      
    'regressor__max_depth': [10, 20, None],         
    'regressor__min_samples_leaf': [1, 2, 4]        
}

print("\nTraining Model and tuning parameters")
grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print(f"Best Parameters Found: {grid_search.best_params_}")

y_pred_prob = best_model.predict(X_test)

print("\n--- Regression Metrics ---")
mse = mean_squared_error(y_test, y_pred_prob)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_prob)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R2 Score: {r2:.4f} (Higher is better)")

y_pred_class = (y_pred_prob > 0.50).astype(int)

print("\n--- Classification Metrics ---")
accuracy = accuracy_score(y_test, y_pred_class)
print(f"Accuracy: {accuracy*100:.2f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred_class))
preprocessor_step = best_model.named_steps['preprocessor']
rf_step = best_model.named_steps['regressor']
cat_names = preprocessor_step.named_transformers_['cat'].get_feature_names_out(categorical_cols)
all_feature_names = numerical_cols + list(cat_names)

importances = rf_step.feature_importances_

fi_df = pd.DataFrame({'Feature': all_feature_names, 'Importance': importances})
fi_df = fi_df.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=fi_df, palette='viridis')
plt.title('Feature Importance: What drives Churn?')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.show()

print("\n--- Example Prediction ---")
sample_customer = X_test.iloc[0:1] 
true_status = y_test.iloc[0]
predicted_risk = best_model.predict(sample_customer)[0]

print("Customer Data:")
print(sample_customer.to_string(index=False))
print(f"\nActual Status: {'Churned (1)' if true_status==1 else 'Stayed (0)'}")
print(f"Predicted Risk Score: {predicted_risk:.4f}")
print(f"Model Decision: {'High Risk' if predicted_risk > 0.5 else 'Safe'}")