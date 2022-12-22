from PySide2 import QtWidgets
from helper.helper import read_group_list
from components.shared.ListEditorComponent import ListEditorComponent
from components.shared.SaveButtonComponent import SaveButtonComponent
from viewmodel.PersonTypeViewModel import PersonTypeViewModel

class PersonTypeSettingWidget(QtWidgets.QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.viewmodel = PersonTypeViewModel(read_group_list(), config_key_name="type")

        self.__main_layout = None
        self.main_type_setting = None
        self.sub_type_setting = None
        self.__save_button_component = None

        self.render_components()
        self.connect_signal()

    def render_components(self):
        self.__main_layout = QtWidgets.QVBoxLayout(self)
        self.main_type_setting = ListEditorComponent("กลุ่มเป้าหมายหลัก", self.viewmodel.data_dict, ["เพิ่ม", "แก้ไข", "ลบ"], False)
        self.sub_type_setting = ListEditorComponent("กลุ่มเป้าหมายย่อย", [], ["เพิ่ม", "แก้ไข", "ลบ"])
        self.__save_button_component = SaveButtonComponent()

        self.__main_layout.addWidget(self.main_type_setting)
        self.__main_layout.addWidget(self.sub_type_setting)
        self.__main_layout.addWidget(self.__save_button_component)

    def connect_signal(self):
        self.main_type_setting.set_on_current_item_changed_slot(self.set_sub_type_from_main)
        self.main_type_setting.onAddItem.connect(self.viewmodel.add_main_key)
        self.main_type_setting.onEditItem.connect(self.viewmodel.edit_main_key)
        self.main_type_setting.onRemoveItem.connect(self.viewmodel.remove_main_key)
        self.__save_button_component.set_save_func(self.viewmodel.write_config)

    # UI Signal Handler Method
    def set_sub_type_from_main(self, current_item):
        key = current_item.text()
        if key in self.viewmodel.data_dict:
            self.sub_type_setting.set_data_list(self.viewmodel.data_dict[current_item.text()])
        else:
            self.sub_type_setting.listbox.clear()
