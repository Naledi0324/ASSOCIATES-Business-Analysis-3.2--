# Tests for ML models
import unittest
import numpy as np
from app.ml_models.anomaly_detection import detect_anomalies
from app.ml_models.supervised_learning import train_supervised_model, predict_supervised
from app.ml_models.reinforcement_learning import ReinforcementModel
from app.ml_models.time_series_analysis import analyze_time_series

class TestMLModels(unittest.TestCase):
    
    def test_anomaly_detection(self):
        # Sample data for anomaly detection
        data = [1, 2, 3, 4, 100, 6, 7]  # 100 is an outlier
        anomalies = detect_anomalies(data)
        self.assertIn(100, anomalies, "Anomaly detection failed to identify the outlier.")

    def test_supervised_model(self):
        # Sample data for supervised model (classification or regression)
        X_train = np.array([[0], [1], [2], [3], [4]])
        y_train = np.array([0, 0, 1, 1, 1])
        
        # Train the model
        model = train_supervised_model(X_train, y_train)
        
        # Test predictions
        X_test = np.array([[1.5]])
        y_pred = predict_supervised(model, X_test)
        self.assertIn(y_pred[0], [0, 1], "Supervised model prediction is incorrect.")

    def test_reinforcement_model(self):
        # Initialize and test reinforcement model
        env = np.array([0, 1, 2, 3])  # Example environment setup
        agent = ReinforcementModel(action_space=4)
        
        # Simulate a step in the environment
        action = agent.select_action(env)
        self.assertIn(action, range(4), "Reinforcement model action out of bounds.")

    def test_time_series_analysis(self):
        # Sample data for time series analysis
        time_series_data = [10, 11, 12, 13, 14, 15]
        
        # Perform analysis (e.g., forecasting)
        forecast = analyze_time_series(time_series_data)
        
        # Example assertion - check if forecast length is as expected
        expected_length = 3  # Modify based on analyze_time_series output
        self.assertEqual(len(forecast), expected_length, "Time series analysis forecast length is incorrect.")
        
if __name__ == '__main__':
    unittest.main()


