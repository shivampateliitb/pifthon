# [PIFthon](https://github.com/sandipghosal/pifthon)(Python Information Flow Monitor)

PIFthon is a monitor to keep a track of the information flow taking place while compiling a python code.

>[Pifthon Version 1.1](https://github.com/sandipghosal/pifthon) 

Currently it offers reading the labels of objects from a json file and detecting whether it is a secure information flow or an insecure information flow.

##Local Setup Instructions
Clone the project from the source:
```
git clone https://github.com/sandipghosal/pifthon && cd pifthon
```
Installing the requirements :
```
pip install -r requirements.txt
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
+ Open the input.json file
```
gedit input.json
```

+ Modify this json to suit your need and don't forget to save the file.You may need to change the labels of the entities involved in your program.Identify the labels as
```
1.file
2.function name
3.global variables
4.output file(if any)
```
After you have set the labels : 

```
in the 4th line change the value of key "path" to inputs/<program_name_with_.py>
```
+ Move out of this directory
```
cd ..
```
+ Run the main.py file 
```
shell
python3 main.py inputs/input.json
```
This creates an ast file saved in the inputs directory, to see this file:
```
cd inputs
gedit <program_name_with_.py>.ast
```
To see the output:
```
cd log
```
and open the most recent file according to the timestamp.

The log file gives you the result.
Here is a demo for the using this tool :
![Demo](https://user-images.githubusercontent.com/28708494/42624749-cb27366a-85e3-11e8-9969-df122db10d61.gif)