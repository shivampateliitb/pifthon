import sys
from PyQt4 import QtGui, QtCore
from PyQt4 import *
import db_manager
import sys
import logging
import datetime
import parse_input_file_1
import abstract_syntax_tree
import user_interface

import dynamic_labelling

class Window(QtGui.QMainWindow):
    #everytime the window object is made the init method runs
    def __init__(self):
       super(Window, self).__init__()
       Window.setGeometry(self, 100, 100, 600, 300)
       self.setWindowTitle("PIFthon Monitor")
       self.setWindowIcon(QtGui.QIcon('./python_icon.png'))
       #main menu
       #general way to make main menu option dropdown
       #1.create the next four lines
       # extractAction = QtGui.QAction("&GET TO THE CHOPPAH",self)
       # extractAction.setShortcut("Ctrl+Q")
       # extractAction.setStatusTip('Leave The App')
       # extractAction.triggered.connect(self.close_application)
       #2.use self.statusBar
       #self.statusBar()
       #3.add it to the main menu object
       # mainMenu = self.menuBar()
       # fileMenu = mainMenu.addMenu('&File')
       #taking the file name from the user
       print("Opening Application")
       file_path = self.obtain_file_name()
       if "/" in file_path:
           length = len(file_path.split("/"))
           file_name = file_path.split("/")[length-1]
       else:
           file_name = file_path
       #this only gives the program_name from program_name.py file
       file_name = file_name.rsplit('.',1)[0]
       #the database corresponding to this program gets created in the DB Browser
       db_manager.create_table(file_name)

       #1.opening file
       openFile = QtGui.QAction('&Open File', self)
       openFile.setShortcut("Ctrl+O")
       openFile.setStatusTip("Open File")
       openFile.triggered.connect(self.file_open)

       ##saving file
       saveFile = QtGui.QAction('&Save File', self)
       saveFile.setShortcut("Ctrl+S")
       saveFile.setStatusTip("Save File") 
       saveFile.triggered.connect(self.file_save)

       #close file
       extractAction = QtGui.QAction("&Close Application",self)
       extractAction.setShortcut("Ctrl+W")
       extractAction.setStatusTip('Leave The App')
       extractAction.triggered.connect(self.close_application)

       #open editor
       openEditor = QtGui.QAction('&Editor', self)
       openEditor.setShortcut("Ctrl+E")
       openEditor.setStatusTip("Open Editor")
       openEditor.triggered.connect(self.editor)
        
       self.statusBar()
       #taking mainMenu object
       mainMenu = self.menuBar()
       #adding file menu option to main menu bar
       fileMenu = mainMenu.addMenu('&File')

       fileMenu.addAction(openFile)
       fileMenu.addAction(saveFile)
       fileMenu.addAction(extractAction)

       #adding editor option to main menu bar
       editorMenu = mainMenu.addMenu('&Editor')
       editorMenu.addAction(openEditor)
       #setting user input dialog box
       #this function takes the input from the user and stores it in the database.
       self.user_input(file_name, file_path)
       
       #to display all the graphics
       

    #function to take the user input from the gui
    def user_input(self, file_name, file_path):
        #getting the file name
        print("Taking input")
        qid = QtGui.QInputDialog(self)
        db_manager.create_table(file_name)
        #inserting the file name and other details of the file into the database
        title = file_name
        label = "******************************************************file info*********************************************************"
        mode = QtGui.QLineEdit().Normal
        default = "Enter the file owner of objects"
        file_owner, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
        default = "Enter the file readers"
        file_readers, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
        default = "Enter the file writers"
        file_writers, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
        db_manager.dynamic_data_entry(file_name, "file", file_name, file_owner, file_readers, file_writers)
        
        #taking information about other objects
        label = "******************************************************Number of Objects*********************************************************"
        mode = QtGui.QLineEdit().Normal
        default = "Enter the number of objects"
        text, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
        text = int(text)
        
        for i in range(text):   

          title = file_name + " : Object"+" "+str(i)
          label = "Enter type of object\n2.global_vars \n3.function_name \n4.outputfile"
          default = "Object "+str(i) +" information "  
          Type, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
          while Type == "":
            default = "Wrong Input!!!Enter again"
            Type, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)

          label = "****************Enter name of object*********************"
          default = "Object "+str(i) +" information "  
          Input, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
          while Input == "":
            default = "Wrong Input!!!Enter again"
            Input, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)

          label = "************************Enter owner of object******************************"
          default = "Object "+str(i) +" information "  
          Owner, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
          while Owner == "":
            default = "Wrong Input!!!Enter again"
            Owner, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)

          label = "*************************Enter readers of object***************************"
          default = "Object "+str(i) +" information "  
          Readers, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
          while Readers == "":
            default = "Wrong Input!!!Enter again"
            Readers, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)

          label = "*************************Enter writers of object*****************************"
          default = "Object "+str(i) +" information "  
          Writers, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
          while Input == "":
            default = "Wrong Input!!!Enter again"
            Input, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)

          db_manager.dynamic_data_entry(file_name, Type, Input, Owner, Readers, Writers)
          print(Type+"    "+Input+"     "+Owner+",{"+Readers+"}, {"+Writers+"}\n")
        print("Input taken")
        self.show()
        print("Opening EDITOR....")
        self.editor()
        self.main(file_name, file_path)

    #taking file name as input
    def obtain_file_name(self):
        qid = QtGui.QInputDialog(self)
        title = "enter input"
        label = "***************File Name***************"
        mode = QtGui.QLineEdit().Normal
        default = "enter the file name(full path)"
        text, ok = QtGui.QInputDialog.getText(qid, title, label, mode, default)
        return text

    #function to save the file
    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close

    #to help open the file
    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name, 'r')
        self.editor()
        with file:
            text = file.read()
            self.textEdit.setText(text)


    #function called when user wants to close the application
    def close_application(self):
        #adding the confirmation query for close application
        choice = QtGui.QMessageBox.question(self, 'Extract', 
                                          "Are you sure you want to quit?",
                                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Exiting now")
            sys.exit()
        else:
            pass
         
    #to add the editor to the gui
    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
    #this is the same main.py file from version 1.1 of pifthon
    def main(self, file_name, file_path):
        # create a log file name with timestamp
        log_file = 'log/pifthon' + str(datetime.datetime.now()).split(' ')[1] + '.log'
        #logging.getLogger().addHandler(logging.StreamHandler())
        logging.basicConfig(filename=log_file, level=logging.DEBUG)
        
        logging.info("\n\n*********** Monitor started **********\n\n")
        logging.info('Parsing %s started' % file_path)
        
        #Obtain the name of the source file
        #input_program contain the path to the source file
        try:

            logging.info('program file name:'+ file_path)
        
            #Obtain security label of executing subject
            #clearance is the highest achievable security label by the executing subject
            clearance = db_manager.read_from_db_file(file_name)
            logging.info('highest achievable label by the executing subject = %s',  clearance.to_string())
        
            #Obtain global variables and their respective security label
            #global_vars is a dictionary containing variable as key and mapped to it's security label
            global_vars = db_manager.read_from_db_global_vars(file_name)
                
            # Obtain subject label given for each function
            func_labels = db_manager.read_from_db_function_label(file_name)

            #the file in which the output is to be printed
            output_file = db_manager.read_from_db_outputfile(file_name)
        except ValueError as e:
            print('ERROR: invalid json: %s' %e)
            logging.warning('****** Monitor Aborted ******')
            sys.exit()
          
        logging.info('Parsing %s is completed' % file_name)
        
        #A abstract syntax tree (AST) named tree is created and populated with the AST of the given program
        tree=abstract_syntax_tree.create_ast(file_path)
        
        ast_file = file_path + '.ast'
        abstract_syntax_tree.write_ast_into_file(tree, ast_file)
        logging.info('AST written into file: %s' % ast_file)
        
        lbl_function = dynamic_labelling.create_labelling_function()
        
        # initialize the functions dictionary of the labelling function
        if func_labels:
            for key in func_labels.keys():
                lbl_function.insert_into_function_list(key, func_labels[key])
        # print(lbl_function.print_function_labels())
        logging.info('%s', lbl_function.print_function_labels())
        
        # initialize the global dictionary of the labelling function
        if global_vars:
            for key in global_vars.keys():
                lbl_function.insert_into_global_list(key, global_vars[key])
        # print(lbl_function.print_global_labels())
        logging.info('%s', lbl_function.print_global_labels())

        #initialize the output_file dictionary
        if output_file:
            for key in output_file.keys():
                lbl_function.insert_into_output_file_list(key, output_file[key])

        logging.info('%s', lbl_function.print_output_file_list())
        
        logging.info('Starting dynamic labelling')
        # Call the labelling function of DynamicLabelling class    
        lbl_function = dynamic_labelling.perform_labelling(ast_file, clearance, lbl_function)
        logging.info('Dynamic labelling completed')
        #to ensure the new details are updated everytime when a program is checked\
        #the database is deleted but if you want to see the database created at the end of execution\
        #comment out these lines and manually delete the INPUT.db file created in the tool's repository
        db_manager.del_and_update(file_name)
        logging.info('Table deleted from the database')
        logging.info("Derived labels of local variables from main file:")
        logging.info('%s' %lbl_function.print_local_labels())
        
        print('Program is information flow secure')
        logging.info("Program is information flow secure")
        logging.info("\n\n*********** Monitor stopped **********\n\n")

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()

