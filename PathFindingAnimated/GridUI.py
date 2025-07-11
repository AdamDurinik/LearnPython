from PyQt5.QtWidgets import (
    QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
import sys
import time

from config import *
from PathAlgorithms import bfs, dfs, dijkstra, astar, greedy
from Animator import animate_path

class GridCanvas(QFrame):
    def __init__(self, rows, cols, cell_size, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.setFixedSize(cols * cell_size, rows * cell_size)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None
        self.setMouseTracking(True)
        self.mouse_down = False
        self.mouse_button = None

    def mousePressEvent(self, event):
        self.mouse_down = True
        self.mouse_button = event.button()
        self.modify_grid(event)

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        self.mouse_button = None

    def mouseMoveEvent(self, event):
        if self.mouse_down:
            self.modify_grid(event)

    def modify_grid(self, event):
        x = event.x() // self.cell_size
        y = event.y() // self.cell_size
        if 0 <= x < self.cols and 0 <= y < self.rows:
            if self.mouse_button == Qt.RightButton:
                if (x, y) == self.start:
                    self.start = None
                elif (x, y) == self.end:
                    self.end = None
                else:
                    self.grid[y][x] = 0
            else:  # Left click
                if not self.start:
                    self.start = (x, y)
                elif not self.end and (x, y) != self.start:
                    self.end = (x, y)
                elif (x, y) != self.start and (x, y) != self.end:
                    self.grid[y][x] = 1
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        for y in range(self.rows):
            for x in range(self.cols):
                rect_x = x * self.cell_size
                rect_y = y * self.cell_size
                if (x, y) == self.start:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_START))
                elif (x, y) == self.end:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_END))
                elif self.grid[y][x] == 1:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_WALL))
                elif self.grid[y][x] == 2:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_VISITED))
                elif self.grid[y][x] == 3:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_PATH))
                else:
                    qp.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(*COLOR_EMPTY))
                qp.setPen(QColor(200, 200, 200))
                qp.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

    def reset(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.end = None
        self.update()


class GridApp(QWidget):
    def __init__(self, grid_w, grid_h, cell_size):
        super().__init__()
        self.setWindowTitle("Pathfinding Visualizer")
        self.setLayout(QHBoxLayout())

        self.canvas = GridCanvas(grid_h, grid_w, cell_size)
        self.layout().addWidget(self.canvas)

        self.algorithm = "BFS"
        self.steps_label = QLabel("Steps: 0")
        self.time_label = QLabel("Time: 0 ms")

        self.init_ui()
        self.show()

    def init_ui(self):
        control_panel = QVBoxLayout()

        control_panel.addWidget(QLabel("Select Algorithm:"))
        algo_buttons = QButtonGroup(self)

        for name in ["BFS", "DFS", "Dijkstra", "A*", "Greedy"]:
            btn = QRadioButton(name)
            if name == "BFS":
                btn.setChecked(True)
            algo_buttons.addButton(btn)
            control_panel.addWidget(btn)

        def on_algo_changed():
            for btn in algo_buttons.buttons():
                if btn.isChecked():
                    self.algorithm = btn.text()

        algo_buttons.buttonClicked.connect(on_algo_changed)

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.run_algorithm)
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.canvas.reset)
        self.step_mode = False
        self.step_data = []  # holds visited + path
        self.step_index = 0

        step_mode_btn = QPushButton("Step Mode")
        step_mode_btn.clicked.connect(self.enable_step_mode)

        next_btn = QPushButton("Next Step")
        next_btn.clicked.connect(self.advance_step)
        control_panel.addWidget(start_btn)
        control_panel.addWidget(reset_btn)
        control_panel.addWidget(self.steps_label)
        control_panel.addWidget(self.time_label)
        control_panel.addWidget(step_mode_btn)
        control_panel.addWidget(next_btn)
        control_panel.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(control_panel)
        self.layout().addWidget(right_widget)

    def enable_step_mode(self):
        if not self.canvas.start or not self.canvas.end:
            return

        for y in range(len(self.canvas.grid)):
            for x in range(len(self.canvas.grid[0])):
                if self.canvas.grid[y][x] in (2, 3):
                    self.canvas.grid[y][x] = 0
        self.canvas.update()

        algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "Dijkstra": dijkstra,
            "A*": astar,
            "Greedy": greedy
        }

        fn = algorithms[self.algorithm]
        visited, path = fn(self.canvas.grid, self.canvas.start, self.canvas.end)

        self.step_data = visited + path
        self.step_index = 0
        self.step_mode = True
        self.time_label.setText("Step mode active")
        self.steps_label.setText("Steps: 0")

    def advance_step(self):
        if not self.step_mode or self.step_index >= len(self.step_data):
            return

        x, y = self.step_data[self.step_index]
        if (x, y) != self.canvas.start and (x, y) != self.canvas.end:
            self.canvas.grid[y][x] = 2 if self.step_index < len(self.step_data) - len(path) else 3
            self.canvas.update()
            self.steps_label.setText(f"Steps: {self.step_index + 1}")
        self.step_index += 1


    def run_algorithm(self):
        if not self.canvas.start or not self.canvas.end:
            return

        algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "Dijkstra": dijkstra,
            "A*": astar,
            "Greedy": greedy
        }
        fn = algorithms[self.algorithm]

        for y in range(len(self.canvas.grid)):
            for x in range(len(self.canvas.grid[0])):
                if self.canvas.grid[y][x] in (2, 3):
                    self.canvas.grid[y][x] = 0
        self.canvas.update()

        grid = self.canvas.grid
        start = self.canvas.start
        end = self.canvas.end

        start_time = time.time()
        visited, path = fn(grid, start, end)
        elapsed = int((time.time() - start_time) * 1000)

        self.steps_label.setText(f"Steps: {len(visited)}")
        self.time_label.setText(f"Time: {elapsed} ms")

        animate_path(self.canvas, visited, path, self.steps_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GridApp(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    sys.exit(app.exec_())
