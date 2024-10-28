#this file is responsible for training models for medication adherence predictions
import tensorflow as tf
from tensorflow.keras import layers, models

def create_medication_adherence_model():
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(10,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, train_data, train_labels):
    model.fit(train_data, train_labels, epochs=10, batch_size=8)
