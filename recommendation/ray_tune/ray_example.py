from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from ray import tune
import pickle

# Load and split the data
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
print(X_train)
print(y_train)

# Define the training function


# Run the hyperparameter search
