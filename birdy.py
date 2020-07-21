#! /usr/bin/env python3

# MIT License

# Copyright (c) 2020 afhpayne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# 79 spaces-------------------------------------------------------------------|
import csv
import glob
import itertools
import os
from pathlib import Path    ## to use environment variables
import platform             ## to get platform name
import readline             ## avoid junk characters for backspace
import shutil               ## to perform file operations
import socket               ## to get host name
import subprocess           ## to invoke bash commands
import sys
import tarfile              ## to create tar archives
import time                 ## for sleep pauses and time stamps

# Software Name
soft_name = "Birdy"
soft_tag  = "a simple program to backup and restore files"

# Version
soft_vers = "0.4.0"

# Colors
W = '\033[0m'  # white (normal)
O = '\033[33m' # orange
G = '\033[92m' # light green

# Get distro
tupl = platform.system()
distro = tupl
distro = distro.strip()

# Get hostname
sysname = (socket.gethostname())
sysname = sysname.split(".")
sysname = (sysname[0]).strip()

# Define the local directories
global user_home
user_home = os.environ['HOME']

# Define the backup directories
remote_base = os.path.join(os.environ['HOME'], 'Dropbox')
remote_dolly = os.path.join(remote_base, 'Linux_Shared', 'dolly_files')
remote_forklift = os.path.join(remote_base, 'Linux_Forklift')
remote_backup = os.path.join(remote_base, 'Linux_Backups')
remote_sysname = os.path.join(remote_base, 'Linux_Backups', sysname)

# Safety folders
back_safe = os.path.join("/tmp/backup_safety")
local_safe = os.path.join("/tmp/local_safety")
birdy_work = os.path.join("/tmp/birdy_work")

# Birdy config file
systemlist_src = os.path.join(user_home, ".config", "birdy", "system_list.csv")

# Birdy pgp_email
with open(
        os.path.join(
            user_home, '.config', 'birdy', 'pgp_email.txt'), 'r') as pgp_recip:
    pgp_recip = pgp_recip.read().strip()

# Lists
system_list_full = []
system_list_pruned = []
system_list_basic = []
system_list_dolly = []
system_list_fork = []

enc_list = []
unenc_list = []
dolly_list = []
fork_list = []

key_enc_pretty = []
key_unenc_pretty = []
key_dolly_pretty = []
key_fork_pretty = []

# Dictionaries
syslist_dict = {}

# Make a python list from the CSV config
def read_system_list_func():
    # os.system('clear')
    with open(systemlist_src) as system_list:
        reader = csv.reader(system_list, delimiter=',')
        for row in itertools.islice(reader, 1, None, None):
            system_list_full.append(row)


# Filters files not present on the system
def prune_system_list_4backup_func():
    for row in system_list_full:
        if row[7] == "user_home":
            item_path = os.path.join(user_home, row[8], row[1])
        else:
            item_path = os.path.join(row[7], row[8], row[1])
        if os.path.isfile(item_path) or os.path.isdir(item_path):
            system_list_pruned.append(row)


# Filters files not present in the backup
def prune_system_list_4restore_func():
    for row in system_list_full:
        if (row[7] == "user_home" and
            row[4] == "n" and
            row[5] == "x" and
            row[6] == "x"):
            item_path = os.path.join(
                remote_sysname, row[8], row[1])
        elif (row[7] == "user_home" and
              row[4] == "E" and
              row[5] == "x" and
              row[6] == "x"):
            item_path = os.path.join(
                remote_sysname, row[8], (row[1] + ".tar.bz2.gpg"))
        elif (row[7] == "user_home" and
              row[4] == "E" and
              row[5] == "L" and
              row[6] == "x"):
            item_path = os.path.join(
                remote_dolly, row[8], (row[1] + ".tar.bz2.gpg"))
        elif (row[7] == "user_home" and
              row[4] == "E" and
              row[5] == "x" and
              row[6] == "F"):
            item_path = os.path.join(
                remote_forklift, row[8], (row[1] + ".tar.bz2.gpg"))
        else:
            item_path = os.path.join(
                remote_sysname, row[7], row[8], row[1])
        if os.path.isfile(item_path) or os.path.isdir(item_path):
            system_list_pruned.append(row)


