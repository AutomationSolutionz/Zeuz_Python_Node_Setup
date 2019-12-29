#!/usr/bin/env python
# Copyright 2015, Automation Solutionz
# ---
# Function: Installs all required libraries and modules for automation, except for IOS or Android files

import subprocess, re, os, sys  # These modules should be available on every platform
import getpass  # For check_if_ran_with_sudo()

try:
    import subprocess  # We need commands to do anything, so if it's not installed, use subprocess to install it first
except:
    print(
        "Module Commands is missing. I'll attempt to install it manually. If it fails, you'll need to do this yourself: sudo apt-get install python-cmd2.\n")
    print(subprocess.check_output('sudo apt-get install python-cmd2', shell=True))
    import subprocess  # Try to import again

# Import local modules
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))  # Set the path, so the can find the modules
from Crossplatform import CommonUtils

# Global variables
sudo_pass = ''
logfile = "TestNode_Core_Logs.log"

# Libraries and modules to be installed
apt_get_module_list = ["python3-pip", "python3-tk", "python3-setuptools", "libxss1", "libappindicator1",
                       "libindicator7", "python3-dateutil", "python3-xlib", "python3-gi", "curl"]
pip_module_list = ["pip", "psutil", "pillow", "pyserial", "numpy", "imutils", "urllib3", "selenium",
                   "uiautomator", "requests", "wheel","colorama",
                   "pyautogui", "Appium-Python-Client", "lxml", "xlrd", "pyscreenshot", "futures", "image",
                   "tzlocal", "pyautocad", "PyPDF2",
                   "locustio", "realbrowserlocusts", "pyshortcuts"]

# Commands that help with installation
install_str = "pip3 install -U"
apt_get_str = "apt-get -y install"


# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    if type == "pip":
        command = 'echo "%s" | sudo -S %s %s' % (sudo_pass, install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
        print("Installing: %s " % command.replace(sudo_pass, '*****'))
    elif type == "apt-get":
        command = 'echo "%s" | sudo -S %s %s --yes' % (sudo_pass, apt_get_str, module_name)
        print("Installing: %s " % command.replace(sudo_pass, '*****'))
    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd)  # Run command with sudo
    else:
        command = cmd  # Run command exactly as provided
        print("Running: %s " % command.replace(sudo_pass, '*****'))

    status, output = subprocess.getstatusoutput(command)
    print(output)
    if status > 0:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file

    print("\n")
    print((78 * '-'))
    print("\n")
    print("\n")

    return status, output


def Installer_With_Apt_get():
    for each in apt_get_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="apt-get", module_name=each)
        except:
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file


def Installer_With_Pip():
    for each in pip_module_list:
        try:
            if each == "xlwings":
                install(cmd="export INSTALL_ON_LINUX=1")
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            if each == 'psutil': continue  # This is expected to fail if installed
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file


