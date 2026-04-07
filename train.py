import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from prometheus_client import start_http_server, Gauge
import os
import time

# MLflow Server
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
mlflow.set_experiment("iris-classification")

# Prometheus metric
accuracy_metric = Gauge('training_accuracy', 'Model accuracy')

def train():
    # شغل metrics server
    start_http_server(8000)

    # Load Data
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Parameters
    n_estimators = int(os.getenv("N_ESTIMATORS", 100))
    max_depth = int(os.getenv("MAX_DEPTH", 3))

    with mlflow.start_run():
        # Train
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth
        )
        model.fit(X_train, y_train)

        # Evaluate
        accuracy = accuracy_score(y_test, model.predict(X_test))

        # MLflow logs
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")

        # Prometheus metric
        accuracy_metric.set(accuracy)

        print(f"✅ Accuracy: {accuracy:.4f}")
        print(f"✅ Logged to MLflow successfully")

        # مهم جدًا عشان Prometheus يلحق يسحب
        time.sleep(60)

if __name__ == "__main__":
    train()
