import os
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        style_path = os.path.join(os.path.dirname(__file__), "style.css")
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.resize(650, 450)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Left side: Matplotlib canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)
        self.figure.tight_layout()

        self.canvas = FigureCanvasQTAgg(self.figure)
        main_layout.addWidget(self.canvas, 1)

        # Right side: Controls column
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        controls_layout.addWidget(self.body_combo)

        self.draw_button = QPushButton("Draw")
        controls_layout.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        controls_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export to CSV")
        controls_layout.addWidget(self.export_button)

        controls_layout.addStretch(1)
        main_layout.addLayout(controls_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec())