# Make the three group lists
def make_group_lists_func():
    for row in system_list_pruned:
        if int(row[0]) < 99:
            system_list_basic.append(row)
        if 100 <= int(row[0]) < 200:
            system_list_dolly.append(row)
        if 200 <= int(row[0]) < 300:
            system_list_fork.append(row)


def make_sorted_lists_func():
    for row in system_list_pruned:
        if int(row[0]) <= 99 and row[4] == "E":
            enc_list.append(os.path.join(row[8], row[1]))
            enc_list.sort()
        if int(row[0]) <= 99 and row[4] == "n":
            unenc_list.append(os.path.join(row[8], row[1]))
            unenc_list.sort()
        if 100 <= int(row[0]) < 200 and row[5] == "L":
            dolly_list.append(os.path.join(row[8], row[1]))
            dolly_list.sort()
        if 200 <= int(row[0]) < 300 and row[6] == "F":
            fork_list.append(os.path.join(row[8], row[1]))
            fork_list.sort()


def make_sorted_lists_keys_func():
    key_enc = list(range(1, (1 + len(enc_list))))
    for i in key_enc:
        key_enc_pretty.append("[" + str(i) + "]")

    key_unenc = list(range(50, (50 + len(unenc_list))))
    for i in key_unenc:
        key_unenc_pretty.append("[" + str(i) + "]")

    key_dolly = list(range(100, (100 + len(dolly_list))))
    for i in key_dolly:
        key_dolly_pretty.append("[" + str(i) + "]")

    key_fork = list(range(200, (200 + len(fork_list))))
    for i in key_fork:
        key_fork_pretty.append("[" + str(i) + "]")


def print_pruned_sorted_system_list_func():
    print('{:<35}{:<35}{:<36}{:<}'.format(
        "Encrypted", "Unencrypted", "Dolly Files", "Forklift Files\n"))
    for c1,c2,c3,c4,c5,c6,c7,c8 in itertools.zip_longest(
            key_enc_pretty,
            enc_list,
            key_unenc_pretty,
            unenc_list,
            key_dolly_pretty,
            dolly_list,
            key_fork_pretty,
            fork_list,
            fillvalue=""):
        print('{:<5}{:<30}{:<5}{:<30}{:<6}{:<30}{:<6}{}'.format(
            c1, c2, c3, c4, c5, c6, c7, c8))


def print_basic_list_func():
    print('{:<35}{:<30}'.format(
        "Encrypted", "Unencrypted\n"))
    for c1,c2,c3,c4 in itertools.zip_longest(
            key_enc_pretty,
            enc_list,
            key_unenc_pretty,
            unenc_list,
            fillvalue=""):
        print('{:<5}{:<30}{:<5}{:<30}'.format(
            c1, c2, c3, c4))


def print_dolly_list_func():
    print('{:<}'.format(
        "Dolly Files\n"))
    for c1,c2 in itertools.zip_longest(
            key_dolly_pretty,
            dolly_list,
            fillvalue=""):
        print('{:<6}{}'.format(
            c1, c2))


# Make dictionaries to reference user input to backup items
def make_dicts_for_input_func():
    key_1 = 1
    key_50 = 50
    key_100 = 100
    key_200 = 200
    for i in enc_list:
        i = i.split("/")
        try:
            syslist_dict.update({key_1:i[1]})
        except(IndexError):
            syslist_dict.update({key_1:i[0]})
        key_1 += 1
    for i in unenc_list:
        i = i.split("/")
        try:
            syslist_dict.update({key_50:i[1]})
        except(IndexError):
            syslist_dict.update({key_50:i[0]})
        key_50 += 1
    for i in dolly_list:
        syslist_dict.update({key_100:i})
        key_100 += 1
    for i in fork_list:
        i = i.split("/")
        try:
            syslist_dict.update({key_200: i[1]})
        except(IndexError):
            syslist_dict.update({key_200: i[0]})
        key_200 += 1


