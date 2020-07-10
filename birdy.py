#! /usr/bin/env python3

import csv
import itertools
import os
from pathlib import Path    ## to use environment variables
import platform             ## to get platform name
import shutil               ## to perform file operations
import socket               ## to get host name
import subprocess           ## to invoke bash commands
import sys
import tarfile              ## to create tar archives
import time                 ## for sleep pauses and time stamps
import readline             ## avoid junk characters for backspace

# Software Name
soft_name = "Birdy"
soft_tag  = "a simple program to backup and restore files"

# Version
soft_vers = "beta 0.3.5"

## List of variables
distro          = ''
sysname         = ''
usr_inp         = ''
usr_nag         = ''
usr_num         = ''
key_num         = ''
tar             = ''
do_more         = ''
tupl            = ''
W               = ''
O               = ''
pgp_recip       = ''
remote_root     = ''
remote_dolly    = ''
remote_forklift = ''
remote_sysname  = ''
item            = ''
rel_path        = ''
dorf            = ''
enc_flag        = ''
dolly_flag      = ''
fork_flag       = ''
back_safe       = ''
local_safe      = ''
backup_path     = ''
key_list        = []

## List of colors
W  = '\033[0m'  ## white (normal)
O  = '\033[33m' ## orange
G  = '\033[92m' ## light green

## Get distro
tupl=platform.system()
distro=tupl
distro=distro.strip()

## Get hostname
sysname=(socket.gethostname())
sysname=sysname.split(".")
sysname=(sysname[0]).strip()
sysname=sysname.strip()

## Define the local directories
global user_home
user_home = os.environ['HOME']

## Define the backup directories
remote_root     = os.path.join(os.environ['HOME'], 'Dropbox')
remote_dolly    = os.path.join(remote_root, 'Linux_Shared', 'dolly_files')
remote_forklift = os.path.join(remote_root, 'Linux_Forklift') 
remote_sysname  = os.path.join(remote_root, 'Linux_Backups', sysname)

## Safety folders
back_safe   = '/tmp/backup_safety'
local_safe  = '/tmp/local_safety'

# Welcome screen
os.system('clear')
print("\nWelcome to " + str(soft_name) + " " + str(soft_vers) + " - " + str(soft_tag) + ".")

if sysname == '':
    print("\nCan't find system name...\n")
    sysname=input("Please enter a system name: ")
    if sysname == '':
        print("\nSystem needs a name...")
        sys.exit()
    else:
        print("\nThank you, this", O+ distro +W, "system will use system name", O+ sysname +W, "\n")
else:
    print("\nThis distro is", O+ distro +W, "and the system name is", O+ sysname +W)

## Check for backup folder matching current system name
if os.path.exists(remote_sysname):
    print("\nFound matching backup directory:", remote_sysname)
else:
    print("\nNo backup directory called " + str(sysname) + ", create it? y/n")
    make_dir=input("")
    if make_dir == 'y' or make_dir == 'Y':
        print("\nCreated ", remote_sysname)
        os.mkdir(remote_sysname)
    else:
        print("It can't be blank")
        sys.exit()

# The all important system_list.csv file, containing a list of files to backup
systemlist_src = os.path.join(user_home, '.config', 'birdy', 'system_list.csv')


## Let's get started
usr_inp=input("\nOptions:\n (b)ackup birdy group\n (i)ndividual files\n (r)estore\n (d)olly transfer\n (y)ank from another backup\n\nor (e)xit the program\n")

