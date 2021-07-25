# Function: Contains functions and variables used amongst the various platform installers

import subprocess, sys, shutil, os, os.path
# Do not import "requests" here - Causes Mac core install to fail

# Global variables
error = False # Set to True when any errors occur
log_gui = [] # Log lines kept here for GUI
sudo_pass = ''
if sys.platform == 'win32': tmpdir = os.getenv('TMP')
else: tmpdir = '/tmp'
gui_prints_log_filename = os.path.join(tmpdir, 'zeuz_node_gui.log')
gui_prints_position = 0

# Commands that help with installation
install_str = "pip install -U pip"
apt_get_str = "apt-get -y install"
Node_branch = "beta"  # Todo: When we have a proper release procedure of node then change it to release branch

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""

    # Install with pip (with sudo)
    if type == "pip":
        command = 'echo "%s" | sudo -S %s %s' % (sudo_pass, install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
        print("Installing: %s " %command)
    
    # Install with apt (with sudo)
    elif type == "apt-get":
        command = 'echo "%s" | sudo -S %s %s --yes' % (sudo_pass, apt_get_str, module_name)
        print("Installing: %s " %command)
    
    # Run command as root
    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd) # Run command with sudo
    
    # Run command as regular user
    else:
        command = cmd # Run command exactly as provided
        print("Running: %s " % command.replace(sudo_pass, '*****'))

    status, output = subprocess.getstatusoutput(command)
    print(output)
    print("\n")
    print((78 * '-'))
    print("\n")
    return output


def Installer_With_Apt_get():
    for each in apt_get_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True) # Print to terminal window, and log file
            install(type="apt-get", module_name=each)
        except:
            global error
            error = True
            sys.stdout.write("\tAn error occured. See log file\n", True) # Print to terminal window, and log file

def Installer_With_Pip():
    for each in pip_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True) # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except:
            if each == 'psutil': continue # This is expected to fail if installed
            global error
            error = True
            sys.stdout.write("\tAn error occured. See log file\n", True) # Print to terminal window, and log file

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
            passwd = getpass.getpass()
            print("checking to see if you have entered correct sudo")
            command = "echo 'sudo check'"
            p = os.system('echo %s|sudo -S %s' % (passwd, command)) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
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

class Logger(object):
    def __init__(self, logfile, gui):
        self.gui = gui
        self.terminal = sys.stdout
        self.log = open(logfile, "w") # All output goes to this log
        self.guilog = open(gui_prints_log_filename, "w") # Only formatted status updates go to this log, which is displayed in the GUI log window

    def write(self, message, to_screen = False):
        self.log.write(message)
        if to_screen:
            if self.gui:
                global log_gui
                log_gui.append(message)
                self.guilog.write(message)
                self.guilog.flush()
            else:
                self.terminal.write(message)
                self.terminal.flush()
        
    def error(self, message):
        global error
        error = True
        self.log.write(message)
        if self.gui:
            global log_gui
            log_gui.append(message)
            self.guilog.write(message)
            self.guilog.flush()
        else:
            self.terminal.write(message)
            self.terminal.flush()

    def close(self):
        self.log.close()
        self.guilog.close()

def Logger_Setup(logfile, gui):
    # Setup logging
    global oerr, oout, Log
    oerr = sys.stderr # Backup handle for STDOUT/ERR
    oout = sys.stdout
    Log = Logger(logfile, gui) # Create Logging instance
    sys.stdout = Log # Capture STDOUT output
    sys.stderr = Log # Capture STDERR output

def Logger_Teardown(logfile):    
    # Check if there were any errors and inform the user if so
    global error, oerr, oout, Log
    
    if error:
        sys.stdout.write("\nAn error occurred. See %s for more details\n" % logfile, True)
    else:
        sys.stdout.write("\nInstallation Complete\n", True)

    # Clean up logger, and reinstate STDOUT/ERR
    Log.close()
    sys.stderr = oerr
    sys.stdout = oout
    error = False # Reset for next run

def Read_GUI_Log():
    # Essentially tails a log - returns only newly added lines
    global gui_prints_position
    if os.path.exists(gui_prints_log_filename):
        with open(gui_prints_log_filename, 'r') as f:
            f.seek(gui_prints_position) # Go to last position
            log = f.read() # Read all new content
            f.seek(0, 2) # Go to end of file
            gui_prints_position = f.tell() # Save new position
        return [log]
    return []
    
def read_log():
    global log_gui
    size = len(log_gui)
    data = log_gui[:size]
    del log_gui[:size]
    return data

def unzip(zipFilePath, destDir = ''):
    # Unzips a file to a destination directory if specified, or the current working directory
    import os, zipfile, os.path

    try:
        zfile = zipfile.ZipFile(zipFilePath)
        if destDir and not os.path.exists(destDir): os.mkdir(destDir) # 
    
        print("Unzipping %s to %s" % (zipFilePath, destDir))
        for name in zfile.namelist():
            (dirName, fileName) = os.path.split(name)
    
            # Create sub-directory
            if fileName == '':
                newDir = os.path.join(destDir, dirName)
                if not os.path.exists(newDir):
                    os.mkdir(newDir)
            
            # Create file
            else:
                # file
                fd = open(os.path.join(destDir, name), 'wb')
                fd.write(zfile.read(name))
                fd.close()
        zfile.close()
        return True
    except Exception as e:
        print("Error unzipping: %s" % e)
        return False

def Download_File(url, filename = ''):
    # Download a file with progress update in percentage
    # If no filename provided, we will try to get it from the url
    
    import os, os.path, requests, sys, time
    
    chunk_size = 4096 # Size in bytes of data to download at a time
    total = 0 # Total data downloaded at any given time
    pp = 0 # Number of backspaces - used in displaying progres in one spot
    update = time.time() # Keep track of last progress update
    timeout = 1 # How often in seconds to display progress
    
    try:
        if filename == '': filename = url.split('/')[-1] # No filename given. Try to get the filename automatically
        
        r = requests.get(url, stream = True) # Create object to get file
        for i in range(0,10): # May need to connect several times before we get a valid value
            try:
                #size = float(r.headers.get('content-length')) # Get file size
                break
            except: time.sleep(1)

        sys.stdout.write("\t", True) # Indent, so it's clear this is attributed to the previous line
        with open(filename, 'wb') as f: # Open file on disk
            for data in r.iter_content(chunk_size): # Download and write contents to disk
                if data:
                    total += len(data) # Update amount which has been downloaded
                    
                    current = time.time()
                    if current > (update + timeout):
                        update = current
                        
                        #p = "%.1f%%" % round(total / size * 100, 1) # Calculate percentage completed and display

                        #sys.stdout.write(chr(8) * pp, True) # Erase previous percentage from terminal
                        #sys.stdout.write(p, True) # Print percentage of downloaded file

                        #pp = len(p) + 1 # Save length of this percentage, so we can erase it on the next iteration
                                            
                    f.write(data) # Write data to disk

        #sys.stdout.write(chr(8) * pp, True) # Erase previous percentage from terminal
        sys.stdout.write("100.0%\n", True) # Need a new line after percentage display is complete. We specify 100% here because we may miss the opportunity to display it above if the update doesn't occur on the last block of data
        
        if os.sep not in filename: filename = os.path.join(os.getcwd(), filename)
        return filename
    except Exception as e:
        print("Error downloading: %s" % e)
        return False

