def weighted_sum_model(current_sensor_context_data, user_preferences):
  return sum([x*y for x,y in zip(current_sensor_context_data, user_preferences)])
  
def weighted_product_model():
  x = 0
  return x