# Create safety directories for local and remote files
def make_safety_dirs_func():
    if os.path.isdir(back_safe):
        shutil.rmtree(back_safe)
    subprocess.run(['mkdir', '-p', back_safe])
    if os.path.isdir(local_safe):
        shutil.rmtree(local_safe)
    subprocess.run(['mkdir', '-p', local_safe])
    if os.path.isdir(birdy_work):
        shutil.rmtree(birdy_work)
    subprocess.run(['mkdir', '-p', birdy_work])


# BACKUP FUNCTIONS------------------------------------------------------------|
# Copy remote target files to /tmp/backup_safety
# def make_remote_safe_func():
#     if dolly  == "L":
#         path_concat_remote = os.path.join(remote_dolly)
#     elif fork == "F":
#         path_concat_remote = os.path.join(remote_forklift)
#     else:
#         path_concat_remote = os.path.join(
#             remote_base, back_base, sysname, local_path, back_path)
#         subprocess.run(
#             ['mkdir', '-p', path_concat_remote])
#         copy_remote_files_func()
#         path_concat_backsafe = os.path.join(
#             back_safe, back_path, local_path, '')
#         subprocess.run(
#             ['mkdir', '-p', path_concat_backsafe])
#         path_concat_localsafe = os.path.join(
#             local_safe, back_path, local_path, '')
#         subprocess.run(
#             ['mkdir', '-p', path_concat_localsafe])


def copy_remote_files_func():
    simple_remote_path = (os.path.join(
        remote_base,
        back_base,
        sysname,
        local_path,
        back_path))
    simple_backsafe_path = (os.path.join(
        back_safe,
        local_path,
        back_path))
    simple_localsafe_path = (os.path.join(
        local_safe,
        local_path,
        back_path))
    
    # if os.path.isfile(os.path.join(
    #     simple_remote_path, (
    #         item +
    #         ".tar.bz2.gpg"))):
    #     subprocess.run(
    #         ['rsync', '-p', '-t', '-E', (
    #             os.path.join(
    #                 simple_remote_path,
    #                 (item + '.tar.bz2.gpg'))), (
    #                     os.path.join(
    #                         simple_backsafe_path,
    #                         (item + '.tar.bz2.gpg')))]
    #     )
    # if os.path.isdir(os.path.join(
    #         simple_remote_path,
    #         item)):
    #     subprocess.run(
    #         ['rsync', '-r', '-p', '-t', '-E', (
    #             os.path.join(
    #                 simple_remote_path,
    #                 item)), (
    #                     os.path.join(
    #                         simple_backsafe_path,
    #                         item))]
    #     )
    # if os.path.isfile(os.path.join(
    #         simple_remote_path,
    #         item)):
    #     subprocess.run(
    #         ['rsync', '-p', '-t', '-E', (os.path.join(
    #             simple_remote_path,
    #             item)), (
    #                 os.path.join(
    #                     simple_backsafe_path,
    #                     item))]
    #     )


# def copy_remote_files_func():
#     if os.path.isfile(os.path.join(path_concat_remote, (item + ".tar.bz2.gpg"))) is True:
#         subprocess.run(
#             ['rsync', '-p', '-t', '-E', (os.path.join(
#                 path_concat_remote, (item + '.tar.bz2.gpg'))), (
#                     os.path.join(
#                         path_concat_backsafe, (item + '.tar.bz2.gpg')))])
#     if os.path.isdir(path_concat_remote + item) is True:
#         subprocess.run(
#             ['rsync', '-r', '-p', '-t', '-E', (os.path.join(
#                 path_concat_remote, item)), (
#                     os.path.join(
#                         path_concat_backsafe, item))])
#     if os.path.isfile(os.path.join(path_concat_remote, item)) is True:
#         subprocess.run(
#             ['rsync', '-p', '-t', '-E', (os.path.join(
#                 path_concat_remote, item)), (
#                     os.path.join(
#                         path_concat_backsafe, item))])


