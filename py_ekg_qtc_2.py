from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import numpy as np
import math
import sys
import glob

##------------------------------------------------------------ 

class main_window(QtGui.QWidget):
    
    def __init__(self):
        super(main_window, self).__init__()
        self.initUI()
        
    def initUI(self):
        layout = QtGui.QGridLayout()
        self.p = pg.PlotWidget()

        r1_pen = QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.SolidLine)
        self.r1_line = self.p.addLine(x=.5, pen=r1_pen, movable=True)
        self.r1_line.sigPositionChangeFinished.connect(self.r1_move)
        
        r2_pen = QtGui.QPen(QtCore.Qt.darkYellow, 0 , QtCore.Qt.SolidLine)
        self.r2_line = self.p.addLine(x=1, pen=r2_pen, movable=True)
        self.r2_line.sigPositionChangeFinished.connect(self.r2_move)
 
        q_pen = QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine)
        self.q_line = self.p.addLine(x=1.5, pen=q_pen, movable=True)
        self.q_line.sigPositionChangeFinished.connect(self.q_move)

        t_pen = QtGui.QPen(QtCore.Qt.blue, 0, QtCore.Qt.SolidLine)
        self.t_line = self.p.addLine(x=2, pen=t_pen, movable=True)
        self.t_line.sigPositionChangeFinished.connect(self.t_move)
        
        timer_btn = QtGui.QPushButton('Collect Data',self)
        timer_btn.clicked.connect(self.timer_toggle)
        
        calc_btn = QtGui.QPushButton('Calc',self)
        calc_btn.clicked.connect(self.calc_qtc)
        
        quit_btn = QtGui.QPushButton('Quit',self) 
        quit_btn.clicked.connect(self.quit_button)

        self.timer_lbl = QtGui.QLabel('Waiting to Capture')
        
        r1_lbl = QtGui.QLabel('R1 = ')
        self.r1_val_lbl = QtGui.QLabel('0')
        r1_palette = QtGui.QPalette()
        r1_palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        r1_lbl.setPalette(r1_palette)
        
        r2_lbl = QtGui.QLabel('R2 = ')
        self.r2_val_lbl = QtGui.QLabel('0')
        r2_palette = QtGui.QPalette()
        r2_palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.darkYellow)
        r2_lbl.setPalette(r2_palette)
        
        q_lbl = QtGui.QLabel('Q = ')
        self.q_val_lbl = QtGui.QLabel('0')
        q_palette = QtGui.QPalette()
        q_palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.green)
        q_lbl.setPalette(q_palette)
        
        t_lbl = QtGui.QLabel('T = ')
        self.t_val_lbl = QtGui.QLabel('0')
        t_palette = QtGui.QPalette()
        t_palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.blue)
        t_lbl.setPalette(t_palette)

        rr_lbl = QtGui.QLabel('RR = ')
        self.rr_val_lbl = QtGui.QLabel('0')

        h_lbl = QtGui.QLabel('HeartRate = ')
        self.h_val_lbl = QtGui.QLabel('0')

        qt_lbl = QtGui.QLabel('QT = ')
        self.qt_val_lbl = QtGui.QLabel('0')
        
        qtc_lbl = QtGui.QLabel('QTc = ')
        self.qtc_val_lbl = QtGui.QLabel('0')

        layout.addWidget(timer_btn,         0, 0)   
        layout.addWidget(self.timer_lbl,    0, 1)
        layout.addWidget(r1_lbl,            1, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.r1_val_lbl,   1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(r2_lbl,            2, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.r2_val_lbl,   2, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(q_lbl,             3, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.q_val_lbl,    3, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(t_lbl,             4, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.t_val_lbl,    4, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(calc_btn,          5, 0)
        layout.addWidget(h_lbl,             6, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.h_val_lbl,    6, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(h_lbl,             7, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.h_val_lbl,    7, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(qt_lbl,            8, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.qt_val_lbl,   8, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(qtc_lbl,           9, 0, QtCore.Qt.AlignRight)
        layout.addWidget(self.qtc_val_lbl,  9, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(quit_btn,          10, 0)   
        layout.addWidget(self.p,            0, 2, 10, 5)

        self.setLayout(layout)

    def calc_qtc(self):
        r1 = self.r1_line.value()
        r2 = self.r2_line.value()
        q = self.q_line.value()
        t = self.t_line.value()

        rr = r2-r1
        self.rr_val_lbl.setText(str("%.3f" % rr))
        
        h = 60/(r2-r1)
        self.h_val_lbl.setText(str("%.3f" % h))

        qt = (t - q)
        self.qt_val_lbl.setText(str("%.3f" % qt))
        
        qtc = (t - q)/math.sqrt(r2-r1)
        self.qtc_val_lbl.setText(str("%.3f" % qtc))

    def quit_button(self):
        timer.stop()
        self.close()

    def timer_toggle(self):
        global ptr, data, tline
        if (timer.isActive()):
            timer.stop()
            self.timer_lbl.setText('Captured ' + str("%.3f" % ptr) + ' sec')
            ydata = np.array(data,dtype='float64')
            xdata = np.array(tline,dtype='float64')
            curve.setData(xdata,ydata)
            ptr = 0
            data = [512]
            tline = [0]
            app.processEvents()            
        else:
            self.timer_lbl.setText('Capturing')
            timer.start(0)

    def r1_move(self):
        r1 = self.r1_line.value() 
        self.r1_val_lbl.setText(str("%.3f" % r1))

    def r2_move(self):
        r2 = self.r2_line.value() 
        self.r2_val_lbl.setText(str("%.3f" % r2))

    def q_move(self):
        q = self.q_line.value()
        self.q_val_lbl.setText(str("%.3f" % q))

    def t_move(self):
        t = self.t_line.value() 
        self.t_val_lbl.setText(str("%.3f" % t))
        
##------------------------------------------------------------        
class ListPortsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ListPortsDialog, self).__init__(parent)
        self.setWindowTitle('List of serial ports')

        self.ports_list = QtGui.QListWidget()
        self.tryopen_button = QtGui.QPushButton('Try to open')
        self.tryopen_button.clicked.connect(self.on_tryopen)

        quit_btn = QtGui.QPushButton('Continue',self) 
        quit_btn.clicked.connect(self.quit_button)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ports_list)
        layout.addWidget(self.tryopen_button)
        layout.addWidget(quit_btn)
        self.setLayout(layout)

        self.fill_ports_list()

    def quit_button(self):
        self.close()

    def on_tryopen(self):
        global port_name
        
        cur_item = self.ports_list.currentItem()
        
        if cur_item is not None:
            port_name = str(cur_item.text())
            ##print(port_name)
            try:
                ser = serial.Serial(port_name, 57600)
                ser.close()
                QtGui.QMessageBox.information(self, 'Success',
                    'Opened %s successfully' % cur_item.text())
            except SerialException as e:
                QtGui.QMessageBox.critical(self, 'Failure',
                    'Failed to open %s:\n%s' % (
                        cur_item.text(), e))

    def fill_ports_list(self):
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            comports = None

        if comports:
            sys.stderr.write('\n--- Available ports:\n')
            for port in sorted(comports()):
                print(port)
                self.ports_list.addItem(port[0])

##------------------------------------------------------------
def readData():
    global data, ptr, port, tline
    if (port.inWaiting() > 0):
        ptr += .0039
        line = float(port.readline().strip())
        if (line >= 1024.0):
            line = 1024.0
        port.flush();
        data.append(line)
        tline.append(ptr)

##------------------------------------------------------------
if __name__ == '__main__':
    global curve, data, ptr, port, tline, port_name

    ser_app = QtGui.QApplication(sys.argv)
    form = ListPortsDialog()
    form.show()
    ser_app.exec()

    ptr = 0
    data = [512]
    tline = [0]
    
    app = QtGui.QApplication(sys.argv)
    ex = main_window()
    ex.show()
    
    curve = ex.p.plot()

    port = serial.Serial(port_name, 57600)

    timer = QtCore.QTimer()
    timer.timeout.connect(readData)

    sys.exit(app.exec_())
    port.close()
    
