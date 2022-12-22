
class BaseModelWithDictDataType:
    def __init__(self, config_json, json_config_key) -> None:
        self.config_data: dict = config_json
        self.config_key = json_config_key
        self.data_dict: dict = self.config_data[self.config_key]

    def add_main_key(self, added_key: str):
        if added_key not in self.data_dict:
            self.data_dict[added_key] = []

    def edit_main_key(self, new_value: str, old_value: str):
        if old_value in self.data_dict:
            temp = self.data_dict[old_value]
            del self.data_dict[old_value]
            self.data_dict[new_value] = temp

    def remove_main_key(self, deleted_key: str) -> bool:
        if deleted_key in self.data_dict:
            del self.data_dict[deleted_key]
            return True
        else:
            return False

    def add_sub_val(self, selected_main_key: str, added_key: str):
        if added_key not in self.data_dict[selected_main_key]:
            self.data_dict[selected_main_key].append(added_key)

    def edit_sub_val(self, selected_main_key: str, new_val: str, idx: int) -> bool:
        if selected_main_key in self.data_dict[selected_main_key]:
            self.data_dict[selected_main_key][idx] = new_val
            return True
        else:
            return False

    def remove_sub_val(self, selected_main_key:str, deleted_key: str) -> bool:
        if deleted_key in self.data_dict[selected_main_key]:
            self.data_dict[selected_main_key].remove(deleted_key)
            return True
        else:
            return False

    def format_to_config_format(self):
        json_obj: dict = { self.config_key: self.data_dict }
        return json_obj
