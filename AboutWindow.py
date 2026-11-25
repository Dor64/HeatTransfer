import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        style_path = os.path.join(os.path.dirname(__file__), "style.css")
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About - Heat Transfer")
        self.setFixedSize(420, 480)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Main content card
        self.card_frame = QFrame()
        self.card_frame.setObjectName("about_card")
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = os.path.join(os.path.dirname(__file__), "about_image.jpeg")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                320,
                180,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)
        card_layout.addWidget(self.image_label)

        card_layout.addSpacing(4)

        # App Title
        self.title_label = QLabel("Heat Transfer Simulation")
        self.title_label.setObjectName("about_title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title_label)

        # Short Description
        self.description_label = QLabel(
            "An interactive simulation of 1D heat conduction between two physical "
            "bodies connected by a thermal bridge."
        )
        self.description_label.setObjectName("about_description")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.description_label)

        card_layout.addSpacing(6)

        # Author & Course
        self.author_label = QLabel("Developed by Dor")
        self.author_label.setObjectName("about_author")
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.author_label)

        self.course_label = QLabel("Physics on Computer Course")
        self.course_label.setObjectName("about_course")
        self.course_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.course_label)

        # Clickable GitHub Repository link
        self.github_label = QLabel(
            '<a href="https://github.com/Dor64/HeatTransfer" '
            'style="color: #2b6cb0; text-decoration: none;">GitHub Repository</a>'
        )
        self.github_label.setObjectName("about_link")
        self.github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github_label.setOpenExternalLinks(True)
        card_layout.addWidget(self.github_label)

        card_layout.addStretch(1)
        main_layout.addWidget(self.card_frame, 1)

        # Close button row
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    sys.exit(app.exec())
