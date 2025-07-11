from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

COLOR_VISITED = QColor(100, 100, 255)
COLOR_PATH = QColor(255, 255, 0)

def animate_path(canvas, visited, path, steps_label=None):
    total = visited + path
    delay = 10  # ms
    step = 0

    def update():
        nonlocal step
        if step < len(total):
            x, y = total[step]
            if total[step] != canvas.start and total[step] != canvas.end:
                canvas.grid[y][x] = 2 if step < len(visited) else 3
                canvas.update()
                if steps_label:
                    steps_label.setText(f"Steps: {step+1}")
            step += 1
        else:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(delay)
