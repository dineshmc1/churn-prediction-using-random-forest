import pandas as pd
import numpy as np

np.random.seed(42)

def generate_churn_data(n_rows=10000):
    data = []
    
    for i in range(n_rows):
        customer_id = f"CUST_{1000+i}"
        age = np.random.randint(18, 75)
        gender = np.random.choice(['Male', 'Female'])
        
        tenure_months = np.random.randint(1, 72)
        contract_type = np.random.choice(['Month-to-month', 'One year', 'Two year'], p=[0.5, 0.3, 0.2])
        payment_method = np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'])
        monthly_charges = np.round(np.random.uniform(30.0, 120.0), 2)
        total_charges = np.round(monthly_charges * tenure_months, 2)
        
        num_support_calls = np.random.randint(0, 6)
        avg_login_per_month = np.random.randint(1, 30)
        
        base_prob = 0.40
        
        if tenure_months > 48: base_prob -= 0.25
        elif tenure_months > 24: base_prob -= 0.15
        elif tenure_months < 6: base_prob += 0.10
        
        if contract_type == 'Month-to-month': base_prob += 0.15
        elif contract_type == 'Two year': base_prob -= 0.15
        
        if num_support_calls > 3: base_prob += 0.25
        if num_support_calls == 0: base_prob -= 0.05
        
        if monthly_charges > 100: base_prob += 0.05
        
        noise = np.random.normal(0, 0.05)
        churn_prob = base_prob + noise
        churn_prob = np.clip(churn_prob, 0.0, 1.0)
        
        churn_status = 1 if np.random.random() < churn_prob else 0
        
        data.append([
            customer_id, age, gender, tenure_months, contract_type, 
            payment_method, monthly_charges, total_charges, 
            num_support_calls, avg_login_per_month, 
            churn_status
        ])
        
    columns = [
        'CustomerID', 'Age', 'Gender', 'Tenure_Months', 'Contract_Type', 
        'Payment_Method', 'Monthly_Charges', 'Total_Charges', 
        'Num_Support_Calls', 'Avg_Login_Per_Month', 'Churn'
    ]
    
    return pd.DataFrame(data, columns=columns)

df = generate_churn_data(10000)
df.to_csv('customer_churn_data.csv', index=False)
print("Data generated. Head:")
print(df.head())