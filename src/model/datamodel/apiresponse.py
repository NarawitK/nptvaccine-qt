class HOSXPCovidResponse:

    def __init__(self):
        self.__immunization_datetime = None
        self.__hn = None
        self.__cid = None
        self.__vaccine_name = None
        self.__dose = None

    def __init__(self, immunization_datetime, hn, cid, vaccine_name, dose):
        self.__immunization_datetime = immunization_datetime
        self.__hn = hn
        self.__cid = cid
        self.__vaccine_name = vaccine_name
        self.__dose = dose
    
    @property
    def immunization_datetime(self):
        return self.__immunization_datetime

    @property
    def hn(self):
        return self.__hn

    @property
    def cid(self):
        return self.__cid

    @property
    def vaccine_name(self):
        return self.__vaccine_name

    @property
    def dose(self):
        return self.__dose

    @immunization_datetime.setter
    def visitdate(self, value):
        self.__immunization_datetime = value

    @hn.setter
    def hn(self, value):
        self.__hn = value

    @cid.setter
    def cid(self, value):
        self.__cid = value

    @vaccine_name.setter
    def vaccine_name(self, value):
        self.__vaccine_name = value

    @dose.setter
    def dose(self, value):
        self.__dose = value


class MOPHICResponse:
    def __init__(self):
        self.__hash_cid = None
        self.__fullname = None
        self.__vaccine_manufacture_id = None
        self.__vaccine_name = None
        self.__vaccine_plan_no = None
        self.__person_main_type = None
        self.__person_sub_type = None

    @property
    def hash_cid(self):
        return self.__hash_cid

    @property
    def fullname(self):
        return self.__fullname

    @property
    def vaccine_manufacture_id(self):
        return self.__vaccine_manufacture_id
    
    @property
    def vaccine_name(self):
        return self.__vaccine_name

    @property
    def vaccine_plan_no(self):
        return self.__vaccine_plan_no
    
    @property
    def person_main_type(self):
        return self.__person_main_type
    
    @property
    def person_sub_type(self):
        return self.__person_sub_type

    @hash_cid.setter
    def hash_cid(self, value):
        self.__hash_cid = value

    @fullname.setter
    def fullname(self, value):
        self.__fullname = value
    
    @vaccine_manufacture_id.setter
    def vaccine_manufacture_id(self, value):
        self.__vaccine_manufacture_id = value

    @vaccine_name.setter
    def vaccine_name(self, value):
        self.__vaccine_name = value

    @vaccine_plan_no.setter
    def vaccine_plan_no(self, value):
        self.vaccine_plan_no = value

    @person_main_type.setter
    def person_main_type(self, value):
        self.__person_main_type = value

    @person_sub_type.setter
    def person_sub_type(self, value):
        self.__person_sub_type = value
