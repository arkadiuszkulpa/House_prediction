def check_null_population(minimum_percentage, data):
    """
    Identifies features in the dataset where the proportion of null values exceeds a given threshold.

    Parameters:
    - minimum_percentage (float): The minimum percentage threshold (between 0 and 1) for null values to be considered significant.
    - data (DataFrame): The dataset to analyze.

    Returns:
    - dict: A dictionary where keys are feature names and values are dictionaries containing:
        - "number" (int): The count of null values in the feature.
        - "percentage" (float): The percentage of null values in the feature.

    Prints:
    - A summary of features with null values exceeding the threshold.
    """
    null_dict = {}
    for feature in data:
        number_of_nulls = data[feature].isnull().sum()
        number_of_values = data[feature].count()
        number_total = number_of_nulls + number_of_values
        null_percentage = number_of_nulls / number_total

        if null_percentage > minimum_percentage:
            null_dict[feature] = {
                "number": number_of_nulls,
                "percentage": null_percentage
            }

    for feature, stats in null_dict.items():
        print(f"Feature '{feature}' has {stats['number']} nulls, "
              f"which is {(stats['percentage'] * 100):.2f}% of the total.")

    return null_dict


def preprocess_categorical(data, feature_name, mapping_dict):
    """
    Preprocesses a categorical feature by filling missing values and applying a specified mapping.

    Parameters:
    - data (DataFrame): The dataset containing the categorical feature.
    - feature_name (str): The name of the categorical feature to preprocess.
    - mapping_dict (dict): A dictionary mapping old values to new values.

    Returns:
    - None: The function modifies the DataFrame in place.

    Prints:
    - Value counts of the feature before and after preprocessing.
    """
    print(f"Value Counts for '{feature_name}' before preprocessing:")
    print(data[feature_name].value_counts())

    data[feature_name] = data[feature_name].fillna(0)
    data[feature_name] = data[feature_name].replace(mapping_dict)

    # Explicitly infer data types
    data[feature_name] = data[feature_name].infer_objects()

    print(f"Value Counts for '{feature_name}' after preprocessing:")
    print(data[feature_name].value_counts())

def filter_dataframes_by_percentage(df_dict, min_threshold=0.8, max_threshold=0.9):
    return {
        key: df for key, df in df_dict.items()
        if df['percentage'].max() > min_threshold and df['percentage'].max() <= max_threshold
    }

def create_top_x_percentage_dict(data, min_percentage, max_percentage = 1):
  
  data = filter_dataframes_by_percentage(data, min_percentage, max_percentage)
  # data = {key: df for key, df in data.items() if ((df["percentage"] > min_percentage) & (df["percentage"] <= max_percentage)).any()}

  for x in data:
    dominant_value = data[x].query("binary == 1")[x].iloc[0]
    dominant_percentage = data[x].query("binary == 1")["percentage"].iloc[0]
    print(f"For Feature {x}, Value {dominant_value} constitutes {(dominant_percentage*100).round(2)}%")
    #x_dominant = [x[x["binary"]
    #print(f"{x.key} has a dominant value {x.}")

  return data
  #print(len(percentage_dict_95))

import datetime

def replace_year_feature_with_age(feature, new_feature_name, train_data):
  """
  Replaces a given year-based feature in a dataset with the corresponding age and removes the original feature.

  Parameters:
  -----------
  feature : str
      The column name in the dataset representing a year.
  new_feature_name : str
      The name of the new column that will store the computed age.
  data : pandas.DataFrame
      The dataset containing the feature column.

  Returns:
  --------
  pandas.DataFrame
      The modified dataset with the new age feature and the original feature removed.

  Notes:
  ------
  - The function calculates age by subtracting the year values in `feature` from the current year.
  - If `feature` is not found in the dataset, it prints "Feature Not Found".
  - If `feature` is already deleted or missing, it prints "Feature already deleted".
  - Prints the new feature values and the correlation check result using `check_correlation(new_feature_name)`.
  - Assumes `check_correlation` is a predefined function that takes the new feature name as input.
  """
  current_year = datetime.date.today().year
  try:
    train_data[new_feature_name] = current_year - train_data[feature]
  except:
    print("Feature Not Found")
  try:
    train_data = train_data.drop(columns = [feature], axis=1)
  except:
    print("Feature already deleted")
  return train_data

from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

def null_imputation_preprocessing(data):
  """
  Preprocesses categorical and numerical features in the dataset by applying categorical encoding and 
  imputing missing numerical values using KNN imputation.

  Steps:
  1. Encode specific categorical features using predefined mappings.
  2. Apply label encoding to selected categorical columns.
  3. Impute missing values in numerical columns using KNN imputation.

  Parameters:
  data (pd.DataFrame): The input dataset containing missing values and categorical features.

  Returns:
  pd.DataFrame: The transformed dataset with imputed values and encoded categorical features.
  """
  # Set the future behavior option
  pd.set_option('future.no_silent_downcasting', True)

  categorical_mappings = {
    "Alley": {'Grvl': 1, 'Pave': 2},
    "PoolQC": {'Gd': 1, 'Ex': 1, 'Fa': 1},
    "Fence": {'MnPrv': 1, 'MnWw': 1, 'GdPrv': 2, 'GdWo': 2},
    "MiscFeature": {'Shed': 1, 'Gar2': 2, 'Othr': 3, 'TenC': 4},
    "MasVnrType": {'BrkCmn': 1, 'BrkFace': 2, 'CBlock': 3, 'Stone': 4},
    "BsmtExposure": {'No': 1, 'Mn': 2, 'Av': 3, 'Gd': 4},
    "GarageFinish": {'Unf': 1, 'RFn': 2, 'Fin': 3}
  }

  for column, mapping in categorical_mappings.items():
    preprocess_categorical(data, column, mapping)

  mapping = {'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
  feature_names = ["FireplaceQu", "BsmtQual", "BsmtCond", "GarageQual", "GarageCond"]
  for x in feature_names:
    preprocess_categorical(data, x, mapping)

  mapping = {'Unf': 1, 'LwQ': 2, 'Rec': 3, 'BLQ': 4, 'ALQ': 5, 'GLQ': 6}
  feature_names = ["BsmtFinType1", "BsmtFinType2"]
  for x in feature_names:
    preprocess_categorical(data, x, mapping)

  feature_names_label_encoding = ["Electrical", "GarageType"]
  label_encoder = LabelEncoder()
  
  debug = False
  encoding_results = {}

  for feature in feature_names_label_encoding:

    encoding_results[feature] = {
        "before": data[feature].value_counts(),
        "after": None
    }

    data[feature] = label_encoder.fit_transform(data[feature])
    encoding_results[feature]["after"] = data[feature].value_counts()

  if debug:
    for feature, results in encoding_results.items():
      print(f"Value Counts before encoding for {feature}:\n{results['before']}")
      print(f"Value Counts after encoding for {feature}:\n{results['after']}")

  # Impute remaining nulls using knn
  features_to_impute = ["LotFrontage", "MasVnrArea", "GarageYrBlt"]
  df_knn = data[features_to_impute]
  scaler = StandardScaler()
  df_knn_scaled = scaler.fit_transform(df_knn)
  imputer = KNNImputer(n_neighbors=5)  # Choose k based on dataset size
  df_knn_imputed = imputer.fit_transform(df_knn_scaled)
  df_knn_original = scaler.inverse_transform(df_knn_imputed)
  data[features_to_impute] = df_knn_original  # Update original dataframe
  print(data[features_to_impute].isnull().sum())

  return data


