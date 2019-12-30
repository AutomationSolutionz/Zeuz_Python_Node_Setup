#!/usr/bin/env python
# Function: Download and installs Zeuz Node software
import os, os.path, glob, sys, shutil
from Crossplatform import CommonUtils

try: import subprocess  # We need commands to do anything, so if it's not installed, use subprocess to install it first
except Exception as e:
    import subprocess
    print("Module Commands is missing. I'll attempt to install it manually. If it fails, you'll need to do this yourself: sudo apt-get install python-cmd2.\n")
    print(subprocess.check_output('sudo apt-get install python-cmd2', shell = True))
    import subprocess # Try to import again


node_sw_url = 'https://github.com/AutomationSolutionz/Zeuz_Python_Node/archive/master.zip' # URL pointing to Zeuz Node
chunk_size = 4096
logfile = 'Install_Zeuz_Node_Logs.log'

# Tmp directory
if sys.platform == 'win32': tmp_dir = os.getenv('TMP')
else: tmp_dir = '/tmp'
tmp_dir = os.path.join(tmp_dir, 'ZNtmp')

def file_downloader(url, filename):
    sys.stdout.write("Downloading\n", True)
    CommonUtils.Download_File(url, filename)

    if os.path.exists(filename):
        return filename
    else:
        prints("\tError downloading\n")
        return False
    
def unzip_pkg(filename):
    prints("Unpacking\n")
    shutil.rmtree(tmp_dir, ignore_errors = True)
    result = CommonUtils.unzip(filename, tmp_dir)
    if result:
        return True
    else:
        prints("\tError unzipping\n")
        return False

def create_shortcuts(shortcut_name, target_exe_path, startin, icon_path):
    import winshell
    from win32com.client import Dispatch

    if startin is None:
        startin = winshell.desktop()

    shell = Dispatch('WScript.Shell')
    shortcut_file = os.path.join(winshell.desktop(), shortcut_name + '.lnk')
    shortcut = shell.CreateShortCut(shortcut_file)
    shortcut.Targetpath = target_exe_path
    shortcut.WorkingDirectory = startin
    shortcut.IconLocation = icon_path
    shortcut.save()

def move_zeuznode():
    try:
        # Find unpacked zeuz node directory and rename it
        os.chdir(tmp_dir)
        dirname = glob.glob('*')[0]
        os.rename(dirname, 'Zeuz_Node')
        dirname = 'Zeuz_Node'
        prints("Moving %s to Desktop\n" % dirname)
        
        # Get home directory
        if sys.platform == 'win32': homedir = os.getenv('USERPROFILE')
        else: homedir = os.getenv('HOME')
        
        # Move zeuz node to desktop
        dst = str(os.path.join(homedir, 'Desktop'))
        if os.path.exists(os.path.join(dst, dirname)): shutil.rmtree(os.path.join(dst, dirname), ignore_errors = True) # Remove desktop installation if previously done, because it will cause a failure if it exists
        shutil.move(dirname, dst)
        #create a shortcut
        try:
            from pyshortcuts import make_shortcut

            Node_file_gui = str(os.path.join(homedir, 'Desktop')) + os.sep + "ZeuZ_Node" + os.sep + "node_gui.py"
            Node_file_cli = str(os.path.join(homedir, 'Desktop')) + os.sep + "ZeuZ_Node" + os.sep + "node_cli.py"
            target_gui = Node_file_gui
            target_cli = Node_file_cli
            
            
            current_script_path = '%s'%(sys.path[0])
            ZeuZ_Icon_Path = (current_script_path.split('Zeuz_Node')[0])+os.sep+"images"+os.sep+"zeuz.ico"
            if sys.platform == 'win32':
                create_shortcuts(shortcut_name="Zeuz Node GUI",target_exe_path=target_gui,startin=None,icon_path=ZeuZ_Icon_Path)
                create_shortcuts(shortcut_name="Zeuz Node CLI",target_exe_path=target_cli,startin=None,icon_path=ZeuZ_Icon_Path)
            
            else:
                make_shortcut(target_gui, name='ZeuZ_Node',icon=ZeuZ_Icon_Path)
                make_shortcut(target_cli, name='ZeuZ_Node',icon=ZeuZ_Icon_Path)


        except Exception as e:
            print("Shortcut Exception: ", e)
            sys.stdout.error("\n Unable to create ZeuZ Short Cut\n")
            
        
        
        
        return True
    except Exception as e:
        prints("\tError moving: %s\n" % e)
        return False

def cleanup(filename):
    try:
        shutil.rmtree(tmp_dir, ignore_errors = True)
        os.unlink(filename)
    except: pass

def prints(msg):
    sys.stdout.write(msg, True) # Write all information to gui/terminal window
    
def install_all():
    filename = file_downloader(node_sw_url, 'master.zip')
    if filename == False: return False
    if unzip_pkg(filename) == False: return False
    if move_zeuznode() == False: return False
    cleanup(filename)
    prints("Zeuz Node installed on the desktop\n")

def main(rungui = True):

    # Setup logging
    CommonUtils.Logger_Setup(logfile, rungui)

    # Install
    install_all()

    # Clean up logger, and reinstate STDOUT/ERR
    CommonUtils.Logger_Teardown(logfile)

    return True

if __name__ == '__main__':
    main()