# Create tar.bz2 archive of local file
def create_tar_func():
    tar = tarfile.open(os.path.join(birdy_work, (item + '.tar.bz2')), 'w:bz2')
    tar.add(os.path.join(user_home, local_path, item), arcname=item)
    tar.close()


## Encrypt gpg file from tar.bz2 archive
def enc_gpg_func():
    subprocess.run(
        ['gpg', '--yes', '-o', (
            os.path.join(birdy_work, (
                item + '.tar.bz2.gpg'))), '-r', pgp_recip, '--encrypt', (
                    os.path.join(birdy_work, (item + '.tar.bz2')))])


# Move archive to remote directory
def replace_remote_gpg_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '--progress', (
            os.path.join(birdy_work, (item + '.tar.bz2.gpg'))), (
                os.path.join(path_concat_remote, (item + '.tar.bz2.gpg')))])


# Replace remote dir contents from local
def replace_remote_dir_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '--progress', (
            os.path.join(user_home, local_path, item, '')), (
                os.path.join(path_concat_remote, item, ''))])


# Replace remote file contents from local
def replace_remote_file_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '--progress', (
            os.path.join(user_home, local_path, item)), (
                os.path.join(path_concat_remote, item))])


# RESTORE FUNCTIONS ----------------------------------------------------------|
# Copy the LOCAL target files to the local_safety folder in /tmp
def make_local_safe_func():
    path_concat_local = os.path.join(
        user_home, local_path)
    subprocess.run(
        ['mkdir', '-p', path_concat_local])
    path_concat_localsafe = os.path.join(
        local_safe, local_path)
    subprocess.run(
        ['mkdir', '-p', path_concat_localsafe])
    if os.path.isdir(os.path.join(path_concat_local, item)) is True:
        subprocess.run(
            ['rsync', '-r', '-p', '-t', '-E', (os.path.join(
                path_concat_local, item)), (os.path.join(
                    path_concat_localsafe, item))])
    elif os.path.isfile(os.path.join(path_concat_local, item)) is True:
        subprocess.run(
            ['rsync', '-p', '-t', '-E', (
                path_concat_local + item), (os.path.join(
                    path_concat_localsafe, item))])


# Decrypt gpg and extract tar.bz2 file
def dec_gpg_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['gpg', '--yes', '-o', (
            os.path.join(
                birdy_work, (item + '.tar.bz2'))), '--decrypt', (
                    os.path.join(
                        path_concat_remote, (item + '.tar.bz2.gpg')))])


# Extract user file from tar.bz2 archive
def extract_tar_func():
    tar = tarfile.open(os.path.join(birdy_work, (item + '.tar.bz2')), 'r:bz2')
    tar.extractall(path=(os.path.join(birdy_work)))
    tar.close()


# Replace local dir contents from ENCRYPTED backup
def replace_local_dir_enc_func():
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '-u', '--delete', '--progress', (
            os.path.join(birdy_work, item, '')), (
                os.path.join(user_home, local_path, item, ''))])


# Replace local file from ENCRYPTED backup
def replace_local_file_enc_func():
    subprocess.run(
        ['rsync', '-p', '-t', '-E', '--progress', (
            os.path.join(birdy_work, item)), (
                os.path.join(user_home, local_path))])


# Replace local dir contents from backup
def replace_local_dir_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '-u', '--delete', '--progress', (
            os.path.join(path_concat_remote, item, '')), (
                os.path.join(user_home, local_path, item, ''))])


# Replace local file from backup
def replace_local_file_func():
    path_concat_remote = os.path.join(
        remote_base, back_base, sysname, local_path, back_path)
    subprocess.run(
        ['rsync', '-r', '-p', '-t', '-E', '-u', '--progress', (
            os.path.join(path_concat_remote, item)), (
                os.path.join(user_home, local_path, item))])


