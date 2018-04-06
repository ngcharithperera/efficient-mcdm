
import db_manager
import numpy
import mcdm_techniques
import util

def top_k_finder(required_set, mcdm_technique, DECISION_MAKER_PREFERENCE,combination,TO_REMOVE, total_number_of_criteria, total_solution_space):
    db_manager.create_heuristic_mcdm_table(2)
    
    #TO_REMOVE_LIST = [i * TO_REMOVE for i in DECISION_MAKER_PREFERENCE]
    TO_REMOVE_LIST_ROUND =  combination
    #TO_REMOVE_LIST_ROUND = [total_solution_space - i for i in TO_REMOVE_LIST_ROUND]

    #sql_tuple = util.heuristic_sql_creator(TO_REMOVE_LIST_ROUND)

    HEURISTIC_TOP_k = []
    CPHF_sql = db_manager.prepare_bruteforce_sql(TO_REMOVE_LIST_ROUND, total_number_of_criteria,total_solution_space)
    results = db_manager.read_dataset_for_heuristic_mcdm(CPHF_sql)
    for records in results:
        rows = records.fetchall()
        for row in rows:
            solution_id = row[0]

            current_sensor_context_data = numpy.asarray(list(row[1:]))
            user_preferences = numpy.asarray(DECISION_MAKER_PREFERENCE[:])
            heuristic_mcdm_index = mcdm_techniques.weighted_sum_model(current_sensor_context_data, user_preferences)

        
            db_manager.insert_data_to_heuristic_table(solution_id, heuristic_mcdm_index)

    BRUTEFORCE_HEURISTIC_TOP_k = db_manager.sort_select_heuristic_table(required_set)


    return BRUTEFORCE_HEURISTIC_TOP_k


def accuracy(TRADITIONAL_TOP_k, HEURISTIC_TOP_k):
    return (100.0 * len(set(TRADITIONAL_TOP_k) & set(HEURISTIC_TOP_k))) / len(set(TRADITIONAL_TOP_k))
