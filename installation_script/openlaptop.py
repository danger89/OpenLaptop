#!/usr/bin/env python
import os, subprocess, sys, platform, shutil, tempfile
from subprocess import Popen, PIPE, STDOUT
from urllib2 import urlopen, URLError, HTTPError

# TODO: http://apt.alioth.debian.org/python-apt-doc/library/index.html

# Install packages should by default True, only set it False while debugging
INSTALL_PACKAGES=False

def machine():
    """Return type of machine."""
    if os.name == 'nt' and sys.version_info[:2] < (2,7):
        return os.environ.get("PROCESSOR_ARCHITEW6432", 
               os.environ.get('PROCESSOR_ARCHITECTURE', ''))
    else:
        return platform.machine()

def os_bits(machine=machine()):
    """Return bitness of operating system, or None if unknown."""
    machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
    return machine2bits.get(machine, None)

def dlfile(url, location):
    """Download file from link to filesystem"""
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(location, "wb") as local_file: #os.path.basename(url)
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

def changeHosts():
    file = "/etc/hosts"

    #Create temp file
    fh, abs_path = tempfile.mkstemp()
    new_file = open(abs_path,'w')
    host_file = open(file)
    for i,line in enumerate(host_file):
        if i==1:
            # 2nd line
            new_file.write("127.0.1.1    OpenLaptop\n")
        else:
            new_file.write(line)
    #close temp file
    new_file.close()
    os.close(fh)
    host_file.close()
    
    #Remove original file
    os.remove(file)
    #Move new file
    shutil.move(abs_path, file)

def install_packages():
    success = True

    print "### Pre process packages ###\n"
    print "Downloading deb files..."

    skype_file = "skype.deb"
    if os_bits() == 64: 
        url = "http://www.skype.com/go/getskype-linux-deb-64"
    else:
        url = "http://www.skype.com/go/getskype-linux-deb"
    if os.path.isfile(skype_file):
        print "Skype already downloaded."
    else:
        dlfile(url, skype_file)

    print "Installing debs..."
    proc = subprocess.Popen('dpkg --install skype.deb', shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash") #stdout= open (os.devnull,"wb")
    proc.wait()
    print "Done"
    print "\n\n"

    print "Add OpenLaptop PPA..."
    proc = subprocess.Popen('add-apt-repository ppa:openlaptop/stable', shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash")
    proc.wait()
    print "Done"
    print "\n\n"

    print "### Installing packages ###\n"
    print "Update package list..."
    proc = subprocess.Popen('apt-get update', shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash")
    proc.wait()
    if proc.returncode == 0:
        print "Done"
    else:
        success = False
        print "Error!\nUpdate failed:\n", proc.stdout.read()

    print "Upgrade filesystem..."
    proc = subprocess.Popen('apt-get upgrade', shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash")
    # Poll process for new output until finished
    for line in iter(proc.stdout.readline, ""):
        print line,

    proc.wait()
    if proc.returncode == 0:
        print "Done"
    else:
        success = False
        print "Error!\nUpgrade failed:\n", proc.stdout.read()

    print "Downloading & installing packages, please wait one moment..."

    # No packages (anymore): gstreamer0.10-plugins-ugly-multiverse
    codecs = ' ubuntu-restricted-extras flashplugin-installer gstreamer0.10-ffmpeg gstreamer0.10-fluendo-mp3 gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-plugins-bad-multiverse icedtea6-plugin libavcodec-extra-53 libmp4v2-2'
    archive = ' rar unrar'
    language = ' language-pack-nl language-pack-gnome-nl firefox-locale-nl'
    webcam = ' cheese cheese-common'
    remaining = ' chromium-browser vlc desktop-webmail nautilus-open-terminal synaptic'
    openlaptop = ' openlaptop'
    packages =  codecs + archive + language + webcam + remaining + openlaptop

    proc = subprocess.Popen('apt-get install -y ' + packages, shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash")

    # Poll process for new output until finished
    for line in iter(proc.stdout.readline, ""):
        print line,

    proc.wait()
    if proc.returncode == 0:
        print "Done"
    else:      
        success = False  
        print "Output:", proc.stdout.read()
        print "Error!\rTry exiting other package manager(s) (like Synaptic):\n", proc.stdout.read()
    print "\n\n"

    return success
# Using gsettings (dconf-editor) to set the settings
def enable_icons():
    success = True
    # Set username
    set_username = 'ON_USER=$(cat /etc/passwd | grep :1000: | cut -d \':\' -f 1)'
    # Set dbus
    set_debus_session = 'export DBUS_SESSION=$(grep -v "^#" /home/$ON_USER/.dbus/session-bus/`cat /var/lib/dbus/machine-id`-0)'
    # Enable menu icons
    enable_menu_icons = 'sudo -u $ON_USER $DBUS_SESSION gsettings set org.gnome.desktop.interface menus-have-icons true'
    # Enable button icons
    enable_button_icons = 'sudo -u $ON_USER $DBUS_SESSION gsettings set org.gnome.desktop.interface buttons-have-icons true'
    proc = subprocess.Popen(set_username + ' && ' + set_debus_session + ' && ' + enable_menu_icons + ' && ' + enable_button_icons, shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, executable="/bin/bash")
    proc.wait()
    if proc.returncode == 0:
        print "Done"
    else:
        success = False
        print "Error!\rCouldn't enable menu icons"
    return success

def install():
    success = True

    if INSTALL_PACKAGES:
        success = install_packages()
    else:
        print "### Skipping package installation ###\n\n" 

    print "### Post installation configure packages ###\n"

    print "Enable icons in Nautilus..."
    success = enable_icons()
   
    print "Configure desktop-webmail using gmail as default..." 

    print "\n\n"

    print "### Post installtion  packages ###\n"
    print "Editing hostname file..."
    # Open the hosts file
    hostname  = open("/etc/hostname",'w')
    try:
        hostname.write("OpenLaptop")
        print "Done"
    except:
        success = False
        print "Could not write the hostname file.\nPlease check whether the file really exists or whether you have administrator rights or not."
    hostname.close()
    print "Editing host file..."
    try:
        changeHosts()
        print "Done"
    except:
        success = False
        print "Could not write the host file.\nPlease check whether the file really exists or whether you have administrator rights or not."
    hostname.close()

    print "\n\n"

    if success:
        print "### Installation successfully completed! ###"
    else:
        print "### Installation was unsuccessfully ###"

if __name__ == "__main__":    
    # Check sudo rights
    if os.getuid() == 0:
        install()
    else:
        print "Please run this script as root. \nTry: sudo ./openlaptop.py"
        sys.exit(0)
    
