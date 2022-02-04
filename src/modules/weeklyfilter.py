import pandas as pd
import helper.helper as helper

class WeeklyFilter:
    def __init__(self, filepath):
        self.__row_list = None
        self.__df  = helper.read_spreadsheet(filepath)
        self.__config = helper.read_weekly_config()
        self.__min_dose = self.__config['min_dose']
        self.__max_dose = self.__config['max_dose']
        self.__df = self.filter_address()
        (self.__df, self.__row_list) = self.group_filter(self.__df)
        self.to_clipboard()

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, value):
        self.__df = value

    def filter_address(self, province_code = 73, district_code = 12, prefecture_code = 2):
        return self.__df[(self.__df["chw_code"] == province_code) & 
        (self.__df["tmb_code"] == district_code) & 
        (self.__df["amp_code"] == prefecture_code)]

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

    def to_clipboard(self):
        if(self.__row_list is not None):
            clipboard_df = pd.DataFrame(self.__row_list)
            clipboard_df.to_clipboard(index=False, header=False)
