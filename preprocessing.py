

def check_null_population(minimum_percentage, data):
  """
  check which features have a population of nulls greater than 80%

  Returns a null_dict of items over 
  """
  null_dict = {}
  for feature in data:
    number_of_nulls = data[feature].isnull().sum()
    number_of_values = data[feature].count().sum()
    number_total = number_of_nulls + number_of_values
    null_percentage = number_of_nulls / number_total
    if null_percentage > minimum_percentage:
      null_dict[feature] = {"number": number_of_nulls,
                            "percentage": null_percentage}

  for x in null_dict:
    print(f"feature {x} has {null_dict[x]['number']} nulls, which is a percentage of {(null_dict[x]['percentage']*100).round(2)}%")

  return null_dict

