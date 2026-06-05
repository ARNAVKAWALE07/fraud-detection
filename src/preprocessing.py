import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def preprocess(path):
    df = pd.read_csv(path)

    scaler = StandardScaler()
    df['Amount'] = scaler.fit_transform(df[['Amount']])
    df['Time'] =  scaler.fit_transform(df[['Time']])

    X = df.drop('Class', axis=1)
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
    smote = SMOTE(random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

    print(f"Training sample after SMOTE: {len(X_train_bal)}")
    print(f"Fraud ratio:{y_train_bal.mean():.2%}")

    return X_train_bal, X_test, y_train_bal, y_test


