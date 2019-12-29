#!/usr/bin/env python
# Copyright 2016, Automation Solutionz Inc.
# ---

import subprocess, os, sys, os.path, glob
try: import subprocess  # We need commands to do anything, so if it's not installed, use subprocess to install it first
except:
    print("Module Commands is missing. I'll attempt to install it manually. If it fails, you'll need to do this yourself: sudo apt-get install python-cmd2.\n")
    print(subprocess.check_output('sudo apt-get install python-cmd2', shell = True))
    import subprocess # Try to import again
import getpass # For check_if_ran_with_sudo()

# Import local modules
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # Set the path, so the can find the modules
from Crossplatform import CommonUtils

apt_get_module_list = ["python3-pip", "build-essential", "python3-setuptools", "curl", "libcurl4-openssl-dev", "libexpat-dev", "libncurses-dev", "zlib1g-dev",
                       "openjdk-8-jdk", "openjdk-8-jre", "libc6:i386", "libstdc++6:i386", "zlib1g:i386", "libconfig-dev", "g++-multilib", "gcc-multilib",
                       ]
#"git", "m4", "texinfo", "libbz2-dev", "make", "cmake", "scons", "autoconf", "automake", "autoconf-archive", "libtool", "flex", "bison",  ]

sudo_pass = ''
logfile = "TestNode_Android_Logs.log"

install_str = "pip3 install -U"
apt_get_str = "apt-get install"
br_install_str = "brew install -v"

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""

    if type == "pip":
        command = 'echo "%s" | sudo -S %s %s' % (sudo_pass, install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
        print("Installing: %s " %command.replace(sudo_pass, '*****'))
    elif type == "apt-get":
        command = 'echo "%s" | sudo -S %s %s --yes' % (sudo_pass, apt_get_str, module_name)
        print("Installing: %s " %command.replace(sudo_pass, '*****'))
    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd) # Run command with sudo
    else:
        command = cmd # Run command exactly as provided
        print("Running: %s " % command.replace(sudo_pass, '*****'))

    status, output = subprocess.getstatusoutput(command)
    print(output)
    print("\n")
    print((78 * '-'))
    print("\n")
    print("\n")
    return status, output

def update_node_version():
    install(cmd="curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -")


def Install_With_Apt():
    # update_node_version()
    # Update apt first
    try:
        sys.stdout.write("Updating: Apt\n", True)
        install(type="sudo", cmd="apt-get update -y")
    except:
        sys.stdout.error("\tError updating - See log file\n")
        

    for module in apt_get_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % module, True)
            install(type="apt-get" ,module_name = module)
        except:
            sys.stdout.error("\tError installing - See log file\n")


def get_npm_url():
    import urllib3 # Here because it needs to be imported after we install it
    os = {'win32': 'windows', 'linux2': 'linux', 'darwin': 'macOS'}
    mainurl = 'https://nodejs.org/en/download/'
    
    # Download page
    http = urllib3.PoolManager()
    r = http.request('GET', mainurl)
    wp = str(r.data).split('\n')

    # Find url and filename
    found = False
    for line in wp: # For each line in the webpage
        if 'Linux Binaries (x64)' in line:
            if os[sys.platform].lower() in line.lower():
                found = True
        elif found and '64-bit' in line:
            found = False
            url = line.split('href')[1]
            url = url.split('"')[1]
            filename = url.split('/')[-1]
            return filename, url
    return '', ''

def setup_npm():
    try:
        # Install npm/node. We need this to install and run appium
        sys.stdout.write("Downloading: npm\n", True)
        npm_file, npm_url = get_npm_url()
        print("Downloading %s" % npm_url)
        #install(cmd="wget %s" % npm_url)
        CommonUtils.Download_File(npm_url)
    except:
        sys.stdout.error("\tError downloading - See log file\n")
        
    try:
        sys.stdout.write("Unpacking: npm\n", True)
        print("Unpacking %s" % npm_file)
        install(cmd="tar -xf %s" % npm_file)
    except:
        sys.stdout.error("\tError unpacking - See log file\n")
        
    try:
        sys.stdout.write("Installing: npm\n", True)
        
        # Try to find npm directory
        npm_dir = ''
        if npm_file.split('.')[-2] == 'tar': npm_dir = '.'.join(npm_file.split('.')[:-2]) # Remove .tar.gz, .tar.xz, etc
        else: npm_dir = '.'.join(npm_file.split('.')[:-1]) # Remove .zip, .tar, etc

        # Directory not found, try our best to find it
        if npm_dir != '':
            if os.path.exists(npm_dir) == False: npm_dir = ''
        if npm_dir == '':
            dirs = glob.glob('*') # Get list of all files/dirs
            for d in dirs:
                if os.path.isdir(d) and 'node-' in d:
                    npm_dir = d
                    break

        if npm_dir == '':
            print("npm unpack directory not found, despite our best efforts")
            sys.stdout.error("\tError installing - See log file\n")
            return
        
        if os.path.exists(npm_dir) == False:
            print("Can't find npm from constructed path")
            sys.stdout.error("\tError unpacking - See log file\n")
        print("Found npm path: %s" % npm_dir)
        
        # Copy files to filesystem
        install(type="sudo", cmd="chown root.root -R %s" % npm_dir) # Need to change ownership before moving into file system
        dirs = glob.glob(os.path.join(npm_dir, '*'))
        for ndir in dirs:
            if os.path.isdir(ndir):
                install(type="sudo", cmd="cp -a %s /usr/" % ndir) # Copy each directory into bin/
        install(type="sudo", cmd="rm -rf %s" % npm_dir) # Remove the download directory
    except:
        sys.stdout.error("\tError installing - See log file\n")

    try:
        sys.stdout.write("Updating: npm\n", True)
        install(type="sudo", cmd="npm update npm")
    except:
        sys.stdout.error("\tError updating - See log file\n")
        
