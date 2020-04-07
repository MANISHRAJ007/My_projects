#!/usr/bin/python

from os import system
from os import path
from subprocess import PIPE,Popen
from datetime import date,time,datetime,timedelta


def date_check(date_):
    if(date_[2]!='/' or date_[5]!='/'):
        print('Enter the date in mm/dd/yyy format')
        exit()

    mm, dd, yy = date_.split('/')
    dd = int(dd)
    mm = int(mm)
    yy = int(yy)
    if (mm == 1 or mm == 3 or mm == 5 or mm == 7 or mm == 8 or mm == 10 or mm == 12):
        max1 = 31
    elif (mm == 4 or mm == 6 or mm == 9 or mm == 11):
        max1 = 30

    elif (yy % 4 == 0 and yy % 100 != 0 or yy % 400 == 0):
        max1 = 29
    else:
        max1 = 28
    if (mm < 1 or mm > 12):
        print("Date is invalid.")
        exit()
    elif (dd < 1 or dd > max1):
        print("Date is invalid.")
        exit()


def date_order_check(sd,ed):
    if (sd[6:10]>sd[6:10]):
        print('1')
        print('Start Date should be less than End Date')
    elif(sd[6:10]<ed[6:10]):
        return

    elif (sd[6:10]==ed[6:10]):
        if (sd[0:2]>ed[0:2]):
           print('2')
           print('Start Date should be less than End Date')
           exit(0)
        elif(sd[0:2]==ed[0:2]): 
            if(sd[3:5]>=ed[3:5]):
                print('3')
                print('Start Date should be less than End Date')
                exit(0)


def node_decider(*argf):
    if (len(shell_cmd('echo $TWO_TASK'))-1):
        mt_backup(argf[0],argf[1])
    elif(len(shell_cmd('echo $ORACLE_SID'))-1):
        db_backup(f)
    else:
        print('Source the environment and try again!')


def mt_backup(sdate,edate):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\t\t\tMT Backups\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    t_date={'sdate':sdate,'edate':edate}
    print(shell_cmd(['/usr/openv/netbackup/bin/bpclimagelist -U  -s {d[sdate]} -e {d[edate]}'.format(d=t_date)]))


def db_backup(f):
    print('db_backup')


def shell_cmd(cmd):
    t1=Popen(cmd,shell=True,stdin=None,stdout=PIPE,stderr=PIPE)
    out,err=t1.communicate()
    return out
    
def format_1(n):
    today=datetime.now()
    n_date=timedelta(days=n)
    sdate=(today-n_date).strftime("%m/%d/%Y")
    edate=today.strftime("%m/%d/%Y")
    node_decider(sdate,edate)

def format_2():
    s_date=raw_input('Enter the Start Date(mm/dd/yyyy):')
    date_check(s_date)
    e_date=raw_input('Enter the End Date(mm/dd/yyyy):')
    date_check(e_date)
    #Checking date order
    date_order_check(s_date,e_date)
    node_decider(s_date,e_date)

def format_decider(choice):
    if (choice==1):
        n=input('Enter the value of N:')
        format_1(n)
    elif(choice==2):
        format_2()
    else:
        print('Enter Valid Option')
        exit(0)
    
def main():    
    choice=input("1.Display last 'N' Backups\n2.Display Backup between some date\n")
    #Checking Netbackup Directory Check
    if (path.exists('/usr/openv/netbackup/')):
        print('!!!!NetBackup Installed!!!!')
    else:
        print('NetBackup is not installed')
        exit()
 
    format_decider(choice)


if __name__=='__main__':
    main()
