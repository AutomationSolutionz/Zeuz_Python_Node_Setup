#!/usr/bin/env python
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/tkinter.pdf
# Written by Lucas Donkers
# Function: Front-end to Windows, Mac, and Linux installer scripts
import getpass,subprocess

sudo_pass = ''
install_str = "pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -U"

def detect_admin():
    # Windows only - Return True if program run as admin
    
    if sys.platform == 'win32':
        command = 'net session >nul 2>&1' # This command can only be run by admin
        try: output = subprocess.check_output(command, shell=True) # Causes an exception if we can't run
        except: return False
    return True

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

# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    if type == "pip":
        command = '%s %s' % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)

    elif type == "sudo":
        command = 'echo "%s" | sudo -S %s' % (sudo_pass, cmd) # Run command with sudo
    else:
        command = cmd # Run command exactly as provided

    print("Installing: %s " % command.replace(sudo_pass, '*****'))

    status, output = subprocess.getstatusoutput(command)
    if status > 0:
        if module_name in ('numpy', 'selenium', 'Appium-Python-Client'): return # Don't show an error on these items - they often fail and it's not a concern
        sys.stdout.error("\tAn error occured. See log file\n")  # Print to terminal window, and log file
    print(output)
    print((78 * '-'))


try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os

    DEVNULL = open(os.devnull, 'wb')


def install_missing_modules():
    """
    Purpose: This function will check all the installed modules, compare with what is in requirements-win.txt file
    If anything is missing from requirements-win.txt file, it will install them only
    """
    try:
        req_file_name = 'installation_files' + os.sep + "startup_requirements.txt"
        req_file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + req_file_name
        req_list = list()
        with open(req_file_path) as fd:
            for i in fd.read().splitlines():
                if not i.startswith("http"):
                    req_list.append(i.split("==")[0])

        # get all the modules installed from freeze
        try:
            from pip._internal.operations import freeze
        except ImportError:
            # pip < 10.0
            from pip.operations import freeze

        freeze_list = freeze.freeze()
        alredy_installed_list = []
        for p in freeze_list:
            name = p.split("==")[0]
            if "@" not in name:
                # '@' symbol appears in some python modules in Windows
                alredy_installed_list.append(str(name).lower())

        # installing any missing modules
        installed = False
        for module_name in req_list:
            if module_name.lower() not in alredy_installed_list:
                try:
                    print("module_installer: Installing module: %s" % module_name)
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name], stderr=DEVNULL,
                                          stdout=DEVNULL, )
                    print("module_installer: Installed missing module: %s" % module_name)
                    installed = True
                except:
                    print("module_installer: Failed to install module: %s" % module_name)

    except Exception as e:
        print("Import Exception : {}".format(e))