# Let's get started
os.system('clear')
print("\nWelcome to "
      + str(soft_name)
      + " "
      + str(soft_vers)
      + " - "
      + str(soft_tag)
      + ".")

if sysname == '':
    print("\nCan't find system name...\n")
    sysname = input("Please enter a system name: ")
    if sysname == '':
        print("\nSystem needs a name...")
        exit(1)
    else:
        print("\nThank you, this"
              , O+ distro +W
              , "system will use system name"
              , O+ sysname +W
              , "\n")
else:
    print("\nThis distro is"
          , O+ distro +W
          , "and the system name is"
          , O+ sysname +W)

# Check for backup folder matching current system name
if os.path.exists(remote_sysname):
    print("\nFound matching backup directory:", remote_sysname)
else:
    print("\nNo backup directory called "
          + str(sysname)
          + ", create it? y/n")
    make_dir = input("")
    if make_dir == 'y' or make_dir == 'Y':
        print("\nCreated ", remote_sysname)
        try:
            os.mkdir(remote_backup)
        except(FileExistsError):
            pass
        os.mkdir(remote_sysname)
    else:
        print("It can't be blank")
        exit(1)

usr_inp = input("\nOptions:(q)uit the program or\
    \n\n\t(b)ackup birdy group\
    \n\t(i)ndividual files\
    \n\t(r)estore\
    \n\t(d)olly transfer\
    \n\t(y)ank from another backup\
    \n\n\tChoice: ")

if usr_inp in ["B", "b"]:
    print("")
    read_system_list_func()
    prune_system_list_4backup_func()
    make_group_lists_func()
    make_sorted_lists_func()
    make_sorted_lists_keys_func()
    print_basic_list_func()

    make_safety_dirs_func()

    backup_choice = input("\nBack up all birdy files? Y/n ")
    if backup_choice not in ["Y", "y"]:
        exit(0)
    else:
        print("")
        for row in system_list_basic:
            unused_key = row[0]
            item       = row[1]
            category   = row[2]
            dorf       = row[3]
            enc        = row[4]
            dolly      = row[5]
            fork       = row[6]
            local_base = row[7]
            local_path = row[8]
            back_base  = row[9]
            back_path  = row[10]
            
            make_remote_safe_func()

            if enc == "E":
                print("\nCompressing... ", item)
                create_tar_func()
                print("Encrypting...")
                enc_gpg_func()
                print("Copying...\n")
                replace_remote_gpg_func()
            elif enc != "E" and dorf == "D":
                print("\nCopying... ", item)
                replace_remote_dir_func()
            elif enc != "E" and dorf == "f":
                print("\nCopying... ", item)
                replace_remote_file_func()

elif usr_inp in ["I", "i"]:
    print("")
    read_system_list_func()
    prune_system_list_4backup_func()
    make_group_lists_func()
    make_sorted_lists_func()
    make_sorted_lists_keys_func()
    print_pruned_sorted_system_list_func()

    make_dicts_for_input_func()

    make_safety_dirs_func()

    x = 1
    while x == 1:
        backup_choice = input("\nPlease enter a number to BACK UP a file: ")
        if backup_choice in ["Q", "q"]:
            exit(0)
        elif backup_choice.isdigit() is False:
            print("-->", backup_choice, "is not an option")
        elif backup_choice.isdigit() is True:
            for key,value in syslist_dict.items():
                if key == int(backup_choice):
                    for row in system_list_pruned:
                        if value == row[1]:
                            unused_key = row[0]
                            item       = row[1]
                            category   = row[2]
                            dorf       = row[3]
                            enc        = row[4]
                            dolly      = row[5]
                            fork       = row[6]
                            local_base = row[7]
                            local_path = row[8]
                            back_base  = row[9]
                            back_path  = row[10]

                            make_remote_safe_func()

                            if row[5] == "L" or row[6] == "F":
                                sysname = ""

                            if enc == "E":
                                print("Compressing... ", item)
                                create_tar_func()
                                print("Encrypting...")
                                enc_gpg_func()
                                print("Copying...\n")
                                replace_remote_gpg_func()
                            elif enc != "E" and dorf == "D":
                                print("Copying... ", item)
                                replace_remote_dir_func()
                            elif enc != "E" and dorf == "f":
                                print("Copying... ", item)
                                replace_remote_file_func()
                            time.sleep(1.5)
                            os.system("clear")
                            print_pruned_sorted_system_list_func()

