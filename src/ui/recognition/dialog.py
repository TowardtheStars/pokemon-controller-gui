from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QDialogButtonBox, QHBoxLayout, QComboBox
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator, QValidator, QFont
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QSpacerItem, QSizePolicy


class LaunchRecognitionParasDialog(QDialog):
    def __init__(self, parent, paras: dict):
        super().__init__(parent)
        self._paras = paras.copy()
        self._edit_widgets = dict()
        self._bool_validator = QRegularExpressionValidator(QRegularExpression(
            '^(true|false)$', QRegularExpression.CaseInsensitiveOption))
        self._int_validator = QIntValidator()
        self._double_validator = QDoubleValidator()
        self.setWindowTitle('执行脚本')
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        row = self._add_title_label(0)
        row = self._add_row_spacer(row, 20)
        row = self._add_widgets(row)
        row = self._add_row_spacer(row, 30)
        row = self._add_buttons(row)
        self.adjustSize()

    def get_paras(self) -> dict:
        paras = self._paras.copy()
        for para in paras.values():
            edit_widgets = self._edit_widgets[para.name]
            if edit_widgets is None:
                continue
            text = edit_widgets.text()
            if para.value_type == bool:
                if text.lower() == 'true':
                    para.set_value(True)
                else:
                    para.set_value(False)
            elif para.value_type == int:
                para.set_value(int(text))
            elif para.value_type == float:
                para.set_value(float(text))
            elif para.value_type == str:
                para.set_value(text)
        return paras

    def _add_title_label(self, row) -> int:
        title_label = QLabel('参数设置')
        font = QFont()
        font.setPointSize(18)
        title_label.setFont(font)
        self.layout.addWidget(title_label, row, 0, 1, 3)
        row += 1
        return row

    def _add_widgets(self, row) -> int:
        row += 1
        for para in self._paras.values():
            para_summary = para.description
            para_default = para.default_value
            para_label = QLabel(f'{para_summary}')
            para_edit = QLineEdit(str(para_default))
            self._set_lineEdit_validator(para_edit, para.value_type)
            self.layout.addWidget(para_label, row, 0, 1, 2)
            self.layout.addWidget(para_edit, row, 2, 1, 2)
            self._edit_widgets[para.name] = para_edit
            row += 1
        return row

    def _set_lineEdit_validator(self, widget: QLineEdit, value_type: type):
        if value_type == bool:
            widget.setValidator(self._bool_validator)
        elif value_type == int:
            widget.setValidator(self._int_validator)
        elif value_type == float:
            widget.setValidator(self._double_validator)
        elif value_type == str:
            pass
        else:
            raise TypeError("type must be int, float, str or bool")
        return

    def _add_row_spacer(self, row, height=10) -> int:
        spacer = QSpacerItem(
            1, height, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer, row, 0)
        row += 1
        return row

    def _add_buttons(self, row) -> int:
        button_box = QDialogButtonBox()
        button_box.addButton('运行', QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton('取消', QDialogButtonBox.ButtonRole.RejectRole)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.layout.addWidget(button_box, row, 2, 1, 2)
        row += 1
        return row
