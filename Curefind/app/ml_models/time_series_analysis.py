# Code for time series analysis
# leveraging user_engagement.csv to  allow the model to predict potential drops in adherence or engagement, helping schedule timely reminders and interventions.
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR  # Use VAR for multivariate time series
from sklearn.metrics import mean_squared_error

class TimeSeriesAnalyzer:
    def __init__(self):
        self.model = None

    def fit(self, data):
        """
        Fit the VAR model to the time series data.
        :param data: A pandas DataFrame containing the time series data with multiple columns.
        """
        self.model = VAR(data)
        self.model = self.model.fit()

    def forecast(self, steps=1):
        """
        Forecast future values using the fitted VAR model.
        :param steps: Number of steps to forecast into the future.
        :return: Forecasted values.
        """
        if self.model is None:
            raise Exception("Model has not been fitted yet. Call fit() before forecasting.")
        return self.model.forecast(self.model.y, steps=steps)

    def evaluate(self, test_data):
        """
        Evaluate the model's predictions against test data.
        :param test_data: Actual values to compare against.
        :return: Mean Squared Error of the predictions.
        """
        forecasted_values = self.model.forecast(self.model.y, steps=len(test_data))
        mse_values = {}
        for i, col in enumerate(test_data.columns):
            mse_values[col] = mean_squared_error(test_data.iloc[:, i], forecasted_values[:, i])
        return mse_values

if __name__ == "__main__":
    # Load Curefind_Dataset and user_engagement data
    data_curefind = pd.read_csv('CureApp/data/Curefind_Dataset.csv', parse_dates=['date'], index_col='date')
    data_engagement = pd.read_csv('CureApp/data/user_engagement.csv', parse_dates=['Last_Interaction_Date'], index_col='Last_Interaction_Date')

    # Merge on date for time series analysis
    merged_data = pd.merge(data_curefind, data_engagement, left_index=True, right_index=True)

    # Select relevant columns for time series analysis
    time_series_data = merged_data[['Adherence_Level', 'Login_Count', 'Reminders_Viewed']]

    # Initialize the time series analyzer
    analyzer = TimeSeriesAnalyzer()

    # Fit the model on the merged time series data
    analyzer.fit(time_series_data)

    # Forecast future values
    forecasted_values = analyzer.forecast(steps=5)  # Forecast next 5 time points
    print("Forecasted Values:", forecasted_values)
