import pandas as pd

def displayObjectFeatures(feature_names: pd.Series, train_data: pd.DataFrame, columns, singlefigsize: tuple[int, int]):
  """
  Displays bar charts for categorical (object-type) features in a given DataFrame.

    This function selects all object-type (categorical) columns from the provided DataFrame
    and generates bar plots to visualize their frequency distributions. The plots are arranged
    in a grid layout based on the specified number of columns and figure size.

    Parameters:
    ----------
    train_data : pd.DataFrame
        The input DataFrame containing features, including categorical (object-type) features.
    columns : int
        The number of columns to arrange the subplots in the figure.
    singlefigsize : tuple[int, int]
        The single figure size (width, height) for the total matplotlib figure.

  Raises:
    ------
    ValueError
        If the number of categorical features is less than the required grid size.
    IndexError
        If accessing an invalid column index due to incorrect row/column calculation.

    Example:
    -------
    >>> import pandas as pd
    >>> import matplotlib.pyplot as plt
    >>> data = pd.DataFrame({"Category": ["A", "B", "A", "C", "B", "C", "A"],
                             "Type": ["X", "Y", "X", "Z", "Y", "Z", "X"],
                             "Value": [10, 20, 10, 30, 20, 30, 10]})
    >>> displayObjectFeatures(data, columns=2, figsize=(10, 5))
  """
  filtered_train_data = train_data[feature_names.index]
  train_data_objects = filtered_train_data.select_dtypes(include="object")
  train_data_object_columns = train_data_objects.columns

  no_features = len(train_data_object_columns)

  if not isinstance(columns, int) or columns <= 0:
    raise ValueError("Parameter 'columns' must be a positive integer.")

  number_of_columns = min(no_features, int(columns))
  number_of_rows = max(1, -(-no_features // number_of_columns)) #Ceil Division Equivalent

  import matplotlib.pyplot as plt
  total_figsize = [singlefigsize[0] * number_of_columns, singlefigsize[1] * number_of_rows]
  print(total_figsize)
  fig, axes = plt.subplots(number_of_rows, number_of_columns, sharex=False, sharey=False, squeeze=False, figsize=total_figsize)

  feature_index = 0
  for row in range(number_of_rows):
    for col in range(number_of_columns):
      if feature_index >= no_features:
        break
      current_feature = train_data_object_columns[feature_index]
      feature_index += 1

      #print(current_feature)
      feature = train_data[current_feature].value_counts()
      chart = axes[row, col]
      chart.set_title(feature.index.name)
      chart.bar(feature.index, feature.values)



