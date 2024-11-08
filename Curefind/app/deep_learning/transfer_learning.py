# Transfer learning for NLP tasks
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

class TransferLearningModel:
    def __init__(self, input_shape, num_classes):
        """
        Initialize the Transfer Learning model using VGG16.
        :param input_shape: Shape of the input images (height, width, channels).
        :param num_classes: Number of classes for classification.
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.base_model = VGG16(weights='imagenet', include_top=False, input_shape=self.input_shape)
        self.model = self.build_model()

    def build_model(self):
        """
        Build the Transfer Learning model.
        :return: Compiled model with VGG16 base.
        """
        # Freeze the base model
        for layer in self.base_model.layers:
            layer.trainable = False

        # Create a new model on top of the base model
        x = self.base_model.output
        x = Flatten()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)

        # Complete model
        model = Model(inputs=self.base_model.input, outputs=predictions)

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    def train(self, train_data, val_data, epochs=50, batch_size=32):
        """
        Train the Transfer Learning model on the training data.
        :param train_data: Training data generator.
        :param val_data: Validation data generator.
        :param epochs: Number of epochs for training.
        :param batch_size: Batch size for training.
        """
        # Use EarlyStopping to avoid overfitting
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

        self.model.fit(train_data,
                       validation_data=val_data,
                       epochs=epochs,
                       steps_per_epoch=train_data.samples // batch_size,
                       validation_steps=val_data.samples // batch_size,
                       callbacks=[early_stopping])

    def evaluate(self, test_data):
        """
        Evaluate the Transfer Learning model on the test data.
        :param test_data: Test data generator.
        :return: Loss and accuracy of the model on the test set.
        """
        return self.model.evaluate(test_data)

# Example usage
if __name__ == "__main__":
    # Define the path to your dataset and create data generators
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_data = train_datagen.flow_from_directory(
        'CureApp/data/Curefind_Dataset.csv',  # Replace with your dataset path
        target_size=(224, 224),  # VGG16 input size
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )

    val_data = train_datagen.flow_from_directory(
        'CureApp/data/Curefind_Database.csv',  
        target_size=(224, 224),  # VGG16 input size
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )

    # Initialize and train the Transfer Learning model
    transfer_learning_model = TransferLearningModel(input_shape=(224, 224, 3), num_classes=train_data.num_classes)
    transfer_learning_model.train(train_data, val_data, epochs=10, batch_size=32)

    # Evaluate the model
    loss, accuracy = transfer_learning_model.evaluate(val_data)
    print(f"Validation Loss: {loss:.4f}, Validation Accuracy: {accuracy:.4f}")
