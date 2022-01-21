import os
import pandas as pd
from helper import helper

class GroupFilter():
    __min_dose = 1
    __max_dose = 4

    def __init__(self):
        pass

    def __init__(self, filepath):
        self.__df = None
        self.__result_set = []
        self.readSpreadSheet(filepath)

    def readSpreadSheet(self, filepath):
        try:
            _, file_extension = os.path.splitext(filepath)
            if(file_extension == '.xlsx' or file_extension == '.xls'):
                self.__df = pd.read_excel(filepath)
            elif(file_extension == '.csv'):
                self.__df = pd.read_csv(filepath)
            else:
                raise Exception('Unknown File Extension')
        except:
            raise Exception('Something going on about your file')

    def filter_vaccine_group(self):
        filter_list = helper.read_config()
        self.__min_dose = filter_list['min_dose']
        self.__max_dose = filter_list['max_dose']
        vac_types = self.collectVaccineType()

        for vac_name in vac_types:
            index = len(self.__result_set)
            self.__result_set.append({"vaccine": vac_name, "data": {}})

            for main_key in filter_list['type']:
                if(main_key in filter_list['sub_type']):
                    for sub_key in filter_list['sub_type'][main_key]:
                        self.__result_set[index]["data"][sub_key] = []
                        for dose in range(self.__min_dose, self.__max_dose+1):
                            count = len(self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['vaccine_ref_name'] == vac_name) & (self.__df['person_risk_type_name'] == sub_key) & (self.__df['vaccine_plan_no'] == dose)])
                            if(sub_key == 'ประชาชนทั่วไป'):
                                #Recently Adjusted
                                count += len(self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['vaccine_ref_name'] == vac_name) &(self.__df['person_risk_type_name'].isnull()) & (self.__df['vaccine_plan_no'] == dose)])
                            self.__result_set[index]["data"][sub_key].append(count)
                else:
                    self.__result_set[index]["data"][main_key] = []
                    for dose in range(self.__min_dose, self.__max_dose+1):
                        count = len(self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['vaccine_ref_name'] == vac_name) & (self.__df['vaccine_plan_no'] == dose)])
                        self.__result_set[index]["data"][main_key].append(count) 

    def collectVaccineType(self):
        return self.__df["vaccine_ref_name"].drop_duplicates().sort_values().tolist()

    def map_vac_with_alias(self, vac_types, vac_alias):
        try:
            vac_alias_dict = {}
            for vac_name in vac_types:
                vac_alias_dict[vac_name] = vac_alias[vac_name]
            return vac_alias_dict
        except:
            raise Exception("No vaccine alias in current config list. Please update vaccine list in your config file.")
            

    def export_tabular_df(self):
            group_count = len(self.__result_set[0]["data"])
            cols = []
            rows = [[] for _ in range(0, group_count)]
            indexes = []
            row_index = 0
            vac_types = self.collectVaccineType()
            filter_list = helper.read_config()
            vac_alias = self.map_vac_with_alias(vac_types, filter_list["vaccine_alias"])
            #Append Dose as Dataframe Columns
            for dataset in self.__result_set:
                for dose_no in range(self.__min_dose, self.__max_dose+1):
                    cols.append(vac_alias[dataset["vaccine"]] + " Dose " + str(dose_no))

                for person_key in dataset["data"]:
                    for x in dataset["data"][person_key]:
                        rows[row_index].append(x)
                    row_index += 1
                row_index = 0

            for key in self.__result_set[0]["data"]:
                indexes.append(key)
            df = pd.DataFrame(rows, columns=cols, index=indexes)
            return df