from flaml import AutoML
from sklearn.datasets import fetch_california_housing

# Initialize an AutoML instance
automl = AutoML()
# Specify automl goal and constraint
automl_settings = {
    "time_budget": 100,  # in seconds
    "metric": 'r2',
    "task": 'regression',
    "log_file_name": "california.log",
}
X_train, y_train = fetch_california_housing(return_X_y=True)
# Train with labeled input data
print(y_train)
automl.fit(X_train=X_train, y_train=y_train,
           **automl_settings)
# Predict
print(automl.predict(X_train))
# Print the best model
print(automl.model.estimator)
