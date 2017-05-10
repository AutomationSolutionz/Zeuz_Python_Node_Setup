# Copyright 2015, Automation Solutionz
# ---
import os
import sys
import getpass 



def check_if_ran_with_sudo(expect):
    ''' if we expect TRUE that means we want to make sure SUDO password was given.  If expect = FALSE that means we expect not to get sudo'''
    global sudo_pass
    sudo_pass = None
    if os.getuid() == 0 and expect == True:
        return True
    elif os.getuid() == 0 and expect == False:
        return False
  
    elif os.getuid() != 0 and expect == False:
        return True
    
    else:
        max_try = 3
        counter=0
        have_pass = False
        while counter != max_try:
            print "This program needs sudo access.  please provide sudo password"
            passwd = getpass.getpass()
            print "checking to see if you have entered correct sudo"
            command = "echo 'sudo check'"
            p = os.system('echo %s|sudo -S %s' % (passwd, command)) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
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
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    #install_str = "echo %s|sudo -S /usr/local/bin/pip install -U " %sudo_pass
    install_str = "/usr/local/bin/pip install --user -U "
    brew_str = "/usr/local/bin/brew install"
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "brew":
        command = "%s %s --yes" % (brew_str, module_name)
    else:
        command = cmd
    print "Installing: %s " %command
    output = os.system(command)
    print output
    print (78 * '-')

def Installer_With_Brew():

    brew_module_list = ["wget", "duplicity","wxmac"]
    for each in brew_module_list:
        try:
            cmd="brew install %s"%each
            output = os.system(cmd)
            print output
            print (78 * '-')
        except:
            print "Unable to install %s"%each

def Installer_With_Pip():
    pip_module_list = ["pip","psutil", "pillow","pyserial", "numpy","imutils", "simplejson","urllib3","selenium","requests", "poster","wheel" , "python3-xlib", "pyautogui", "Appium-Python-Client", "lxml", "gi","xlrd"]
    pip_only_mac = ["appscript"]
    
    for each in pip_module_list:
        try:
            print "Installing %s module"%each
            install(type="pip", module_name=each)
        except:
            print "unable to install/update %s"%each
            
    for each in pip_only_mac:
        try:
            print "Installing %s module"%each
            install(type="pip", module_name=each)
        except:
            print "unable to install/update %s"%each

def Install_Chrome_Drivers():
    import urllib3
    http = urllib3.PoolManager()
    try:
        print "Getting latest version of chrome driver"
        r = http.request('GET', 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        latest_version = r.data.split('\n')[0]
        print "latest version is: %s" % latest_version
    except:
        print "Unable to get the latest version."
        return
    download_link = ('http://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip') % latest_version
    print "Downloading latest Chrome driver from: %s" % download_link
    install(cmd="/usr/local/bin/wget -N " + download_link)
    install(cmd="unzip chromedriver_linux64.zip")
    install(cmd="chmod +x chromedriver")
    install(cmd="sudo mv -f chromedriver /usr/local/share/chromedriver")
    install(cmd="sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver")
    install(cmd="sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver")


def Install_Firefox_Drivers():
    Install_Chrome_Browser()
    import urllib3
    http = urllib3.PoolManager()
    import re

    try:
        print "Getting latest version of firefox driver"
        r = http.request('GET', 'https://github.com/mozilla/geckodriver/releases/latest')
        raw_data = str(r.data).split('\n')

        for each in raw_data:
            if '<span class="css-truncate-target">v' in each:
                result = re.search('<span class="css-truncate-target">(.*)</span>', each)
                latest_version = result.group(1)
                print "Latest geckodriver for Firefox is: %s" % latest_version
                break
    except:
        print "Unable to get the latest version."
        return "failed"
    download_link = ('https://github.com/mozilla/geckodriver/releases/download/%s/geckodriver-%s-macos.tar.gz') % (
    latest_version, latest_version)
    download_link = str(download_link)
    print "Downloading latest 64bit geckodriver from: %s" % download_link
    install(cmd="/usr/local/bin/wget -N " + download_link)
    geckodriver_cmd = ('tar -xvzf geckodriver-%s-macos.tar.gz') % (latest_version)
    geckodriver_cmd = str(geckodriver_cmd)
    install(cmd=geckodriver_cmd)
    install(cmd="chmod +x geckodriver")
    install(cmd="sudo mv -f geckodriver /usr/local/share/geckodriver")
    install(cmd="sudo ln -s /usr/local/share/geckodriver /usr/local/bin/geckodriver")
    install(cmd="sudo ln -s /usr/local/share/geckodriver /usr/bin/geckodriver")


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("TestNode_Installer_Logs.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()

def Install_Chrome_Browser():
    ## Install Chrome
    print (78 * '-')
    print ('Chrome Installation')
    print (78 * '-')
    os.system( "brew cask install google-chrome")



def Install_Brew():
        # brew Need to implement if brew is already implemented 
    try:
        brew_string ='/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'
        print os.system(brew_string)
        print "Successfully installed brew"
    except:
        print "Unable to install brew.  Please install brew manually"
        return False

def main():
    # Make sure we are not running as root.  Brew doesn't like it
    sys.stdout = Logger()  
    if check_if_ran_with_sudo(False):
        print "Running without root"
    else:
        print "Please do not run with sudo.  We will ask for sudo when needed.  Run again without sudo"
        quit()
    Install_Brew()
    Installer_With_Brew()
    Installer_With_Pip()
    Install_Chrome_Drivers()
    Install_Firefox_Drivers()
    sys.stdout.close()

if __name__=="__main__":
    main()


