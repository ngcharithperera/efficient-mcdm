
from operator import itemgetter


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