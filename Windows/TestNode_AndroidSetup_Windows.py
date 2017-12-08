# Copyright 2017, Automation Solutionz

def detect_admin():
    # Windows only - Return True if program run as admin
    
    import subprocess
    if sys.platform == 'win32':
        command = 'net session >nul 2>&1' # This command can only be run by admin
        try: output = subprocess.check_output(command, shell=True) # Causes an exception if we can't run
        except: return False
    return True


import subprocess
from subprocess import PIPE, Popen,STDOUT
import shutil
import os, os.path, win32api, win32con, win32gui
from os.path import expanduser
import sys
import getpass
import time
from clint.textui import progress
import platform
import requests
import psutil
import inspect
import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPVOID #this belongs to registry editor
LRESULT = LPARAM  # synonymous.  This belongs to registry
import _winreg as winreg

# Import local modules
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')) # Set the path, so the can find the modules
from Crossplatform import CommonUtils


#since nothing is able to refresh the command line calling directly, we will define the npm full path
global npm_path
global PATH_VAR
global appium_path
global Android_Home_Dir
global Android_Tools_Dir
global Android_Tools_bin_Dir
global Android_Build_Tools_Dir
global Downloaded_Path
global Temp_Tools_Dir
global current_script_path

npm_path = os.environ["ProgramW6432"]+os.sep+ "nodejs"
appium_path = os.getenv('APPDATA') + os.sep + "npm" + os.sep + "appium"
Android_Home_Dir  =  expanduser("~")+os.sep + "Desktop" + os.sep +  "sdk"
Android_Tools_bin_Dir = Android_Home_Dir + os.sep + "tools" + os.sep + "bin"
Android_Tools_Dir = Android_Home_Dir + os.sep + "tools" + os.sep + "bin"
Android_Platform_Tools_Dir = Android_Home_Dir + os.sep + "platform-tools"
Android_Build_Tools_Dir = Android_Home_Dir + os.sep + "build-tools"
Downloaded_Path = expanduser("~")+os.sep + "Downloads" 
Temp_Tools_Dir = expanduser("~")+os.sep + "Downloads" + os.sep + "tools"
logfile = "TestNode_Android_Logs.log"

current_script_path = sys.path[0]

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def Check_Pre_Req():
    admin_check = is_admin()
    if admin_check == False:
        print ""
        sys.stdout.error("Unable to elevate current action to run as admin.\n") # Print to terminal window, and log file
        return False
    else:
        print "Admin check pass"
        
    if os.name != 'nt':
        sys.stdout.error("This installer must be run on Windows\n") # Print to terminal window, and log file
        return False
    if sys.version_info[:2] != (2,7):
        sys.stdout.error("32bit Python v2.7 must be installed\n") # Print to terminal window, and log file
        return False
    if platform.architecture()[0] != '32bit':
        sys.stdout.error("32bit Python v2.7 must be installed\n") # Print to terminal window, and log file
        return False
    if 'setuptools' not in cmdline("easy_install --version"):
        sys.stdout.error("'easy_install' is not installed or not in the PATH.\n") # Print to terminal window, and log file
        return False
    if 'pip' not in cmdline("pip --version"):
        sys.stdout.error("pip is not installed, or not in your PATH variable.\n") # Print to terminal window, and log file
        return False
    
    print "Pre-requirements verified successfully"
    return True


def Kill_Process(name):
    this_proc = os.getpid()
    for proc in psutil.process_iter():
        procd = proc.as_dict(attrs=['pid', 'name'])
        if name in str(procd['name']) and procd['pid'] != this_proc:
            proc.kill()

def Get_Home_Dir():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        home_dir = expanduser("~")
        return home_dir
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def Download_File(base_url, file_name,md5=False):
    try:
        print "Downloading from: %s"%(base_url+file_name)
        file_url = base_url + file_name
        download_path =  Get_Home_Dir()+os.sep + 'Downloads' + os.sep +  file_name
        
        if os.path.isfile(download_path):
            print "already downloading... skipping download"
            return download_path
        
        r = requests.get(file_url, stream=True)
        path = download_path
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        print "Download completed"
        return download_path
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        return False

