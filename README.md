# For Core Test Node Setup
### Pre-Setup Requirements: 
         . You have already setup ZEUZ Server
         . Make sure you have admin rights and internet connection.  Based on your connection speed, it may take anywhere between 10-30 minutes.
         . Make sure Python 2.7 is installed & set in your env variables:  Verify by opening Terminal -> Type "python" should open Python Terminal
         . Make sure PIP is installed: Verify by opening Terminal -> Type "python -m pip" should display help file - Instructions for installing pip: https://pip.pypa.io/en/latest/installing/
         . Make sure easy_install is installed: Verify by opening Terminal -> Type "easy_install" should display help file - Instructions for installing easy_install: https://pypi.python.org/pypi/setuptools


### Run ZEUZ Test Node Setup Script:
         . Navigate to ../Framework_0.1/Automationz/AutomationSetup/AutomationSetup
         . Run by typing "python TestNode_CoreSetup_Windows.py" or "python TestNode_CoreSetup_Linux.py" or "python TestNode_CoreSetup_Mac.py"
         . This script will install all dependent PIP Modules
         . While running multiple scripts one after another, be sure to run each script in a new terminal/command line prompt.

### Verify ZEUZ Test Node is setup correctly
	 . Navigate to ../Framework_0.1/Automationz/AutomationFW/CoreFramework
	 . Modify following Test Node Configuration in Login.conf & Global.py
		. Username/Password/Project/Team
		. Server
		. Branch
		. Dependency
	 . Run "python AS.py"
	 . If everything is working as expected, you should see the following in the terminal,
                # Running on Test Environment...
                # Username =  <username>  : Project =  <Project>  : Team =  <Team>
                # All the dependency present in the configuration file - Login.conf
	 . At this point using your browser navigate to ZEUZ Dashboard
	 . Login with your Credentials
	 . Navigate To Testing -> Run -> Assign -> Available Machines 
	 . Your Test Node Machine should appear under 'Available Machines'
	 . You can kick off the sameple Test on Test Node now

Note: In case of any issues with Test Node Setup, contact us at info@automationsolutionz.com [Please do attach TestNode_Installer_Logs]



---------------------------
### For Android Test Node Setup
### Pre-Setup Requirements: 
         . ZEUZ Test Node was setup successful
         . You can run Tests on Test Node via ZEUZ webpage
	     . Run python TestNode_AndroidSetup_Windows.py or TestNode_AndroidSetup_Linux.py

If you want to do android automation then please do follow the following steps:

- Install Android SDK (http://developer.android.com/sdk/index.html)
- Set the ADT_HOME and ANDROID_HOME in environment variable.
-  ADT_HOME and ANDROID_HOME both should be the default android sdk root directory
- Now add this following line to path variable.
	%ADT_HOME%\tools;%ADT_HOME%\platform-tools;%ANT_HOME%\bin;%MAVEN_HOME%\bin;
- Put the phone in developement mode from development options
- If no developer options are found, then go to Settings->About->BuildNumber. tap 7 times on it
- Put Tick on USB debugging in the Developer Options
- Allow apps to install from unknown sources on device settings.

### Verify Android Setup: 
         . connect your android device using usb with your PC.
         . Open Terminal -> Type "adb devices" -> Should list connected android device
