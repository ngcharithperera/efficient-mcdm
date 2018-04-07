#====Imports=====
import db_manager
import util
import traditional_mcdm
import heuristic_mcdm
import bruteforce_heuristic_mcdm
import numpy as np




#====Configuration Settings=====
TOTAL_NUMBER_OF_CRITERIA = [3]
TOTAL_SOLUTION_SPACE = [10]
MCDM_TECHNIQUE = [1]
NUMBER_OF_DATASETS = 10
TOTAL_DECISION_MAKER_PREFERENCES = 10
#REMOVAL_COMBINATION = [[1,7],[3,6],[5,5]]




#====Database Creation======
#====create two databases: (1) store Temp data (2) store results
db_manager.create_database()
#db_manager.create_results_database()
#db_manager.create_traditional_heuristic_results_table()
#db_manager.create_bruteforce_heuristic_results_table()




#====Experiment Design=====
for total_number_of_criteria in TOTAL_NUMBER_OF_CRITERIA:
# Factor 1 (total_number_of_criteria)
 
  for total_solution_space in TOTAL_SOLUTION_SPACE:
  # Factor 2 (total_solution_space)  

    for required_set in util.required_set_generator(total_solution_space):       
      required_set_percentage = (required_set / total_solution_space)
      # Factor 3 (required_set)

      for mcdm_technique in MCDM_TECHNIQUE:          
      # Factor * (mcdm_technique)  

        for margine in util.margin_generator(total_solution_space, required_set):          
          margine_percentage = (margine / required_set) 
          TO_REMOVE = util.removal_tracker(total_solution_space, required_set, margine)
          # Factor 4 (margine)
          
          for dataset_id in  range(1, NUMBER_OF_DATASETS):            
            db_manager.create_dataset_table(total_number_of_criteria)
            db_manager.create_dataset(total_number_of_criteria,total_solution_space)
            table_description = db_manager.describe_table()            
            table_description_sql = util.create_table_description_sql(total_number_of_criteria, table_description)
            
            for decision_id in range(1, TOTAL_DECISION_MAKER_PREFERENCES):
              DECISION_MAKER_PREFERENCE = util.generate_prefernce(total_number_of_criteria)
              preference_weight_1 = DECISION_MAKER_PREFERENCE[0]
              preference_weight_2 = DECISION_MAKER_PREFERENCE[1]
              TRADITIONAL_TOP_k = []
              TRADITIONAL_TOP_k = traditional_mcdm.top_k_finder(required_set, mcdm_technique, DECISION_MAKER_PREFERENCE)
              HEURISTIC_TOP_k = []
              HEURISTIC_TOP_k  = heuristic_mcdm.top_k_finder(required_set, mcdm_technique, DECISION_MAKER_PREFERENCE,TO_REMOVE, total_number_of_criteria, total_solution_space)              
              accuracy = heuristic_mcdm.accuracy(TRADITIONAL_TOP_k, HEURISTIC_TOP_k)
              if total_number_of_criteria < 3:
                preference_weight_3 = "NULL"
              if total_number_of_criteria >= 3:
                preference_weight_3 = DECISION_MAKER_PREFERENCE[2]
                
              db_manager.insert_data_to_traditional_heuristic_results_table(total_number_of_criteria, total_solution_space, required_set, required_set_percentage, mcdm_technique, margine , margine_percentage , dataset_id , decision_id, preference_weight_1 , preference_weight_2, preference_weight_3 , accuracy) 
              filtering_combinations = np.asarray(list(util.generate_all_combinations(total_number_of_criteria,TO_REMOVE)))
              for combination in filtering_combinations:
                  CP1_removal = CP2_removal = CP3_removal = "NULL"
                  CP1_removal = combination[0]
                  CP2_removal = combination[1]
                  if total_number_of_criteria > 2:
                    CP3_removal = combination[2]
                  BRUTEFORCE_HEURISTIC_TOP_k = bruteforce_heuristic_mcdm.top_k_finder(required_set, mcdm_technique, DECISION_MAKER_PREFERENCE, combination,TO_REMOVE, total_number_of_criteria, total_solution_space)
                  accuracy_bruteforce = bruteforce_heuristic_mcdm.accuracy(TRADITIONAL_TOP_k, BRUTEFORCE_HEURISTIC_TOP_k)
                  all_top_k = "TRADITIONAL: " + str(TRADITIONAL_TOP_k) + " : " + "HEURISTIC: " + str(HEURISTIC_TOP_k) + " : " + "BRUTEFORCE_HEURISTIC: " + str(BRUTEFORCE_HEURISTIC_TOP_k)
                  
                  db_manager.insert_data_to_bruteforce_heuristic_results_table(total_number_of_criteria, total_solution_space, required_set, required_set_percentage, mcdm_technique, margine , margine_percentage , dataset_id , decision_id, preference_weight_1 , preference_weight_2 , preference_weight_3, accuracy, accuracy_bruteforce, CP1_removal, CP2_removal, CP3_removal, all_top_k, table_description_sql ) 
     
              
            
            
            
            
    