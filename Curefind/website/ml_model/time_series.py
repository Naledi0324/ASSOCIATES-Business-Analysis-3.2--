#this file analyse medication schedules with time series modelling
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_medication_adherence(user_data):
    adherence_data = pd.Series(user_data['adherence_times'])
    model = ARIMA(adherence_data, order=(5, 1, 0))  # Example ARIMA order
    model_fit = model.fit()
    return model_fit.forecast(steps=7)