def get_required_mods():
    print("Tkinter is not installed. This is required to start the graphical interface. I'll try to install it, but you may need to do this manualy. Please enter the root password if asked.\n")
    
    if sys.platform == 'win32':
        try:
            # Elevate permissions
            if not detect_admin():
                os.system('powershell -command Start-Process "python \'%s\'" -Verb runAs' % sys.argv[0].split(os.sep)[-1]) # Re-run this program with elevated permissions to admin
                quit()
            # Install
            # Note: Tkinter is not available through pip nor easy_install, we assume it was packaged with Python
            print(subprocess.check_output('python -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org oauthlib -vvv'))
            
            #python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow
            print(subprocess.check_output('python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org setuptools -U'))
            print(subprocess.check_output('pip download --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow')) # Must be done before installing or Image and ImageTk will fail
            print(subprocess.check_output('python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow -U'))
            print(subprocess.check_output('python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests -U'))
        except Exception as e:
            print("Failed to install. Please run: pip download pillow & pip install pillow")
            print("Exception is: ", e)
            input('Press ENTER to exit')
            quit()

    elif sys.platform in ['linux2','linux']:
        try:
            print(subprocess.check_output('sudo apt-get update', shell = True))
            print(subprocess.check_output('sudo apt-get -y install python3-tk python3-pil python3-pil.imagetk python3-requests', shell = True))
        except:
            print("Failed to install. Please run: sudo apt-get -y install python3-tk python3-pil python3-pil.imagetk python3-requests")
            input('Press ENTER to exit')
            quit()
    elif sys.platform == 'darwin':
        try:
            global sudo_pass
            if check_if_ran_with_sudo():
                print("Running with root privs\n")
            else:
                print("Error - Need root privleges\n")
                quit()

            install(type="sudo", cmd="easy_install pip")

            install(type="pip", module_name="--upgrade pip")

            # Download pip directly, and run its installer
            #install(cmd="wget https://bootstrap.pypa.io/get-pip.py")
            #install(type="sudo", cmd="python get-pip.py")

            install(type="sudo", cmd="pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests")
            install(type="sudo", cmd="pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org image")
            install(type="sudo", cmd="pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org tzlocal")



        except:
            print("Failed to install for mac. Please install the required modules")
            input('Press ENTER to exit')
            quit()
    else:
        print("Could not automatically install required modules")
        input('Press ENTER to exit')
        quit()
        
    # Verify install worked
    try:
        global tk, Image, ImageTk, requests
        import requests
        import tkinter as tk
        from PIL import Image, ImageTk
        print("Successfully installed. Will now try to run the graphical interface.")
    except Exception as e:
        print("Import Exception : {}".format(e))
        print("Failed to install. Please try to install manually")
        input('Press ENTER to exit')
        quit()

# Import modules
import os, os.path, _thread, sys, time, glob, _thread, subprocess, importlib, queue

# Have user install Tk if this fails
try:
    install_missing_modules()
    import requests
    from PIL import Image, ImageTk
    import tkinter as tk
except Exception as e:
    print("Import Exception : {}".format(e))
    get_required_mods()
        
import tkinter.messagebox

# Import local modules
need_to_download = False
sys.path.append(os.path.dirname(os.path.realpath(__file__))) # Set the path, so the can find the modules
CommonUtils = None
try: from installation_files.Crossplatform import CommonUtils
except: need_to_download = True

gui_title = 'Zeuz Node Installer'
help_text = "\
Zeuz Node Installer Help\n\n\
Description:\n\
This is a graphical front-end for the Windows, Mac and Linux installer scripts.\n\n\
Quit: Exit immediately - Any running automation will be stopped\n\
Install: Install the selected modules\n\
Root Password: This program requires root access to use apt, pip, npm, etc to install the required libraries and modules\n\
"
start_up_text = "\
Welcome to the Zeuz Node Installer\n\n\
This program will help to setup libraries and modules required by the Zeuz Node automation software. The Test Cases the Zeuz Node runs must be initiated from the Zeuz webpage. You must have your own Zeuz server, or use the public server at http://zeuz.automationsolutionz.com.\n\n\
Core Setup: This is required for all automation. It must be installed before Zeuz Node will work\n\
Android Setup: This is required if testing Android devices\n\
IOS Setup: If on Mac, this is required if testing IOS devices\n\
Zeuz Node: This is the automation software which you will run any time you deploy an automation run from the Zeuz server\n\
Root Password: This is required for Linux to properly install the required libraries and modules\n\n\
Usage:\n\
Check the setup checkbox you wish to install, enter the root password if required, and press the Install button. You will see all the modules that are installed, and will be notified when complete.\n\n\
Currently supported operating systems: Windows 7, Windows 10, Debian, Ubuntu, Lubuntu, Linux Mint, etc (Debian based), Mac OS X\n\n\
"
q = queue.Queue() # Initiate queue for logging
install_complete_check = False
zeuz_installer_url = 'https://github.com/AutomationSolutionz/Zeuz_Python_Node_Setup/archive/master.zip' # Location of the installer files - used when they are already downloaded
installer_location = os.path.dirname(os.path.realpath(__file__)) # Default location of the installer files is where this program was run from
titlebar_icon = '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' # Base64 encoded zeuz.gif for titlebar icon

