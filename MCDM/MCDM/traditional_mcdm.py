import db_manager
import numpy
import mcdm_techniques

def top_k_finder(required_set, mcdm_technique, DECISION_MAKER_PREFERENCE):
    db_manager.create_traditional_mcdm_table(2)

    results = db_manager.read_dataset_for_traditional_mcdm()
    for records in results:
        rows = records.fetchall()
        for row in rows:
            solution_id = row[0]

            current_sensor_context_data = numpy.asarray(list(row[1:]))
            user_preferences = numpy.asarray(DECISION_MAKER_PREFERENCE[:])
            traditional_mcdm_index = mcdm_techniques.weighted_sum_model(current_sensor_context_data, user_preferences)

        
            db_manager.insert_data_to_traditional_table(solution_id, traditional_mcdm_index)

    TRADITIONAL_TOP_k = db_manager.sort_select_traditional_table(required_set)

    
    return TRADITIONAL_TOP_k