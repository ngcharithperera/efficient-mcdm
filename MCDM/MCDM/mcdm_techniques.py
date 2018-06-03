def weighted_sum_model(current_sensor_context_data, user_preferences):
  return sum([x*y for x,y in zip(current_sensor_context_data, user_preferences)])
  
def weighted_product_model(current_sensor_context_data, user_preferences):
  x = numpy.prod(numpy.asarray([x**y for x,y in zip(current_sensor_context_data, user_preferences)]))
  return x