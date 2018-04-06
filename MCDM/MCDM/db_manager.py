import mysql
import random
import logging
import scipy
import util
from mysql import connector
from mysql.connector import cursor
import numpy as np
import pandas as pd
#from scipy.lib.six import xrange

#Setting Database Configuration Parameters
USER_NAME = 'root'
PASSWORD = '123asdASD'

#Table names
SOLUTION_SPACE_DATA_TABLE = 'solutionspacedata'
RESULTS_TABLE_FULL = 'results_full'
RESULTS_TABLE_TRADITIONAL_HEURISTIC = 'results_traditional_heuristic'
RESULTS_TABLE_BRUTEFORCE_HEURISTIC = 'results_bruteforce_heuristic'
VIRTUAL_SENSOR_DATA_TABLE = 'virtualsensordata'
TRADITIONAL_MCDM_TABLE = 'Traditional_MCDM_TABLE'
HEURISTIC_MCDM_TABLE = 'Heuristic_MCDM_TABLE'

#Table IDs
SOLUTION_SPACE_DATA_TABLE_ID = "sid"
RESULTS_ID_FULL = "rfid"
RESULTS_ID_SUMMARY = "rsid"

#Database names
DB_NAME = 'TESTDATA'
RESULTS_DB_NAME = 'RESULTS'
BRUTEFORCE_RESULTS_DB_NAME = 'BRUTEFORCERESULTS'

TEMP_DB_NAME = 'TEMP'


def create_bruteforce_heuristic_results_table():
    full_sql = "CREATE TABLE results.results_traditional_heuristic ( results_id INT NOT NULL AUTO_INCREMENT, total_number_of_criteria BIGINT NULL, total_solution_space BIGINT NULL, required_set BIGINT NULL, required_set_percentage FLOAT NULL, mcdm_technique BIGINT NULL, margine BIGINT NULL, margine_percentage FLOAT NULL, dataset_id BIGINT NULL, decision_id BIGINT NULL, preference_weight_1 FLOAT NULL, preference_weight_2 FLOAT NULL, preference_weight_3 FLOAT NULL, accuracy FLOAT NULL, PRIMARY KEY (results_id)); "
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + BRUTEFORCE_RESULTS_DB_NAME+"."+RESULTS_TABLE_BRUTEFORCE_HEURISTIC + ";")
        cursor.execute(full_sql)
        logging.debug(full_sql)
    except connector.Error as err:
        print(err)

def create_traditional_heuristic_results_table():
    full_sql = "CREATE TABLE results.results_traditional_heuristic ( results_id INT NOT NULL AUTO_INCREMENT, total_number_of_criteria BIGINT NULL, total_solution_space BIGINT NULL, required_set BIGINT NULL, required_set_percentage FLOAT NULL, mcdm_technique BIGINT NULL, margine BIGINT NULL, margine_percentage FLOAT NULL, dataset_id BIGINT NULL, decision_id BIGINT NULL, preference_weight_1 FLOAT NULL, preference_weight_2 FLOAT NULL, preference_weight_3 FLOAT NULL, accuracy FLOAT NULL, PRIMARY KEY (results_id)); "
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + RESULTS_DB_NAME+"."+RESULTS_TABLE_TRADITIONAL_HEURISTIC + ";")
        cursor.execute(full_sql)
        logging.debug(full_sql)
    except connector.Error as err:
        print(err)


#====Create the Results Database=====
def create_results_database():
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(RESULTS_DB_NAME))
    except connector.Error as err:
        print("Failed creating database: {}".format(err))

#====Create the Database=====
def create_database():
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except connector.Error as err:
        print("Failed creating database: {}".format(err))


#====Create the Dataset Table=====
def create_dataset_table(total_number_of_criteria):
    #print("create_tables_for_simulated_sensor_data")
    full_sql = prepare_create_table_sql(total_number_of_criteria, DB_NAME, SOLUTION_SPACE_DATA_TABLE,
                                        SOLUTION_SPACE_DATA_TABLE_ID)
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + DB_NAME+"."+SOLUTION_SPACE_DATA_TABLE + ";")
        cursor.execute(full_sql)
        logging.debug(full_sql)
    except connector.Error as err:
        print(err)



