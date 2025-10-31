"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.0.0
"""
import logging
import typing as t

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

logger = logging.getLogger(__name__)

def split_data(df: pd.DataFrame, parameters: t.Dict) -> t.Tuple:
    X = df[parameters["features"]]
    y = df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = parameters["test_size"], random_state=parameters["random_state"])
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor

def evaluate_model(regressor: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    r2_score_value = r2_score(y_test, regressor.predict(X_test))
    logger.info( "R2 Score of the model is: %.3f", r2_score_value)