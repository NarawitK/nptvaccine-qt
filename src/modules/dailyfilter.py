import json
import os
from helper import helper
import pandas as pd

class DailyFilter():
    __df = None
    __result_set = {}
    __min_dose = 1
    __max_dose = 4

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

    def checkdatecount(self):
        dataframe = self.__df
        dataframe['immunization_date'] = dataframe['immunization_datetime'].astype('datetime64[ns]').dt.date
        date_count = len(dataframe['immunization_date'].drop_duplicates())
        print(date_count)
        if(date_count == 1):
            return True
        elif(date_count > 1):
            raise Exception("ในไฟล์ต้นฉบับมีวันที่ฉีดมากกว่า 1 วัน")
        else:
            raise Exception("ในไฟล์ต้นฉบับไม่มีวันที่ฉีดเลย")

    def prepareData(self):
        filter_list = helper.read_config()
        self.__min_dose = filter_list['min_dose']
        self.__max_dose = filter_list['max_dose']
        for main_key in filter_list['type']:
            if(main_key in filter_list['sub_type']):
                for sub_key in filter_list['sub_type'][main_key]:
                    self.__result_set[sub_key] = []
                    for dose in range(self.__min_dose, self.__max_dose+1):
                        count = len(self.__df[(self.__df['person_type_name'] == main_key)& (self.__df['person_risk_type_name'] == sub_key) & (self.__df['vaccine_plan_no'] == dose)])
                        if(sub_key == 'ประชาชนทั่วไป'):
                            #Recently Adjusted
                            count += len(self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['person_risk_type_name'].isnull()) & (self.__df['vaccine_plan_no'] == dose)])
                        self.__result_set[sub_key].append(count)
            else:
                self.__result_set[main_key] = []
                for dose in range(self.__min_dose, self.__max_dose+1):
                    count = len(self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['vaccine_plan_no'] == dose)])
                    self.__result_set[main_key].append(count)

    def to_clipboard(self, dataframe):
        clipboard_df = pd.DataFrame(dataframe)
        clipboard_df.to_clipboard(index = False, header = False)
        return "Result Copied To Clipboard. Ready to Paste to Excel"

    def export_df_for_npt(self):
        norm_set = [[]]
        for key in self.__result_set:
            for elem in self.__result_set[key]:
                norm_set[0].append(elem)
        '''
        #Client don't want dosage col so I commented out.
        for key in self.__result_set:
            dose_no = 1
            for elem in self.__result_set[key]:
                norm_set[0].append(key+ ' เข็มที่ '+ str(dose_no))
                norm_set[1].append(elem)
                dose_no += 1
        '''
        return norm_set

    def export_tabular_df(self):
        cols = []
        rows = []
        indexes = []
        #Append Dose as Dataframe Columns
        for dose_no in range(self.__min_dose, self.__max_dose+1):
            cols.append("Dose "+ str(dose_no))
        for main_key in self.__result_set:
            indexes.append(main_key)
            temp = []
            for total in self.__result_set[main_key]:
                temp.append(total)
            rows.append(temp)
        df = pd.DataFrame(rows, columns=cols, index=indexes)
        return df