def Delete_File(file_path):
    try:
        sys.stdout.error("Deleting file: %s\n"%file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            if os.path.exists(file_path) == False:
                sys.stdout.error("\tDeleted successfully\n")
                return True
            else: 
                sys.stdout.error("\tWe could not delete the file\n")
                return False
        else:
            print "file does not exits"
            sys.stdout.error("\tFile was not found\n")
            return True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def Delete_Folder(src_folder):
    try:
        sys.stdout.error("Deleting folder: %s\n"%src_folder)
        if os.path.exists(src_folder) == False:
            print "Source folder does not exists"
            sys.stdout.error("\tSource folder does not exists\n")
            return True
        if os.path.exists(src_folder) == True:
            print "Existing folder found.. will delete"
            sys.stdout.error("\tExisting folder found.. will delete\n")
            shutil.rmtree(src_folder)
            if os.path.exists(src_folder) == True:
                sys.stdout.error("\tWe tried to delete the folder but could not delete\n")
                return False
            else:
                sys.stdout.error("\tFolder found and successfully deleted\n")
                return True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def Move_and_Overwrite_Folder(src_folder, des_folder):
    try:
        sys.stdout.error("\tMoving from %s to %s\n"%(src_folder, des_folder))
        if os.path.exists(src_folder) == False:
            print "Source folder does not exists...Unable to copy"
            return False
        if os.path.exists(des_folder) == True:
            print "Existing folder found.. will delete"
            Delete_Folder(des_folder)
            
        print "moving folders.."
        print shutil.move(src_folder, des_folder)
        return des_folder
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False    
    
def Copy_and_Overwrite_Folder(src_folder, des_folder):
    try:
        if os.path.exists(src_folder) == False:
            print "Source folder does not exists...Unable to copy"
            return False
        if os.path.exists(des_folder) == True:
            print "Existing folder found.. will delete"
            shutil.rmtree(des_folder)
        print "Copying folders.. from: %s to %s"%((src_folder, des_folder))
        print shutil.copytree(src_folder, des_folder)
        return des_folder
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        print "Unable to copy and overwrite folder and its content"
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False    
    
def Install_JDK():
    '''
    This function will first check if you have java/JRE/JDK installed.  If you have, we are gonna skip installer.  If you 
    don't have java installed or if you don't have java set in path, we will install a known latest version that we have in our repo.
    '''
    try:
        sys.stdout.write("Validating if JDK is installed...\n", True) # Print to terminal window, and log file
        print "Validating if JDK is installed..."
        base_url = "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/"
        check_JDK = Check_If_JDK_Installed()
        print check_JDK
        if check_JDK == False:
            sys.stdout.write("JDK was not installed  We will download and install known stable version of JDK \n", True) # Print to terminal window, and log file
            print "JDK was not installed  We will download and install known stable version of JDK"
            #Download 3 parts of installer
            print "part 1 of 3"
            sys.stdout.write("Downloading JDK part 1 of 3 \n", True)
            installer_file_part_1 = "jdk-8-144-windows-x64.sfx.part1.exe"
            java_installer_path_1 = Download_File(base_url, installer_file_part_1)
            print "part 2 of 3"
            sys.stdout.write("Downloading JDK part 2 of 3 \n", True)
            installer_file_part_2 = "jdk-8-144-windows-x64.sfx.part2.rar"
            java_installer_path_2 = Download_File(base_url, installer_file_part_2)
            print "part 3 of 3"
            sys.stdout.write("Downloading JDK part 3 of 3 \n", True)
            installer_file_part_3 = "jdk-8-144-windows-x64.sfx.part3.rar"
            java_installer_path_3 = Download_File(base_url , installer_file_part_3)            
            
            #extracting file
            sys.stdout.write("Please wait while we extracting files silently...\n", True) # Print to terminal window, and log file
            print "Extracting files silently..."
            silent_extract_command = "%s /s"%(Downloaded_Path + os.sep + installer_file_part_1)
            os.system(silent_extract_command)   
            sys.stdout.write("JDK Extraction completed\n", True)
            print "Extracting completed"
            
            print "We are installing java silently, please wait..."
            
            jdk_exe_path = current_script_path + os.sep+ r"jdk-8u144-windows-x64.exe"
            silent_installer_command = "%s /s"%jdk_exe_path
            sys.stdout.write("Installing JDK silently from %s.  This will take some time...\n"%jdk_exe_path, True) # Print to terminal window, and log file

            os.system(silent_installer_command)     
            #this will set all paths as well
            Check_If_JDK_Installed()
            sys.stdout.write("Cleaning up temp JDK installer files...\n", True) # Print to terminal window, and log file
            print "Cleaning up temp JDK installer files..."
            Delete_File(Downloaded_Path + os.sep + installer_file_part_1)
            Delete_File(Downloaded_Path + os.sep + installer_file_part_2)
            Delete_File(Downloaded_Path + os.sep + installer_file_part_3)
            Delete_File(current_script_path + os.sep + 'jdk-8u144-windows-x64.exe')
            #setting java path
            JAVA_PATH()
            sys.stdout.write("JDK Install completed\n", True)
        else:
            sys.stdout.write("JDK is already installed\n", True)
            print "JDK is already installed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def Check_If_JDK_Installed():
    try:
        try:
            java_check = subprocess.check_call(["javac", "-version"], stderr=subprocess.STDOUT)
            print "JDK is installed"
            result = JAVA_PATH()
            if result == False:
                return False
            else:
                return True
        except:
            print "JDK is not found in path"
            print "We will check if JDK was installed.  If found, we will set all the PATH"
            result = JAVA_PATH()
            if result == True:
                return True
            else:
                return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def JAVA_PATH():
    try:
        sys.stdout.error("\tWe will check default location to see if we can locate JDK\n")
        print "We will check default location to see if we can locate JDK"
        java_path_64 = r'C:\Program Files\Java'
        java_path_32 = r'C:\Program Files (x86)\Java'
        if (os.path.isdir(java_path_64)):
            java_path_default = java_path_64
        elif (os.path.isdir(java_path_32)):
            java_path_default = java_path_32
        else:
            print "We couldnt find java installed in default Program Files directory"
            sys.stdout.error("\tWe couldnt find java installed in default Program Files directory\n")
            return False
        print "Found java installed in: %s" %java_path_default
        sys.stdout.error("\tFound java installed in: %s\n"%java_path_default)
       
        java_list = filter(os.path.isdir, [os.path.join(java_path_default,f) for f in os.listdir(java_path_default)])
        for each in java_list:
            if "jdk" in each:
                print "we found JDK in default program files path.  We will set javac to the path"
                javac_path = each +os.sep + "bin"
                print "Setting JAVA_HOME to Environment"
                Add_To_Path("JAVA_HOME",each)
                print "Adding Java bin to PATH"
                Add_To_Path("PATH",javac_path)
                return True
        print "JDK is not found in the default program files path"
        sys.stdout.error("\tJDK is not found in the default program files path\n")
        return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

 
  

def Android_SDK_PATH():
    try:            
        #set android home path

        print "Setting ANDROID_HOME to Environmental variable"
        Add_To_Path("ANDROID_HOME", Android_Home_Dir)
        #set tools to path
        print "Setting tools dir to PATH"
        Add_To_Path("PATH", Android_Tools_Dir)
        #set tools bin to path
        print "Setting tools bin dir to PATH"
        Add_To_Path("PATH", Android_Tools_bin_Dir)
        #set platforms_tools
        print "Setting platform-tools dir to PATH"
        Add_To_Path("PATH", Android_Platform_Tools_Dir)
        #ANT_HOME
        print "Setting ANT_HOME to Environmental variable"
        ANT_HOME = Android_Home_Dir + os.sep + 'apache-ant-1.10.1' + os.sep + 'bin'
        Add_To_Path("ANT_HOME", ANT_HOME)
        #M2_HOME
        print "Setting M2_HOME to Environmental variable"
        M2_HOME = Android_Home_Dir + os.sep + "apache-maven-3.5.0"
        Add_To_Path("M2_HOME", M2_HOME)      
        #M2
        print "Setting maven to Environmental variable"
        M2 = Android_Home_Dir + os.sep + "apache-maven-3.5.0" + os.sep + "bin"
        Add_To_Path("M2", M2)   
        #M2 to PATH
        print "Setting maven to PATH"
        M2 = Android_Home_Dir + os.sep + "apache-maven-3.5.0" + os.sep + "bin"
        Add_To_Path("PATH", M2)   
        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False  
         
def Android_SDK(upgrade=False):    
    try:
        sdk_check = Check_If_ANDROID_SDK_Installed()
        if sdk_check == False:
            try:
                sys.stdout.write("Downloading: Android SDK\n", True) # Print to terminal window, and log file
                print "Downloading known android SDK for zeuz"
                base_url = "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/"
                #Download 4 parts of installer
                installer_file_part_1 = "sdk.part01.exe"
                installer_file_part_2 = "sdk.part02.rar"
                installer_file_part_3 = "sdk.part03.rar"
                installer_file_part_4 = "sdk.part04.rar"
                installer_file_part_5 = "sdk.part05.rar"
                print "part 1 of 5"       
                sys.stdout.write("part 1 of 5\n", True)
                android_installer_path_1 = Download_File(base_url, installer_file_part_1)
                print "part 2 of 5"
                sys.stdout.write("part 2 of 5\n", True)
                android_installer_path_2 = Download_File(base_url, installer_file_part_2)
                print "part 3 of 5"
                sys.stdout.write("part 3 of 5\n", True)
                android_installer_path_3 = Download_File(base_url, installer_file_part_3)   
                print "part 4 of 5"
                sys.stdout.write("part 4 of 5\n", True)
                android_installer_path_4 = Download_File(base_url, installer_file_part_4)          
                print "part 5 of 5"
                sys.stdout.write("part 5 of 5\n", True)
                android_installer_path_5 = Download_File(base_url, installer_file_part_5)                      
                #silent install
                sys.stdout.write("Silently extracting android SDK package with ant and maven.  This can take 3-5 minutes.\n", True) # Print to terminal window, and log file 
                time.sleep(3)
                Kill_Process("adb.exe")
                Extracted_Folder_Path =    Downloaded_Path + os.sep + "sdk"  
                if os.path.exists(Extracted_Folder_Path) == True:
                    print "Existing folder found.. will delete"
                    shutil.rmtree(Extracted_Folder_Path)
                print "Silently extracting android SDK package with ant and maven.  This can take 3-5 minutes."
                silent_extract_command = "%s /s"%(Downloaded_Path + os.sep +installer_file_part_1)
                os.system(silent_extract_command)    
                time.sleep(3)  
                
                sys.stdout.write("Moving SDK folder to desktop\n", True) # Print to terminal window, and log file
                print "Moving SDK folder to desktop"
                src_folder = current_script_path + os.sep + "sdk"  
                des_folder = Android_Home_Dir
                Move_and_Overwrite_Folder(src_folder, des_folder)
                sys.stdout.write("Cleaning up temp android SDK files \n", True) # Print to terminal window, and log file
                Delete_File(Downloaded_Path + os.sep +installer_file_part_1)
                Delete_File(Downloaded_Path + os.sep +installer_file_part_2)
                Delete_File(Downloaded_Path + os.sep +installer_file_part_3)
                Delete_File(Downloaded_Path + os.sep +installer_file_part_4)
                Delete_File(Downloaded_Path + os.sep +installer_file_part_5) 
                
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()        
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
                print Error_Detail        
        
        else:
            sys.stdout.write("Android SDK for ZeuZ is already Installed.\n", True) # Print to terminal window, and log file
        #setting SDK paths
        Android_SDK_PATH()
        #we need to  investigate this further     
        #Upgrade_Android_SDK()
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False    

def Check_If_ANDROID_SDK_Installed():
    try:
        if (os.path.isdir(Android_Home_Dir) and os.path.isdir(Android_Tools_Dir) and os.path.isdir(Android_Platform_Tools_Dir) and os.path.isdir(Android_Build_Tools_Dir)) :
            print "Android SDK for zeuz is setup"
            return True
        else:
            print "Android SDK for zeuz is not found"
            return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False    

    
def Upgrade_Android_SDK():
    try:
        # upgrade SDK
        Kill_Process("adb.exe")
        if Check_If_ANDROID_SDK_Installed():
            #remove any old tools file
            if os.path.exists(Temp_Tools_Dir) == True:
                print "Existing folder found.. will delete"
                shutil.rmtree(Temp_Tools_Dir)
            
            result = Copy_and_Overwrite_Folder(Android_Tools_Dir, Temp_Tools_Dir)
            if result == False:
                print "Unable to locate android tools dir under: %s"%Android_Tools_Dir
            sdkmanager_temp = Temp_Tools_Dir + os.sep + 'bin'+os.sep+ 'sdkmanager.bat'
            print "Upgrading android SDK Tool"
            upgrade_command = '"%s" --sdk_root= "%s" --update'%(sdkmanager_temp,Android_Home_Dir)
            print os.system(upgrade_command) 
            print "Cleaning up..."
            if os.path.exists(Temp_Tools_Dir) == True:
                shutil.rmtree(Temp_Tools_Dir)
            print "Successfully setup Android for Appium"
        else:
            print "Please install Android SDK first before upgrading"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False    

def Install_NodeJS(upgrade=False):
    try:
        print "Installing NodeJS ...and other pre-req"
        #VisualcppBuildTools()
        #VisualCpythonCompiler()
        base_url = "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/"
        file_name = 'node-v9.0.0-x64.msi'
        installer_path  = Download_File(base_url, file_name)
        print "Installing NodeJS silently from: %s"%installer_path
        command = 'msiexec.exe /i "%s"  /passive' %(installer_path)
        os.system(command)
        print "Adding npm to the path"
        Add_To_Path("PATH",npm_path)
        print "Cleaning up..."
        time.sleep(2)
        print os.remove(installer_path)
        print "adding NPM to python current path"
        os.environ['PATH'] += ';'+npm_path
        #os.system('%s config set python python2.7'%npm_path)
        #os.system('% config set msvs_version 2015'%npm_path)
        return True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False        
 
def Install_Appium(upgrade=False):   
    try:
        #check if NPM is installed
        sys.stdout.write("Checking: NPM\n", True) # Print to terminal window, and log file
        print "Checking pre-req for Appium installer"
        npm_check = Check_If_NPM_Installed()
        if npm_check == False:
            sys.stdout.write("Installing: NPM\n", True) # Print to terminal window, and log file
            print "NodeJS is not installed.  We will install it"
            Install_NodeJS()
            
            sys.stdout.write("Installing: Appium\n", True) # Print to terminal window, and log file
            print "Installing appium via NPM"
            appium_installer = 'npm install -g appium'
            print "Installing appium... This may take several minutes"
            sys.stdout.write("Installing appium... This may take several minutes\n", True) # Print to terminal window, and log file
            Installer_Result = subprocess.check_call(appium_installer, shell = True)
            print "Adding appium to the path"
            Add_To_Path("PATH",appium_path)
            print "Completed appium installer..."
            return True
        else:
            check_appium = Check_If_Appium_Installed()
            if check_appium == True:
                return True
            
            sys.stdout.write("Installing: Appium\n", True) # Print to terminal window, and log file
            appium_installer = 'npm install -g appium'
            print "Installing appium... This may take several minutes"
            sys.stdout.write("Installing appium... This may take several minutes\n", True) # Print to terminal window, and log file
            Installer_Result = subprocess.check_call(appium_installer, shell = True)
            print "Adding appium to the path"
            Add_To_Path("PATH",appium_path)
            print "Completed appium installer..."
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False
 
def Check_If_NPM_Installed():
    try:
        try:
            print "Checking if NPM is installed..."
            npm_check = subprocess.check_output(["node", "-v"], stderr=subprocess.STDOUT)
            sys.stdout.write("NPM version: %s is installed\n"%npm_check, True) # Print to terminal window, and log file
            print "NPM version: %s is installed"%npm_check
            return True
        except:
            print "NPM is not installed"
            return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False        

def Check_If_Appium_Installed():
    try:
        try:
            print "Checking if Appium is installed..."
            appium_check = subprocess.check_output(["where", "appium"], stderr=subprocess.STDOUT)
            print "Appium is installed"
            appium_version = subprocess.check_output(appium_path + " -v", shell = True)
            print "Appium verion is: %s"%appium_version
            return True
        except:
            print "Appium is not installed"
            print "Checking to see if we can locate appium in appdata folder"
            if (os.path.isdir(appium_path)):
                print 'found in appdata folder.  setting it to path'
                Add_To_Path("PATH", appium_path)
                print "Added appium to your path.."
                return True
            else:
                print "Appium is not found under appdata folder"
                return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False
 
def Get_Current_Logged_User():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #works on all platoform
        current_user_name = getpass.getuser()
        return current_user_name
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def Add_To_Path(PATH_NAME,value):
    try:
        sys.stdout.write("Adding path: '%s' to windows system environment with value: %s\n"%(PATH_NAME,value), True) # Print to terminal window, and log file
        result_path_check = Check_If_in_Path(PATH_NAME,value)
        if result_path_check ==True:
            return True
        
        Update_Sys_Env_Variable(PATH_NAME,value)
        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False        


def Check_If_in_Path(PATH_NAME,value):
    print "Checking if %s is already in %s"%(value, PATH_NAME)
    try:
        try:
            #we will always set the path in run time just to be on the same side
            if PATH_NAME == "PATH":
                current_value = os.environ['PATH']
                path_list = current_value.split(";")
                if value not in value_list:
                    os.environ['PATH'] += ';'+value
            else:
                os.environ[PATH_NAME] = value
        except:
            True
        reg_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        try:
            system_environment_variables = winreg.QueryValueEx(reg_key, PATH_NAME)[0]
        except:
            print "Value = '%s' is not found.  We will add it."%value
            return False
        if value in system_environment_variables:
            print "Value = '%s' already exists under %s"%(value, PATH_NAME)
            return True
        else:
            print "Value = '%s' is not found.  We will add it."%value
            return False
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print "Environmental Variable provided '%s' does not exists"%( PATH_NAME)
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False
          
def Update_Sys_Env_Variable(PATH_NAME,my_value):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_ALL_ACCESS) 
        try:
            value, _ = winreg.QueryValueEx(key, PATH_NAME)
        except WindowsError:
            # in case the PATH variable is undefined
            value = ''
        if PATH_NAME != "PATH":
            value = my_value
        else:
            #we always append PATH
            value_list = value.split(";")
            if my_value in value_list:
                print "Already there"
                return True
            else:
                value = value + ";" + my_value
        # write it back
        winreg.SetValueEx(key, PATH_NAME, 0, winreg.REG_EXPAND_SZ, value)
        winreg.CloseKey(key)

        # notify the system about the changes
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
        # we will add python path again to be on the safe side
        try:    
            if PATH_NAME == "PATH":
                current_value = os.environ['PATH']
                path_list = current_value.split(";")
                if my_value not in value_list:
                    os.environ['PATH'] += ';'+my_value
            else:
                os.environ[PATH_NAME] = my_value
        except:
            True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print "Environmental Variable provided '%s' does not exists"%( PATH_NAME)
        sys.stdout.error("\tAn error occurred. See log for more details: %s\n"%Error_Detail)
        return False

def main(rungui = False):
    if not rungui: # GUI elevates already, so no need to do it again
        # If run in Windows, elevate permissions 
        if sys.platform == 'win32':
            if not detect_admin():
                os.system('powershell -command Start-Process "python \'%s\'" -Verb runAs' % sys.argv[0].split(os.sep)[-1]) # Re-run this program with elevated permissions to admin
                quit() # Exit this program, the elevated program should run

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Install
    if Check_Pre_Req():
        Install_JDK()
        Android_SDK()
        Install_Appium()

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)

if __name__=="__main__":
    main()
    raw_input("Press ENTER to exit")