def Installing_appium():
    
    # setup_npm()
        
    # Remove appium if installed, so we can upgrade cleanly from a known state
    try:
        sys.stdout.write("Uninstalling: Appium\n", True)
        install(type="sudo", cmd="npm uninstall -g appium")
    except: pass

    # Install appium - Compilation may fail, but also may still install properly
    try:
        sys.stdout.write("Installing: Appium\n", True)
        s, o = install(type="sudo", cmd="npm install -g appium")
        if s > 0:
            sys.stdout.write("\tRegular Appium install failed. Trying again with --unsafe-perm\n", True)
            install(type="sudo", cmd="npm install -g appium --unsafe-perm") # Install with unsafe permissions, which avoids odd permission errors
    except:
        sys.stdout.error("\tError installing - See log file\n")

    try:
        sys.stdout.write("Installing: npm wd (WebDriver)\n", True)
        install(type="sudo", cmd="npm install wd")
    except:
        sys.stdout.error("\tError installing - See log file\n")
    if os.path.exists('node_modules'): install(type="sudo", cmd="rm -rf node_modules") # Created by wd - we need to remove because root owns it, and will cause issues for the user to delete this directory
        
def get_android_sdk_url():
    import urllib3 # Here because it needs to be imported after we install it
    os = {'win32': 'windows', 'linux2': 'linux', 'darwin': 'darwin'}
    mainurl = 'https://developer.android.com/studio/index.html'
    
    # Download page
    http = urllib3.PoolManager()
    r = http.request('GET', mainurl)
    wp = str(r.data).split('\n')

    # Find url and filename
    for line in wp: # For each line in the webpage
        if 'sdk-tools-' in line: # If we find a tools like (should be 3)
            if os[sys.platform] in line: # Keep going until we find the line for this platform
                url = line.split('"')[1] # Get url between the quotes - this is the direct link to the tools package
                filename = url.split('/')[-1]
                return filename, url
    return '', ''
                
def Installing_android_sdk(): #!!! Disabled. Don't think this is required any longer. if "android-tools-adb" fails to provide the required tools, may need to re-enable this using functino above
    android_dir = os.path.join(os.getenv('HOME'), 'android-sdk-tools')
    
    print((78 * '-'))

    ## Install android sdk
    try:
        sys.stdout.write("Downloading: Android SDK\n", True)
        filename, url = get_android_sdk_url()
        #install(cmd="wget \"%s\"" % url)
        CommonUtils.Download_File(url)
    except:
        sys.stdout.error("\tError downloading - See log file\n")

    try:
        sys.stdout.write("Unpacking: SDK\n", True)
        install(cmd="mkdir %s" % android_dir)
        install(cmd="unzip -o -q %s -d %s" % (filename, android_dir))
    except:
        sys.stdout.error("\tError unpacking - See log file\n")

    try:
        sys.stdout.write("Installing: Android Tools\n", True)
        #os.chdir(os.path.join(android_dir, 'tools'))
        install(cmd="echo -n \"\\ny\" | %s update sdk --use-sdk-wrapper" % os.path.join(android_dir, 'tools', 'android')) # Update android to get platform-tools, and answer YES to accept license
        #os.chdir(os.path.dirname(os.path.realpath(__file__)))
    except:
        sys.stdout.error("\tError installing - See log file\n")

    try:
        sys.stdout.write("Configuring: .bashrc\n", True)
        install(cmd="echo 'export ANDROID_HOME=%s' >>~/.bashrc")
        install(cmd="echo 'export PATH=${PATH}:%s/platform-tools:%s/tools' >>~/.bashrc" % (android_dir, android_dir))
        #install(cmd="source ~/.bashrc") # Would like to use, but doesn't work from Python or shell script called by Python
    except:
        sys.stdout.err("\tError configuring - See log file")
         

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
            print("This program needs sudo access.  please provide sudo password")
            global passwd
            passwd = getpass.getpass()
            print("checking to see if you have entered correct sudo")
            command = "echo 'sudo check'"
            p = os.system('echo "%s"|sudo -S %s' % (passwd, command)) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
            if p == 256:
                print("You didnt enter the correct sudo password.  Chances left: %s"%(max_try-counter-1))
                counter = counter+1
            else:
                print("sudo authentication verified!")
                have_pass = True
                break    
        if have_pass == False:
            return False
        else:   
            sudo_pass = passwd
            return True
        
def main(rungui = False):
    if rungui: # GUI will only run this if it already has the password, and it's verified
        global sudo_pass
        sudo_pass = rungui # Save password
    else:
        # Make sure we have root privleges
        if check_if_ran_with_sudo():
            print("Running with root privs\n")
        else:
            print("Error - Need root privleges\n")
            quit()

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Install apt modules
    Install_With_Apt()
    
    ## android install
    #Installing_android_sdk() # No longer used

    ## appium install
    Installing_appium()
    
    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__=="__main__":
    main()
