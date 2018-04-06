
from operator import itemgetter
import numpy as np# learn more: https://python.org/pypi/numpy
import pandas as pd

def required_set_generator(total_solution_space):
  if total_solution_space <= 10:
    REQUIRED_SET = list(range(1, total_solution_space))
    #print(REQUIRED_SET)
  return REQUIRED_SET
  
  
def margin_generator(total_solution_space, required_set):
  if total_solution_space <= 10:
    MARGINE = list(range(0, (total_solution_space - required_set) + 1))
    #print(MARGINE)
  return MARGINE
  
  
def removal_tracker(total_solution_space, required_set, margine):
  to_remove = total_solution_space - (required_set + margine)
  return to_remove

def heuristic_sql_creator(TO_REMOVE_LIST_ROUND):
    i = 0
    sql_tuple = []
    for x in TO_REMOVE_LIST_ROUND:
        i = i + 1
        criteria = 'CP'+ str(i) 
        x = [criteria, x]
        sql_tuple.append(x)
    return sql_tuple

def order_removal_list(criteria_list):
    criteria_list =sorted(criteria_list, key=lambda student: student[1]) 
    return criteria_list



def generate_all_combinations(total_number_of_criteria,TO_REMOVE):
  n = total_number_of_criteria
  total = TO_REMOVE
  if n == 1:
      yield (total,)
  else:
    for i in range(total + 1):
      for j in generate_all_combinations(n - 1,total - i):
        yield (i,) + j


def create_table_description_sql(total_number_of_criteria, table_description):
    table_description_sql = ""
    CP1_mean = table_description.loc["CP1", "mean"]
    CP1_std = table_description.loc["CP1", "std"]
    CP1_min = table_description.loc["CP1", "min"]
    CP1_25 = table_description.loc["CP1", "25%"]
    CP1_50 = table_description.loc["CP1", "50%"]
    CP1_75 = table_description.loc["CP1", "75%"]
    CP1_max = table_description.loc["CP1", "max"]

    CP2_mean = table_description.loc["CP2", "mean"]
    CP2_std = table_description.loc["CP2", "std"]
    CP2_min = table_description.loc["CP2", "min"]
    CP2_25 = table_description.loc["CP2", "25%"]
    CP2_50 = table_description.loc["CP2", "50%"]
    CP2_75 = table_description.loc["CP2", "75%"]
    CP2_max = table_description.loc["CP2", "max"]
    if total_number_of_criteria > 2:
        CP3_mean = table_description.loc["CP3", "mean"]
        CP3_std = table_description.loc["CP3", "std"]
        CP3_min = table_description.loc["CP3", "min"]
        CP3_25 = table_description.loc["CP3", "25%"]
        CP3_50 = table_description.loc["CP3", "50%"]
        CP3_75 = table_description.loc["CP3", "75%"]
        CP3_max = table_description.loc["CP3", "max"]
    return table_description_sql