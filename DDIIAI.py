from sys import argv
import os
import temp
from subprocess import PIPE,Popen


obj=temp.Application(argv[1])
#print('I am in ndecebsts1.py file')
#print('I am about to RUn SQL statement from ndecebsts1.py file')
print('*****Checking the Workflow Admin Role*****')
def fileopen_cmds(file_name):
    session=Popen(['sh',file_name],stdin=PIPE,stdout=PIPE,stderr=PIPE)
    print(session.stdout.read())



obj.RunStatement("@mysqlfile.sql")



#step-13
print('Step-13   Running ScriptToRemoveSmtpSettingsFromBurstingFiles.sql file\n')
obj.RunStatement('@ScriptToRemoveSmtpSettingsFromBurstingFiles.sql')

#step-15
print('Step-15  Setting Workflow Admin Role\n')
fileopen_cmds('step15.sh')
obj.RunStatement('select text from wf_resources where name=\'WF_ADMIN_ROLE\';')



#fileopen_cmds('step20.sh')
#obj.RunStatement('select value from XDO_CONFIG_VALUES  where PROPERTY_CODE=\'SYSTEM_TEMP_DIR\';')
#obj.RunStatement('update apps.XDO_CONFIG_VALUES set value=/'/u01/install/APPS/$fs/inst/apps/${trg_cn}/appltmp/' where PROPERTY_CODE='SYSTEM_TEMP_DIR';')
#fh2.write(stout_obj)
#fh2.close()

#step-26
print("Step-26:  Checking Enable RRA: Enabled 'Report Review Agent'")
print('Running RRA.sql file')
obj.RunStatement('@RRA.sql')


#step-36
print('\n\n Step-36   Checking s_tools_twotask\n')
fileopen_cmds('step36.sh')



#obj.RunStatement('spool tsdt1.txt \n select sysdate from dual;select name from v$database; spool off;')

#Step-15)Workflow Admin Role



