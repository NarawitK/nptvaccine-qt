from PySide2 import QtWidgets
from helper.helper import read_config
from components.shared.ListEditorComponent import ListEditorComponent
from components.shared.DoseSpinner import DoseSpinner
from components.settings.daily.subcomponents.NPTSettingComponent import NPTSettingComponent
from components.shared.SaveButtonComponent import SaveButtonComponent
from viewmodel.DailySettingViewModel import DailySettingViewModel


class DailySettingWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.viewmodel = DailySettingViewModel(read_config())

        self.__main_layout = None
        self.person_type_setting = None
        self.sub_person_type_setting = None
        self.vaccine_name_setting = None
        self.__vaccine_alias_label = None
        self.vaccine_alias_setting = None
        self.vaccine_alias_apply_btn = None
        self.dose_spinner = None
        self.__npt_setting_component = None
        self.__save_button_component = None

        self.render_components()
        self.connect_signal()

    def render_components(self):
        self.__main_layout = QtWidgets.QVBoxLayout(self)
        self.person_type_setting = ListEditorComponent("กลุ่มเป้าหมายหลัก", self.viewmodel.main_person_type, ["เพิ่ม", "แก้ไข", "ลบ"])
        self.sub_person_type_setting = ListEditorComponent("กลุ่มเป้าหมายย่อย", [], ["เพิ่ม", "แก้ไข", "ลบ"])
        self.vaccine_name_setting = ListEditorComponent("ชื่อวัคซีนในแผนวัคซีน HOSXP ของโรงพยาบาล", self.viewmodel.vaccine_alias, ["เพิ่ม", "แก้ไข", "ลบ"])
        self.__vaccine_alias_label = QtWidgets.QLabel("ชื่อวัคซีนที่แสดงในโปรแกรมนี้")
        self.vaccine_alias_setting = QtWidgets.QLineEdit()
        self.vaccine_alias_setting.setEnabled(False)
        self.vaccine_alias_apply_btn = QtWidgets.QPushButton("Apply")
        self.vaccine_alias_apply_btn.setEnabled(False)

        self.dose_spinner = DoseSpinner(self.viewmodel.min_dose, self.viewmodel.max_dose)
        self.__npt_setting_component = NPTSettingComponent(self.viewmodel.npt_url)
        self.__save_button_component = SaveButtonComponent()

        # Add Widget to Main Layout
        self.__main_layout.addWidget(self.person_type_setting)
        self.__main_layout.addWidget(self.sub_person_type_setting)
        self.__main_layout.addWidget(self.vaccine_name_setting)
        self.__main_layout.addWidget(self.__vaccine_alias_label)
        self.__main_layout.addWidget(self.vaccine_alias_setting)
        self.__main_layout.addWidget(self.vaccine_alias_apply_btn)
        self.__main_layout.addWidget(self.dose_spinner)
        self.__main_layout.addWidget(self.__npt_setting_component)
        self.__main_layout.addWidget(self.__save_button_component)

    def connect_signal(self):
        self.person_type_setting.set_on_current_item_changed_slot(self.set_sub_person_from_person)
        self.person_type_setting.onAddItem.connect(self.viewmodel.add_main_person_type)
        self.person_type_setting.onEditItem.connect(self.viewmodel.update_main_person_type)
        self.person_type_setting.onRemoveItem.connect(self.viewmodel.remove_main_person_type)
        self.sub_person_type_setting.onAddItem.connect(self.manipulate_sub_person)
        self.sub_person_type_setting.set_on_edit_button_slot(self.manipulate_sub_person)
        self.sub_person_type_setting.onRemoveItem.connect(self.manipulate_sub_person)

        self.vaccine_name_setting.set_on_current_item_changed_slot(self.set_vac_alias_text_from_vaccine)
        self.vaccine_name_setting.onAddItem.connect(self.viewmodel.add_main_vaccine_key)
        self.vaccine_name_setting.onEditItem.connect(self.viewmodel.edit_main_vaccine_key)
        self.vaccine_name_setting.onRemoveItem.connect(self.viewmodel.remove_main_vaccine_key)
        self.vaccine_alias_apply_btn.clicked.connect(self.on_vaccine_alias_edited)

        self.dose_spinner.onMinDoseChanged.connect(self.viewmodel.set_min_dose)
        self.dose_spinner.onMaxDoseChanged.connect(self.viewmodel.set_max_dose)
        self.__npt_setting_component.onUrlValid.connect(self.viewmodel.set_npt_url)
        self.__save_button_component.set_save_func(self.viewmodel.write_config)

    # Slot
    def manipulate_sub_person(self):
        main_person_key = self.person_type_setting.listbox.currentItem().text()
        sub = self.sub_person_type_setting.get_data_list()
        self.viewmodel.manipulate_sub_person(main_person_key, sub)

    def remove_sub_person(self, remove_value: str):
        main_person_key = self.person_type_setting.listbox.currentItem().text()
        self.viewmodel.remove_sub_person(main_person_key, remove_value)

    def on_vaccine_alias_edited(self):
        vaccine_name = self.vaccine_name_setting.line_edit.text()
        vaccine_alias = self.vaccine_alias_setting.text()
        self.viewmodel.edit_vaccine_alias(vaccine_name, vaccine_alias)

    # UI Slot
    def set_vac_alias_text_from_vaccine(self, current_item):
        key = current_item.text()
        self.vaccine_alias_setting.setEnabled(True)
        self.vaccine_alias_setting.setText(self.viewmodel.vaccine_alias[key])
        self.vaccine_alias_apply_btn.setEnabled(True)

    def set_sub_person_from_person(self, current_item):
        key = current_item.text()
        if key in self.viewmodel.sub_person_type:
            self.sub_person_type_setting.set_data_list(self.viewmodel.sub_person_type[current_item.text()])
        else:
            self.sub_person_type_setting.listbox.clear()
