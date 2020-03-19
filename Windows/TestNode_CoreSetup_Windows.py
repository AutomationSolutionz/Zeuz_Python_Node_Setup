# Copyright 2015, Automation Solutionz
# ---
import os, sys
import importlib

python_dir = os.path.dirname(sys.executable)
python_scripts_dir = os.path.join(python_dir,'Scripts')


def detect_admin():
    # Windows only - Return True if program run as admin

    import subprocess
    if sys.platform == 'win32':
        command = 'net session >nul 2>&1'  # This command can only be run by admin
        try:
            output = subprocess.check_output(command, shell=True)  # Causes an exception if we can't run
        except:
            return False
    return True


def get_required_mods():
    print("A required module is missing. I'll try to install it automatically.\n")

    import subprocess, os, sys
    if sys.platform == 'win32':
        try:
            # Elevate permissions
            if not detect_admin():
                os.system('powershell -command Start-Process "python \'%s\'" -Verb runAs' % sys.argv[0].split(os.sep)[
                    -1])  # Re-run this program with elevated permissions to admin
                quit()
            # Install
            # Note: Tkinter is not available through pip nor easy_install, we assume it was packaged with Python
            print(subprocess.check_output(
                'python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org setuptools -U'))
            print(subprocess.check_output(
                'python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests -U'))
            print(subprocess.check_output(
                'python -m pip download --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow'))  # Must be done before installing or Image and ImageTk will fail
            print(subprocess.check_output(
                'python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow -U'))
        except:
            print("Failed to install. Please run: pip download setuptools")
            input('Press ENTER to exit')
            quit()

    else:
        print("Could not automatically install required modules")
        input('Press ENTER to exit')
        quit()

    # Verify install worked
    try:
        import subprocess
        import shutil, os, sys, platform, subprocess, requests
        from subprocess import PIPE, Popen
        print("Successfully installed. Will now try to run the graphical interface.")
    except:
        print("Failed to install. Please try to install manually")
        input('Press ENTER to exit')
        quit()


# Have user install Tk if this fails - we try to do it for them first
try:
    import subprocess
    import shutil, os, sys, platform, subprocess, requests
    from subprocess import PIPE, Popen
except:
    get_required_mods()

# Import local modules
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))  # Set the path, so the can find the modules
from Crossplatform import CommonUtils

install_str = "python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -U"
logfile = "TestNode_Core_Logs.log"


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True,
        encoding='utf8'
    )
    return process.communicate()[0]


# Installation function
def install(type="", module_name="", module_version=None, cmd=""):
    command = ""

    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    else:
        command = cmd
    print("installing: %s " % command)
    print(cmdline(command))


def Installer_With_Pip():
    # upgrade pip itself

    pip_module_list = ["pip", "clint", "pillow", "setuptools", "pyserial", "numpy", "simplejson", "urllib3",
                       "selenium", "uiautomator", "requests", "wheel", "pyautogui", "lxml",
                       "SpeechRecognition","colorama",
                       "python-dateutil", "Appium-Python-Client", "futures", "xlwings", "image", "tzlocal", "pyautocad",
                       "PyPDF2",
                       "pyshortcuts", "datefinder", "regex","pyttsx3==2.71",
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/PyAudio-0.2.11-cp38-cp38-win32.whl",
                       "https://github.com/AutomationSolutionz/PyGetWindow-0.0.5/archive/master.zip",
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/psutil-5.6.3-cp38-cp38-win32.whl",
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/pythonnet-2.4.1.dev0-cp38-cp38-win32.whl",
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/pywin32-225-cp38-cp38-win32.whl"
                       ]
    pip_module_win_only = ["wmi", "pyautoit", "winshell"]

    for each in pip_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
            import site
            importlib.reload(site)
        except Exception as e:
            print("{} Exception :{}".format(each, e))
            sys.stdout.error("\tAn error occurred. See log for more details.\n")

    for each in pip_module_win_only:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
        except Exception as e:
            print("{} Exception :{}".format(each, e))
            sys.stdout.error("\tAn error occurred. See log for more details.\n")

    # poster installation
    sys.stdout.write("Installing: poster3\n", True)
    command = "python poster3" + os.sep + "setup.py install"
    try:
        install(cmd=command)
    except Exception as e:
        print("poster Exception :{}".format(e))
        sys.stdout.error("\tAn error occurred. See log for more details.\n")


