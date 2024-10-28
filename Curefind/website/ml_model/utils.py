#provides utility functions for data proprocessing and model support
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def preprocess_data(data, target_column):
    """
    Splits the data into features and target, and applies scaling.
    
    Parameters:
        data (DataFrame): The dataset containing features and the target column.
        target_column (str): The column name of the target variable.
        
    Returns:
        X_train, X_test, y_train, y_test: Scaled and split data.
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def reshape_for_lstm(data, timesteps=1, features=1):
    """
    Reshapes data to fit the input requirements of LSTM layers.
    
    Parameters:
        data (array-like): The data to be reshaped.
        timesteps (int): The number of timesteps for the LSTM.
        features (int): The number of features in each timestep.
        
    Returns:
        reshaped_data: The reshaped data for LSTM.
    """
    return np.reshape(data, (data.shape[0], timesteps, features))

def load_sample_data():
    """
    Loads or generates a small dataset for testing purposes.
    
    Returns:
        sample_data: A small sample dataset with features and target.
    """
    # Example: Generating a dataset of medication adherence times
    np.random.seed(0)
    data = {
        'adherence_times': np.random.randint(0, 100, 50),
        'dosage': np.random.randint(1, 5, 50),
        'adherence': np.random.randint(0, 2, 50)  # 0 for missed dose, 1 for taken
    }
    return data
