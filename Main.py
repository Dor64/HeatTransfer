import sys
from pathlib import Path
from PySide6.QtCore import Qt, QTimer
from Body import Body
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

        # add other needed variables
        self.body1 = None
        self.body2 = None
        self.dt = 0.05  # צעד זמן בשניות (50 אלפיות השנייה)
        self.current_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []                        

        # initialize the timer
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.timer_method)    

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

        self.left_slider.valueChanged.connect(self.left_temperature_changed)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)
        self.start_button.clicked.connect(self.start_stop_button_method)

    def open_graph_window(self):
        self.graph_window.show()

    def open_about_window(self):
        self.about_window.show()

    def set_body_color(self, body_frame, temp):
        red = int((temp / 200) * 255)
        red = max(0, min(255, red))
        body_frame.setStyleSheet(f"background-color: rgb({red}, 0, 0); border-radius: 10px;")

    def left_temperature_changed(self):
        temp = self.left_slider.value()
        self.left_temp_label.setText(f"{temp:.1f} °C")
        self.set_body_color(self.left_body_frame, temp)

    def right_temperature_changed(self):
        temp = self.right_slider.value()
        self.right_temp_label.setText(f"{temp:.1f} °C")
        self.set_body_color(self.right_body_frame, temp)

    def start_stop_button_method(self):
        if self.start_button.isChecked():
            m1 = self.left_mass_spinbox.value()
            c1 = self.left_hcap_spinbox.value()
            t1 = self.left_slider.value()
            self.body1 = Body(m1, c1, t1)

            m2 = self.right_mass_spinbox.value()
            c2 = self.right_hcap_spinbox.value()
            t2 = self.right_slider.value()
            self.body2 = Body(m2, c2, t2)

            self.current_time = 0.0
            self.time_history = [0.0]
            self.body1_temp_history = [t1]
            self.body2_temp_history = [t2]

            self.start_button.setText("Stop")
            self.timer.start()
            
        else:
            self.timer.stop()
            self.start_button.setText("Start")

    def timer_method(self):
        sigma = self.conductivity_spinbox.value()
        t1 = self.body1.temperature
        t2 = self.body2.temperature

        # חישוב זרם החום וכמות החום בכל צעד זמן
        i1 = sigma * (t2 - t1)
        i2 = sigma * (t1 - t2)
        dq1 = i1 * self.dt
        dq2 = i2 * self.dt

        # עדכון הגופים וקבלת הטמפרטורות החדשות
        new_t1 = self.body1.add_heat(dq1)
        new_t2 = self.body2.add_heat(dq2)

        self.current_time += self.dt
        self.time_history.append(round(self.current_time, 3))
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        # עדכון הסליידרים בלי להפעיל את הסיגנל כדי לא לדרוס את הדיוק העשרוני
        self.left_slider.blockSignals(True)
        self.left_slider.setValue(int(round(new_t1)))
        self.left_slider.blockSignals(False)

        self.right_slider.blockSignals(True)
        self.right_slider.setValue(int(round(new_t2)))
        self.right_slider.blockSignals(False)

        # עדכון הטמפרטורה המדויקת והצבע של שני הגופים
        self.left_temp_label.setText(f"{new_t1:.1f} °C")
        self.set_body_color(self.left_body_frame, new_t1)

        self.right_temp_label.setText(f"{new_t2:.1f} °C")
        self.set_body_color(self.right_body_frame, new_t2)         


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
