# used for predicting medication adherence patterns based on past user behavior.
#leveraging user_engagement.csv to predict which users are likely to follow reminders or may need additional interventions, helping tailor reminders to individual needs. 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

class SupervisedModel:
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)

    def load_and_preprocess_data(self, file_path_curefind, file_path_engagement):
        """
        Load data from CSV files and preprocess it for training.
        :param file_path_curefind: Path to the Curefind_Dataset.csv file.
        :param file_path_engagement: Path to the user_engagement.csv file.
        :return: Preprocessed features and target labels.
        """
        # Load both datasets
        data_curefind = pd.read_csv(file_path_curefind)
        data_engagement = pd.read_csv(file_path_engagement)

        # Merge datasets on User_ID
        data = pd.merge(data_curefind, data_engagement, on="User_ID")

        # Selecting features from both datasets
        features = data[['Age', 'Dosage_mg', 'Missed_Doses_Last_30_Days', 'Login_Count', 'Reminders_Viewed', 'Feedback_Rating']]
        target = data['Adherence_Level']

        # Encoding target labels
        label_encoder = LabelEncoder()
        target_encoded = label_encoder.fit_transform(target)
        self.label_encoder = label_encoder  # Save encoder for later use

        # Splitting data
        X_train, X_test, y_train, y_test = train_test_split(features, target_encoded, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        """
        Train the model on the provided features and labels.
        :param X_train: Training features.
        :param y_train: Training labels.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """
        Predict the labels for the provided features.
        :param X: Features to predict.
        :return: Predicted labels.
        """
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model's accuracy on the test set.
        :param X_test: Test features.
        :param y_test: True labels for test features.
        :return: Accuracy score.
        """
        predictions = self.predict(X_test)
        return accuracy_score(y_test, predictions)

if __name__ == "__main__":
    file_path_curefind = 'CureApp/data/Curefind_Dataset.csv'
    file_path_engagement = 'CureApp/data/user_engagement.csv'

    model = SupervisedModel()
    X_train, X_test, y_train, y_test = model.load_and_preprocess_data(file_path_curefind, file_path_engagement)
    
    # Train the model
    model.train(X_train, y_train)
    
    # Evaluate the model
    accuracy = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
