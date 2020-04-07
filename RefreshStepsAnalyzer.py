#
#Author: dasari.pranaya.manish.raj@oracle.com
#
#!/usr/bin/python
import re
from os import system,path,chdir
from subprocess import Popen,PIPE
from datetime import datetime,date,timedelta

global_list=[]

def shell_cmd(cmd):
    t1=Popen(cmd,shell=True,stdin=None,stdout=PIPE,stderr=PIPE)
    out,err=t1.communicate()
    return out
     
def date_to_str(par1,par2):
    ##par1##
    if (len(par1)==19):
        r1=datetime.strptime(par1,'%Y-%m-%d %H:%M:%S')
    else:
        s=list(par1)
        s[5]='-20'
        r1=datetime.strptime("".join(s),'%m-%d-%Y %H:%M:%S')
    ##par2##
    if (len(par2)==14):
	r2=datetime.strptime(par2,'%Y%m%d%H%M%S')
    elif (len(par2)==19):
        r2=datetime.strptime(par2,'%Y-%m-%d %H:%M:%S')
    else:
        s1=list(par2)
        s1[5]='-20'
        r2=datetime.strptime("".join(s1),'%m-%d-%Y %H:%M:%S')
    return r1,r2
def summaray_RE(pattern_,line1):
    obj1 = re.compile(pattern_)
    try:
        return obj1.search(line1).group()
    except:
        return 'None_' 

