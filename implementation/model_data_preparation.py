import pandas as pd
import numpy as np
import logging
import statsmodels.api as sm
from data_models import MapCoordinates
from data_models import RowRange
from data_models import ColumnRange
from data_models import GridCell
from data_models import get_row_range
from data_models import get_col_range


def prepare_model_data(grid):
    map_coordinates = MapCoordinates()
    model_df = pd.DataFrame({
        'daynight': pd.Series(dtype='str'),
        'year': pd.Series(dtype='str'),
        # 'brightness': pd.Series(dtype='float'),
        # 'confidence': pd.Series(dtype='float'),
        # 'frp': pd.Series(dtype='float'),
        # 'bright_t31': pd.Series(dtype='float'),
        # 'fire_occurrence': pd.Series(dtype='int'),
        'month': pd.Series(dtype='int'),
        'day': pd.Series(dtype='int'),
        '10m_u_component_of_wind': pd.Series(dtype='float'),
        '10m_v_component_of_wind': pd.Series(dtype='float'),
        '2m_temperature': pd.Series(dtype='float'),
        'soil_temperature_level_1': pd.Series(dtype='float'),
        'soil_temperature_level_2': pd.Series(dtype='float'),
        'soil_temperature_level_3': pd.Series(dtype='float'),
        'soil_temperature_level_4': pd.Series(dtype='float'),
        'soil_type': pd.Series(dtype='float'),
        'total_precipitation': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_1': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_2': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_3': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_4': pd.Series(dtype='float'),
        'number_of_fire': pd.Series(dtype='int'),
    })
    for row in range(0, map_coordinates.meridians_length):
        for column in range(0, map_coordinates.parallels_length):
            grid_cell = grid[row, column]
            if grid_cell.fire_count > 0:
                fire_points_rows = []
                for fire_point in grid_cell.fire_points:
                    date_split = fire_point['acq_date'].split("-")
                    year = date_split[0]
                    month = date_split[1]
                    day = date_split[2]

                    fire_point_row = {
                        'daynight': fire_point.daynight,
                        'year': year,
                        'month': month,
                        'day': day
                    }
                    fire_points_rows.append(fire_point_row)

                fire_points_df = pd.DataFrame(fire_points_rows, columns=['daynight', 'year', 'month', 'day'])

                fire_points_df = fire_points_df.groupby(['daynight', 'year', 'month', 'day']).size().to_frame(
                    name='number_of_fire').reset_index()

                climate_points_rows = []

                for climate_point in grid_cell.climate_points:
                    date_split = climate_point.date.split("-")
                    year = date_split[0]
                    month = date_split[1]
                    day = date_split[2]

                    climate_point_row = {
                        'daynight': climate_point.daynight,
                        'year': year,
                        'month': month,
                        'day': day,
                        '10m_u_component_of_wind': climate_point['10m_u_component_of_wind'],
                        '10m_v_component_of_wind': climate_point['10m_v_component_of_wind'],
                        '2m_temperature': climate_point['2m_temperature'],
                        'soil_temperature_level_1': climate_point['soil_temperature_level_1'],
                        'soil_temperature_level_2': climate_point['soil_temperature_level_2'],
                        'soil_temperature_level_3': climate_point['soil_temperature_level_3'],
                        'soil_temperature_level_4': climate_point['soil_temperature_level_4'],
                        'soil_type': climate_point['soil_type'],
                        'total_precipitation': climate_point['total_precipitation'],
                        'volumetric_soil_water_layer_1': climate_point['volumetric_soil_water_layer_1'],
                        'volumetric_soil_water_layer_2': climate_point['volumetric_soil_water_layer_2'],
                        'volumetric_soil_water_layer_3': climate_point['volumetric_soil_water_layer_3'],
                        'volumetric_soil_water_layer_4': climate_point['volumetric_soil_water_layer_4']

                    }
                    climate_points_rows.append(climate_point_row)

                cell_fire_point_df = pd.DataFrame(climate_points_rows, columns=['daynight',
                                                                                'year',
                                                                                'month',
                                                                                'day',
                                                                                '10m_u_component_of_wind',
                                                                                '10m_v_component_of_wind',
                                                                                '2m_temperature',
                                                                                'soil_temperature_level_1',
                                                                                'soil_temperature_level_2',
                                                                                'soil_temperature_level_3',
                                                                                'soil_temperature_level_4',
                                                                                'soil_type',
                                                                                'total_precipitation',
                                                                                'volumetric_soil_water_layer_1',
                                                                                'volumetric_soil_water_layer_2',
                                                                                'volumetric_soil_water_layer_3',
                                                                                'volumetric_soil_water_layer_4'
                                                                                ])
                on_columns = ['daynight',
                              'year',
                              'month',
                              'day', ]
                result = pd.merge(fire_points_df, cell_fire_point_df, how='left', left_on=on_columns,
                                  right_on=on_columns)
                print(result.columns.tolist())
                # result = result.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])

                model_df = pd.concat([model_df, result])
                print(f"{row}:{column} row completed with count - {grid_cell.fire_count}")
    model_df.to_csv('poisson_regression_model_data_1.csv')
    return model_df
