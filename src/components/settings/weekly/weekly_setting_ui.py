from PySide2 import QtWidgets
from components.shared.ListEditorComponent import ListEditorComponent
from components.shared.DoseSpinner import DoseSpinner
from components.shared.SaveButtonComponent import SaveButtonComponent
from viewmodel.WeeklySettingViewModel import WeeklySettingViewModel
from helper.helper import read_weekly_config

class WeeklySettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.viewmodel = WeeklySettingViewModel(read_weekly_config())
        self.__main_layout = None
        self.__person_type_setting = None
        self.__sub_person_type_setting = None
        self.__dose_spinner = None
        self.__save_button_component = None
        self.render_components()
        self.connect_signal()

    def render_components(self):
        self.__main_layout = QtWidgets.QVBoxLayout(self)
        self.__person_type_setting = ListEditorComponent("กลุ่มเป้าหมายหลัก", self.viewmodel.main_person_type, ["เพิ่ม", "แก้ไข", "ลบ"])
        self.__sub_person_type_setting = ListEditorComponent("กลุ่มเป้าหมายย่อย", [], ["เพิ่ม", "แก้ไข", "ลบ"])
        self.__dose_spinner = DoseSpinner(self.viewmodel.min_dose, self.viewmodel.max_dose)
        self.__save_button_component = SaveButtonComponent()

        # Add Widget to Main Layout
        self.__main_layout.addWidget(self.__person_type_setting)
        self.__main_layout.addWidget(self.__sub_person_type_setting)
        self.__main_layout.addWidget(self.__dose_spinner)
        self.__main_layout.addWidget(self.__save_button_component)

    def connect_signal(self):
        self.__person_type_setting.set_on_current_item_changed_slot(self.set_sub_person_from_person)
        self.__person_type_setting.onAddItem.connect(self.viewmodel.add_main_person_type)
        self.__person_type_setting.onEditItem.connect(self.viewmodel.update_main_person_type)
        self.__person_type_setting.onRemoveItem.connect(self.viewmodel.remove_main_person_type)

        self.__sub_person_type_setting.onAddItem.connect(self.prepare_manipulate_sub_person)
        self.__sub_person_type_setting.set_on_edit_button_slot(self.prepare_manipulate_sub_person)
        self.__sub_person_type_setting.onRemoveItem.connect(self.prepare_manipulate_sub_person)

        self.__dose_spinner.onMinDoseChanged.connect(self.viewmodel.set_min_dose)
        self.__dose_spinner.onMaxDoseChanged.connect(self.viewmodel.set_max_dose)

        self.__save_button_component.set_save_func(self.viewmodel.write_config)

    # UI Signal Handler
    def prepare_manipulate_sub_person(self):
        main_person_key = self.__person_type_setting.listbox.currentItem().text()
        sub = self.__sub_person_type_setting.get_data_list()
        self.viewmodel.manipulate_sub_person(main_person_key, sub)
    
    def set_sub_person_from_person(self, current_item):
        key = current_item.text()
        if key in self.viewmodel.sub_person_type:
            self.__sub_person_type_setting.set_data_list(self.viewmodel.sub_person_type[current_item.text()])
        else:
            self.__sub_person_type_setting.listbox.clear()
