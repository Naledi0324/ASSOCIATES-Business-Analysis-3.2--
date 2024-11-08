# Useful for identifying unusual medication usage or irregularities in user patterns that might need attention.
# leveraging user_engagement.csv to identify anomalies that could indicate a user is disengaging, prompting proactive outreach or adjusted reminder strategies. 
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        """
        Initialize the anomaly detector with the specified contamination rate.
        :param contamination: The proportion of observations to be considered as outliers.
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42)

    def load_and_preprocess_data(self, file_path_curefind, file_path_engagement):
        """
        Load and preprocess data from CSV files.
        :param file_path_curefind: Path to the Curefind_Dataset.csv file.
        :param file_path_engagement: Path to the user_engagement.csv file.
        :return: Preprocessed DataFrame.
        """
        # Load both datasets
        data_curefind = pd.read_csv(file_path_curefind)
        data_engagement = pd.read_csv(file_path_engagement)

        # Merge datasets on User_ID
        data = pd.merge(data_curefind, data_engagement, on="User_ID")

        # Selecting relevant numeric features for anomaly detection
        features = data[['Age', 'Dosage_mg', 'Missed_Doses_Last_30_Days', 'Login_Count', 'Reminders_Viewed']]

        # Handling missing values by filling with median values
        features = features.fillna(features.median())

        return features

    def fit(self, data):
        """
        Fit the Isolation Forest model to the data.
        :param data: A pandas DataFrame containing the features for anomaly detection.
        """
        self.model.fit(data)

    def predict(self, data):
        """
        Predict anomalies in the provided data.
        :param data: A pandas DataFrame containing the features to predict.
        :return: A numpy array of -1 for outliers and 1 for inliers.
        """
        return self.model.predict(data)

    def get_anomalies(self, data):
        """
        Get the anomalies detected in the provided data.
        :param data: A pandas DataFrame containing the features to predict.
        :return: A DataFrame of the anomalies detected.
        """
        predictions = self.predict(data)
        anomalies = data[predictions == -1]
        return anomalies

if __name__ == "__main__":
    file_path_curefind = 'CureApp/data/Curefind_Dataset.csv'
    file_path_engagement = 'CureApp/data/user_engagement.csv'

    # Initialize the anomaly detector
    detector = AnomalyDetector()

    # Load and preprocess the data
    data = detector.load_and_preprocess_data(file_path_curefind, file_path_engagement)
    
    # Fit the model on the data
    detector.fit(data)

    # Get anomalies
    anomalies = detector.get_anomalies(data)

    # Display the detected anomalies
    print("Detected anomalies:")
    print(anomalies)
