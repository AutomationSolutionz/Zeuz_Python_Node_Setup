### Run Test Node Setup Script:
- Run the core setup python file: sudo python TestNode_CoreSetup_Linux.py
- Provide the password for sudo (if asked)

If you are going to be doing iOS and Android Automaiton Follow the instruction below.  If you are doing only Web Automation; Skip everything below.


- Open a new terminal and navigate to Linux folder:
- Note: YOU HAVE TO OPEN A NEW TERMINAL
- Run the first part of the android setup for linux python file: python TestNode_AndroidSetup_Linux_Part_1.py
- Note: DO NOT USE THE SUDO COMMAND 
- Note: If the ruby command seems to hang for more than five minutes, press enter. It may be hiding a sudo password prompt
- Provide the password for sudo (if asked)
- Open a new terminal and navigate to Linux folder:
- Run the first part of the android setup for linux python file: python TestNode_AndroidSetup_Linux_Part_2.py
- Note: DO NOT USE THE SUDO COMMAND
- When the Android SDK Manager window appears, click "Install", then Accept License, and Install (may need to do several times). Close window when done
- Provide the password for sudo (if asked)
- Once all steps are complete, the environment should be setup for Appium testing.