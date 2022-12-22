import viewmodel.base.BaseModelWithDictDataType as BaseViewModel
from helper.helper import write_group_list

class PersonTypeViewModel(BaseViewModel.BaseModelWithDictDataType):

    def __init__(self, config_json, config_key_name) -> None:
        super().__init__(config_json, config_key_name)

    def write_config(self):
        write_group_list(self.format_to_config_format())