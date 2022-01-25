import pandas as pd
import xlsxwriter

class FinancialFilter:
    def __init__(self, filepath):
        self.__dates = []
        self.__data_sheets = {}
        self.__dataframe = None
        self.read_file(filepath)

    def read_file(self, filepath):
        try:
            self.__dataframe = pd.read_excel(filepath, dtype={'ref_hn': str})
        except FileNotFoundError:
            raise Exception("ไม่พบไฟล์ที่นี่: " + str(filepath))
        except Exception:
            try:
                self.__dataframe = pd.read_csv(filepath, dtype={'ref_hn': str})
            except Exception:
                raise Exception("ไม่สามารถอ่านไฟล์ได้ กรุณาตรวจสอบประเภทของไฟล์ว่าเป็น Excel หรือ CSV")

    def filter_date(self):
        if('immunization_datetime' in self.__dataframe.columns):
            self.__dataframe = self.__dataframe.sort_values(by=['immunization_datetime'])
            self.__dataframe['immunization_date'] = self.__dataframe['immunization_datetime'].astype('datetime64[ns]').dt.date
            self.__dates = self.__dataframe["immunization_date"].drop_duplicates().to_list()
        else:
            raise Exception("คอลัมน์ในไฟล์ไม่ถูกต้อง ตรวจสอบไฟล์ต้นฉบับว่าถูกหรือไม่")

    def prepare_filtered_date_sheets(self):
        for date in self.__dates:
            filter_dataframe = self.__dataframe.loc[self.__dataframe["immunization_date"] == date, [
                "cid", "immunization_datetime", "ref_hn", "ref_patient_name", "vaccine_plan_no", "vaccine_ref_name"]]
            self.__data_sheets[date] = filter_dataframe

    def write_to_excel(self, output_path):
        try:
            file_name = output_path
            with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
                workbook = writer.book
                for key in self.__data_sheets:
                    sheetname = str(key)
                    df = self.__data_sheets[key]
                    df.to_excel(writer, header=False, index=False, sheet_name=sheetname, startcol=1, startrow=3)
                    worksheet = writer.sheets[sheetname]
                    self.__fill_border(workbook, worksheet, df)
                    self.__column_auto_width(df, worksheet)
                    self.__column_format(workbook, worksheet)
                    self.__write_rows_number(workbook, worksheet, len(df))
                    self.__write_data_header(workbook, worksheet)
                    self.__write_static_col(workbook, worksheet, key, len(df))
        
        except Exception as e:
            raise Exception("ไม่สามารถเขียนไฟล์ Excel ได้ ลองตรวจสอบไฟล์ต้นฉบับว่าเนื้อหาถูกต้อง, Path ที่ทำการบันทึกว่ามีสิทธิ์เข้าถึงหรือมีอยู่จริงหรือไม่ \n(Details): "+ str(e))


    # Excel Utilities for Formatting
    def __fill_border(self, workbook, worksheet, df):
        border_format = workbook.add_format({'bottom':1, 'top':1, 'left':1, 'right':1})
        worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, len(df)+2, len(df.columns)), {'type': 'no_errors', 'format': border_format})

    def __column_auto_width(self, df, worksheet_instance):
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet_instance.set_column(col_idx+1, col_idx+1, column_width)

    def __column_format(self, workbook, worksheet):
        data_header_format = workbook.add_format({'bold': 1, 'font_name': 'TH SarabunPSK', 'font_size': 10})
        worksheet.set_column(0, 0, 3.3)
        worksheet.set_column(0, 6, None, data_header_format)

    def __write_rows_number(self, workbook, worksheet_instance, df_length, startrow=2, startcol=0):
        sub_format = workbook.add_format(
            {'bold': 1, 'font_name': 'TH SarabunPSK', 'font_size': 10})
        worksheet_instance.set_column(0, 0, 3.3)
        current_row = startrow
        worksheet_instance.write_string(
            current_row, startcol, 'ลำดับ', sub_format)
        current_row += 1
        for i in range(df_length):
            worksheet_instance.write_number(current_row, startcol, i+1)
            current_row += 1

    def __write_static_col(self, workbook, worksheet_instance, date, count):
        title_format = workbook.add_format({
            'bold': 1,
            'font_name': 'TH SarabunPSK',
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter'
        })
        sub_format = workbook.add_format({
            'font_name': 'TH SarabunPSK',
            'font_size': 10,
            'bold': 1
        })
        date_format = workbook.add_format({
            'font_name': 'TH SarabunPSK',
            'font_size': 10,
            'num_format': '[$-,1070000]d mmmm yyyy;@',
            'bold': 1,
            'font_color': 'red'
        })
        worksheet_instance.write_string('A2', 'วันที่', sub_format)
        worksheet_instance.write_datetime('B2', date, date_format)
        worksheet_instance.write_string('C2', '', sub_format)
        worksheet_instance.write_string('G2', '', sub_format)
        worksheet_instance.write_string('D2', 'จำนวน', sub_format)
        worksheet_instance.write_number('E2', count, sub_format)
        worksheet_instance.write_string('F2', 'คน', sub_format)
        worksheet_instance.merge_range('A1:G1', 'ทะเบียน ผู้ที่รับบริการฉีด Vaccine ที่หน่วยให้บริการ : ศูนย์ฉีดวัคซีนคอนเวนชั่น มหาวิทยาลัยเกษตรศาสตร์', title_format)

    def __write_data_header(self, workbook, worksheet_instance):
        header_format = workbook.add_format({
            'bold': 1,
            'font_name': 'TH SarabunPSK',
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            #'border': 1
        })
        worksheet_instance.write_string('B3', 'cid', header_format)
        worksheet_instance.write_string('C3', 'เวลาฉีด', header_format)
        worksheet_instance.write_string('D3', 'hn', header_format)
        worksheet_instance.write_string('E3', 'ชื่อ', header_format)
        worksheet_instance.write_string('F3', 'เข็ม', header_format)
        worksheet_instance.write_string('G3', 'ชื่อวัคซีน', header_format)
