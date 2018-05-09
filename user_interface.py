import sys
from PyQt4 import QtGui

def window():
   app = QtGui.QApplication(sys.argv)
   w = QtGui.QWidget()
   b = QtGui.QLabel(w)
   b.setText("Path to the input python program file:")
   w.setGeometry(0,0,640,480)
   b.move(50,20)
   w.setWindowTitle('Pifthon')
   
   w.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   window()