def summary_printing_funct(all_file_list):
    summary_output_dict={}
    for l in range(len(all_file_list)):
        fh=open((all_file_list[l]).strip(),'r')
        while(True):
            line1=fh.readline()
            if line1== '':
                break
            if (summaray_RE('Starting evali_fun \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line1) == 'None_'):
                continue
            else:
                result = summaray_RE('Starting \w{5}_\w{3} \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line1)
                if (result != 'None_'):
                    summary_output_dict.setdefault(result[9:18], []).append(result[19:len(result)])
                    while (True):
                        line2 = fh.readline()
                        result2 = summaray_RE('completion of ' + result[9:18] + ' \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line2)
                        ktmp=summaray_RE('ERROR! exit code 1  in step '+ result[9:18] + ' \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line2)
                        if ktmp!= 'None_':
                            summary_output_dict.setdefault(result[9:18], []).append(ktmp[38:len(ktmp)])
                            break
                        if (result2 != 'None_'):
                            summary_output_dict.setdefault(result2[14:23], []).append(result2[24:len(result2)])
                            break
                        elif (line2 == ''):
                            del summary_output_dict[result[9:18]]
                            break

                while (True):
                    line1 = fh.readline()
                    if line1 == '':
                        break
                    else:
                        result = summaray_RE('Starting \w{5}_\w{3} \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line1)
                        if (result != 'None_'):
                            summary_output_dict.setdefault(result[9:18], []).append(result[19:len(result)])
                            while (True):
                                line2 = fh.readline()
                                result2 = summaray_RE('completion of ' + result[9:18] + ' \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',line2)
                                ktmp = summaray_RE('ERROR! exit code 1  in step ' + result[9:18] + ' \d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',line2)
                                if ktmp != 'None_':
                                    summary_output_dict.setdefault(result[9:18], []).append(ktmp[38:len(ktmp)])
                                    break
                                if (result2 != 'None_'):
                                    summary_output_dict.setdefault(result2[14:23], []).append(result2[24:len(result2)])
                                    break
                                elif (line2 == ''):
                                    del summary_output_dict[result[9:18]]
                                    break

    #print(summary_output_dict)
    print('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++ Automation Time Details ++++++++++++++++++')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    return_final_dict={}
    for i in range(len(global_list)):
        if(global_list[i] in summary_output_dict.keys()):
            k=global_list[i]
            v=summary_output_dict[global_list[i]]
            Len=len(v)
            if Len==2:
                p1,p2=date_to_str(v[0],v[1])
                tt=p2-p1 
                #tt=datetime.strptime(v[1],'%Y-%m-%d %H:%M:%S')-datetime.strptime(v[0],'%Y-%m-%d %H:%M:%S')
                return_final_dict[k]=tt
                print('Function {0} took {1} to complete'.format(k,tt))
            else:
                if (Len%2==0):
        	    sum_ = timedelta(days=0)
                    for i in range(0,Len,2):
                    
                        p1,p2=date_to_str(v[i],v[i+1])
                        sum_=sum_+(p2-p1)
                    return_final_dict[k]=sum_
                    print('Function {0} took {1} to complete'.format(k, sum_))

                else:
                    print(v)
                    print('Time is not gathered properly for {0} check with dasari.pranaya.manish.raj'.format(k))
    return return_final_dict


def logic_part(file_name_dict):
    #print('In logic')
    var = 0
    tmp_dict = {}
    list_ = []
    sorted_files_list = sorted(file_name_dict)
    for var in range(len(sorted_files_list)):
        k=len(file_name_dict[sorted_files_list[var]])
        if var == (len(sorted_files_list) - 1): break
        if ((file_name_dict[sorted_files_list[var]])[0][0:9] == (file_name_dict[sorted_files_list[var + 1]])[0][0:9]):
            tmp_dict.setdefault((file_name_dict[sorted_files_list[var]])[0][0:9], []).append((file_name_dict[sorted_files_list[var]]))
        else:
            tmp_dict.setdefault((file_name_dict[sorted_files_list[var]])[0][0:9], []).append((file_name_dict[sorted_files_list[var]]))
            tmp_dict.setdefault((file_name_dict[sorted_files_list[var]])[0][0:9], []).append(sorted_files_list[var + 1][-18:-4])
            
    final_dict={}
    #print('Printing tmp_dct',tmp_dict)
    #Making of all_file_list for printing of time elasped for each function
    retrn_sum_prt=summary_printing_funct(sorted_files_list)
    tmp_dict_keys_list=list(tmp_dict.keys())
    for i in range(len(tmp_dict_keys_list)):
	no_of_tries = len(tmp_dict[tmp_dict_keys_list[i]]) - 1
        if no_of_tries != 1:
     	    p1=tmp_dict[tmp_dict_keys_list[i]][0][1]
	    p2=tmp_dict[tmp_dict_keys_list[i]][-2][0]
	    s_date,e_date=date_to_str(p1[10:len(p1)],p2[10:len(p2)])
	else:
	    if (len(tmp_dict[tmp_dict_keys_list[i]][0])==1):
	        p1=tmp_dict[tmp_dict_keys_list[i]][0]
		p2=tmp_dict[tmp_dict_keys_list[i]][-1]
		s_date,e_date=date_to_str(p1[0][10:len(p1[0])],p2)
	    else:
		p1=tmp_dict[tmp_dict_keys_list[i]][0][1]
		p2=tmp_dict[tmp_dict_keys_list[i]][-1]
		s_date,e_date=date_to_str(p1[10:len(p1)],p2)
        d=e_date-s_date
        final_dict.setdefault(tmp_dict_keys_list[i],[]).append(d)
        final_dict.setdefault(tmp_dict_keys_list[i], []).append(no_of_tries)
    
    sum_=0
    print('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++ Troubleshooting Time Details +++++++++++++++')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        
    for k,v in final_dict.items():
        print('Function {0} took {1} with {2}  tries '.format(k,v[0],v[1]))
        sum_=v[0].seconds+sum_ 
     
    total_tb_time=timedelta(seconds=sum_)
    addit=timedelta(days=0)
    for t in retrn_sum_prt.values():
        addit=addit+t
    automation_run_time=addit
    total_time=automation_run_time+total_tb_time
    print('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++ Total Summary +++++++++++++++')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    print('Total troubleshooting time: {0}'.format(total_tb_time))
    print('Automation Run Time:        {0}'.format(automation_run_time))
    print('Total time to completed:    {0}'.format(total_time))

def tem_def(inp_str):
    #print('tetsting',inp_str)
    obj1=re.compile(r'\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    try:
        return obj1.search(inp_str).group()
    except:
        return 'None_'
def main():
    file_name={}
    dir_name=raw_input('Enter the directory name:')
    path.isdir(dir_name)
    chdir(dir_name)
    indx=dir_name.find('/clone_stage')
    fun_name=dir_name[0:indx+1]+'clone_tool/AutoC/clone/target/bin/'
    tmp1=shell_cmd('ls '+fun_name+'AUTOC_*TRG.sh')
    fh=open('buf1_file.txt','w+')
    if(len(tmp1)!=0):
        fh.seek(0)
        fh.write(shell_cmd('sh '+tmp1))
        fh.seek(0)
        while(True):
	    line=fh.readline()
            if (line==''):
                break
            else:
                tmp2=summaray_RE(r'\w\w\w\w\w_fun',line)
	        if(tmp2!='None_'):
                    global_list.append(tmp2)
        fh.close()
    print(shell_cmd('rm -f buf1_file.txt'))
    value__=[]
    tmp=shell_cmd('ls --time-style=+"%Y-%m-%d %H:%M:%S" autoc_*[0-9].log')
    file_list=tmp.split()
    #print(len(file_list))
    ''' Instead of noting failure with each fun take failure of first fun and then onwards take start of fucn'''
    for list_index in range(len(file_list)):
        fh=open(file_list[list_index])
        l1=fh.read()
        if (l1.find('fatal error')!=-1 or l1.find('ERROR')!=-1):
            indx=l1.rfind('_fun')
            last_indx=summaray_RE('\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1[indx:indx+25])
            while(True):
                if (last_indx !='None_'):
                    #print('In first loop',file_list[list_index])
 		    strt_time=summaray_RE('Starting ' +l1[indx - 5:indx + 5]+ '\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1)
   		    if (strt_time!='None_'):
			file_name.setdefault(file_list[list_index],[]).append(strt_time[9:len(strt_time)])		
		    file_name.setdefault(file_list[list_index],[]).append(l1[indx - 5:indx + 5] + last_indx)
		    break
                else:
                    indx=l1.rfind('_fun',0,indx-1)
		    last_indx=summaray_RE('\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1[indx:indx+25])
        else :
            indx=l1.rfind('_fun')
            if (l1[indx-5:indx] == 'endcl'):
		last_indx=summaray_RE('\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1[indx:indx+25])
                if (last_indx!='None_'):
		    #print('IN endcl',file_list[list_index])
                    strt_time=summaray_RE('Starting ' +l1[indx - 5:indx + 5]+ '\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1)
                    if (strt_time!='None_'):
			file_name.setdefault(file_list[list_index],[]).append(strt_time[9:len(strt_time)])
		    file_name.setdefault(file_list[list_index],[]).append(l1[indx - 5:indx + 5] + last_indx)
                else:
                    print('New Test Case Found Contact dasari.pranaya.manish.raj@oracle.com')
                    exit()
            else :
                if (l1.find('_fun') == -1):
                    continue
		last_indx=summaray_RE('\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1[indx:indx+25])
                while(True):
                    if (last_indx !='None_'):
			#print('Infinity Loop',file_list[list_index])
			file_name.setdefault(file_list[list_index],[]).append(l1[indx - 5:indx + 5] + last_indx)
			file_name.setdefault(file_list[list_index],[]).append(l1[indx - 5:indx + 5] + last_indx)
                        break
                    else:
                        indx=l1.rfind('_fun',0,indx-1)
			last_indx=summaray_RE('\d\d(\d\d)?-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',l1[indx:indx+25])

        if (file_name[file_list[list_index]]=='None_'):
            file_name.pop(file_list[list_index],None)
    fh.close()
    logic_part(file_name)

if __name__=='__main__':
    main()
