import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys
from generate_text import generate


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())
        self.setWindowTitle("NASA Tweet Generator")
        self.setWindowIcon(qtg.QIcon("src/assets/rocket.png"))

        output_label = qtw.QLabel("")
        output_label.setFont(qtg.QFont("Helvetica", 10))
        self.layout().addWidget(output_label)

        enter_seed_label = qtw.QLabel("Enter seed : ")
        enter_seed_label.setFont(qtg.QFont("Helvetica", 10))
        self.layout().addWidget(enter_seed_label)

        enter_seed_entry = qtw.QLineEdit()
        enter_seed_entry.setObjectName("seed_field")
        enter_seed_entry.setText("Enter seed")
        self.layout().addWidget(enter_seed_entry)

        confirm_seed_button = qtw.QPushButton("Confirm",
                                              clicked=lambda: display())
        self.layout().addWidget(confirm_seed_button)

        self.show()

        def display():
            output_label.setText(generate(enter_seed_entry.text()))
            enter_seed_entry.setText("Enter seed")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()

    sys.exit(app.exec_())