class Application(tk.Frame):
    
    # Widget settings
    entry_width = 20
    button_width = 20
    filelist = {}
    runlist = []
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill = 'both', expand = True) # Need to pack top level, to allow widgets to expand when window is resized
        tk.Grid.columnconfigure(self, 0, weight=1) # Allows mainframe to expand
        tk.Grid.rowconfigure(self, 0, weight=1) # Allows mainframe to expand
        self.createWidgets()

    def createWidgets(self):
        # Create main frame and sub-frames to contain everything
        self.mainframe = tk.Frame(self)
        self.mainframe.grid(sticky = 'snew')
        tk.Grid.columnconfigure(self.mainframe, 1, weight=1) # Allows rightframe to expand
        tk.Grid.rowconfigure(self.mainframe, 0, weight=1) # Allows rightframe to expand
        
        # Contains settings and buttons
        self.leftframe = tk.Frame(self.mainframe)
        self.leftframe.grid(row = 0, column = 0, sticky = 'snew')
        tk.Grid.rowconfigure(self.leftframe, 1, weight=1) # Allows left side to expand down
        
        # Contains log window
        self.rightframe = tk.Frame(self.mainframe)
        self.rightframe.grid(row = 0, column = 1, sticky = 'snew')
        tk.Grid.columnconfigure(self.rightframe, 0, weight=1) # Allows log textbox to expand
        tk.Grid.rowconfigure(self.rightframe, 1, weight=1) # Allows log textbox to expand
        
        # Top Left buttons
        self.topframe = tk.Frame(self.leftframe)
        self.topframe.grid(row = 0, column = 0, sticky = 'w')
        
        # Middle left - Content
        self.installerframe = tk.Frame(self.leftframe)
        self.installerframe.grid(row = 1, column = 0, sticky = 'w')
        
        # Bottom left - Images
        self.imgframe = tk.Frame(self.leftframe)
        self.imgframe.grid(row = 2, column = 0, sticky = 's')
        
        # Add images for operating systems
        self.img_mac = tk.Label(self.imgframe)
        self.img_mac.grid(row = 0, column = 0)
        self.display_image(self.img_mac, 'installation_files' + os.sep + 'images' + os.sep + 'Apple.png')
        
        self.img_win = tk.Label(self.imgframe)
        self.img_win.grid(row = 0, column = 1)
        self.display_image(self.img_win, 'installation_files' + os.sep + 'images' + os.sep + 'Windows.png')
        
        self.img_lin = tk.Label(self.imgframe)
        self.img_lin.grid(row = 0, column = 2)
        self.display_image(self.img_lin, 'installation_files' + os.sep + 'images' + os.sep + 'Linux.png')
        
        # Put highlight around image for current OS
        #!!! Doesn't work on windows, doesn't look good when run as a standalone with no images
        #if sys.platform == 'win32':
        #    self.img_win.config(highlightbackground="red", highlightthickness = 1)
        #elif sys.platform == 'linux2':
        #    self.img_lin.config(highlightbackground="red", highlightthickness = 1)
        #elif sys.platform == 'darwin':
        #    self.img_mac.config(highlightbackground="red", highlightthickness = 1)

        # Buttons
        self.help_button = tk.Button(self.topframe, text = 'Help', width = self.button_width, command = self.show_help)
        self.help_button.grid(row = 0, column = 1, sticky = 'w')

        self.quitButton = tk.Button(self.topframe, text='Quit', width = self.button_width, command=self.teardown)
        self.quitButton.grid(row = 0, column = 0)
        
        # Password - Root password is required
        if sys.platform != 'win32': # Don't show this on windows - not used there
            tk.Label(self.topframe, text = "Root password:").grid(row = 1, column = 0, sticky = 'e')
            self.password = tk.Entry(self.topframe, width = self.entry_width, show = '*')
            self.password.grid(row = 1, column = 1, sticky = 'w')
            self.password.focus_set() # Set initial focus

        # Create text area for log output
        self.log = tk.Text(self.rightframe, wrap = tk.WORD, bg = 'white')
        self.log.grid(row = 1, column = 0, sticky = 'snew')
        self.logscrollY = tk.Scrollbar(self.rightframe, command = self.log.yview) # Create scrollbar for log window
        self.logscrollY.grid(row = 1, column = 1, sticky = 'ns')
        self.log['yscrollcommand'] = self.logscrollY.set
        self.log.insert('end', start_up_text)
        self.log.bind('<Button-3>', self.rClicker) # Bind copy/paste menu to right click
        
        # Based on OS, display the corrosponding installer options
        self.core = tk.IntVar()
        self.android = tk.IntVar()
        self.ios = tk.IntVar()
        self.zeuznode = tk.IntVar()
        self.performance = tk.IntVar()

        tk.Label(self.installerframe, text = "Core Setup:").grid(row = 0, column = 0, sticky = 'w')
        tk.Checkbutton(self.installerframe, variable = self.core).grid(row = 0, column = 1, sticky = 'w')
        
        tk.Label(self.installerframe, text = "Android Setup:").grid(row = 1, column = 0, sticky = 'w')
        tk.Checkbutton(self.installerframe, variable = self.android).grid(row = 1, column = 1, sticky = 'w')

        tk.Label(self.installerframe, text = "IOS Setup (Mac only):").grid(row = 2, column = 0, sticky = 'w')
        maccheck = tk.Checkbutton(self.installerframe, variable = self.ios)
        maccheck.grid(row = 2, column = 1, sticky = 'w')
        if sys.platform != 'darwin': maccheck.configure(state = 'disabled') # Disable checkbox for all but Mac
        
        self.core.set(1) # Set by default
        self.zeuznode.set(1) # Set by default 

        tk.Label(self.installerframe, text = "Install Zeuz Node:").grid(row = 3, column = 0, sticky = 'w')
        tk.Checkbutton(self.installerframe, variable = self.zeuznode).grid(row = 3, column = 1, sticky = 'w')

        install_button_row = 5

        tk.Label(self.installerframe, text="Performance Testing:").grid(row=4, column=0, sticky='w')
        perf = tk.Checkbutton(self.installerframe, variable=self.performance)
        perf.grid(row=4, column=1, sticky='w')
        perf.configure(state='disabled')

        self.install_button = tk.Button(self.installerframe, text = "Install", width = self.button_width, command = self.run_installer)
        self.install_button.grid(row = install_button_row, column = 0, columnspan = 2)
        
        if need_to_download: self.download_installer_files()
        
    def run_installer(self):
        # Put selected installer scripts on a list to run, in order
        try:
            # Read installer scripts for this OS, and place in a dictionary
            self.filelist = {}
            self.filelist = self.get_installer_scripts('installation_files' + os.sep + 'Zeuz_Node') # Get Crossplatform scripts - needed for zeuz node sw
            if sys.platform == 'win32':
                self.filelist.update(self.get_installer_scripts('installation_files' + os.sep + 'Windows'))
            elif sys.platform in ['linux2','linux']:
                self.filelist.update(self.get_installer_scripts('installation_files' + os.sep + 'Linux'))
            elif sys.platform == 'darwin':
                self.filelist.update(self.get_installer_scripts('installation_files' + os.sep + 'Mac'))
            else: self.log.insert('end', "Error: could not detect platform. Windows, Mac, and Linux are supported.")
            sys.path.append(installer_location) # Set the path, so the can find the modules
            
            # With those installer scripts that were found, assign them to the run list, in order
            if self.core.get() == 1: self.runlist.append(self.filelist['core'])
            if self.android.get() == 1: self.runlist.append(self.filelist['android'])
            if self.ios.get() == 1: self.runlist.append(self.filelist['ios'])
            if self.zeuznode.get() == 1: self.runlist.append(self.filelist['zeuznode'])
            if self.performance.get() == 1:
                self.runlist.append(self.filelist['performance'])
        except Exception as e:
            print("Run Installer Exception: {}".format(e))
            self.download_installer_files()
            return
        
        # Execute selected installer scripts
        if sys.platform != 'win32':
            if len(self.password.get()) == 0:
                tkinter.messagebox.showerror('Error', 'Root password must be entered to continue')
                return
            else:
                p = os.system('echo "%s" | sudo -S echo 2>/dev/null' % self.password.get()) # Issue: if shell has sudo permissions already, but user starts script without sudo, this will pass with the wrong password, because sudo won't ask for it
                if p != 0: # Wrong password
                    tkinter.messagebox.showerror('Error', 'Root password is incorrect. Please re-enter it.')
                    return
        if len(self.runlist) > 0:
            self.install_button.grid_remove() # Hide installer button
            root.after(2000, self.install_complete) # Show installer button when complete
            root.after(500, self.read_log) # Start log reader
            _thread.start_new_thread(self.execute, ())
        else:
            tkinter.messagebox.showerror('Error', 'At least one installer needs to be checked')
        
    def execute(self):
        # Must be called in a thread - executes all scripts in order

        global q, module, install_complete_check
        for installer in self.runlist:
            q.put('----------------------------------------\n%s - Begin\n----------------------------------------\n\n' % installer)
            time.sleep(1) # Allow enough time for read_log() to detect the module is finished and exit (prevent concurrent after()'s)
            self.module = installer.replace('.py', '') # Create module name from filename
            module = importlib.import_module(self.module) # Import module (path set above)
            if sys.platform == 'win32': module.main() # Execute installer in GUI mode (Permissions already elevated)
            else: module.main() # Execute installer in GUI mode and send root password
            q.put('----------------------------------------\n%s - End\n----------------------------------------\n\n' % installer)
            time.sleep(1) # Allow enough time for read_log() to read off the last log lines

        # All installers complete
        module = None
        self.runlist = [] # Clear run list
        install_complete_check = True # Trigger to show installer button
        q.put("\nAll installers completed. Review above for errors\n")
        
    def install_complete(self):
        global need_to_download
        if install_complete_check:
            # Read remaining log lines
            time.sleep(1)
            self.read_log()
            
            if need_to_download: # If run as standalone file, re-run gui from temp location
                os.chdir(need_to_download) # Move into that directory, so any files downloaded stay there
                subprocess.Popen(['python', (os.path.join(need_to_download, os.path.basename(sys.argv[0])))])
                root.destroy() # Exit this program, so the other one can take over
                quit()
            else: # Regular run, installation complete
                self.install_button.grid() # Show installer button
        else: # Installation not yet complete, reschedule check
            root.after(2000, self.install_complete)
        
    def read_log(self):
        # Read local and module prints
        # Starts and stops when Install starts and ends
        
        global q
        try:
            loglines = []
            try: loglines = CommonUtils.Read_GUI_Log() #read_log() # Get log lines from installer
            except: pass # Lets us use this function when we don't have all the installer files available
            while not q.empty(): loglines.append(q.get()) # Read any local log lines
            
            for line in loglines: # Show all lines in log window
                if len(line) > 0 and ord(line[0]) == 8: # Special handling to allow updating of the same line. If a series of backspace characters are received, delete that number
                    self.log.delete('end -%dc' % (len(line)), 'end') # Delete length of previous length, -1 for the newline tk.Text() automatically puts in
                else:
                    self.log.insert('end', line)
                    self.log.see('end')
            if not install_complete_check: root.after(500, self.read_log) # Schedule this function again
        except: pass # In the event the module was removed, but this is still running
        
    def show_help(self):
        ''' Display help information in the log window '''
        self.log.delete(0.0, 'end')
        self.log.insert('end', help_text)

    def teardown(self):
        root.destroy()
        quit()
        
    def get_installer_scripts(self, opsys):
        files = glob.glob(os.path.join(installer_location, opsys) + os.sep + '*.py')
        filelist = {}
        sys.path.append(os.path.join(installer_location, opsys)) # Update path, so we can import these modules
        for ff in files:
            f = os.path.basename(ff) # Keep just the filename
            if 'core' in f.lower():
                filelist['core'] = f.replace(opsys + os.sep, '')
            elif 'android' in f.lower():
                filelist['android'] = f.replace(opsys + os.sep, '')
            elif 'ios' in f.lower():
                filelist['ios'] = f.replace(opsys + os.sep, '')
            elif 'performance' in f.lower():
                filelist['performance'] = f.replace(opsys + os.sep, '')
            elif 'node' in f.lower():
                filelist['zeuznode'] = f.replace(opsys + os.sep, '')

        return filelist

    def display_image(self, w, filename):
        basewidth = 50
        
        if filename and os.path.exists(filename): # Make sure we read a filename from the config file and that it exists
            image = Image.open(filename) # Read image into memory at a certain size
            
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            image.thumbnail((basewidth, hsize), Image.ANTIALIAS)

            display = ImageTk.PhotoImage(image) # Convert into BMP for Tk
            w.configure(image = display) # Display in the window
            w.image = display # Anchor image
            #w.imageList = display # May be needed for bug that can cause image to not appear in certain circumstances
            
    def rClicker(self, e):
        ''' right click context menu for all Tk Entry and Text widgets '''

        try:
            # Bind events to menu items
            def rClick_Copy(e, apnd=0): e.widget.event_generate('<Control-c>')
            def rClick_Cut(e): e.widget.event_generate('<Control-x>')
            def rClick_Paste(e): e.widget.event_generate('<Control-v>')

            # Define menu items and commands
            e.widget.focus()
            nclst=[
                (' Cut', lambda e=e: rClick_Cut(e)),
                (' Copy', lambda e=e: rClick_Copy(e)),
                (' Paste', lambda e=e: rClick_Paste(e)),
            ]

            # Create menu, and add menu items
            rmenu = tk.Menu(None, tearoff=0, takefocus=0)
            for (txt, cmd) in nclst: rmenu.add_command(label=txt, command=cmd)
            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        except: pass


    def download_installer_files(self):
        # If this program is run without the accompanying installer files, download and unpack them before continuing
        # Once unpacked, we will exit this program, and restart from the temp location. Not my ideal solution, but there's a problem with importing CommonUtils after this is done - it doesn't share namespace with the other installers which use it, so the GUI never gets updates. Restarting this program from the temp location is the work around

        import zipfile, requests, time, glob
        global installer_location, q, install_complete_check, root, need_to_download

        tkinter.messagebox.showinfo('Downloading', 'Installation files are missing. Please watch the log window for updates as we download them. Press OK to start.')
        
        # Standalone functions needed to perform this work when we don't have access to CommonUtils.py
        def Download_File(url, filename):
            global q
            q.put("Downloading: ")
            pp, total, update = 0, 0, time.time()
            try:
                r = requests.get(url, stream = True) # Create object to get file
                size = float(r.headers.get('content-length')) # Size of file to download
                with open(filename, 'wb') as f: # Open file on disk
                    for data in r.iter_content(4096): # Download and write contents to disk
                        if data:
                            f.write(data) # Write data to disk
                            total += len(data)
                            current = time.time()
                            if current > (update + 1):
                                update = current
                                p = "%.1f%%" % round(total / size * 100, 1) # Calculate percentage completed and display
                                q.put(chr(8) * pp) # Erase previous percentage from terminal
                                q.put(p) # Print percentage of downloaded file
                                pp = len(p)+1 # Save length of this percentage, so we can erase it on the next iteration
                q.put(chr(8) * pp) # Erase previous percentage from terminal
                q.put("100.0%\n") # Need a new line after percentage display is complete. We specify 100% here because we may miss the opportunity to display it above if the update doesn't occur on the last block of data
                return True
            except Exception as e:
                print("Download Exception: ",e)
                q.put("Error")
                return False
    
        def unzip(zipFilePath, destDir):
            global q
            q.put("Unpacking archive...")
            try:
                zfile = zipfile.ZipFile(zipFilePath)
                if destDir and not os.path.exists(destDir): os.mkdir(destDir) 
                for name in zfile.namelist():
                    (dirName, fileName) = os.path.split(name)
                    if fileName == '': # Create sub-directory
                        newDir = os.path.join(destDir, dirName)
                        if not os.path.exists(newDir): os.mkdir(newDir)
                    else: # Create file
                        with open(os.path.join(destDir, name), 'wb') as fd: fd.write(zfile.read(name))
                zfile.close()
                q.put("Done\n")
                return True
            except Exception as e:
                print("Unzip Exception : ",e)
                q.put("Error")
                return False
    
        def main():
            global install_complete_check, installer_location, CommonUtils, need_to_download
            
            # Directory where installer files will be kept
            if sys.platform == 'win32': tmp = os.getenv('TEMP')
            else: tmp = '/tmp'
            installer_location = os.path.join(tmp, 'zeuz_node_install')
            if not os.path.exists(installer_location): os.mkdir(installer_location)
            zipname = os.path.join(installer_location, 'installer.zip')
            
            # Download and unzip
            if Download_File(zeuz_installer_url, zipname): # Download to temp directory
                if unzip(zipname, installer_location): # Unzip to temp directory
                    for f in glob.glob(os.path.join(installer_location, '*')): # Find the unzip directory
                        if os.path.isdir(f): 
                            installer_location = f # Program will look for installer scripts from here
                            need_to_download = installer_location # Used as a trigger to exit this program and re-launch the downloaded version
                            break
                    # Success
                    q.put('Installer files downloaded. You may now start installing.\n')
                    install_complete_check = True # Shutdown read_log(), and put display button
                    sys.path.append(installer_location)
                    try: from installation_files.Crossplatform import CommonUtils # Try to import again, in case it failed the first time
                    except Exception as e:
                        print("Platform Exception : ", e)
                        q.put('Installer files downloaded and unzipped, but something is wrong. You will need to download the entire installer package manually.\n')
                
                # Bitter failure
                else:
                    q.put('Installer files failed to unzip. You will need to download the entire installer package manually.\n')
            else:
                q.put('Installer files failed to download. You will need to download the entire installer package manually.\n')
            
            
        # Setup writing and modifying GUI in this thread, then run installer in a separate thread
        install_complete_check = False
        self.install_button.grid_remove() # Hide install button, so users can't do anything until we're done
        self.after(2000, self.install_complete) # Show installer button when complete
        self.after(500, self.read_log) # Start log reader, so we can update the user
        _thread.start_new_thread(main, ()) # Download installer files in separate thread, so we don't block
        

