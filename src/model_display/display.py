import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys
from generate_text import generate


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())
        self.setFixedWidth(634)
        self.setWindowTitle("NASA Tweet Generator")
        self.setWindowIcon(qtg.QIcon("src/assets/rocket.png"))
        self.setStyleSheet("background-color: #15202b;")

        top_of_tweet_label = qtw.QLabel()
        top_of_tweet_pixmap = qtg.QPixmap('src/assets/top_of_tweet.png')
        top_of_tweet_label.setPixmap(top_of_tweet_pixmap)
        self.layout().addWidget(top_of_tweet_label)

        output_label = qtw.QLabel("")
        output_label.setFont(qtg.QFont("Times", 12, weight=qtg.QFont.Bold))
        output_label.setStyleSheet("color: white; padding: 10px;")
        output_label.setWordWrap(True)
        self.layout().addWidget(output_label)

        bottom_of_tweet_label = qtw.QLabel()
        bottom_of_tweet_pixmap = qtg.QPixmap('src/assets/bottom_of_tweet.png')
        bottom_of_tweet_label.setPixmap(bottom_of_tweet_pixmap)
        self.layout().addWidget(bottom_of_tweet_label)

        enter_seed_label = qtw.QLabel("Enter starting text (max 40 chars) : ")
        enter_seed_label.setFont(qtg.QFont("Helvetica", 10))
        enter_seed_label.setStyleSheet("color: white;")
        self.layout().addWidget(enter_seed_label)

        enter_seed_entry = qtw.QLineEdit()
        enter_seed_entry.setObjectName("seed_field")
        enter_seed_entry.setStyleSheet("color: white;")
        self.layout().addWidget(enter_seed_entry)

        enter_diversity_label = qtw.QLabel("Enter diversity value : ")
        enter_diversity_label.setFont(qtg.QFont("Helvetica", 10))
        enter_diversity_label.setStyleSheet("color: white;")
        self.layout().addWidget(enter_diversity_label)

        enter_diversity_entry = qtw.QLineEdit()
        enter_diversity_entry.setObjectName("seed_field")
        enter_diversity_entry.setText("0.3")
        enter_diversity_entry.setStyleSheet("color: white;")
        self.layout().addWidget(enter_diversity_entry)

        confirm_seed_button = qtw.QPushButton("Confirm",
                                              clicked=lambda: display())
        confirm_seed_button.setStyleSheet("color: white;")
        self.layout().addWidget(confirm_seed_button)

        self.show()

        def display():
            try:
                diversity = float(enter_diversity_entry.text())
            except:
                output_label.setText("Invalid diversity value")
            else:
                output_label.setText(
                    generate(enter_seed_entry.text(), diversity=diversity))

                enter_seed_entry.setText("")
                enter_diversity_entry.setText("0.3")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()

    sys.exit(app.exec_())