if usr_inp != 'e' :
    ## BEGIN FUNCTION LIST ##
    ## show_list_func pretty prints the list of backup candidates in system_list 
    def show_list_func():
        os.system('clear')
        system_list = []
        list10_1 = []
        list10_2 = []
        list20_1 = []
        list20_2 = []
        list30_1 = []
        list30_2 = []
        list40_1 = []
        list40_2 = []
        list50_1 = []
        list50_2 = []
        list60_1 = []
        list60_2 = []
        list70_1 = []
        list70_2 = []
        list200_1 = []
        list200_2 = []
        with open(systemlist_src) as system_list:
            reader = csv.reader(system_list, delimiter=',')
            for row in itertools.islice(reader, 1, None, None):
                space         = ''
                key           = row[0]
                key_num   = int(key)
                item          = row[1]
                group         = row[2]
                dorf          = row[3]
                enc_flag      = row[4]
                dolly_flag    = row[5]
                fork_flag     = row[6]
                local_folder  = row[7]
                rel_path      = row[8]
                backup_folder = row[9]
                if local_folder == 'user_home':
                    local_folder = user_home
                if backup_folder == 'backups':
                    backup_path = remote_sysname

                    ## BACKUP CONDITION
                    if usr_inp == 'b' or usr_inp == 'B' or usr_inp == 'I' or usr_inp == 'i':
                        if os.path.isfile(os.path.join(local_folder, rel_path, item)) or os.path.isdir(os.path.join(local_folder, rel_path, item)):
                    ## System Files
                            if key_num <= 14:
                                list10_1.append(f'[{key_num:2d}]{space:2}{item:9}')
                            elif key_num >= 15 and key_num <= 19:
                                list10_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 20-29
                            elif key_num >= 20 and key_num <= 24:
                                list20_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 25 and key_num <= 29:
                                list20_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 30-39
                            elif key_num >= 30 and key_num <= 34:
                                list30_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 35 and key_num <= 39:
                                list30_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 40-49
                            elif key_num >= 40 and key_num <= 44:
                                list40_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 45 and key_num <= 49:
                                list40_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 50-59
                            elif key_num >= 50 and key_num <= 54:
                                list50_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 55 and key_num <= 59:
                                list50_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Window Manager Configs
                            elif key_num >= 60 and key_num <= 64:
                                list60_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 65 and key_num <= 69:
                                list60_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## User Files
                            elif key_num >= 70 and key_num <= 74:
                                list70_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 75 and key_num <= 79:
                                list70_2.append(f'[{key_num:2d}]{space:2}{item}')

                    ## RESTORE CONDITION
                    if usr_inp == 'r' or usr_inp == 'R' or usr_inp == 'y' or usr_inp == 'Y':
                        if os.path.isfile(os.path.join(remote_sysname, rel_path, item)) or os.path.isfile(os.path.join(remote_sysname, rel_path, item + ".tar.bz2.gpg")) or os.path.isdir(os.path.join(remote_sysname, rel_path, item)):
                    ## System Files
                            if key_num <= 14:
                                list10_1.append(f'[{key_num:2d}]{space:2}{item:9}')
                            elif key_num >= 15 and key_num <= 19:
                                list10_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 20-29
                            elif key_num >= 20 and key_num <= 24:
                                list20_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 25 and key_num <= 29:
                                list20_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 30-39
                            elif key_num >= 30 and key_num <= 34:
                                list30_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 35 and key_num <= 39:
                                list30_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 40-49
                            elif key_num >= 40 and key_num <= 44:
                                list40_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 45 and key_num <= 49:
                                list40_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Application settings 50-59
                            elif key_num >= 50 and key_num <= 54:
                                list50_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 55 and key_num <= 59:
                                list50_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## Window Manager Configs
                            elif key_num >= 60 and key_num <= 64:
                                list60_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 65 and key_num <= 69:
                                list60_2.append(f'[{key_num:2d}]{space:2}{item}')
                    ## User Files
                            elif key_num >= 70 and key_num <= 74:
                                list70_1.append(f'[{key_num:2d}]{space:2}{item}')
                            elif key_num >= 75 and key_num <= 79:
                                list70_2.append(f'[{key_num:2d}]{space:2}{item}')

        print("System is set to " + O+ sysname +W)
        print("\nHere are the files available to birdy:\n")                 
        print("System Files")
        for c1, c2 in itertools.zip_longest(list10_1, list10_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("\nApplication Settings")
        for c1, c2 in itertools.zip_longest(list20_1, list20_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("")
        for c1, c2 in itertools.zip_longest(list30_1, list30_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("")
        for c1, c2 in itertools.zip_longest(list40_1, list40_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("")
        for c1, c2 in itertools.zip_longest(list50_1, list50_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("\nWindow Manager Configs")
        for c1, c2 in itertools.zip_longest(list60_1, list60_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        print("\nUser Files")
        for c1, c2 in itertools.zip_longest(list70_1, list70_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
    
    ## show_dolly_list_func pretty prints the list files flagged for dolly 
    def show_dolly_list_func():
        list100_1 = []
        list100_2 = []
        with open(systemlist_src) as system_list:
            reader = csv.reader(system_list, delimiter=',')
            for row in itertools.islice(reader, 1, None, None):
                space   = ''
                key     = row[0]
                key_num = int(key)
                item    = row[1]
                if key_num >= 100 and key_num <= 109:
                    list100_1.append(f'[{key_num:3d}]{space:2}{item}')
        print("\nDolly!")
        for c1, c2 in itertools.zip_longest(list100_1, list100_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
    
    ## show_fork_list_func pretty prints the list files flagged for forklift 
    def show_fork_list_func():
        list200_1 = []
        list200_2 = []
        list300_1 = []
        list300_2 = []
        with open(systemlist_src) as system_list:
            reader = csv.reader(system_list, delimiter=',')
            for row in itertools.islice(reader, 1, None, None):
                space         = ''
                key           = row[0]
                key_num   = int(key)
                item          = row[1]
                group         = row[2]
                dorf          = row[3]
                enc_flag      = row[4]
                dolly_flag    = row[5]
                fork_flag     = row[6]
                local_folder  = row[7]
                rel_path      = row[8]
                backup_folder = row[9]
                if local_folder == 'user_home':
                    local_folder = user_home
                #if backup_folder == 'backups':
                #    backup_path = remote_sysname
                if backup_folder == 'forklift':
                    backup_path = remote_forklift
                    ## BACKUP CONDITION
                    if usr_inp == 'I' or usr_inp == 'i':
                        if os.path.isfile(os.path.join(local_folder, rel_path, item)) or os.path.isdir(os.path.join(local_folder, rel_path, item)):
                    ## Forklift Archives
                            if key_num >= 200 and key_num <= 204:
                                list200_1.append(f'[{key_num:3d}]{space:2}{item}')
                            if key_num >= 205 and key_num <= 209:
                                list200_2.append(f'[{key_num:3d}]{space:2}{item}')
                            if key_num >= 300 and key_num <= 304:
                                list300_1.append(f'[{key_num:3d}]{space:2}{item}')
                    ## RESTORE CONDITION
                    if usr_inp == 'r' or usr_inp == 'R' or usr_inp == 'y' or usr_inp == 'Y':
                        if os.path.isfile(os.path.join(remote_forklift, rel_path, item)) or os.path.isfile(os.path.join(remote_forklift, rel_path, item + ".tar.bz2.gpg")) or os.path.isdir(os.path.join(remote_forklift, rel_path, item)):
                    ## Forklift Archives
                            if key_num >= 200 and key_num <= 204:
                                list200_1.append(f'[{key_num:3d}]{space:2}{item}')
                            if key_num >= 205 and key_num <= 209:
                                list200_2.append(f'[{key_num:3d}]{space:2}{item}')
                            if key_num >= 300 and key_num <= 304:
                                list300_1.append(f'[{key_num:3d}]{space:2}{item}')
        print("\nFORKLIFT - large Archive Files; individual only")
        for c1, c2 in itertools.zip_longest(list200_1, list200_2, fillvalue=''):
            print("%-30s %s" % (c1, c2))
        if list300_1:
            print("Glacier Archives")
            for c1, c2 in itertools.zip_longest(list300_1, list300_2, fillvalue=''):
                print("%-30s %s" % (c1, c2))
    
    
    # Create safety directories for intermediate steps
    def make_safety_dirs_func():
        subprocess.run(['mkdir', '-p', (os.path.join('/tmp/local_safety'))])
        subprocess.run(['mkdir', '-p', (os.path.join('/tmp/backup_safety'))])
    
    ## Create remote directory if needed
    def make_remote_dirs_func():
        subprocess.run(['mkdir', '-p', (os.path.join(remote_sysname, rel_path))])
        subprocess.run(['mkdir', '-p', (os.path.join(remote_dolly))])
        subprocess.run(['mkdir', '-p', (os.path.join(remote_forklift))])
    
    ## Create local directory if needed
    def make_loc_dirs_func():
        subprocess.run(['mkdir', '-p', (os.path.join(user_home, rel_path, item))])
    
    ## For uploads:
    ## Copy the remote ENCRYPTED target files to the backup_safety folder in /tmp
    def make_remote_safe_gpg_func():
        shutil.copy2((os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))), (os.path.join(back_safe, (item + '.tar.bz2.gpg'))))
    
    ## Copy the remote target files to the backup_safety folder in /tmp
    def make_remote_safe_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', (os.path.join(backup_path, rel_path, item)), (os.path.join(back_safe))])
        os.rename((os.path.join(back_safe, item)), (os.path.join(back_safe, (item + '_' + str(time.monotonic()))))) 
    
    ## Create a tar bz2 archive that can be encrypted with gpg
    def create_tar_func():
        tar = tarfile.open(os.path.join(local_safe, (item + '.tar.bz2')), 'w:bz2')
        tar.add(os.path.join(user_home, rel_path, item), arcname=item)
        tar.close()
    
    ## Encrypt gpg file from tar.bz2 archive
    def enc_gpg_func():
        subprocess.run(['gpg', '--yes', '-o', (os.path.join(local_safe, (item + '.tar.bz2.gpg'))), '-r', pgp_recip, '--encrypt', (os.path.join(local_safe, (item + '.tar.bz2')))])
    
    ## Move archive to remote directory
    def replace_remote_gpg_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '--progress', (os.path.join(local_safe, (item + '.tar.bz2.gpg'))), (os.path.join(backup_path, rel_path, ''))])
    
    ## Replace remote dir contents from local
    def replace_remote_dir_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '--progress', (os.path.join(user_home, rel_path, item, '')), (os.path.join(backup_path, rel_path, item, ''))])
    
    ## Replace remote file contents from local
    def replace_remote_file_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '--progress', (os.path.join(user_home, rel_path, item)), (os.path.join(backup_path, rel_path, item))])
    
    ## For downloads:
    ## Copy the LOCAL target files to the local_safety folder in /tmp
    def make_local_safe_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', (os.path.join(user_home, rel_path, item)), (os.path.join(local_safe))])
        #shutil.copytree((os.path.join(user_home, rel_path, item)), (os.path.join(local_safe, item)))
        os.rename((os.path.join(local_safe, item)), (os.path.join(local_safe, (item + '_' + str(time.monotonic()))))) 
    
    ## Decrypt gpg and extract tar.bz2 file
    def dec_gpg_func():
        subprocess.run(['gpg', '--yes', '-o', (os.path.join(back_safe, (item + '.tar.bz2'))), '--decrypt', (os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg')))])
    
    ## Extract user file from tar.bz2 archive
    def extract_tar_func():
        tar = tarfile.open(os.path.join(back_safe, (item + '.tar.bz2')), 'r:bz2')
        tar.extractall(path=(os.path.join(back_safe)))
        tar.close()
    
    ## Replace local dir contents from ENCRYPTED backup
    def replace_local_dir_enc_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '-u', '--delete', '--progress', (os.path.join(back_safe, item, '')), (os.path.join(user_home, rel_path, item, ''))])
    
    ## Replace local dir contents from backup
    def replace_local_dir_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '-u', '--delete', '--progress', (os.path.join(backup_path, rel_path, item, '')), (os.path.join(user_home, rel_path, item, ''))])
    
    ## Replace local file from ENCRYPTED backup
    def replace_local_file_enc_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '-u', '--progress', (os.path.join(back_safe, item)), (os.path.join(user_home, rel_path, item))])
    
    ## Replace local file from backup
    def replace_local_file_func():
        subprocess.run(['rsync', '-r', '-p', '-t', '-E', '-u', '--progress', (os.path.join(backup_path, rel_path, item)), (os.path.join(user_home, rel_path, item))])
    
    ## Give the backup file extracted to /tmp a unique name to not interfere with next backup
    ## MUST be kept separate since this name change would conflict with decrypting and extracting
    def unique_back_name_func():
        os.rename((os.path.join(back_safe, item)), (os.path.join(back_safe, (item + '_' + str(time.monotonic())))))
    
    ## Show the actions being performed
    def show_actions_enc_func():
        print("\nENCRYPTING...")
        print(os.path.join(user_home, rel_path, item))
        print("to...")
        print(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg')))
    
    def show_actions_dec_func():
        print("\nDECRYPTING...")
        print(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg')))
        print("to...")
        print(os.path.join(user_home, rel_path, item))
    
    def show_actions_up_func():
        print("\ncopying...")
        print(os.path.join(user_home, rel_path, item))
        print("to...")
        print(os.path.join(backup_path, rel_path, item))
    
    def show_actions_dn_func():
        print("\ncopying...")
        print(os.path.join(backup_path, rel_path, item))
        print("to...")
        print(os.path.join(user_home, rel_path, item))
    
    ## Show the option to do more work or exit the program
    def do_more_func():
        do_more=input("\nContinue? y/n? ")
        if do_more == 'y' or do_more == 'Y':
            os.system('clear')
        else:
            sys.exit()
    ## END FUNCTION LIST ##

    if usr_inp=='b':
        show_list_func()
        usr_nag=input("\nOverwrite ALL backup files? y/n ")
        if usr_nag=='y' or usr_nag=='Y':
            ## get pgp recipient name from external file
            with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                pgp_recip = pgp_recip.read().strip()
            with open (systemlist_src) as system_list:
                system_list = csv.reader(system_list, delimiter=',')
                for row in itertools.islice(system_list, 1, None, None):
                    space         = ''
                    key           = row[0]
                    key_num       = 1
                    item          = row[1]
                    group         = row[2]
                    dorf          = row[3]
                    enc_flag      = row[4]
                    dolly_flag    = row[5]
                    fork_flag     = row[6]
                    local_folder  = row[7]
                    rel_path      = row[8]
                    backup_folder = row[9]
                    if local_folder == 'user_home':
                        local_folder = user_home
                    if backup_folder == 'backups':
                        backup_path = remote_sysname
                    elif backup_folder == 'dolly':
                        backup_path = remote_dolly
                    elif backup_folder == 'forklift':
                        backup_path = remote_forklift
                       
                    if system_list:
                        if fork_flag == 'x' and dolly_flag != 'L':
                            if enc_flag == 'E' or enc_flag == 'e':
                                make_safety_dirs_func()
                                ## See if the local dir exists
                                if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                    ## See if the remote gpg exists and copy it to safety
                                    if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                        make_remote_safe_gpg_func()
                                    else:
                                        pass
                                    show_actions_enc_func()
                                    ## Create tar archive in /tmp
                                    create_tar_func()
                                    ## Create gpg encrypted file from /tmp
                                    enc_gpg_func()
                                    ## Create the remote directories if needed
                                    make_remote_dirs_func()
                                    ## Move archive to remote directory
                                    replace_remote_gpg_func()
                                else:
                                    ## First see if the local file exists
                                    if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                        ## Then see if the remote file exists and copy it to safety
                                        if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                            make_remote_safe_gpg_func()
                                        else:
                                            pass
                                        show_actions_enc_func()
                                        ## Create tar archive in /tmp
                                        create_tar_func()
                                        ## Create gpg encrypted file from /tmp
                                        enc_gpg_func()
                                        ## Create the remote directories if needed
                                        make_remote_dirs_func()
                                        ## Move archive to remote directory
                                        replace_remote_gpg_func()
                                    else:
                                        pass
                            elif enc_flag == 'n':
                                make_safety_dirs_func()
                                ## First see if the local dir exists
                                if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                    ## Then see if the remote dir exists and copy it to safety
                                    if os.path.isdir(os.path.join(backup_path, rel_path, item)):
                                        make_remote_safe_func()
                                    else:
                                        pass
                                    show_actions_up_func()
                                    make_remote_dirs_func()
                                    replace_remote_dir_func()
                                else:
                                    ## First see if the local file exists
                                    if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                        ## Then see if the remote file exists and copy it to safety
                                        if os.path.isfile(os.path.join(backup_path, rel_path, item)):
                                            make_remote_safe_func()
                                        else:
                                            pass
                                        show_actions_up_func()
                                        make_remote_dirs_func()
                                        replace_remote_file_func()
                                    else:
                                        pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        print("Check the backup list, it seems to be empty.")
                        sys.exit()
                print("")
                print("Backup complete!")
                print("")
        else:
            sys.exit()
    
    elif usr_inp == 'i':
        while usr_inp == 'i':
            show_list_func()
            show_fork_list_func()
            with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                pgp_recip = pgp_recip.read().strip()
            with open (systemlist_src) as system_list:
                system_list = csv.reader(system_list, delimiter=',')
                for row in itertools.islice(system_list, 1, None, None):
                    space         = ''
                    key           = row[0]
                    item          = row[1]
                    group         = row[2]
                    dorf          = row[3]
                    enc_flag      = row[4]
                    dolly_flag    = row[5]
                    fork_flag     = row[6]
                    local_folder  = row[7]
                    rel_path      = row[8]
                    backup_folder = row[9]
                    if local_folder == 'user_home':
                        local_folder = user_home
                    if backup_folder == 'backups':
                        backup_path = remote_sysname
                    elif backup_folder == 'dolly':
                        backup_path = remote_dolly
                    elif backup_folder == 'forklift':
                        backup_path = remote_forklift
                    key_list.extend((key, item, group, dorf, enc_flag, dolly_flag, fork_flag, local_folder, rel_path, backup_folder))
    
                usr_num=''
                usr_num=input("\nYou can (e)xit or enter a number: ")
                if usr_num=='e':
                    sys.exit()
                else:
                    if usr_num not in key_list:
                        print("[" + str(usr_num) + "]","is not an option.  Nothing copied.")
                        do_more_func()
                        continue
                    else:
                        key_index = key_list.index(usr_num)
                        item_index          = key_index + 1
                        group_index         = key_index + 2 
                        dorf_index          = key_index + 3 
                        enc_flag_index      = key_index + 4 
                        dolly_flag_index    = key_index + 5 
                        fork_flag_index     = key_index + 6 
                        local_folder_index  = key_index + 7
                        rel_path_index      = key_index + 8 
                        backup_folder_index = key_index + 9 
                        key           = usr_num
                        item          = key_list[item_index].strip()
                        group         = key_list[group_index].strip()
                        dorf          = key_list[dorf_index].strip()
                        enc_flag      = key_list[enc_flag_index].strip()
                        dolly_flag    = key_list[dolly_flag_index].strip()
                        fork_flag     = key_list[fork_flag_index].strip()
                        local_folder  = key_list[local_folder_index].strip()
                        rel_path      = key_list[rel_path_index].strip()
                        backup_folder = key_list[backup_folder_index].strip()
                        if local_folder == 'user_home':
                            local_folder = user_home
                        if backup_folder == 'backups':
                           backup_path = remote_sysname
                        elif backup_folder == 'dolly':
                           backup_path = remote_dolly
                        elif backup_folder == 'forklift':
                           backup_path = remote_forklift
    
                    if enc_flag == 'E':
                        make_safety_dirs_func()
                        if os.path.isdir(os.path.join(user_home, rel_path, item)):
                            if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                make_remote_safe_gpg_func()
                            else:
                                pass
                            show_actions_enc_func()
                            create_tar_func()
                            enc_gpg_func()
                            make_remote_dirs_func()
                            replace_remote_gpg_func()
                        else:
                            if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                    make_remote_safe_gpg_func()
                                else:
                                    pass
                                show_actions_enc_func()
                                create_tar_func()
                                enc_gpg_func()
                                make_remote_dirs_func()
                                replace_remote_gpg_func()
                            else:
                                print(item, "is not found on this system")
                    else:
                        make_safety_dirs_func()
                        if os.path.isdir(os.path.join(user_home, rel_path, item)):
                            if os.path.isdir(os.path.join(backup_path, rel_path, item)):
                                make_remote_safe_func()
                            else:
                                pass
                            show_actions_up_func()
                            make_remote_dirs_func()
                            replace_remote_dir_func()
                        else:
                            if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                if os.path.isfile(os.path.join(backup_path, rel_path, item)):
                                    make_remote_safe_func()
                                else:
                                    pass
                                show_actions_up_func()
                                make_remote_dirs_func()
                                replace_remote_file_func()
                            else:
                                print(item, "is not found on this system")
                do_more_func()
    
    elif usr_inp=='r':
        while usr_inp == 'r':
            show_list_func()
            show_fork_list_func()
            with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                pgp_recip = pgp_recip.read().strip()
            with open (systemlist_src) as system_list:
                system_list = csv.reader(system_list, delimiter=',')
                for row in itertools.islice(system_list, 1, None, None):
                    space         = ''
                    key           = row[0]
                    item          = row[1]
                    group         = row[2]
                    dorf          = row[3]
                    enc_flag      = row[4]
                    dolly_flag    = row[5]
                    fork_flag     = row[6]
                    local_folder  = row[7]
                    rel_path      = row[8]
                    backup_folder = row[9]
                    if local_folder == 'user_home':
                        local_folder = user_home
                    if backup_folder == 'backups':
                        backup_path = remote_sysname
                    elif backup_folder == 'dolly':
                        backup_path = remote_dolly
                    elif backup_folder == 'forklift':
                        backup_path = remote_forklift
                    key_list.extend((key, item, group, dorf, enc_flag, dolly_flag, fork_flag, local_folder, rel_path, backup_folder))
                   
                usr_num=''
                usr_num=input("\nYou can (e)xit or enter a number: ")
                if usr_num=='e':
                    sys.exit()
                else:
                    if usr_num not in key_list:
                        print("[" + str(usr_num) + "]","is not an option.  Nothing copied.")
                        do_more_func()
                        continue
                    else:
                        key_index = key_list.index(usr_num)
                        item_index          = key_index + 1
                        group_index         = key_index + 2 
                        dorf_index          = key_index + 3 
                        enc_flag_index      = key_index + 4 
                        dolly_flag_index    = key_index + 5 
                        fork_flag_index     = key_index + 6 
                        local_folder_index  = key_index + 7
                        rel_path_index      = key_index + 8 
                        backup_folder_index = key_index + 9 
                        key           = usr_num
                        item          = key_list[item_index].strip()
                        group         = key_list[group_index].strip()
                        dorf          = key_list[dorf_index].strip()
                        enc_flag      = key_list[enc_flag_index].strip()
                        dolly_flag    = key_list[dolly_flag_index].strip()
                        fork_flag     = key_list[fork_flag_index].strip()
                        local_folder  = key_list[local_folder_index].strip()
                        rel_path      = key_list[rel_path_index].strip()
                        backup_folder = key_list[backup_folder_index].strip()
                        if local_folder == 'user_home':
                            local_folder = user_home
                        if backup_folder == 'backups':
                           backup_path = remote_sysname
                        elif backup_folder == 'dolly':
                           backup_path = remote_dolly
                        elif backup_folder == 'forklift':
                           backup_path = remote_forklift
    
                    ## if local target is encrypted
                    if enc_flag == 'E':
                        make_safety_dirs_func()
                        ## if local target is a directory
                        if dorf == 'D':
                            ## if local target exists
                            if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_dir_enc_func()
                                unique_back_name_func()
                            ## if local target does not exist
                            else:
                                make_loc_dirs_func() 
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_dir_enc_func()
                                unique_back_name_func()
                        ## if local target is a file
                        elif dorf == 'f':
                            ## if local target exists
                            if os.path.isfile(os.path.join(user_home, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_file_enc_func()
                                unique_back_name_func()
                            ## if local target does not exist
                            else:
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_file_enc_func()
                                unique_back_name_func()
                        else:
                            pass
                    ## if local target is NOT encrypted
                    else:
                        make_safety_dirs_func()
                        ## if local target is a directory
                        if dorf == 'D':
                            ## if local target exists
                            if os.path.isdir(os.path.join(user_home, rel_path, item)):
                               make_local_safe_func()
                               ## replace the local target
                               show_actions_dn_func()
                               replace_local_dir_func()
                            ## if local target does not exist
                            else:
                               make_loc_dirs_func()
                               ## replace the local target
                               show_actions_dn_func()
                               replace_local_dir_func()
                        ## if local target is a file
                        elif dorf == 'f':
                            ## if local target exists
                            if os.path.isfile(os.path.join(user_home, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dn_func()
                                replace_local_file_func()
                            ## if local target does not exist
                            else:
                                ## replace the local target
                                show_actions_dn_func()
                                replace_local_file_func()
                        else:
                            pass
                print("")
                print("Restore complete!")
                print("")
                do_more_func()
    
    elif usr_inp=='d':
        os.system('clear')
        dolly_inp = input("\n\nDOLLY! (s)end or (r)eceive?\n")
        if dolly_inp == 's' or dolly_inp == 'S':
            show_dolly_list_func()
            usr_nag=input("\nOverwrite ALL backup files? y/n \n")
            if usr_nag=='y' or usr_nag=='Y':
                with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                    pgp_recip = pgp_recip.read().strip()
                with open (systemlist_src) as system_list:
                    system_list = csv.reader(system_list, delimiter=',')
                    for row in itertools.islice(system_list, 1, None, None):
                        space         = ''
                        key           = row[0]
                        key_num       = 1
                        item          = row[1]
                        group         = row[2]
                        dorf          = row[3]
                        enc_flag      = row[4]
                        dolly_flag    = row[5]
                        fork_flag     = row[6]
                        local_folder    = row[7]
                        rel_path      = row[8]
                        backup_folder = row[9]
                        if local_folder == 'user_home':
                            local_folder = user_home
                        if backup_folder == 'backups':
                            backup_path = remote_sysname
                        elif backup_folder == 'dolly':
                            backup_path = remote_dolly
                        elif backup_folder == 'forklift':
                            backup_path = remote_forklift
    
                        if system_list:
                            if dolly_flag == 'L':
                                if enc_flag == 'E':
                                    make_safety_dirs_func()
                                    ## See if the local dir exists
                                    if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                        ## See if the remote gpg exists and copy it to safety
                                        if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                            make_remote_safe_gpg_func()
                                        else:
                                            pass
                                        show_actions_enc_func()
                                        ## Create tar archive in /tmp
                                        create_tar_func()
                                        ## Create gpg encrypted file from /tmp
                                        enc_gpg_func()
                                        ## Create the remote directories if needed
                                        make_remote_dirs_func()
                                        ## Move archive to remote directory
                                        replace_remote_gpg_func()
                                    else:
                                        ## First see if the local file exists
                                        if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                            ## Then see if the remote file exists and copy it to safety
                                            if os.path.isfile(os.path.join(backup_path, rel_path, (item + '.tar.bz2.gpg'))):
                                                make_remote_safe_gpg_func()
                                            else:
                                                pass
                                            show_actions_enc_func()
                                            ## Create tar archive in /tmp
                                            create_tar_func()
                                            ## Create gpg encrypted file from /tmp
                                            enc_gpg_func()
                                            ## Create the remote directories if needed
                                            make_remote_dirs_func()
                                            ## Move archive to remote directory
                                            replace_remote_gpg_func()
                                        else:
                                            pass
                                elif enc_flag == 'n':
                                    make_safety_dirs_func()
                                    ## First see if the local dir exists
                                    if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                        ## Then see if the remote dir exists and copy it to safety
                                        if os.path.isdir(os.path.join(backup_path, rel_path, item)):
                                            make_remote_safe_func()
                                        else:
                                            pass
                                        show_actions_up_func()
                                        make_remote_dirs_func()
                                        replace_remote_dir_func()
                                    else:
                                        ## First see if the local file exists
                                        if os.path.isfile(os.path.join(user_home, rel_path, item)):
                                            ## Then see if the remote file exists and copy it to safety
                                            if os.path.isfile(os.path.join(backup_path, rel_path, item)):
                                                make_remote_safe_func()
                                            else:
                                                pass
                                            show_actions_up_func()
                                            make_remote_dirs_func()
                                            replace_remote_file_func()
                                        else:
                                            pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            print("Check the backup list, it seems to be empty.")
                            sys.exit()
                print("")
                print("Backup complete!")
                print("")
            else:
                sys.exit()
        elif dolly_inp == 'r' or dolly_inp == 'R':
            show_dolly_list_func()
            usr_nag=input("\nOverwrite LOCAL files? y/n \n")
            if usr_nag=='y':
                with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                    pgp_recip = pgp_recip.read().strip()
                with open (systemlist_src) as system_list:
                    system_list = csv.reader(system_list, delimiter=',')
                    for row in itertools.islice(system_list, 1, None, None):
                        space         = ''
                        key           = row[0]
                        key_num       = 1
                        item          = row[1]
                        group         = row[2]
                        dorf          = row[3]
                        enc_flag      = row[4]
                        dolly_flag    = row[5]
                        fork_flag     = row[6]
                        local_folder  = row[7]
                        rel_path      = row[8]
                        backup_folder = row[9]
                        if local_folder == 'user_home':
                            local_folder = user_home
                        if backup_folder == 'backups':
                            backup_path = remote_sysname
                        elif backup_folder == 'dolly':
                            backup_path = remote_dolly
                        elif backup_folder == 'forklift':
                            backup_path = remote_forklift
    
                        if system_list:
                            if dolly_flag == 'L':
                              ## if local target is encrypted
                                if enc_flag == 'E':
                                    make_safety_dirs_func()
                                    ## if local target is a directory
                                    if dorf == 'D':
                                        ## if local target exists
                                        if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                            make_local_safe_func()
                                            ## replace the local target
                                            show_actions_dec_func()
                                            dec_gpg_func()
                                            extract_tar_func()
                                            replace_local_dir_enc_func()
                                            unique_back_name_func()
                                        ## if local target does not exist
                                        else:
                                            make_loc_dirs_func() 
                                            ## replace the local target
                                            show_actions_dec_func()
                                            dec_gpg_func()
                                            extract_tar_func()
                                            replace_local_dir_enc_func()
                                            unique_back_name_func()
                                    ## if local target is a file
                                    elif dorf == 'f':
                                        ## if local target exists
                                        if os.path.isfile(os.path.join(user_home, item)):
                                            make_local_safe_func()
                                            ## replace the local target
                                            show_actions_dec_func()
                                            dec_gpg_func()
                                            extract_tar_func()
                                            replace_local_file_enc_func()
                                            unique_back_name_func()
                                        ## if local target does not exist
                                        else:
                                            ## replace the local target
                                            show_actions_dec_func()
                                            dec_gpg_func()
                                            extract_tar_func()
                                            replace_local_file_enc_func()
                                            unique_back_name_func()
                                    else:
                                        pass
                                ## if local target is NOT encrypted
                                else:
                                    make_safety_dirs_func()
                                    ## if local target is a directory
                                    if dorf == 'D':
                                        ## if local target exists
                                        if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                           make_local_safe_func()
                                           ## replace the local target
                                           show_actions_dn_func()
                                           replace_local_dir_func()
                                        ## if local target does not exist
                                        else:
                                           make_loc_dirs_func()
                                           ## replace the local target
                                           show_actions_dn_func()
                                           replace_local_dir_func()
                                    ## if local target is a file
                                    elif dorf == 'f':
                                        ## if local target exists
                                        if os.path.isfile(os.path.join(user_home, item)):
                                            make_local_safe_func()
                                            ## replace the local target
                                            show_actions_dn_func()
                                            replace_local_file_func()
                                        ## if local target does not exist
                                        else:
                                            ## replace the local target
                                            show_actions_dn_func()
                                            replace_local_file_func()
                            else:
                                pass
        else:
            print("[" + str(dolly_inp) + "] is not an option.  Nothing copied.")
            do_more_func()
    
    elif usr_inp=='y':
        print("\nHere are the current backup folders: \n")
        backlist = []
        for dirname in os.listdir(os.path.join(remote_root, 'Linux_Backups')):
            backlist.append(dirname)
        for name in sorted(backlist[0:]):
             print(name) 
        altsys=input("\nYour selection: ")
        test_altsys = 1
        while test_altsys == 1:
            if altsys in backlist:
                remote_sysname = os.path.join(remote_root, "Linux_Backups", altsys)
                print("")
                print("Thank you, this", O+ distro +W, "system will use system name", O+ altsys +W)
                test_altsys=0
                time.sleep(2)
            else:
                altsys=input("'" + altsys + "'" + " is not listed.  Your selection: ")
    
        while usr_inp == 'y':
            show_list_func()
            with open(os.path.join(user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
                pgp_recip = pgp_recip.read().strip()
            with open (systemlist_src) as system_list:
                system_list = csv.reader(system_list, delimiter=',')
                for row in itertools.islice(system_list, 1, None, None):
                    space         = ''
                    key           = row[0]
                    item          = row[1]
                    group         = row[2]
                    dorf          = row[3]
                    enc_flag      = row[4]
                    dolly_flag    = row[5]
                    fork_flag     = row[6]
                    local_folder  = row[7]
                    rel_path      = row[8]
                    backup_folder = row[9]
                    if local_folder == 'user_home':
                        local_folder = user_home
                    if backup_folder == 'backups':
                        backup_path = remote_sysname
                    elif backup_folder == 'dolly':
                        backup_path = remote_dolly
                    elif backup_folder == 'forklift':
                        backup_path = remote_forklift
                    key_list.extend((key, item, group, dorf, enc_flag, dolly_flag, fork_flag, local_folder, rel_path, backup_folder))
                   
                usr_num=''
                usr_num=input("\nYou can (e)xit or enter a number: ")
                if usr_num=='e':
                    sys.exit()
                else:
                    if usr_num not in key_list:
                        print("[" + str(usr_num) + "]","is not an option.  Nothing copied.")
                        do_more_func()
                        continue
                    else:
                        key_index = key_list.index(usr_num)
                        item_index          = key_index + 1
                        group_index         = key_index + 2 
                        dorf_index          = key_index + 3 
                        enc_flag_index      = key_index + 4 
                        dolly_flag_index    = key_index + 5 
                        fork_flag_index     = key_index + 6 
                        local_folder_index  = key_index + 7
                        rel_path_index      = key_index + 8 
                        backup_folder_index = key_index + 9 
                        key           = usr_num
                        item          = key_list[item_index].strip()
                        group         = key_list[group_index].strip()
                        dorf          = key_list[dorf_index].strip()
                        enc_flag      = key_list[enc_flag_index].strip()
                        dolly_flag    = key_list[dolly_flag_index].strip()
                        fork_flag     = key_list[fork_flag_index].strip()
                        local_folder  = key_list[local_folder_index].strip()
                        rel_path      = key_list[rel_path_index].strip()
                        backup_folder = key_list[backup_folder_index].strip()
                        if local_folder == 'user_home':
                            local_folder = user_home
                        if backup_folder == 'backups':
                           backup_path = remote_sysname
                        elif backup_folder == 'dolly':
                           backup_path = remote_dolly
                        elif backup_folder == 'forklift':
                           backup_path = remote_forklift
    
                    ## if local target is encrypted
                    if enc_flag == 'E':
                        make_safety_dirs_func()
                        ## if local target is a directory
                        if dorf == 'D':
                            ## if local target exists
                            if os.path.isdir(os.path.join(user_home, rel_path, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_dir_enc_func()
                                unique_back_name_func()
                            ## if local target does not exist
                            else:
                                make_loc_dirs_func() 
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_dir_enc_func()
                                unique_back_name_func()
                        ## if local target is a file
                        elif dorf == 'f':
                            ## if local target exists
                            if os.path.isfile(os.path.join(user_home, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_file_enc_func()
                                unique_back_name_func()
                            ## if local target does not exist
                            else:
                                ## replace the local target
                                show_actions_dec_func()
                                dec_gpg_func()
                                extract_tar_func()
                                replace_local_file_enc_func()
                                unique_back_name_func()
                        else:
                            pass
                    ## if local target is NOT encrypted
                    else:
                        make_safety_dirs_func()
                        ## if local target is a directory
                        if dorf == 'D':
                            ## if local target exists
                            if os.path.isdir(os.path.join(user_home, rel_path, item)):
                               make_local_safe_func()
                               ## replace the local target
                               show_actions_dn_func()
                               replace_local_dir_func()
                            ## if local target does not exist
                            else:
                               make_loc_dirs_func()
                               ## replace the local target
                               show_actions_dn_func()
                               replace_local_dir_func()
                        ## if local target is a file
                        elif dorf == 'f':
                            ## if local target exists
                            if os.path.isfile(os.path.join(user_home, item)):
                                make_local_safe_func()
                                ## replace the local target
                                show_actions_dn_func()
                                replace_local_file_func()
                            ## if local target does not exist
                            else:
                                ## replace the local target
                                show_actions_dn_func()
                                replace_local_file_func()
                        else:
                            pass
                print("")
                print("Restore complete!")
                print("")
                do_more_func()
else:
    sys.exit()