def Installer_With_Easy_Install():
    list_of_exe_link = [
        # "http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.8.py27.exe",
        "http://people.csail.mit.edu/hubert/pyaudio/packages/PyAudio-0.2.9-cp35-none-win_amd64.whl",
        # "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/pywin32-221.win32-py2.7.exe",
        "hashlib",
        "https://github.com/AutomationSolutionz/PyGetWindow-0.0.5/archive/master.zip"
    ]
    for each in list_of_exe_link:
        try:
            sys.stdout.write("Installing: %s\n" % each.split('/')[-1], True)  # Print to terminal window, and log file
            easy_install = "easy_install " + each
            install(cmd=easy_install)
        except Exception as e:
            print("{} Exception :{}".format(each, e))
            sys.stdout.error("\tAn error occurred. See log for more details.\n")


def Installer_With_MSI():
    list_of_msi_link = [
        "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/VCForPython27.msi",
    ]
    for each in list_of_msi_link:
        file_name = each.split('/')[-1]
        try:
            dl_path = r'%s\%s' % (python_dir, file_name)
            if not CommonUtils.Download_File(each, dl_path):
                sys.stdout.error("\tAn error occurred while downloading file. See log for more details.\n")
                # print("\tAn error occurred while downloading file. See log for more details.\n")
                return
            print("installing: %s " % file_name)
            print(os.system('msiexec /i %s /qn' % dl_path))
        except:
            # print("\tAn error occurred In Installing. See log for more details.\n")
            sys.stdout.error("\tAn error occurred In Installing. See log for more details.\n")


def Selenium_Driver_Files_Windows():
    Chrom_Driver_Download()
    Ie_Driver_Download()
    Firefox_Driver_Download()
    selenium_Server_StandAlone_Driver_Download()


