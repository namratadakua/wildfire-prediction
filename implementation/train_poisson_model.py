import statsmodels.api as sm
import statsmodels.discrete.discrete_model as dm
import numpy as np
from patsy import dmatrices
import statsmodels.graphics.tsaplots as tsa
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split


def train_poisson_model(data):
    model_data = data[
        ['daynight', 'month', '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
         'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3', 'soil_temperature_level_4',
         'soil_type', 'total_precipitation', 'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
         'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4', 'number_of_fire']]

    model_data.rename(columns={'10m_u_component_of_wind': 'u_wind'}, inplace=True)
    model_data.rename(columns={'10m_v_component_of_wind': 'v_wind'}, inplace=True)
    model_data.rename(columns={'2m_temperature': 'm_temperature'}, inplace=True)

    # Split the DataFrame into train and test sets (70% train, 30% test)
    train_df, test_df = train_test_split(model_data, test_size=0.3,
                                         random_state=42)  # Set random state for reproducibility

    expression = 'number_of_fire ~ daynight + month + u_wind + v_wind + m_temperature + soil_temperature_level_1 + soil_temperature_level_2 + soil_temperature_level_3 + soil_temperature_level_4 + soil_type +  total_precipitation + volumetric_soil_water_layer_1 + volumetric_soil_water_layer_2 + volumetric_soil_water_layer_3 + volumetric_soil_water_layer_4'

    y_train, X_train = dmatrices(expression, train_df, return_type='dataframe')
    # print(y_train)
    # print(X_train)

    y_test, X_test = dmatrices(expression, test_df, return_type='dataframe')
    # print(y_test)
    # print(X_test)

    nb2_model = dm.NegativeBinomial(endog=y_train, exog=X_train, loglike_method='nb2')
    nb2_model_results = nb2_model.fit(maxiter=100)
    return nb2_model, nb2_model_results