elif usr_inp in ["R", "r"]:
    print("")
    read_system_list_func()
    prune_system_list_4restore_func()
    make_group_lists_func()
    make_sorted_lists_func()
    make_sorted_lists_keys_func()
    print_pruned_sorted_system_list_func()

    make_dicts_for_input_func()
   
    make_safety_dirs_func()

    x = 1
    while x == 1:
        backup_choice = input("\nPlease enter a number to RESTORE a file: ")
        if backup_choice in ["Q", "q"]:
            exit(0)
        elif backup_choice.isdigit() is False:
            print("-->", backup_choice, "is not an option")
        elif backup_choice.isdigit() is True:
            for key,value in syslist_dict.items():
                if key == int(backup_choice):
                    for row in system_list_pruned:
                        if value == row[1]:
                            unused_key = row[0]
                            item       = row[1]
                            category   = row[2]
                            dorf       = row[3]
                            enc        = row[4]
                            dolly      = row[5]
                            fork       = row[6]
                            local_base = row[7]
                            local_path = row[8]
                            back_base  = row[9]
                            back_path  = row[10]

                            make_local_safe_func()

                            if enc == "E" and dorf == "D":
                                print("Decrypting... ", item)
                                dec_gpg_func()
                                print("Expanding...")
                                extract_tar_func()
                                print("Copying...\n")
                                replace_local_dir_enc_func()
                            if enc == "E" and dorf == "f":
                                print("Decrypting... ", item)
                                dec_gpg_func()
                                print("Expanding...")
                                extract_tar_func()
                                print("Copying... ", item)
                                replace_local_file_enc_func()
                            elif enc != "E" and dorf == "D":
                                print("Copying... ", item)
                                replace_local_dir_func()
                            elif enc != "E" and dorf == "f":
                                print("Copying... ", item)
                                replace_local_file_func()
                            time.sleep(1.5)
                            os.system("clear")
                            print_pruned_sorted_system_list_func()

elif usr_inp in ["D", "d"]:
    print("")
    dolly_choice = input("(s)end dolly files to remote or (r)eceive files to local? ")
    if dolly_choice in ["S", "s"]:
        print("")
        read_system_list_func()
        prune_system_list_4backup_func()
        make_group_lists_func()
        make_sorted_lists_func()
        make_sorted_lists_keys_func()
        print_dolly_list_func()

        make_dicts_for_input_func()

        make_safety_dirs_func()

        x = 1
        while x == 1:
            backup_choice = input("\nBackup these items? ")
            if backup_choice in ["Q", "q"]:
                exit(0)
            elif backup_choice in ["Y", "y"]:
                for row in system_list_pruned:
                    unused_key = row[0]
                    item       = row[1]
                    category   = row[2]
                    dorf       = row[3]
                    enc        = row[4]
                    dolly      = row[5]
                    fork       = row[6]
                    local_base = row[7]
                    local_path = row[8]
                    back_base  = row[9]
                    back_path  = row[10]

                    if row[2] in ["100"]:
                        remote_base = remote_dolly
                        sysname = ""
                        

                        # path_concat_remote = os.path.join(remote_dolly)
                        # print(path_concat_remote)


                        # make_remote_safe_func()
                        copy_remote_files_func()
    
                        # print("Compressing... ", item)
                        # create_tar_func()
                        # print("Encrypting...")
                        # enc_gpg_func()
                        # print("Copying...\n")
                        # # replace_remote_gpg_func()
                        # exit(0)
