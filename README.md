# Ladderface

### How to create an .exe file

1. First install pygame and pytmx:

   `pip install pygame-ce`

   `pip install pytmx`

2. Install auto-py-to-exe converter:

   `pip install auto-py-to-exe`

   (https://pypi.org/project/auto-py-to-exe/)

   and then run it:  `auto-py-to-exe`

3. Inside the window:
     - for Script Location choose the main project file: **main.py**
     - for Onefile choose **One Directory**
     - for Console Window choose **Window Based**
     - at Additional Files choose **Add Folder** and choose the project folder
  
     - click on **CONVERT .PY TO .EXE** button
  
4. Open the output folder. Inside **main** folder there is now a **main.exe** file.
   If there are some File Not Found exceptions found when running, copy the project files in the folder with the **main.exe** file and run it again.