#====Create the Dataset Table Generation SQL=====
def prepare_create_table_sql(number_of_context_properties, database_name, table_name, id_column):
    start = id_column + " BIGINT NOT NULL ,"
    end = "PRIMARY KEY (" + id_column + ")"
    mid = ""
    for ithCP in range(1, number_of_context_properties + 1):
        mid = mid + "CP" + str(ithCP) + " DOUBLE NULL , "
    table_definition = start + mid + end
    sql_create_table_main = "CREATE  TABLE IF NOT EXISTS " + database_name + "." + table_name + \
                            " ( " + table_definition + " )"
    full_sql = sql_create_table_main
    return full_sql


#====Create Each Data Record=====
def create_dataset(number_of_context_properties, total_number_of_sensors):
    logging.debug("prepare_simulated_sensor_data_set")
    for sensor_id in range(total_number_of_sensors):
        sensor_data_record = np.random.sample(number_of_context_properties)
        store_data(sensor_id, sensor_data_record, 'sensor_data')


def store_data(row_id, data, table_type):
    # logging.debug("store_data")
    if table_type is 'sensor_data':
        insert_data_to_db(row_id, data, DB_NAME, SOLUTION_SPACE_DATA_TABLE)
    elif 'user_requests_' in table_type:
        insert_data_to_db(row_id, data, DB_NAME, table_type)
    elif 'brute_force_' in table_type:
        insert_data_to_db(row_id, data, TEMP_DB_NAME,  table_type)
    elif 'dcphf_' in table_type:
        insert_data_to_db(row_id, data, TEMP_DB_NAME,  table_type)
    elif 'results_' in table_type:
        insert_data_to_db(row_id, data, RESULTS_DB_NAME,  table_type)
    else:
        logging.debug("something wrong..")

def insert_data_to_traditional_heuristic_results_table(total_number_of_criteria, total_solution_space, required_set, required_set_percentage, mcdm_technique, margine , margine_percentage , dataset_id , decision_id, preference_weight_1 , preference_weight_2 , accuracy):

    sql = "INSERT INTO "+ RESULTS_DB_NAME + "." + RESULTS_TABLE_TRADITIONAL_HEURISTIC +" (total_number_of_criteria, total_solution_space, required_set, required_set_percentage, mcdm_technique, margine , margine_percentage, dataset_id , decision_id , preference_weight_1 , preference_weight_2 , accuracy ) VALUES ("+ str(total_number_of_criteria)+","+ str(total_solution_space)+","+ str(required_set)+","+ str(required_set_percentage)+","+ str(mcdm_technique)+","+ str(margine) +","+ str(margine_percentage)+","+ str(dataset_id) +","+ str(decision_id) +","+ str(preference_weight_1)+","+ str(preference_weight_2) +","+ str(accuracy)+");"
    db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
    cursor = db_connection.cursor()
    cursor.execute(sql)
    db_connection.commit()

def insert_data_to_db(id, data, db_name, table_name):
    # logging.debug("insert_data_to_db")
    values = ''
    # if type(data) is not 'float':
    for ith_data_item in data:
        values = values + ", " + str(ith_data_item)
    # else:
    #     values = values + ", " + str(data)
    sql = "INSERT INTO " + db_name + "." + table_name + " VALUES(" + str(id) + values + ")"
    db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
    cursor = db_connection.cursor()
    cursor.execute(sql)
    db_connection.commit()


#====Create the Traditional MCDM Table=====
def create_traditional_mcdm_table(total_number_of_criteria):
    full_sql = prepare_create_traditional_mcdm_table_sql(total_number_of_criteria, DB_NAME, TRADITIONAL_MCDM_TABLE,
                                        SOLUTION_SPACE_DATA_TABLE_ID)
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + DB_NAME+"."+TRADITIONAL_MCDM_TABLE + ";")
        cursor.execute(full_sql)
        logging.debug(full_sql)
    except connector.Error as err:
        print(err)


#====Create the Traditional MCDM Table Generation SQL=====
def prepare_create_traditional_mcdm_table_sql(number_of_context_properties, database_name, table_name, id_column):
    start = id_column + " BIGINT NOT NULL ,"
    #end = "PRIMARY KEY (" + id_column + ")"
    mid =  "traditional_mcdm_index" + " DOUBLE NULL  "
    table_definition = start + mid
    sql_create_table_main = "CREATE  TABLE IF NOT EXISTS " + database_name + "." + table_name + \
                            " ( " + table_definition + " )"
    full_sql = sql_create_table_main
    return full_sql


