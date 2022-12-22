import viewmodel.base.BaseSettingModelWithPerson as BaseViewModel
from helper.helper import write_weekly_config

class WeeklySettingViewModel(BaseViewModel.BaseSettingModelWithPerson):

    def __init__(self, config_json) -> None:
        super().__init__(config_json)

    def write_config(self):
        write_weekly_config(self.format_to_config_format())