# Copyright 2015, Automation Solutionz
# ---
import os, subprocess
import sys
import getpass

# Import local modules
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))  # Set the path, so the can find the modules
from Crossplatform import CommonUtils

# Commands that help with installation


sudo_pass = ''
logfile = "TestNode_PerformanceTest_Logs.log"

install_str_pip = "pip3 install -U"
install_str_easy_install = "pip install "
brew_str = "/usr/local/bin/brew install"

pip_module_list = ["wheel", "locustio", "realbrowserlocusts"]



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
            global passwd
            passwd = getpass.getpass()
            print("checking to see if you have entered correct sudo")
            command = "echo 'sudo check'"
            p = os.system('echo "%s"|sudo -S %s' % (passwd,
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


# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    # if type == "easy_install":
    #     command = 'echo "%s" | %s %s' % (sudo_pass, install_str_easy_install, module_name)
    #     if module_version:
    #         command = "%s==%s" % (command, module_version)

    if type == "pip":
        command = '%s %s' % (install_str_pip, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "brew":
        command = "%s %s --yes" % (brew_str, module_name)
    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd)  # Run command with sudo
    else:
        command = cmd  # Run command exactly as provided

    print("Installing: %s " % command.replace(sudo_pass, '*****'))

    status, output = subprocess.getstatusoutput(command)
    if status > 0:
        if module_name in ('numpy', 'selenium',
                           'Appium-Python-Client'): return  # Don't show an error on these items - they often fail and it's not a concern
        sys.stdout.error("\t See log file\n")  # Print to terminal window, and log file
    print(output)
    print((78 * '-'))


def Installer_With_Pip():
    for each in pip_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
            print("Prolblem occured while installing %s" % each)


def main(rungui=False):
    global sudo_pass
    if rungui:  # GUI will only run this if it already has the password, and it's verified
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

    # Install_Pip()
    Installer_With_Pip()

    sys.stdout.write("If Android testing is required, please run the Android installer\n")

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__ == "__main__":
    main()
