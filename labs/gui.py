from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys
import traceback
import serial

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('КГП')
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.serial = serial.Serial('COM6', 115200, timeout=0.1)

        self.plot_widget = QtWidgets.QWidget()
        self.plot_layout = QtWidgets.QGridLayout()
        self.plot_widget.setLayout(self.plot_layout)
        self.plot_plt = pg.PlotWidget()
        self.plot_plt.showGrid(x=True, y=True)
        self.plot_layout.addWidget(self.plot_plt)
        self.main_layout.addWidget(self.plot_widget, 1, 0, 3, 3)

        self.setCentralWidget(self.main_widget)
        self.plot_plt.setYRange(max=200, min=90)
        self.data_list = []

        self.button = QtWidgets.QPushButton("Start")
        self.button.clicked.connect(self.timer_start)
        self.plot_layout.addWidget(self.button)

        self.button1 = QtWidgets.QPushButton("Stop")
        self.button1.clicked.connect(self.timer_stop)
        self.plot_layout.addWidget(self.button1)

    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_serial_info)
        self.timer.start(300)

    def timer_stop(self):
        self.timer.stop()

    def get_serial_info(self):
        try:
            data = self.serial.readline()
            self.data_list.append(float(data))
            print(float(data))
            self.plot_plt.plot().setData(self.data_list, pen='g')
        except Exception as e:
            print(traceback.print_exc())

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()