import mlflow
import mlflow.sklearn
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, roc_auc_score, f1_score, precision_score, recall_score)
from preprocessing import preprocess
 
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment("fraud-detection")

def train_and_log(model, name, X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name=name):

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]

        metrics =  {
            "roc_auc": roc_auc_score(y_test, proba),
            "f1": f1_score(y_test, preds),
            "precision": precision_score(y_test, preds),
            "recall": recall_score(y_test, preds)
        }

        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            model,
            name="model",
            registered_model_name=f"fraud-{name}"
        )
        print(f"\n{name}")
        print(classification_report(y_test, preds))
        print(f"ROC-AUC:{metrics['roc_auc']:.4f}")
        return metrics['roc_auc'], model
    
if __name__ == '__main__':
    X_test, X_train, y_test, y_train = preprocess(r"..\data\creditcard.csv")

    models = [
        (LogisticRegression(max_iter=1000), "logistic_regression"),
        (RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),"random forest"),
        (GradientBoostingClassifier(n_estimators=100, random_state=42), "gradient_boosting")
        ]

    best_auc = 0
    best_model = None

    for item in models:
        model = item[0]
        name = item[1]
        auc, trained = train_and_log(model, name, X_train, X_test, y_train, y_test)
        if auc > best_auc:
            best_auc = auc
            best_model = trained

    joblib.dump(best_model, r"..\app\model.pkl")
    print(f"\nBest model saved - AUC :{best_auc:.4f}")
    