from PyQt5.QtWidgets import QApplication
import sys
from GridUI import GridApp
from config import *

def main():
    app = QApplication(sys.argv)
    window = GridApp(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
