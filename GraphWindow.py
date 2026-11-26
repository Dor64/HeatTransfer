import os
import sys
import csv
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
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

        self.draw_button.clicked.connect(self.draw_graph)
        self.clear_button.clicked.connect(self.clear_graph)
        self.export_button.clicked.connect(self.export_to_csv)

    def draw_graph(self):
     if self.main_window is None or not self.main_window.time_history:
         QMessageBox.information(self, "No Data", "Please run the simulation first.")
         return

     time_data = self.main_window.time_history
     selected_body = self.body_combo.currentText()

     if selected_body == "Body 1":
         self.ax.plot(
             time_data,
             self.main_window.body1_temp_history,
             color="red",
             linewidth=2,
             label="Body 1",
         )
     elif selected_body == "Body 2":
         self.ax.plot(
             time_data,
             self.main_window.body2_temp_history,
             color="blue",
             linewidth=2,
             label="Body 2",
         )

     self.ax.set_xlabel("Time (s)")
     self.ax.set_ylabel("Temperature (°C)")
     self.ax.set_title("Heat Transfer Over Time")
     self.ax.grid(True, linestyle="--", alpha=0.5)
     self.ax.legend()
     self.ax.relim()
     self.ax.autoscale(True)
     self.figure.tight_layout()
     self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_title("Heat Transfer Over Time")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.canvas.draw()

    def export_to_csv(self):
        if self.main_window is None or not self.main_window.time_history:
            QMessageBox.information(self, "No Data", "No simulation data to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "heat_transfer_data.csv", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Body 1 Temperature (°C)", "Body 2 Temperature (°C)"])
            for t, t1, t2 in zip(
                self.main_window.time_history,
                self.main_window.body1_temp_history,
                self.main_window.body2_temp_history,
            ):
                writer.writerow([t, round(t1, 2), round(t2, 2)])

        os.startfile(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec())
