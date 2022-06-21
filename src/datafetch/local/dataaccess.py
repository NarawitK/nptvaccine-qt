from model.datamodel.apiresponse import HOSXPCovidResponse

class HOSXPDataAccess:
    def __init__(self, dbFactory):
        self.__dbFactory = dbFactory

    def SelectCovidDataByVisitDate(self, visitdate):
        with(self.__dbFactory.getInstance()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT q.immunization_datetime, q.hn, q.cid, q.vaccine_name, q.dose FROM coquit q '
                'WHERE DATE(q.immunization_datetime) = {};'.format(visitdate))
            result_set = self.__CovidDataToHOSXPResponseList(cursor)
            cursor.close()
            return result_set

    def __CovidDataToHOSXPResponseList(self, cursor):
        result_set = []
        for (immunization_datetime, hn, cid, vaccine_name, dose) in cursor:
            result_set.append(HOSXPCovidResponse(immunization_datetime, hn, cid, vaccine_name, dose))
        return result_set
