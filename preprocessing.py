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