#     elif dolly_choice in ["R", "r"]:
#         read_system_list_func()
#         prune_remote_list_func()
#         make_sorted_lists_func()
#         make_sorted_lists_keys_func()
#         make_dicts_for_input_func()
#         make_safety_dirs_func()

#         x = 1
#         while x == 1:
#             backup_choice = input("\nRestore these files? ")
#             print_dolly_list_func()
#             if backup_choice in ["Q", "q"]:
#                 exit(0)
#             elif backup_choice in ["Y", "y"]:
#                 for row in restore_list_pruned:
#                     if row == 100:
#                         unused_key = row[0]
#                         item       = row[1]
#                         category   = row[2]
#                         dorf       = row[3]
#                         enc        = row[4]
#                         dolly      = row[5]
#                         fork       = row[6]
#                         local_base = row[7]
#                         local_path = row[8]
#                         back_base  = row[9]
#                         back_path  = row[10]

#                         back_base = remote_dolly

#                         make_local_safe_func()
    
#                         if dolly == "L":
#                             print("Decrypting... ", item)
#                             dec_gpg_func()
#                             print("Expanding...")
#                             extract_tar_func()
#                             print("Copying...\n")
#                             replace_local_dir_enc_func()
#                         exit(0)

# elif usr_inp in ["Y", "y"]:
#     w = 1
#     while w == 1:
#         print("\nHere are the systems birdy found:\n")
#         for item in os.scandir(os.path.join(remote_base, "Linux_Backups")):
#             print(item.name)
#         print("")
#         yank_choice = input("\nPlease enter the system name to restore from: ")
#         if not os.path.isdir(os.path.join(remote_base, 'Linux_Backups', yank_choice.strip())):
#             print(yank_choice, " is not an option.")
#         else:
#             w = 2
#             remote_sysname = os.path.join(remote_base, 'Linux_Backups', yank_choice.strip())
#             read_system_list_func()
#             prune_system_list_4restore_func()
#             make_group_lists_func()
#             make_sorted_lists_func()
#             make_sorted_lists_keys_func()
#             print_basic_list_func()
        
#             make_dicts_for_input_func()
        
#             make_safety_dirs_func()
        
#             x = 1
#             while x == 1:
#                 backup_choice = input("\nPlease enter a number to RESTORE a file: ")
#                 if backup_choice in ["Q", "q"]:
#                     exit(0)
#                 elif backup_choice.isdigit() is False:
#                     print("-->", backup_choice, "is not an option")
#                 elif backup_choice.isdigit() is True:
#                     for key,value in syslist_dict.items():
#                         if key == int(backup_choice):
#                             for row in restore_list_pruned:
#                                 if value == row[1]:
#                                     unused_key = row[0]
#                                     item       = row[1]
#                                     category   = row[2]
#                                     dorf       = row[3]
#                                     enc        = row[4]
#                                     dolly      = row[5]
#                                     fork       = row[6]
#                                     local_base = row[7]
#                                     local_path = row[8]
#                                     back_base  = row[9]
#                                     back_path  = row[10]
        
#                                     back_base = user_home
        
#                                     make_local_safe_func()
        
#                                     if enc == "E" and dorf == "D":
#                                         print("Decrypting... ", item)
#                                         dec_gpg_func()
#                                         print("Expanding...")
#                                         extract_tar_func()
#                                         print("Copying...\n")
#                                         replace_local_dir_enc_func()
#                                     elif enc == "E" and dorf == "f":
#                                         print("Decrypting... ", item)
#                                         dec_gpg_func()
#                                         print("Expanding...")
#                                         extract_tar_func()
#                                         print("Copying... ", item)
#                                         replace_local_file_enc_func()
#                                     elif enc != "E" and dorf == "D":
#                                         print("Copying... ", item)
#                                         replace_local_dir_func()
#                                     elif enc != "E" and dorf == "f":
#                                         print("Copying... ", item)
#                                         replace_local_file_func()
#                                     unique_back_name_func()
#                                     time.sleep(1.5)
#                                     os.system("clear")
#                                     print_pruned_sorted_system_list_func()