def read_dataset_for_traditional_mcdm():
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD)
        cursor = db_connection.cursor()
        #sql =  + ""
        results = cursor.execute("SELECT * FROM " + DB_NAME+"."+SOLUTION_SPACE_DATA_TABLE, multi=True)
        #rows = cursor.fetchall()
        #db_connection.commit()
        return results
    except connector.Error as err:
        print(err)
    

def insert_data_to_traditional_table(id, traditional_mcdm_index):
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        sql = "INSERT INTO " + DB_NAME + "." + TRADITIONAL_MCDM_TABLE + " VALUES(" + str(id) + ","+str(traditional_mcdm_index) + ")"
        cursor.execute(sql)
        db_connection.commit()
    except connector.Error as err:
        print(err)


def sort_select_traditional_table(required_set):
    try:
        TRADITIONAL_TOP_k = []
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD)
        cursor = db_connection.cursor()
        #SELECT sid FROM testdata.traditional_mcdm_table ORDER BY traditional_mcdm_index DESC limit 5;
        sql = "SELECT * FROM " + DB_NAME + "." + TRADITIONAL_MCDM_TABLE + " ORDER BY traditional_mcdm_index DESC limit " + str(required_set) + ";"
        results = cursor.execute(sql, multi=True)
        for records in results:
            rows = records.fetchall()
            for row in rows:
                solution_id = row[0]
                TRADITIONAL_TOP_k.append(solution_id)
                #print(solution_id)
        return TRADITIONAL_TOP_k
    except connector.Error as err:
        print(err)




#====Create the Heuristic MCDM Table=====
def create_heuristic_mcdm_table(total_number_of_criteria):
    full_sql = prepare_create_heuristic_mcdm_table_sql(total_number_of_criteria, DB_NAME, HEURISTIC_MCDM_TABLE,
                                        SOLUTION_SPACE_DATA_TABLE_ID)
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + DB_NAME+"."+ HEURISTIC_MCDM_TABLE + ";")
        cursor.execute(full_sql)
        logging.debug(full_sql)
    except connector.Error as err:
        print(err)


#====Create the Heuristic MCDM Table Generation SQL=====
def prepare_create_heuristic_mcdm_table_sql(number_of_context_properties, database_name, table_name, id_column):
    start = id_column + " BIGINT NOT NULL ,"
    #end = "PRIMARY KEY (" + id_column + ")"
    mid =  "heuristic_mcdm_index" + " DOUBLE NULL  "
    table_definition = start + mid
    sql_create_table_main = "CREATE  TABLE IF NOT EXISTS " + database_name + "." + table_name + \
                            " ( " + table_definition + " )"
    full_sql = sql_create_table_main
    return full_sql


def read_dataset_for_heuristic_mcdm(CPHF_sql):
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD)
        cursor = db_connection.cursor()
        #sql =  + ""
        results = cursor.execute(CPHF_sql, multi=True)
        #rows = cursor.fetchall()
        #db_connection.commit()
        return results
    except connector.Error as err:
        print(err)



def insert_data_to_heuristic_table(id, heuristic_mcdm_index):
    try:
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
        cursor = db_connection.cursor()
        sql = "INSERT INTO " + DB_NAME + "." + HEURISTIC_MCDM_TABLE + " VALUES(" + str(id) + ","+str(heuristic_mcdm_index) + ")"
        cursor.execute(sql)
        db_connection.commit()
    except connector.Error as err:
        print(err)

def describe_table():
    db_connection = connector.connect(user=USER_NAME, password=PASSWORD, autocommit=True)
    sql = 'SELECT * FROM ' + DB_NAME +"."+ SOLUTION_SPACE_DATA_TABLE
    df = pd.read_sql(sql, con=db_connection)
    table_description = np.round(df.describe(), 2).T
    print(table_description)
    return table_description


