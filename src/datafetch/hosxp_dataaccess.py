class HosxpDataAccess:
    def __init__(self, db_instance):
        self.__db_instance = db_instance

    def query_injection_by_visitdate(self, startdate, enddate):
        result_set: list = []
        stmt = '''
        SELECT CONCAT(pname, ' ', fname, ' ', lname) 'name', age, cid,
        IF(dose = 1, vaccine_name, NULL) 'vaccine_name_1', 
        IF(dose = 1, DATE(immunization_datetime), NULL) 'date_1',
        IF(dose = 1, dose, NULL) 'dose_1', 
        IF(dose = 2, vaccine_name, NULL) 'vaccine_name_2', 
        IF(dose = 2, DATE(immunization_datetime), NULL) 'date_2',
        IF(dose = 2, dose, NULL) 'dose_2' 
        FROM coquit c 
        WHERE DATE(immunization_datetime) BETWEEN %s AND %s
        && dose IN (1, 2) 
        && cid REGEXP '^[0,7-9]'
        ORDER BY cid DESC;
        '''

        with self.__db_instance as conn:
            with(conn.cursor()) as cursor:
                cursor.execute(stmt, (startdate, enddate))
                for row in cursor.fetchall():
                    # Unpack Tuples
                    (name, age, cid, vaccine_name_1, date_1, dose_1, vaccine_name_2, date_2, dose_2) = row
                    result_set.append({"name": name, "age": age, "cid": cid,
                                       "vaccine_name_1": vaccine_name_1, "date_1": date_1, "dose_1": dose_1,
                                       "vaccine_name_2": vaccine_name_2, "dose_2": dose_2, "date_2": date_2
                                       })
        return result_set
