# LSTM model for time series analysis, predicting future doses and patterns to improve adherence
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

class LSTMModel:
    def __init__(self, input_shape, regression=True):
        """
        Initialize the LSTM model.
        :param input_shape: Shape of the input sequences (timesteps, features).
        :param regression: Set True for regression tasks, False for binary classification.
        """
        self.input_shape = input_shape
        self.regression = regression
        self.model = self.build_model()

    def build_model(self):
        """
        Build the LSTM model.
        :return: Compiled LSTM model.
        """
        model = Sequential()
        
        model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=self.input_shape))
        model.add(Dropout(0.2))  # Prevent overfitting
        
        model.add(LSTM(50, activation='relu'))
        model.add(Dropout(0.2))  # Prevent overfitting
        
        if self.regression:
            model.add(Dense(1))  # For regression tasks
            loss_function = 'mean_squared_error'
        else:
            model.add(Dense(1, activation='sigmoid'))  # For binary classification tasks
            loss_function = 'binary_crossentropy'
        
        model.compile(optimizer='adam', loss=loss_function, metrics=['binary_accuracy'] if not self.regression else [])
        
        return model

    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """
        Train the LSTM model on the training data.
        :param X_train: Training sequences.
        :param y_train: Training labels (continuous or binary).
        :param X_val: Validation sequences.
        :param y_val: Validation labels (continuous or binary).
        :param epochs: Number of epochs for training.
        :param batch_size: Batch size for training.
        """
        
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

        self.model.fit(X_train, y_train, 
                       validation_data=(X_val, y_val),
                       epochs=epochs,
                       batch_size=batch_size,
                       callbacks=[early_stopping])

    def evaluate(self, X_test, y_test):
        """
        Evaluate the LSTM model on the test data.
        :param X_test: Test sequences.
        :param y_test: Test labels (continuous or binary).
        :return: Loss and accuracy of the model on the test set.
        """
        return self.model.evaluate(X_test, y_test)


if __name__ == "__main__":
     df = pd.read_csv('CureApp/data/Curefind_Dataset.csv') 
    
    
     X_train = np.random.rand(1000, 10, 1)  
     y_train = np.random.rand(1000, 1)  # Continuous target values for regression
     X_val = np.random.rand(200, 10, 1)
     y_val = np.random.rand(200, 1)
     X_test = np.random.rand(200, 10, 1)
     y_test = np.random.rand(200, 1)

    # Initialize and train the LSTM model for a regression task
     lstm_model = LSTMModel(input_shape=(10, 1), regression=True)  
     lstm_model.train(X_train, y_train, X_val, y_val, epochs=10, batch_size=32)

    # Evaluate the model
     loss, accuracy = lstm_model.evaluate(X_test, y_test)
     print(f"Test Loss: {loss:.4f}")
     if not lstm_model.regression:
        print(f"Test Accuracy: {accuracy:.4f}")
