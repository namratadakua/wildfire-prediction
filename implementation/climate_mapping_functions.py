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


def set_climate_data(grid, row_ranges, column_ranges, all_data):
    logging.basicConfig(filename='set_climate_data.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # fire_occurrence_data = all_data.query("`fire_occurrence` == 1")
    map_coordinates = MapCoordinates()
    for index, climate_data_row in all_data.iterrows():

        latitude = climate_data_row['latitude']
        longitude = climate_data_row['longitude']

        lower_row_limit, upper_row_limit = get_row_range(longitude, row_ranges)
        lower_col_limit, upper_col_limit = get_col_range(latitude, column_ranges)

        # print(f"{lower_row_limit}:{upper_row_limit} - {lower_col_limit}:{upper_col_limit}")

        # Assign the fire data to a grid
        found = False
        for row in range(lower_row_limit, upper_row_limit):
            for col in range(lower_col_limit, upper_col_limit):
                grid_cell = grid[row, col]

                cell_llat = grid_cell.llat
                cell_ulat = grid_cell.ulat
                cell_llon = grid_cell.llon
                cell_ulon = grid_cell.ulon
                climate_points = grid_cell.climate_points

                if (cell_llat <= latitude < cell_ulat) and (cell_llon <= longitude < cell_ulon):
                    found = True
                    climate_points.append(climate_data_row)
                    # logging.info(f"New Cell {row} {col}: {grid_cell}")
                    grid_cell.climate_points = climate_points
                    grid[row, col] = grid_cell
                    # print(f"climate {index} row completed  - {longitude}:{latitude} at {row}:{col} - {grid_cell}")
                    break

            if found:
                if index % 10 == 0:
                    print(f"climate {index} row completed")
                break
        if not found:
            logging.debug(
                f"climate {index} row not completed {lower_row_limit}:{upper_row_limit} - {lower_col_limit}:{upper_col_limit}  - {longitude} : {latitude} - {climate_data_row['date']} -  {climate_data_row['daynight']}")
            for row in range(0, map_coordinates.meridians_length):
                for col in range(0, map_coordinates.parallels_length):
                    grid_cell = grid[row, col]

                    cell_llat = grid_cell.llat
                    cell_ulat = grid_cell.ulat
                    cell_llon = grid_cell.llon
                    cell_ulon = grid_cell.ulon
                    climate_points = grid_cell.climate_points

                    if (cell_llat <= latitude < cell_ulat) and (cell_llon <= longitude < cell_ulon):
                        found = True
                        climate_points.append(climate_data_row)
                        # logging.info(f"New Cell {row} {col}: {grid_cell}")
                        grid_cell.climate_points = climate_points
                        grid[row, col] = grid_cell
                        # print(f"climate {index} row completed  - {longitude}:{latitude} at {row}:{col} - {grid_cell}")
                        break

                if found:
                    logging.debug(f"retry - climate {index} row completed")
                    break
    return grid
