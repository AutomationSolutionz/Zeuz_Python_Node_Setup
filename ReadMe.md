# ZeuZ Python Node Setup

## Project Requirements:
- Python version >=3.6
- Git

## Project Setup for UNIX systems:

Setup:
1. Check python3 version by typing “python3 --version”. Make sure you have python version 3.6
or above. If your python version is less than 3.6 then follow this link to install python3.8 on mac.
2. Cd into the downloaded ZeuzPythonNodeSetup directory. Like if the downloaded folder is in
downloads then type command “cd ~/Downloads/ZeuzPythonNodeSetup”.
3. Type the command “source start_venv.sh”. The script will create a virtualenv and activate it
and will show the gui installer.
4. Give the sudo password and then Click install when the gui popup appears. Make sure core
setup and install zeuz node is selected before clicking install button.
5. Quit the installer.
6. Again start the gui by command “source start_venv.sh”. Now unselect the defaults and select
ios/android setup according to your needs. Click install again.

Run :
Make sure you have already done setup following the setup instructions mentioned above.
In the setup process we have automatically created a virtualenv folder named “node_env” inside
ZeuzPythonNodeSetup directory. We should activate it before proceeding to next instructions.
1. Cd on to ZeuzPythonNodeSetup directory by command “cd
~/Downloads/ZeuzPythonNodeSetup” if it is in Downloads folder and activate the virtualenv by
typing “source node_env/bin/activate”.
2. Go to the Zeuz_Node directory from that terminal by typing “cd <Zeuz_Node folder path>”. For
example, if Zeuz_Node is in desktop, then type “cd ~/Desktop/Zeuz_Node”.
3. Run “python node_cli.py” or “python node_gui.py”
