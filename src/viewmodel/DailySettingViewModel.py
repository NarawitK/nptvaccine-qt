import viewmodel.base.BaseSettingModelWithPerson as BaseViewModel
from helper.helper import write_daily_config


class DailySettingViewModel(BaseViewModel.BaseSettingModelWithPerson):
    VAC_ALIAS_KEYNAME = "vaccine_alias"
    NPT_URL_KEYNAME = "npt_url"
    DEFAULT_VACCINE_ALIAS = "กรุณาใส่ชื่อย่อวัคซีน"

    def __init__(self, config_json):
        super().__init__(config_json)
        self.vaccine_alias: dict = self.config_data[self.VAC_ALIAS_KEYNAME]
        self.npt_url: str = self.config_data[self.NPT_URL_KEYNAME]

    # Vaccine Alias Section
    def add_main_vaccine_key(self, added_key: str):
        if added_key not in self.vaccine_alias:
            self.vaccine_alias[added_key] = self.DEFAULT_VACCINE_ALIAS

    def edit_main_vaccine_key(self, new_value: str, old_value: str):
        if old_value in self.vaccine_alias:
            temp = self.vaccine_alias[old_value]
            del self.vaccine_alias[old_value]
            self.vaccine_alias[new_value] = temp

    def remove_main_vaccine_key(self, deleted_key: str) -> bool:
        if deleted_key in self.vaccine_alias:
            del self.vaccine_alias[deleted_key]
            return True
        else:
            return False

    def edit_vaccine_alias(self, selected_main_vaccine_key: str, alias: str) -> bool:
        if selected_main_vaccine_key in self.vaccine_alias:
            self.vaccine_alias[selected_main_vaccine_key] = alias
            return True
        else:
            return False

    def format_to_config_format(self) -> dict:
        json_obj = super().format_to_config_format()
        json_obj[self.VAC_ALIAS_KEYNAME] = self.vaccine_alias
        json_obj[self.NPT_URL_KEYNAME] = self.npt_url
        return json_obj

    def write_config(self):
        write_daily_config(self.format_to_config_format())

    def set_npt_url(self, url: str):
        self.npt_url = url
