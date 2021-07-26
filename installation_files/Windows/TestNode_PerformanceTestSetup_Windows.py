# Copyright 2015, Automation Solutionz
# ---
import os, sys
import importlib

python_dir = os.path.dirname(sys.executable)
python_scripts_dir = os.path.join(python_dir, 'Scripts')


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
from installation_files.Crossplatform import CommonUtils

install_str = "python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -U"
logfile = "TestNode_PerformanceTest_Logs.log"


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

    pip_module_list = [
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/greenlet-0.4.15-cp38-cp38-win32.whl",
                       "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/gevent-1.5a2-cp38-cp38-win32.whl",
                       "locustio", "realbrowserlocusts"
                       ]

    for each in pip_module_list:
        try:
            sys.stdout.write("Installing: %s\n" % each, True)  # Print to terminal window, and log file
            install(type="pip", module_name=each)
            import site
            importlib.reload(site)
        except Exception as e:
            print("{} Exception :{}".format(each, e))
            sys.stdout.error("\tAn error occurred. See log for more details.\n")


def Visual_C_Build_Tool():
    list_of_msi_link = [
        "https://github.com/AutomationSolutionz/InstallerHelperFiles/raw/master/Windows/visualcppbuildtools_full.exe",
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
            print(os.system('%s /Passive' % dl_path))
        except:
            # print("\tAn error occurred In Installing. See log for more details.\n")
            sys.stdout.error("\tAn error occurred In Installing. See log for more details.\n")




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
        Visual_C_Build_Tool()
        Installer_With_Pip()


    sys.stdout.write("If Android testing is required, please run the Android installer\n", True)

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)


if __name__ == "__main__":
    main()
    input("Press ENTER to exit")
