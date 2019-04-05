# Copyright 2015, Automation Solutionz
# ---
import os, subprocess
import sys
import getpass

try:
    import commands  # We need commands to do anything, so if it's not installed, use subprocess to install it first
except:

    import commands  # Try to import again

# Import local modules
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # Set the path, so the can find the modules
from Crossplatform import CommonUtils

sudo_pass = ''
logfile = "TestNode_Core_Logs.log"

# Commands that help with installation
install_str = "pip install -U pip"
brew_str = "/usr/local/bin/brew install"


pip_module_list = ["pip", "psutil", "pillow", "pyserial", "numpy", "imutils", "simplejson", "urllib3", "selenium",
                   "requests", "poster", "wheel", "python3-xlib", "pyautogui", "Appium-Python-Client", "lxml",
                   "xlrd","tzlocal","futures"]
pip_only_mac = ["appscript"]
brew_module_list = ["wget", "wxmac", 'geckodriver']

def check_if_ran_with_sudo():
    global sudo_pass
    sudo_pass = None
    if os.getuid() == 0:
        return True
    else:
        max_try = 3
        counter=0
        have_pass = False
        while counter != max_try:
            print "This program needs sudo access.  please provide sudo password"
            global passwd
            passwd = getpass.getpass()
            print "checking to see if you have entered correct sudo"
            command = "echo 'sudo check'"
            p = os.system('echo "%s"|sudo -S %s' % (passwd, command)) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
            if p == 256:
                print "You didnt enter the correct sudo password.  Chances left: %s"%(max_try-counter-1)
                counter = counter+1
            else:
                print "sudo authentication verified!"
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

    if type == "pip":
        command = 'echo "%s" | sudo -S %s %s' % (sudo_pass, install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "brew":
        command = "%s %s --yes" % (brew_str, module_name)
    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd) # Run command with sudo
    else:
        command = cmd # Run command exactly as provided

    print "Installing: %s " % command.replace(sudo_pass, '*****')

    status, output = commands.getstatusoutput(command)
    if status > 0:
        if module_name in ('numpy', 'selenium', 'Appium-Python-Client'): return # Don't show an error on these items - they often fail and it's not a concern
        sys.stdout.error("\t See log file\n")  # Print to terminal window, and log file
    print output
    print (78 * '-')


def Installer_With_Brew():
    for each in brew_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)
            cmd = "brew install %s" % each
            output = os.system(cmd)
            print output
            print (78 * '-')
        except:
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file


def Installer_With_Pip():
    for each in pip_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
            print "Prolblem occured while installing %s" % each

    for each in pip_only_mac:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file

def Install_Hashlib():
    try:
        sys.stdout.write("Installing: Hashlib\n", True)
        cmd = "easy_install hashlib"  # !!! Not working. Not sure why - repository exists
        output = os.system(cmd)

        print output
        print (78 * '-')
    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        print "Unable to install hashlib"

def Install_Chrome_Drivers():
    Install_Chrome_Browser()
    try:
        sys.stdout.write("Installing: Chrome Driver\n", True)
        cmd = "brew cask install chromedriver"
        output = os.system(cmd)
        print output
        print (78 * '-')
    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window and log file
        print "Unable to link chromedriver"


def Install_Firefox_Drivers():
    Install_firefox_Browser()


def Install_Pip():
    try:
        sys.stdout.write("Installing: pip\n", True)
        cmd = "sudo easy_install pip" #!!! Not working. Not sure why - repository exists
        output = os.system(cmd)
        
        # Download pip directly, and run its installer
        install(cmd="wget https://bootstrap.pypa.io/get-pip.py")
        install(type="sudo", cmd="python get-pip.py")
        
        print output
        print (78 * '-')
    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        print "Unable to install pip"


def Install_Chrome_Browser():
    ## Install Chrome
    sys.stdout.write("Installing: Chrome\n", True)
    print (78 * '-')
    print ('Chrome Installation')
    print (78 * '-')
    os.system("brew cask install google-chrome")


def Install_firefox_Browser():
    ## Install Chrome
    sys.stdout.write("Installing: Frefox and Driver\n", True)
    print (78 * '-')
    print ('firefox Installation')
    print (78 * '-')
    os.system("brew cask install firefox")


def Install_Brew():
    # brew Need to implement if brew is already implemented
    try:
        sys.stdout.write("Installing: Brew\n", True)
        brew_string = 'echo "%s" | /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"' % sudo_pass
        print os.system(brew_string)
        print "Successfully installed brew"
    except:
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
        print "Unable to install brew.  Please install brew manually"
        return False


def main(rungui = False):
    global sudo_pass
    if rungui: # GUI will only run this if it already has the password, and it's verified
        sudo_pass = rungui # Save password
    else:
        # Make sure we have root privleges
        if check_if_ran_with_sudo():
            print "Running with root privs\n"
        else:
            print "Error - Need root privleges\n"
            quit()

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Install
    Install_Brew()
    Installer_With_Brew()

    #Install_Pip()
    Installer_With_Pip()
    Install_Hashlib()
    Install_Chrome_Drivers()
    Install_Firefox_Drivers()

    sys.stdout.write("If Android testing is required, please run the Android installer\n", True)
    
    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__=="__main__":
    main()
