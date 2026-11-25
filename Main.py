import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from AboutWindow import AboutWindow
from GraphWindow import GraphWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        # add other window variables here
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)

        style_path = Path(__file__).with_name("style.css")
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.resize(680, 440)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Top Section: Sliders, Bodies, and Conductivity Bridge ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        # Left vertical slider
        self.left_slider = QSlider(Qt.Orientation.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        top_layout.addWidget(self.left_slider)

        # Bodies + Bridge sub-layout (0 spacing so the bridge touches both bodies)
        bodies_layout = QHBoxLayout()
        bodies_layout.setSpacing(0)

        # Left body
        self.left_body_frame = QFrame()
        self.left_body_frame.setObjectName("left_body_frame")
        self.left_body_frame.setMinimumSize(150, 220)
        self.left_body_frame.setStyleSheet(
            "background-color: rgb(255, 0, 0); border-radius: 16px;"
        )
        bodies_layout.addWidget(self.left_body_frame, 1)

        # Center bridge column
        bridge_column_layout = QVBoxLayout()
        bridge_column_layout.setContentsMargins(0, 0, 0, 0)
        bridge_column_layout.setSpacing(6)
        bridge_column_layout.addStretch(1)

        conductivity_controls_layout = QVBoxLayout()
        conductivity_controls_layout.setContentsMargins(16, 0, 16, 4)
        conductivity_controls_layout.setSpacing(4)

        self.conductivity_label = QLabel("Conductivity")
        self.conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conductivity_controls_layout.addWidget(self.conductivity_label)

        self.conductivity_spinbox = QDoubleSpinBox()
        self.conductivity_spinbox.setRange(0.01, 1000.0)
        self.conductivity_spinbox.setDecimals(2)
        self.conductivity_spinbox.setValue(1.00)
        self.conductivity_spinbox.setSuffix(" J/s°C")
        self.conductivity_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conductivity_controls_layout.addWidget(self.conductivity_spinbox)

        bridge_column_layout.addLayout(conductivity_controls_layout)

        self.bridge_frame = QFrame()
        self.bridge_frame.setObjectName("bridge_frame")
        self.bridge_frame.setFixedHeight(22)
        bridge_column_layout.addWidget(self.bridge_frame)

        bridge_column_layout.addStretch(1)
        bodies_layout.addLayout(bridge_column_layout)

        # Right body
        self.right_body_frame = QFrame()
        self.right_body_frame.setObjectName("right_body_frame")
        self.right_body_frame.setMinimumSize(150, 220)
        self.right_body_frame.setStyleSheet(
            "background-color: rgb(0, 0, 0); border-radius: 16px;"
        )
        bodies_layout.addWidget(self.right_body_frame, 1)

        top_layout.addLayout(bodies_layout, 1)

        # Right vertical slider
        self.right_slider = QSlider(Qt.Orientation.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        top_layout.addWidget(self.right_slider)

        main_layout.addLayout(top_layout, 1)

        # --- Bottom Section: Controls and Buttons ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(25)

        # Left controls (under left body)
        left_controls_layout = QGridLayout()
        left_controls_layout.setHorizontalSpacing(10)
        left_controls_layout.setVerticalSpacing(8)

        self.left_temp_label = QLabel("200.0 °C")
        self.left_temp_label.setObjectName("temp_display")

        self.left_mass_spinbox = QDoubleSpinBox()
        self.left_mass_spinbox.setRange(0.01, 1000.0)
        self.left_mass_spinbox.setDecimals(2)
        self.left_mass_spinbox.setValue(10.00)
        self.left_mass_spinbox.setSuffix(" kg")

        self.left_hcap_spinbox = QDoubleSpinBox()
        self.left_hcap_spinbox.setRange(0.01, 10000.0)
        self.left_hcap_spinbox.setDecimals(2)
        self.left_hcap_spinbox.setValue(0.40)
        self.left_hcap_spinbox.setSuffix(" J/kg°C")

        left_controls_layout.addWidget(QLabel("Temp."), 0, 0)
        left_controls_layout.addWidget(self.left_temp_label, 0, 1)
        left_controls_layout.addWidget(QLabel("Mass"), 1, 0)
        left_controls_layout.addWidget(self.left_mass_spinbox, 1, 1)
        left_controls_layout.addWidget(QLabel("H. Cap."), 2, 0)
        left_controls_layout.addWidget(self.left_hcap_spinbox, 2, 1)

        bottom_layout.addLayout(left_controls_layout, 1)

        # Center buttons (under bridge)
        center_buttons_layout = QVBoxLayout()
        center_buttons_layout.setSpacing(8)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("start_button")
        self.start_button.setCheckable(True)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.clicked.connect(self.open_graph_window)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.open_about_window)

        center_buttons_layout.addWidget(self.start_button)
        center_buttons_layout.addWidget(self.graphs_button)
        center_buttons_layout.addWidget(self.about_button)

        bottom_layout.addLayout(center_buttons_layout)

        # Right controls (under right body)
        right_controls_layout = QGridLayout()
        right_controls_layout.setHorizontalSpacing(10)
        right_controls_layout.setVerticalSpacing(8)

        self.right_temp_label = QLabel("0.0 °C")
        self.right_temp_label.setObjectName("temp_display")

        self.right_mass_spinbox = QDoubleSpinBox()
        self.right_mass_spinbox.setRange(0.01, 1000.0)
        self.right_mass_spinbox.setDecimals(2)
        self.right_mass_spinbox.setValue(10.00)
        self.right_mass_spinbox.setSuffix(" kg")

        self.right_hcap_spinbox = QDoubleSpinBox()
        self.right_hcap_spinbox.setRange(0.01, 10000.0)
        self.right_hcap_spinbox.setDecimals(2)
        self.right_hcap_spinbox.setValue(0.40)
        self.right_hcap_spinbox.setSuffix(" J/kg°C")

        right_controls_layout.addWidget(QLabel("Temp."), 0, 0)
        right_controls_layout.addWidget(self.right_temp_label, 0, 1)
        right_controls_layout.addWidget(QLabel("Mass"), 1, 0)
        right_controls_layout.addWidget(self.right_mass_spinbox, 1, 1)
        right_controls_layout.addWidget(QLabel("H. Cap."), 2, 0)
        right_controls_layout.addWidget(self.right_hcap_spinbox, 2, 1)

        bottom_layout.addLayout(right_controls_layout, 1)

        main_layout.addLayout(bottom_layout)

    def open_graph_window(self):
        self.graph_window.show()

    def open_about_window(self):
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
