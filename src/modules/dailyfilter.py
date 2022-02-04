import os
import numpy as np
from helper import helper
import pandas as pd


class DailyFilter:
    __df = None
    __result_set = {}
    __min_dose = 1
    __max_dose = 4

    def __init__(self, filepath):
        self.readSpreadSheet(filepath)

    def get_dataframe(self):
        return self.__df

    def readSpreadSheet(self, filepath):
        try:
            _, file_extension = os.path.splitext(filepath)
            if (file_extension == '.xlsx' or file_extension == '.xls'):
                self.__df = pd.read_excel(filepath)
            elif (file_extension == '.csv'):
                self.__df = pd.read_csv(filepath)
            else:
                raise Exception('Unknown File Extension')
        except:
            raise Exception('Something going on about your file')

    def checkdatecount(self):
        dataframe = self.__df
        dataframe['immunization_date'] = dataframe['immunization_datetime'].astype('datetime64[ns]').dt.date
        date_count = len(dataframe['immunization_date'].drop_duplicates())
        if date_count == 1:
            return True
        elif date_count > 1:
            raise Exception("ในไฟล์ต้นฉบับมีวันที่ฉีดมากกว่า 1 วัน")
        else:
            raise Exception("ในไฟล์ต้นฉบับไม่มีวันที่ฉีดเลย")

    def prepareData(self):
        filter_list = helper.read_config()
        self.__min_dose = filter_list['min_dose']
        self.__max_dose = filter_list['max_dose']
        for main_key in filter_list['type']:
            if main_key in filter_list['sub_type']:
                for sub_key in filter_list['sub_type'][main_key]:
                    self.__result_set[sub_key] = []
                    for dose in range(self.__min_dose, self.__max_dose + 1):
                        count = len(self.__df[(self.__df['person_type_name'] == main_key) & (
                                    self.__df['person_risk_type_name'] == sub_key) & (
                                                          self.__df['vaccine_plan_no'] == dose)])
                        if sub_key == 'ประชาชนทั่วไป':
                            count += len(self.__df[(self.__df['person_type_name'] == main_key) & (
                                self.__df['person_risk_type_name'].isnull()) & (self.__df['vaccine_plan_no'] == dose)])
                        self.__result_set[sub_key].append(count)
            else:
                self.__result_set[main_key] = []
                for dose in range(self.__min_dose, self.__max_dose + 1):
                    count = len(
                        self.__df[(self.__df['person_type_name'] == main_key) & (self.__df['vaccine_plan_no'] == dose)])
                    self.__result_set[main_key].append(count)

    def to_clipboard(self, dataframe):
        clipboard_df = pd.DataFrame(dataframe)
        clipboard_df.to_clipboard(index=False, header=False)

    def export_df_for_npt(self):
        norm_set = [[]]
        for key in self.__result_set:
            for elem in self.__result_set[key]:
                norm_set[0].append(elem)
        return norm_set

    def export_tabular_df(self):
        cols = []
        rows = []
        indexes = []
        # Append Dose as Dataframe Columns
        for dose_no in range(self.__min_dose, self.__max_dose + 1):
            cols.append("Dose " + str(dose_no))
        for main_key in self.__result_set:
            indexes.append(main_key)
            temp = []
            for total in self.__result_set[main_key]:
                temp.append(total)
            rows.append(temp)
        df = pd.DataFrame(rows, columns=cols, index=indexes)
        return df


class DocuChecker:
    def __init__(self, df):
        self.__df = df
        self.__error_df = None
        self.__has_error = self.__check_group_error(self.__df)

    def get_has_error(self):
        return self.__has_error

    def get_error_details(self):
        return self.__error_df

    def __check_group_error(self, df):
        # Index show as Excel Visible Row No.
        group_set = helper.read_group_list()
        error_flag = False
        df.index = range(2, df.shape[0] + 2)
        filter_dataframe = df.loc[
            (self.__df['person_type_name'].isnull()) | (df['person_risk_type_name'].isnull()), ['cid',
                                                                                                'ref_patient_name',
                                                                                                'person_type_name',
                                                                                                'person_risk_type_name']]
        for group_name in group_set['type']:
            person_type_df = df.loc[(self.__df['person_type_name'] == group_name)
                                    & (~self.__df['person_risk_type_name'].isnull())
                                    & (~self.__df['person_risk_type_name'].isin(group_set['type'][group_name])),
                                    ['cid', 'ref_patient_name', 'person_type_name', 'person_risk_type_name']]
            if not person_type_df.empty:
                error_flag = True
                filter_dataframe = filter_dataframe.append(person_type_df)

        if filter_dataframe.empty:
            return error_flag
        else:
            temp_df = self.__generate_error_df_for_tablemodel(filter_dataframe)
            self.__error_df = temp_df.sort_index()
            return error_flag

    def __generate_error_df_for_tablemodel(self, df):
        return df.rename(columns={'cid': 'เลขบัตรประชาชน', 'ref_patient_name': 'ชื่อ-นามสกุล',
                                  'person_type_name': 'กลุ่มเป้าหมายหลัก',
                                  'person_risk_type_name': 'กลุ่มเป้าหมายย่อย'})