def Ie_Driver_Download():
    import urllib3
    import requests
    http = urllib3.PoolManager()
    try:
        sys.stdout.write("Downloading: IE driver\n", True)  # Print to terminal window, and log file
        print("Getting latest version of IE driver")
        r = requests.get('http://selenium-release.storage.googleapis.com')
        tmp = r.text.split('/IEDriverServer_Win32')[:-1]
        latest_version = tmp[-1].split('Key>')[-1]
        print("latest version is: %s" % latest_version)
    except Exception as e:
        print("IE Exception: ", e)
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occurred. See log for more details.\n")
        return
    download_link = ('http://selenium-release.storage.googleapis.com/%s/IEDriverServer_Win32_%s.0.zip') % (
        latest_version, latest_version)
    download_link = str(download_link)
    print("Downloading latest IE 32 bit driver from: %s" % download_link)
    path = r'%s\Scripts\IEdriver_win32.zip' % python_dir
    try:
        with http.request('GET', download_link, preload_content=False) as r, open(path, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
        print("Successfully download the file: %s" % path)
        sys.stdout.write("Unpacking: IE driver\n", True)  # Print to terminal window, and log file
        CommonUtils.unzip(path, r'%s\Scripts' % python_dir)
    except Exception as e:
        print("IE Exception: ", e)
        print("Unable to download: %s " % download_link)
        sys.stdout.error("\tAn error occurred. See log for more details.\n")


def Firefox_Driver_Download():
    import requests, re
    latest_version = None
    try:
        sys.stdout.write("Downloading: Firefox driver\n", True)  # Print to terminal window, and log file
        print("Getting latest version of Firefox driver")
        r = requests.get('https://github.com/mozilla/geckodriver/releases/latest')
        raw_data = str(r.text).split('\n')

        for each in raw_data:
            if '<span class="css-truncate-target"' in each:
                result = re.search('v(.*)</span>', each)
                latest_version = "v" + result.group(1)
                print("Latest geckodriver for Firefox is: %s" % latest_version)
                break
    except Exception as e:
        print("Mozilla Exception: ", e)
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occurred. See log for more details.\n")
        return "failed"
    if not latest_version:
        latest_version = 'v0.25.0'
    download_link = ('https://github.com/mozilla/geckodriver/releases/download/%s/geckodriver-%s-win64.zip' % (
        latest_version, latest_version))
    download_link = str(download_link)
    print("Downloading latest 64bit geckodriver from: %s" % download_link)
    path = r'%s\Scripts\geckodriver.zip' % python_dir

    try:
        if not CommonUtils.Download_File(download_link, path):
            sys.stdout.error("\tAn error occurred. See log for more details.\n")
            return

        print("Successfully download the file: %s" % path)
        sys.stdout.write("Unpacking: Firefox driver\n", True)  # Print to terminal window, and log file
        CommonUtils.unzip(path, r'%s\Scripts' % python_dir)
    except Exception as e:
        print("Mozilla Exception: ", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        print(Error_Detail)
        sys.stdout.error("\tAn error occurred. See log for more details.\n")


def Chrom_Driver_Download():
    import requests
    try:
        """
        version compatibility selection steps is followed from,
        https://sites.google.com/a/chromium.org/chromedriver/downloads/version-selection
        
        """
        chrome_version = subprocess.getoutput('dir /B/AD "C:\Program Files (x86)\Google\Chrome\Application\"|findstr /R /C:"^[0-9].*\..*[0-9]$"')
        chrome_version_number = ".".join(chrome_version.split('.')[:-1])
        sys.stdout.write("Downloading: Chrome driver\n", True)  # Print to terminal window, and log file
        print("Getting compatible version of chrome driver")
        r = requests.get('http://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(chrome_version_number))
        latest_version = r.text.split('\n')[0]
        print("latest version is: %s" % latest_version)
    except Exception as e:
        print("Chrome Exception: ", e)
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occurred. See log for more details.\n")
        return

    download_link = ('http://chromedriver.storage.googleapis.com/%s/chromedriver_win32.zip' % latest_version)
    print("Downloading latest Chrome 32 bit driver from: %s" % download_link)
    path = r'%s\Scripts\chromedriver_win32.zip' % python_dir

    try:
        if not CommonUtils.Download_File(download_link, path):
            sys.stdout.error("\tAn error occurred. See log for more details.\n")
            return

        print("Successfully download the file: %s" % path)
        sys.stdout.write("Unpacking: Chrome driver\n", True)  # Print to terminal window, and log file
        CommonUtils.unzip(path, r'%s\Scripts' % python_dir)
    except Exception as e:
        print("Chrome Exception: ", e)
        print("Unable to download: %s " % download_link)
        sys.stdout.error("\tAn error occurred. See log for more details.\n")


def selenium_Server_StandAlone_Driver_Download():
    import requests
    try:
        sys.stdout.write("Downloading: Selenium driver\n", True)  # Print to terminal window, and log file
        print("Getting latest version of Selenium Server Standalone driver")
        r = requests.get('http://selenium-release.storage.googleapis.com')
        tmp = r.text.split('/selenium-server-standalone')[:-1]
        latest_version = tmp[-1].split('Key>')[-1]
        print("latest version is: %s" % latest_version)
    except Exception as e:
        print("Selenium Exception: ", e)
        print("Unable to get the latest version.")
        sys.stdout.error("\tAn error occurred. See log for more details.\n")
        return

    download_link = ('http://selenium-release.storage.googleapis.com/%s/selenium-server-standalone-%s.0.jar' % (
        latest_version, latest_version))
    download_link = str(download_link)
    print("Downloading latest selenium_Server_StandAlone: %s" % download_link)
    path = r'%s\Scripts\selenium-server-standalone.jar' % python_dir

    try:
        if not CommonUtils.Download_File(download_link, path):
            sys.stdout.error("\tAn error occurred. See log for more details.\n")
            return

        print("Successfully download the file: %s" % path)
    except Exception as e:
        print("Selenium Exception: ", e)
        print("Unable to download: %s " % download_link)
        sys.stdout.error("\tAn error occurred. See log for more details.\n")


def is_admin():
    try:
        import ctypes, sys
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def Check_Pre_Req(gui):
    admin_check = is_admin()
    if admin_check == False:
        if gui:
            sys.stdout.error(
                "We tried to obtain administrator permissions automatically but failed. Please re-run this script with administrator privledges.")
        else:
            input(
                "Please run this script as admin. Click on windows icon > type cmd OR search for cmd > right click on 'Command Line Prompt' and select 'Run as Administrator'.  Hit Enter button to exit")
        return False
    else:
        print("Admin check pass")

    if os.name != 'nt':
        sys.stdout.error("This must be run on Windows 7 and newer")
        return False
    if sys.version_info[:2] != (3, 8):
        print(sys.version_info[:2])
        sys.stdout.error("Python must be v3.8 and 32-bit")
        return False
    if platform.architecture()[0] != '32bit':
        sys.stdout.error(
            "Python must be 32 bit. Some modules which are used require 32bit Python. Please uninstall 64bit Python, and install the 32bit Python, and try again.")
        return False
    if 'setuptools' not in cmdline("easy_install --version"):
        sys.stdout.error("'easy_install' is not installed and is required")
        return False
    if 'pip' not in cmdline("pip --version"):
        sys.stdout.error(
            "pip is not installed, or not in your PATH variable. It should be located in a sub-directory of the Python directory called 'Scripts'")
        return False

    print("Pre-requirements verified successfully")
    return True


def move_all_files_from_folder(src_file, des_file):
    import os
    try:
        import shutil
        files = os.listdir(src_file)
        for f in files:
                shutil.move(src_file+os.sep+f, des_file)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print (Error_Detail)
        return "failed"


def download_dlls_for_windows_automation_and_extract():
    zip_file_destination = r'%s\DLLs\win_dll.zip' % python_dir
    dll_download_link = 'https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/win_dll.zip'
    try:
        sys.stdout.write("Downloading Necessary DLL files for Windows Automation\n", True)
        CommonUtils.Download_File(dll_download_link, zip_file_destination)
        sys.stdout.write("Download completed for necessary DLL files for Windows automation\n", True)
        sys.stdout.write("Extracting DLL files\n", True)
        CommonUtils.unzip(zip_file_destination, r'%s\DLLs' % python_dir)
        sys.stdout.write("DLL files extracted successfully\n", True)
        src_file = r'%s\DLLs\win_dll' % python_dir
        dst_file =  (r'%s\DLLs' % python_dir) 
        move_all_files_from_folder(src_file, dst_file)
    except Exception as e:
        print("Dll Exception: ", e)
        sys.stdout.error(
            "DLL file couldn't be downloaded/extracted. Please manually download it from this link: %s and extract the zip file to %s (or to the path where Python 3 is installed)" % (
                dll_download_link, zip_file_destination))

def post_win32api():
    try:
        python_where = r"where python"
        python_where_output_raw = subprocess.run(python_where, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        python_where_output_bytes = python_where_output_raw.stdout
        python_where_output_str = str(python_where_output_bytes, 'utf-8')
        post_script_file =  (python_where_output_str.split("python.exe")[0].rstrip(os.sep)) + os.sep + "Scripts" + os.sep + "pywin32_postinstall.py -install"
        post_script_file = str(post_script_file)
        os.system(post_script_file)
    except Exception as e:
        print("unable to run post script please browse to Scripts path folder and run  Scripts/pywin32_postinstall.py -install")
        sys.stdout.error("unable to run post script please browse to Scripts path folder and run  Scripts/pywin32_postinstall.py -install")
       

def main(rungui=False):
    if not rungui:  # GUI elevates already, so no need to do it again
        # If run in Windows, elevate permissions 
        if sys.platform == 'win32':
            if not detect_admin():
                os.system('powershell -command Start-Process "python \'%s\'" -Verb runAs' % sys.argv[0].split(os.sep)[
                    -1])  # Re-run this program with elevated permissions to admin
                quit()  # Exit this program, the elevated program should run

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Install
    if Check_Pre_Req(rungui):
        # Installer_With_Easy_Install()
        Installer_With_Pip()
        # Installer_With_MSI()
        Selenium_Driver_Files_Windows()
        download_dlls_for_windows_automation_and_extract()
        
        post_win32api()
        

    sys.stdout.write("If Android testing is required, please run the Android installer\n", True)

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__ == "__main__":
    main()
    input("Press ENTER to exit")
