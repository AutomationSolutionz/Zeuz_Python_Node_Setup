# Copyright 2015, Automation Solutionz
# ---

import subprocess
import os
import sys
import commands

install_str = "sudo pip install -U pip"
apt_get_str = "sudo apt-get install"


# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "apt-get":
        command = "%s %s --yes" % (apt_get_str, module_name)
    else:
        command = cmd
    print "Installing: %s " %command
    status, output = commands.getstatusoutput(command)
    print output
    print (78 * '-')

def Installer_With_Pip():
        # Check and install appscript
    try:
        install(type="pip", module_name="appscript")
    except:
        print "unable to install/update %s"%module_name  

   
    
    
    # install pip
    try:
        install(cmd="sudo easy_install pip")
    except:
        print "Unable to install pip"
        
    # Check and install simplejson
    try:
        import simplejson
    except ImportError as e:
        install(type="pip", module_name="simplejson")

    # Check and install urllib3
    try:
        install(type="pip", module_name="urllib3")
    except:
        print "unable to install/update %s"%module_name  
    
    """
    # Check and install django
    django_version = "1.8.2"
    try:
        install(type="pip", module_name="django", module_version=django_version)
    except:
        print "unable to install/update %s"%module_name  
            
    # Check and install django-celery    
    try:
        install(type="pip", module_name="django-celery")
    except:
        print "unable to install/update %s"%module_name  
    """
    
    # Check and install selenium
    try:
        install(type="pip", module_name="selenium")
    except:
        print "unable to install/update %s"%module_name  
        
    # Check and install requests
    try:
        install(type="pip", module_name="requests")
    except:
        print "unable to install/update %s"%module_name  
        
    # Check and install six
    try:
        install(type="pip", module_name="six")
    except:
        print "unable to install/update %s"%module_name  
    
    # Check and install poster
    try:
        install(type="pip", module_name="poster")
    except:
        print "unable to install/update %s"%module_name  
	
	# Check and install wheel
    try:
        install(type="pip", module_name="wheel")
    except:
        print "unable to install/update %s"%module_name

	# Check and install python-dateutil
    try:
        install(type="pip", module_name="python-dateutil")
    except:
        print "unable to install/update %s"%module_name

	# Check and install dropbox
    try:
        install(type="pip", module_name="dropbox")
    except:
        print "unable to install/update %s"%module_name

    try:
        install(type="pip", module_name="python3-xlib")
    except:
        print "unable to install/update %s"%module_name

    try:
        install(type="pip", module_name="pyautogui")
    except:
        print "unable to install/update %s"%module_name

    try:
        install(type="pip", module_name="Appium-Python-Client")
    except:
        print "unable to install/update %s"%module_name
		
    try:
        install(type="pip", module_name="lxml")
    except:
        print "unable to install/update %s"%module_name

    try:
        install(type="pip", module_name="gi")
    except:
        print "unable to install/update gi"

    # brew
    try:
        install(cmd='/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    except:
        print "Unable to install brew"

    # duplicity
    try:
        install(cmd="brew install duplicity")
    except:
        print "Unable to install duplicity"


def Install_Chrome_Drivers():
    import urllib3
    http = urllib3.PoolManager()
    try:
        print "Getting latest version of chrome driver"
        r = http.request('GET', 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        latest_version = r.data.split('\n')[0]
        print "latest version is: %s"%latest_version
    except:
        print "Unable to get the latest version."
        return
    download_link = ('http://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip')%latest_version
    print "Downloading latest Chrome driver from: %s" %download_link
    install(type = "apt-get", module_name = "unzip")
    install(cmd = "wget -N " + download_link)
    install(cmd = "unzip chromedriver_linux64.zip")
    install(cmd = "chmod +x chromedriver")
    install(cmd = "sudo mv -f chromedriver /usr/local/share/chromedriver")
    install(cmd = "sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver")
    install(cmd = "sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver")


def Install_Firefox_Drivers():

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
    install(cmd="wget -N " + download_link)
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

def main():
    sys.stdout = Logger()

## Print Linux Version
    print (78 * '-')
    print ('Linux Version')
    print (78 * '-')
    command = "lsb_release -a"
    status, output = commands.getstatusoutput(command)
    print output

## Install PIP
    print (78 * '-')
    print ('Python PIP Installation')
    print (78 * '-')
    os.system("sudo add-apt-repository universe")
    os.system("sudo apt-get update --yes")
    install(type = "apt-get", module_name = "python-pip")

## Install PIP modules    
    Installer_With_Pip()

## Install Postgres
    print (78 * '-')
    print ('Postgres Installation')
    print (78 * '-')
    install(type = "apt-get", module_name = "libpq-dev python-dev")
    install(type = "apt-get", module_name = "postgresql postgresql-contrib")

    
## Check and install psycopg2
    print (78 * '-')
    print ('Install Psycopg2')
    print (78 * '-')
    try:
        import psycopg2
    except ImportError as e:
        install(type="apt-get", module_name="python-psycopg2")
    

## Easy install funkload
    try:
        import funkload
    except ImportError as e:
        try:
            funkload_easy_install = "sudo easy_install https://github.com/nuxeo/FunkLoad/archive/master.zip"
            install(cmd=funkload_easy_install)
        except:
            print "unable to install/update funkload"

## Install Chrome
    print (78 * '-')
    print ('Chrome Installation')
    print (78 * '-')
    install(type = "apt-get", module_name = "libxss1 libappindicator1 libindicator7")
    install(cmd = "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    install(cmd = "sudo dpkg -i google-chrome*.deb")
    install(cmd = "sudo apt-get install -f")

## Install Chrome Drivers
    print (78 * '-')
    print ('Chrome Drivers Installation')
    print (78 * '-')
    Install_Chrome_Drivers()



## Install Firefox Drivers
    print (78 * '-')
    print ('Firefox Drivers Installation')
    print (78 * '-')
    Install_Firefox_Drivers()

    # Check and install psutil
    try:
        install(type="pip", module_name="psutil")
    except:
        print "unable to install/update %s"%module_name  


    sys.stdout.close()

if __name__=="__main__":
	main()
