import pandas as pd
import helper.helper as helper

class WeeklyFilter:
    def __init__(self, filepath):
        self.__row_list = None
        self.__df  = helper.read_spreadsheet(filepath)
        self.__config = helper.read_weekly_config()
        self.__min_dose = self.__config['min_dose']
        self.__max_dose = self.__config['max_dose']
        self.__df = self.filter_address(self.__df)
        #(self.__df, self.__row_list) = self.group_filter(self.__df)

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, value):
        self.__df = value
    
    @staticmethod
    def filter_address(df, province_code = 73, district_code = 12, prefecture_code = 2):
        return df[(df["chw_code"] == province_code) & (df["tmb_code"] == district_code) & (df["amp_code"] == prefecture_code)]

    def group_filter(self, df):
        cols = ["Population"]
        rows = []
        idx = []

        for dose_no in range(self.__min_dose, self.__max_dose + 1):
            col_key_name = "Dose " + str(dose_no)
            cols.append(col_key_name)

        for main_type in self.__config['type']:
            if main_type in self.__config['sub_type']:

                for sub_type in self.__config['sub_type'][main_type]:
                    idx.append(sub_type)
                    totals = []
                    sum_row, _ = df[(df["person_type_name"] == main_type) & 
                        (df['person_risk_type_name'] == sub_type)].shape
                    totals.append(sum_row)

                    for dose_no in range(self.__min_dose, self.__max_dose + 1):
                        col_key_name = "vaccine_plan_" + str(dose_no)
                        total_df = df[(df["person_type_name"] == main_type) & 
                        (df['person_risk_type_name'] == sub_type) & (df[col_key_name] == 'Y')]
                        row, _ = total_df.shape
                        totals.append(row)
                    rows.append(totals)
            else:
                idx.append(main_type)
                totals = []
                sum_row, _ = df[df["person_type_name"] == main_type].shape
                totals.append(sum_row)

                for dose_no in range(self.__min_dose, self.__max_dose + 1):
                    col_key_name = "vaccine_plan_" + str(dose_no)
                    total_df = df[(df["person_type_name"] == main_type) & 
                    (df[col_key_name] == 'Y')]
                    row, _ = total_df.shape
                    totals.append(row)
                rows.append(totals)

        result_df = pd.DataFrame(rows, index = idx, columns = cols)
        return (result_df, rows)
    
    def to_clipboard(self, rowlist):
        if(rowlist is not None):
            clipboard_df = pd.DataFrame(rowlist)
            clipboard_df.to_clipboard(index=False, header=False)


class WeeklyGroupChecker:
    def __init__(self, df):
        self.__df = df
        self.__error_df = None
        self.__has_error = self.__check_group_error(self.__df)

    @property
    def has_error(self):
        return self.__has_error

    @property
    def error_df(self):
        return self.__error_df

    def __check_group_error(self, df):
        # Index show as Excel Visible Row No.
        group_set = helper.read_group_list()
        df.index = range(2, df.shape[0] + 2)
        filter_dataframe = df.loc[
            (self.__df['person_type_name'].isnull()) | (df['person_risk_type_name'].isnull()), ['cid',
                                                                                                'prefix',
                                                                                                'first_name',
                                                                                                'last_name',
                                                                                                'person_type_name',
                                                                                                'person_risk_type_name']]
        for group_name in group_set['type']:
            person_type_df = df.loc[(self.__df['person_type_name'] == group_name)
                                    & (~self.__df['person_risk_type_name'].isnull())
                                    & (~self.__df['person_risk_type_name'].isin(group_set['type'][group_name])),
                                    ['cid', 'prefix', 'first_name', 'last_name', 'person_type_name', 'person_risk_type_name']]
            if not person_type_df.empty:
                filter_dataframe = filter_dataframe.append(person_type_df)

        if filter_dataframe.empty:
            return False
        else:
            temp_df = self.__generate_error_df_for_tablemodel(filter_dataframe)
            self.__error_df = temp_df.sort_index()
            return True

    def __generate_error_df_for_tablemodel(self, df):
        return df.rename(columns={'cid': 'เลขบัตรประชาชน', 
                                  'prefix': 'คำนำหน้า','first_name': 'ชื่อ', 'last_name': 'นามสกุล',
                                  'person_type_name': 'กลุ่มเป้าหมายหลัก',
                                  'person_risk_type_name': 'กลุ่มเป้าหมายย่อย'})