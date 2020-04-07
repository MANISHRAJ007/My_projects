#!/usr/bin/python -tt
import os.path
from os import system,path
from getpass import getpass
from sys import argv
from subprocess import Popen,PIPE


class Application:
    def __init__(self,con_str):
        self.con_str=con_str
        
    def RunStatement(self,sqlstatement):
        self.sqlstatement=sqlstatement
        session=Popen(['sqlplus','-S',self.con_str], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print(sqlstatement)
        stdout,stderr=session.communicate(sqlstatement)
        print(stdout)
        print(stderr)
        return stdout

    def Instance_Decider(self,i_name):
        self.i_name=i_name
        #checking in v$database
        if i_name[-7:-2] == 'EBSDB' or i_name[-6:-2] == 'ORCL':
            print('Not a proper DB Name for my task')
        if (i_name[-8:-2]) in ['DDIIAI','DDIIAC','DDII3I','DDII3C','TDIIAI','TDIIAC','PDIIAC','PDIIAI']:
            file_name=i_name[-8:-2]+'.py'
            if path.exists(file_name):
                print('file '+file_name+' is availble')
            else:
                print('File '+file_name+' doesnt exist')
                exit(1)
            print('About to start a new process')
            session=Popen(['python',file_name,self.con_str],stdin=PIPE, stdout=PIPE, stderr=PIPE)
            print(session.stdout.read())
        else:
            print('I will be doing hostname check')  
            session=Popen(['hostname','-f'],stdin=PIPE,stdout=PIPE,stderr=PIPE)  
            i_name=session.stdout.read()[0:10]
            print(i_name)
            file_name=i_name+'.py'
            if path.exists(file_name):
                print('file '+file_name+' is availble')
            else:
                print('File '+file_name+' doesnt exist')
                exit(0)
            session=Popen(['python',file_name,self.con_str],stdin=PIPE, stdout=PIPE, stderr=PIPE)
            print(session.stdout.read())
            print(session.stderr.read())
def main():
    print('I am in main')
    app_pwd = getpass("Enter schema password:")
    con_str='apps/'+app_pwd
    appl=Application(con_str)
    db_name=appl.RunStatement('select name from v$database;')
    appl.Instance_Decider(db_name) 


if __name__=='__main__':
    main()


