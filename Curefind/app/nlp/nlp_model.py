# Code for NLP tasks 
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

class TextClassifier:
    def __init__(self):
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

    def train(self, X, y):
        """
        Train the text classification model.
        :param X: List of text data.
        :param y: Corresponding labels.
        """
        self.model.fit(X, y)

    def predict(self, X):
        """
        Predict the labels for new text data.
        :param X: List of text data.
        :return: Predicted labels.
        """
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model's performance on the test set.
        :param X_test: Test text data.
        :param y_test: True labels for test data.
        :return: Classification report.
        """
        predictions = self.model.predict(X_test)
        return classification_report(y_test, predictions)
