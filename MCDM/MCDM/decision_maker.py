import random

def generate_prefernce(total_number_of_criteria):
  list = []
  
  for i in range(0,total_number_of_criteria):
    x = random.randint(1,10)
    list.append(x)
    normalized_list = [float(i)/sum(list) for i in list]
    #print(normalized_list)
  return normalized_list
  