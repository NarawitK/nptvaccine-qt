class BaseSettingModelWithPerson:
    PERSON_TYPE_KEYNAME = "type"
    SUB_PERSON_TYPE_KEYNAME = "sub_type"
    MIN_DOSE_KEYNAME = "min_dose"
    MAX_DOSE_KEYNAME = "max_dose"

    def __init__(self, config_json: dict):
        self.config_data: dict = config_json
        self.main_person_type: list = []
        self.sub_person_type: dict = {}
        self.min_dose = 1
        self.max_dose = 2
        self.__data_initialization(config_json)

    def __data_initialization(self, config_json: dict):
        if self.PERSON_TYPE_KEYNAME in config_json:
            self.main_person_type: list = self.config_data["type"]
        if self.SUB_PERSON_TYPE_KEYNAME in config_json:
            self.sub_person_type: dict = self.config_data["sub_type"]
        if self.MIN_DOSE_KEYNAME in config_json:
            self.min_dose = self.config_data["min_dose"]
        if self.MAX_DOSE_KEYNAME in config_json:
            self.max_dose = self.config_data["max_dose"]

    def add_main_person_type(self, new_person_type: str):
    # ListEditorComponent use list arg by ref.
        if new_person_type not in self.main_person_type:
            self.main_person_type.append(new_person_type)
        if new_person_type not in self.sub_person_type:
            self.sub_person_type[new_person_type] = []

    def update_main_person_type(self, edited_data: str, old_data: str):
        if old_data in self.sub_person_type:
            self.sub_person_type[edited_data] = self.sub_person_type[old_data]
            del self.sub_person_type[old_data]

    def remove_main_person_type(self, removed_value):
        if removed_value in self.main_person_type:
            self.main_person_type.remove(removed_value)
        if removed_value in self.sub_person_type:
            del self.sub_person_type[removed_value]

    def manipulate_sub_person(self, main_person_key: str, sub_data: list):
        self.sub_person_type[main_person_key] = sub_data

    def remove_sub_person(self, main_person_key: str, remove_val: str):
        if main_person_key in self.main_person_type:
            if remove_val in self.sub_person_type[main_person_key]:
                self.sub_person_type[main_person_key].remove(remove_val)

    def set_min_dose(self, value: int):
        self.min_dose = value

    def set_max_dose(self, value: int):
        self.max_dose = value

    def format_to_config_format(self) -> dict:
        data_dict = {
            "type": self.main_person_type,
            "sub_type": self.sub_person_type,
            "min_dose": self.min_dose,
            "max_dose": self.max_dose,
        }
        return data_dict