def Install_Chrome_Drivers():
    import requests

    print((78 * '-'))
    sys.stdout.write("Installing: Chrome libraries\n", True)  # Print to terminal window, and log file
    print((78 * '-'))

    # Cleanup any outstanding package issues
    try:
        sys.stdout.write("Configuring: dpkg\n", True)
        install(type="sudo", cmd="dpkg --configure -a")
    except:
        sys.stdout.error("\tError configuring - See log file\n")

    # Get latest version
    try:
        """
        version compatibility selection steps is followed from,
        https://sites.google.com/a/chromium.org/chromedriver/downloads/version-selection
        
        """
        chrome_version = subprocess.getoutput('google-chrome --version')
        chrome_version = chrome_version.split()[-1]
        chrome_version_number = ".".join(chrome_version.split('.')[:-1])

        sys.stdout.write("Downloading: Chromedriver\n", True)
        print("Getting compatible version of chrome driver")
        r = requests.get('http://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(chrome_version_number))
        # r = http.request('GET', 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        latest_version = r.text.split('\n')[0]
        print("latest version is: %s" % latest_version)
    except Exception as e:
        print("Chrome Exception: ", e)
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        return

    # Download & Install
    download_link = ('http://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip' % latest_version)
    try:
        # Download
        print("Downloading latest Chrome driver from: %s" % download_link)
        install(type="apt-get", module_name="unzip")
        # install(cmd="wget -N " + download_link)
        CommonUtils.Download_File(download_link)

        # Unpack
        sys.stdout.write("Unpacking: Chrome driver\n", True)  # Print to terminal window, and log file
        install(cmd="unzip -o chromedriver_linux64.zip")

        # Install
        sys.stdout.write("Installing: Chrome driver\n", True)  # Print to terminal window, and log file
        print("Make executable")
        install(cmd="chmod +x chromedriver")
        print("Move to file system")
        install(type="sudo", cmd="mv -f chromedriver /usr/local/share/chromedriver")
        print("Create links")
        install(type="sudo", cmd="ln -f -s /usr/local/share/chromedriver /usr/local/bin/chromedriver")
        install(type="sudo", cmd="ln -f -s /usr/local/share/chromedriver /usr/bin/chromedriver")
    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file

    try:
        install(cmd="rm chromedriver_linux64.zip")
    except Exception as e:
        pass


def Install_Firefox_Drivers():
    import requests # Here because it needs to be imported after we install it

    # Cleanup any outstanding package issues
    try:
        sys.stdout.write("Configuring: dpkg\n", True)
        install(type="sudo", cmd="dpkg --configure -a")
    except Exception as e:
        sys.stdout.error("\tError configuring - See log file\n")

    try:
        sys.stdout.write("Installing: Firefox driver\n", True)  # Print to terminal window, and log file
        r = requests.get('https://github.com/mozilla/geckodriver/releases/latest')
        raw_data = r.text.split('\n')
        latest_version = ''
        for each in raw_data:
            if '<span class="css-truncate-target"' in each:
                result = re.search('v(.*)</span>', each)
                latest_version = "v" + result.group(1)
                print("Latest geckodriver for Firefox is: %s" % latest_version)
                break
    except Exception as e:
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        return

    download_link = ('https://github.com/mozilla/geckodriver/releases/download/%s/geckodriver-%s-linux64.tar.gz') % (
    latest_version, latest_version)
    download_link = str(download_link)
    print("Downloading latest 64bit geckodriver from: %s" % download_link)
    # install(cmd="wget -N " + download_link)
    CommonUtils.Download_File(download_link)

    geckodriver_cmd = ('tar -xvzf geckodriver-%s-linux64.tar.gz') % (latest_version)
    geckodriver_cmd = str(geckodriver_cmd)
    install(cmd=geckodriver_cmd)
    install(cmd="chmod +x geckodriver")
    install(type="sudo", cmd="mv -f geckodriver /usr/local/share/geckodriver")
    install(type="sudo", cmd="ln -f -s /usr/local/share/geckodriver /usr/local/bin/geckodriver")
    install(type="sudo", cmd="ln -f -s /usr/local/share/geckodriver /usr/bin/geckodriver")
    install(cmd='rm geckodriver-%s-linux64.tar.gz' % (latest_version))


def Install_Easy_Installer():
    try:

        items_to_install = ['hashlib', 'https://github.com/AutomationSolutionz/PyGetWindow-0.0.5/archive/master.zip']

        for each in items_to_install:
            try:
                sys.stdout.write("Installing: %s\n" % each, True)
                cmd = "easy_install %s" % each  # !!! Not working. Not sure why - repository exists
                output = os.system(cmd)
                print(output)
                print((78 * '-'))
            except:
                sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
                print("Unable to install %s" % each)

    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        print("Unable to install %s" % each)


def Install_PIP():
    # we should not have to do this ...
    print((78 * '-'))
    sys.stdout.write("Installing: pip\n", True)  # Print to terminal window, and log file
    print((78 * '-'))
    install(type="sudo", cmd="add-apt-repository universe")
    install(type="sudo", cmd="sudo apt-get update --yes")
    install(type="apt-get", module_name="python-pip")


def Install_OpenCV():  # !!! NO LONGER USED !!!
    print((78 * '-'))
    sys.stdout.write("Installing: OpenCV\n", True)  # Print to terminal window, and log file
    print((78 * '-'))
    try:
        os.system("sudo chmod 777 ../backupDriverFiles/Desktop/opencv.sh")
        os.system("./../backupDriverFiles/Desktop/opencv.sh")
        os.system("sudo apt-get install python-opencv")
    except:
        print("unable to install/update OpenCV")
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file


def OS_Version():
    print((78 * '-'))
    sys.stdout.write("Linux Version:\n", True)  # Print to terminal window, and log file
    print((78 * '-'))
    command = "lsb_release -a"
    status, output = subprocess.getstatusoutput(command)
    sys.stdout.write("%s\n" % output, True)  # Print to terminal window, and log file
    sys.stdout.write("\n", True)  # Print to terminal window, and log file


def check_if_ran_with_sudo():
    global sudo_pass
    sudo_pass = None
    if os.getuid() == 0:
        return True
    else:
        max_try = 3
        counter = 0
        have_pass = False
        while counter != max_try:
            print("This program needs sudo access.  please provide sudo password")
            passwd = getpass.getpass()
            print("checking to see if you have entered correct sudo")
            command = "echo 'sudo check'"
            p = os.system('echo %s|sudo -S %s' % (passwd,
                                                  command))  # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
            if p == 256:
                print("You didnt enter the correct sudo password.  Chances left: %s" % (max_try - counter - 1))
                counter = counter + 1
            else:
                print("sudo authentication verified!")
                have_pass = True
                break
        if have_pass == False:
            return False
        else:
            sudo_pass = passwd
            return True


def main(rungui=False):
    if rungui:  # GUI will only run this if it already has the password, and it's verified
        global sudo_pass
        sudo_pass = rungui  # Save password
    else:
        # Make sure we have root privleges
        if check_if_ran_with_sudo():
            print("Running with root privs\n")
        else:
            print("Error - Need root privleges\n")
            quit()

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Perform installation
    OS_Version()
    Installer_With_Apt_get()
    Install_Easy_Installer()
    Installer_With_Pip()
    Install_Chrome_Drivers()
    Install_Firefox_Drivers()

    sys.stdout.write("If Android testing is required, please run the Android installer\n", True)

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__ == "__main__":
    main()
