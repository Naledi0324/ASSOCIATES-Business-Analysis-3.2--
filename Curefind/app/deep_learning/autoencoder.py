#we used autoencoder to identify unusual patterns in medication adherence, helping to flag irregularities or predict missed doses
import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler

class Autoencoder:
    def __init__(self, input_dim, encoding_dim=32):
        """
        Initialize the Autoencoder.
        :param input_dim: The number of features in the input data.
        :param encoding_dim: The dimension of the encoded representation.
        """
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.model = self.build_model()

    def build_model(self):
        """
        Build the autoencoder model.
        :return: Compiled autoencoder model.
        """
        # Input Layer
        input_layer = Input(shape=(self.input_dim,))
        
        # Encoder
        encoded = Dense(self.encoding_dim, activation='relu')(input_layer)
        
        # Decoder
        decoded = Dense(self.input_dim, activation='sigmoid')(encoded)
        
        # Autoencoder Model
        autoencoder = Model(inputs=input_layer, outputs=decoded)
        autoencoder.compile(optimizer='adam', loss='mean_squared_error')
        
        return autoencoder

    def train(self, X, epochs=50, batch_size=256):
        """
        Train the autoencoder on the input data.
        :param X: Input data for training.
        :param epochs: Number of epochs for training.
        :param batch_size: Batch size for training.
        """
        early_stopping = EarlyStopping(monitor='loss', patience=5, verbose=1)

        self.model.fit(X, X, 
                       epochs=epochs,
                       batch_size=batch_size,
                       shuffle=True,
                       callbacks=[early_stopping])

    def encode(self, X):
        """
        Encode the input data into the reduced dimensionality.
        :param X: Input data for encoding.
        :return: Encoded representation of the input data.
        """
        encoder = Model(inputs=self.model.input, outputs=self.model.layers[1].output)
        return encoder.predict(X)

    def reconstruct(self, X):
        """
        Reconstruct data using the full autoencoder model.
        :param X: Input data.
        :return: Reconstructed output from the autoencoder.
        """
        return self.model.predict(X)

# Example usage
if __name__ == "__main__":
    df = pd.read_csv('CureApp/data/Curefind_Dataset.csv')  
    X = df.select_dtypes(include=[np.number]).values  

    # Normalize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Initialize and train the autoencoder
    autoencoder = Autoencoder(input_dim=X_scaled.shape[1], encoding_dim=16)
    autoencoder.train(X_scaled, epochs=100, batch_size=32)

    # Encode and reconstruct data
    encoded_data = autoencoder.encode(X_scaled)
    print("Encoded Data:", encoded_data)

    reconstructed_data = autoencoder.reconstruct(X_scaled)
    print("Reconstructed Data:", reconstructed_data)
