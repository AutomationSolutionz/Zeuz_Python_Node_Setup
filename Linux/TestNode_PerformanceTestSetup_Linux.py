#!/usr/bin/env python
# Copyright 2015, Automation Solutionz
# ---
# Function: Installs all required libraries and modules for automation, except for IOS or Android files

import subprocess, re, os, sys  # These modules should be available on every platform
import getpass  # For check_if_ran_with_sudo()

# Import local modules
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))  # Set the path, so the can find the modules
from Crossplatform import CommonUtils

# Global variables
sudo_pass = ''
logfile = "TestNode_PerformanceTest_Logs.log"

# Libraries and modules to be installed
pip_module_list = [
    "wheel","locustio", "realbrowserlocusts"
]

# Commands that help with installation
install_str = "pip3 install -U"
apt_get_str = "apt-get -y install"


# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    if type == "pip":
        command = 'echo "%s" | %s %s' % (sudo_pass, install_str, module_name)
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


def Installer_With_Pip():
    for each in pip_module_list:
        try:
            if each == "xlwings":
                install(cmd="export INSTALL_ON_LINUX=1")
            sys.stdout.write("Installing: %s\n" % each)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            if each == 'psutil': continue  # This is expected to fail if installed
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file


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
    Installer_With_Pip()

    sys.stdout.write("If Android testing is required, please run the Android installer\n")

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__ == "__main__":
    main()
