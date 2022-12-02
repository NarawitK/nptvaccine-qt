import pandas as pd


class ForeignFilter:
    MOPH_IC_COLS_ARRAY = ["cid", "cid_hash", "chw_code", "amp_code", "tmb_code"]
    MOPH_IC_COLS_CLEAN_UP = ["chw_code", "amp_code", "tmb_code"]

    @property
    def mophic_df(self):
        return self.__mophic_df

    @property
    def hosxp_df(self):
        return self.__hosxp_df

    def __init__(self, moph_group_filepath: str):
        self.__hosxp_df = None
        self.__mophic_df = self.__spreadsheet_reader(moph_group_filepath)
        self.__mophic_df = self.filter_address(self.__mophic_df)
        self.__mophic_df["cid"] = self.__fill_cid_leading_zeroes(self.__mophic_df)
        self.__mophic_col_cleanup()

    # Initialize
    def __spreadsheet_reader(self, filepath: str) -> pd.DataFrame:
        try:
            return pd.read_excel(filepath, dtype={"cid": str, "cid_hash": str}, usecols=self.MOPH_IC_COLS_ARRAY)
        except Exception:
            try:
                return pd.read_csv(filepath, dtype={"cid": str, "cid_hash": str}, usecols=self.MOPH_IC_COLS_ARRAY)
            except Exception:
                raise Exception("This file cannot be opened as Excel or csv")

    def filter_address(self, df: pd.DataFrame, province_code: int = 73, district_code: int = 12,
                       prefecture_code: int = 2):
        try:
            return df[(df["chw_code"] == province_code) & (df["tmb_code"] == district_code) &
                      (df["amp_code"] == prefecture_code)]
        except Exception as e:
            raise Exception(f"Invalid Dataframe passed as argument. \n{e}")

    def __fill_cid_leading_zeroes(self, df: pd.DataFrame) -> pd.DataFrame:
        return df["cid"].map(lambda x: f"{x:0>13}")

    def __mophic_col_cleanup(self):
        self.__mophic_df.drop(self.MOPH_IC_COLS_CLEAN_UP, axis=1, inplace=True)

    # HOSXP Manipulation Section
    def convert_hosxp_to_df(self, hosxp_list: list):
        if self.__mophic_df is not None:
            self.__hosxp_df = pd.DataFrame(hosxp_list)
        else:
            raise Exception("MOPH-IC Dataframe still Unoccupied.")

    # Both Side
    def merge_dataframes(self, hosxp_df: pd.DataFrame, mophic_df: pd.DataFrame) -> pd.DataFrame:
        dose1_df = hosxp_df.loc[~hosxp_df["dose_1"].isna(), ["cid", "vaccine_name_1", "date_1"]]
        dose2_df = hosxp_df.loc[~hosxp_df["dose_2"].isna(), ["cid", "vaccine_name_2", "date_2"]]
        res = self.__filter_cids(dose1_df, dose2_df)
        res = res.merge(hosxp_df[["cid", "name", "age"]].drop_duplicates(subset=['cid']), on="cid", how="inner")
        res = res.merge(mophic_df, on="cid", how="inner")
        res = self.__rearrange_columns(res)
        return res

    def __filter_cids(self, dose1_df, dose2_df):
        cid_intersect_df = dose1_df.merge(dose2_df, on="cid", how="inner")
        only_first_dose_df = dose1_df[~dose1_df["cid"].isin(cid_intersect_df["cid"])]
        only_second_dose_df = dose2_df[~dose2_df["cid"].isin(cid_intersect_df["cid"])]
        return pd.concat([cid_intersect_df, only_first_dose_df, only_second_dose_df])

    def __rearrange_columns(self, mpd: pd.DataFrame) -> pd.DataFrame:
        return mpd[["name", "age", "cid", "cid_hash",
                    "vaccine_name_1", "date_1",
                    "vaccine_name_2", "date_2"
                    ]]

    def export_to_excel(self, path: str, merged_df: pd.DataFrame):
        merged_df.to_excel(path, sheet_name="Result", index=False)