def sort_select_heuristic_table(required_set):
    try:
        HEURISTIC_TOP_k = []
        db_connection = connector.connect(user=USER_NAME, password=PASSWORD)
        cursor = db_connection.cursor()
        #SELECT sid FROM testdata.traditional_mcdm_table ORDER BY traditional_mcdm_index DESC limit 5;
        sql = "SELECT * FROM " + DB_NAME + "." + HEURISTIC_MCDM_TABLE + " ORDER BY heuristic_mcdm_index DESC limit " + str(required_set) + ";"
        results = cursor.execute(sql, multi=True)
        for records in results:
            rows = records.fetchall()
            for row in rows:
                solution_id = row[0]
                HEURISTIC_TOP_k.append(solution_id)
                #print(solution_id)
        return HEURISTIC_TOP_k
    except connector.Error as err:
        print(err)


def prepare_CPHF_sql(TO_REMOVE_LIST_ROUND, total_number_of_criteria, total_solution_space):
    criteria_list = util.heuristic_sql_creator(TO_REMOVE_LIST_ROUND)
    criteria_list_ordered = util.order_removal_list(criteria_list)

    if total_number_of_criteria == 2:

        highest_removal = total_solution_space - criteria_list_ordered[1][1]
        total_solution_space = total_solution_space - criteria_list_ordered[1][1]
        lowest_removal = total_solution_space - criteria_list_ordered[0][1]

        sql_2_criteria = " SELECT *  FROM ( SELECT * FROM " +\
        DB_NAME+"."+ SOLUTION_SPACE_DATA_TABLE   + \
        " ORDER BY " + 	SOLUTION_SPACE_DATA_TABLE +"." + criteria_list_ordered[1][0] +   " DESC LIMIT " + str(highest_removal) + ")" + \
        SOLUTION_SPACE_DATA_TABLE + " ORDER BY "	+ SOLUTION_SPACE_DATA_TABLE +"." + criteria_list_ordered[0][0] + " DESC LIMIT " + str(lowest_removal)
        CPHF_sql = sql_2_criteria

    elif total_number_of_criteria == 3:

        highest_removal = total_solution_space - criteria_list_ordered[2][1]
        total_solution_space = total_solution_space - criteria_list_ordered[2][1]
        mid_removal = total_solution_space - criteria_list_ordered[1][1]
        total_solution_space = total_solution_space - criteria_list_ordered[1][1]
        lowest_removal = total_solution_space - criteria_list_ordered[0][1]

        sql_3_criteria = " SELECT * " + \
        " FROM ( SELECT * FROM ( SELECT * FROM " + \
	    DB_NAME +"."+ SOLUTION_SPACE_DATA_TABLE + \
        " ORDER BY " +\
	    SOLUTION_SPACE_DATA_TABLE +"." + criteria_list_ordered[2][0] + " DESC LIMIT " + str(highest_removal) + ")" + \
        SOLUTION_SPACE_DATA_TABLE + \
        " ORDER BY " + \
	    SOLUTION_SPACE_DATA_TABLE +"." + criteria_list_ordered[1][0] +   " DESC LIMIT " + str(mid_removal)  + ")"+ \
        SOLUTION_SPACE_DATA_TABLE + \
        " ORDER BY " + \
	    SOLUTION_SPACE_DATA_TABLE +"." + criteria_list_ordered[0][0] + " DESC LIMIT " + str(lowest_removal) 


        CPHF_sql = sql_3_criteria
    else:
        CPHF_sql = ""
    return CPHF_sql





#def mysql():
#    sql_2_criteria = "SELECT `solutionspacedata`.`sid` FROM	("+
#                            " SELECT * FROM	`testdata`.`solutionspacedata` `solutionspacedata`" +
#                            " ORDER BY 	`solutionspacedata`.`CP1` DESC LIMIT 8)"+
#                     "`solutionspacedata` ORDER BY	`solutionspacedata`.`CP2` DESC LIMIT 2"

#    sql_3_criteria = " SELECT " +
#	                 " `solutionspacedata`.`sid`" +
#                     " FROM ("+
#                        " SELECT * FROM (" +
#                                " SELECT * FROM " +
#	                            " `testdata`.`solutionspacedata` `solutionspacedata` " +
#                                " ORDER BY " +
#	                            " `solutionspacedata`.`CP1` DESC LIMIT 8)"+
#                            " `solutionspacedata` " +
#                            " ORDER BY " +
#	                        " `solutionspacedata`.`CP1` DESC LIMIT 5)"+
#                        " `solutionspacedata`" +
#                     " ORDER BY " +
#	                 " `solutionspacedata`.`CP2` DESC LIMIT 3 "

#create_database("Teting2")