if __name__ == '__main__':
    # If run in Windows, elevate permissions 
    if sys.platform == 'win32':
        if not detect_admin():
            os.system('powershell -command Start-Process "python \'%s\'" -Verb runAs' % sys.argv[0].split(os.sep)[-1]) # Re-run this program with elevated permissions to admin
            quit() # Exit this program, the elevated program should run
    
    # Root window setup
    r = tk.Tk() # Create instance of Tk for bind
#     if sys.platform == 'win32':
#         icon_img = 'images' + os.sep + 'zeuz.gif'
#     else:
#         icon_img = 'images' + os.sep + 'zeuz.png'
#     if os.path.exists(icon_img):
#         try:
#             icon = tk.PhotoImage(file = icon_img) # Import image into format that next line can understand
#             r.call('wm', 'iconphoto', r._w, icon) # Put icon on titlebar
#         except: pass # Not a big deal if this fails

    r.call('wm', 'iconphoto', r._w, tk.PhotoImage(data = titlebar_icon)) # Put icon on titlebar (using base64 encoded string at the top of this file

    # Main window setup
    root = Application() # Create GUI instance
    r.protocol("WM_DELETE_WINDOW", root.teardown) # Catch any types of exits and teardown properly
    r.bind("<Escape>", lambda e: root.teardown()) # Bind escape to exit
    root.master.title(gui_title) # Set title

    # Execute GUI
    root.mainloop()
