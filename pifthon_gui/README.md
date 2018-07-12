# [PIFthon](https://github.com/sandipghosal/pifthon)(Python Information Flow Monitor)

PIFthon is a monitor to keep a track of the information flow taking place while compiling a python code.

>[Pifthon Version 1.2](https://github.com/sandipghosal/pifthon) 

Currently it offers reading the labels of objects from a json file and detecting whether it is a secure information flow or an insecure information flow.

##Local Setup Instructions
Clone the project from the source:
```
git clone https://github.com/sandipghosal/pifthon && cd pifthon
```
Installing the requirements :

+ Install PyQt4
```
apt-cache search pyqt
sudo apt-get install python-qt4
```

+ Install SQLite DB Browser from this site :
```
https://sqlitebrowser.org/
```
Running the tool:
```
cd pifthon
```

+ Move into the inputs directory

```
cd inputs
```

+ Run sample case/Add your own python program
```
save this code(if you added your program) and note down the name of this file ( with extension).Call this <program_name_with_.py>
```
+ Move out of this directory
```
cd ..
```

+ Run the command :
```
python3 user_interface.py
```
A small input dialog box will appear in the top-left corner.Enter the path of the :
```
<program_name_with_.py>
```
in the dialog box
+ Next enter the information as asked in the text of the dialog box.You can see the status in the terminal/console window.

+ Once you have entered the information correctly an editor will open.You can navigate to your log file on editor :
```
File > Open > log > (File according to time stamp)
```
and open the most recent file according to the timestamp.

The log file gives you the result.

Once you are done viewing the log file you can close the editor by clicking on the cross button.The execution will be terminated.