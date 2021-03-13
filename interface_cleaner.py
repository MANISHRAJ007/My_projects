#!/usr/bin/python
############################################################
# Author        : Manish Raj
# EMAIL         : dasari.pranaya.manish.raj@oracle.com
# Objective     : Space Cleanup in /sftp/i_mndc
# Usage example : interface_cleaner.py
############################################################


from subprocess import PIPE,Popen
from os import path
import datetime 

def Error_Check(err):
    temp_file=open('/home/oracle/DPMR/log/temp_file.txt','w+')
    temp_file.write('Got following problem please check and do the needful:\n------------------------------------------------------------------------\n')
    temp_file.write(err)
    shell_command_runner('mailx  -s "SFTP mount point cleanup || XXXXEBSPRD " d****j@oracle.com,opc***grp@oracle.com, < /home/oracle/DPMR/log/temp_file.txt')
    temp_file.close()
    exit(0)

def shell_command_runner(cmd):
    session=Popen([cmd],shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
    out,err=session.communicate()
    return(out,err)

def main():
    print('In Main')
    dir_list=['/sftp/i_mndc/****EBSPRD/archive','/sftp/i_mndc/****EBSPRD/tmp','/sftp/i_mndc/****EBSPRD/splashbi/output']
    for i in range(len(dir_list)):
        if(path.exists(dir_list[i])):
            pass
        else:
            print("One of following directory doesn't exist.Aborting cleanup!!\n {0}".format(dir_list))
            exit(0)

    
    for i in range(len(dir_list)):       
        out,err=shell_command_runner("find "+dir_list[i]+" -name '*' -type f -mtime +30 -exec ls -lrth {} \;")
        if len(err) != 0:
            Error_Check(err)
        filename = datetime.datetime.now()
        file_head=open('/home/oracle/DPMR/log/files_in_'+dir_list[i][24:].replace('/','_')+'folder_before_removal_'+filename.strftime("%Y%m%d-%H%M%S")+'.txt','w+')
        file_head.write(out)
        out,err=shell_command_runner("find "+dir_list[i]+" -name '*' -type f -mtime +30 -exec rm -rf {} \;")
        if len(err) != 0:
            Error_Check(err)

        print('SFTP mount point cleanup is successful.')
        file_head.close()

    
if __name__ == '__main__':
    main()
