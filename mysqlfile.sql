set serveroutput on size 1000000

DECLARE
statr BOOLEAN;
val BOOLEAN;
value Boolean;
temp Boolean;
step_2_email_au number;
step_2_email_bu number;
step3_comp_status varchar(50);
step17_PARAMETER_NAME varchar(50);
step17_PARAMETER_VALUE varchar(50);
step_6_cnt number;
pname varchar(34);
ptype varchar(34);


CURSOR c_step_17_WFM IS
    select a.PARAMETER_NAME,b.PARAMETER_VALUE 
    from fnd_svc_comp_param_vals_v a,FND_SVC_COMP_PARAM_VALS b 
    where a.PARAMETER_ID=b.PARAMETER_ID and a.PARAMETER_NAME in ('TEST_ADDRESS','FROM','REPLYTO');

CURSOR c_step_4_DB_links IS
    SELECT OWNER,DB_LINK,HOST 
    FROM DBA_DB_LINKS;
step_4_OWNER DBA_DB_LINKS.OWNER%TYPE;
step_4_DB_LINK DBA_DB_LINKS.DB_LINK%TYPE;
step_4_HOST DBA_DB_LINKS.HOST%TYPE;
    

CURSOR c_step_7_WF IS
    select EXPIRATION_DATE, USER_END_DATE,ROLE_END_DATE, effective_end_Date 
    from applsys.WF_LOCAL_USER_ROLES 
    WHERE expiration_date = TO_DATE('01-JAN-1950','DD-MON-YYYY')AND user_name IN (SELECT user_name FROM fnd_user WHERE end_date IS NULL or end_date >= SYSDATE);
step_7_EXPIRATION_DATE 		applsys.WF_LOCAL_USER_ROLES.EXPIRATION_DATE%TYPE;
step_7_USER_END_DATE            applsys.WF_LOCAL_USER_ROLES.USER_END_DATE%TYPE;
step_7_ROLE_END_DATE	 	applsys.WF_LOCAL_USER_ROLES.ROLE_END_DATE%TYPE;
step_7_effective_end_Date       applsys.WF_LOCAL_USER_ROLES.effective_end_Date%TYPE;

CURSOR c_step_7_WF2 IS 
    select END_DATE,USER_END_DATE,ROLE_END_DATE,effective_end_Date 
    from applsys.WF_USER_ROLE_ASSIGNMENTS 
    WHERE END_DATE  = TO_DATE('01-JAN-1950','DD-MON-YYYY')AND user_name IN (SELECT user_name FROM fnd_user WHERE end_date IS NULL or end_date >= SYSDATE);

step_7b_END_DATE                 applsys.WF_USER_ROLE_ASSIGNMENTS.END_DATE%TYPE;
step_7b_USER_END_DATE            applsys.WF_USER_ROLE_ASSIGNMENTS.USER_END_DATE%TYPE;
step_7b_ROLE_END_DATE            applsys.WF_USER_ROLE_ASSIGNMENTS.ROLE_END_DATE%TYPE;
step_7b_effective_end_Date       applsys.WF_USER_ROLE_ASSIGNMENTS.effective_end_Date%TYPE;


FUNCTION smptp(stat IN BOOLEAN ) return Boolean is
BEGIN
IF stat THEN
    dbms_output.put_line( 'Profile FND: SMTP Host updated with null' );
	commit;
    return TRUE;
ELSE
	dbms_output.put_line( 'Profile FND: SMTP Host  could NOT be updated with null' );
    return FALSE;
    END IF;
return NULL;

END;



BEGIN
/******Step-1:update SMTP profile******/

dbms_output.put_line(chr(13) ||chr(10)||''||'Updating SMTP profile'|| chr(13) ||chr(10)||'---------------------------');


val := TRUE;
temp:=smptp(val);
IF temp THEN
    dbms_output.put_line('Step-1 Completed Successfully'|| chr(13) ||chr(10)||''||chr(13) ||chr(10)||'');
    DBMS_OUTPUT.NEW_LINE();
ELSE
   dbms_output.put_line('Step-1 Didnt complete as expected,need to be reviewed'|| chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
END IF;



/******Step-2 Update sent flag for email notifications******/
dbms_output.put_line('Updating sent flag for email notifications'|| chr(13) ||chr(10)||'---------------------------');

select count(1) INTO step_2_email_bu  from xxit_emails where sent = 'N';
dbms_output.put_line('Count of xxit_emails before update:'||step_2_email_bu);

update xxit_emails set SENT = 'Y' where sent = 'N';

select count(1) INTO step_2_email_au  from xxit_emails where sent = 'N';
dbms_output.put_line('Count of xxit_emails after update:'||step_2_email_au);
dbms_output.put_line('Step-2 Completed Successfully'|| chr(13) ||chr(10)||'--------------'|| chr(13) ||chr(10)||'--------------');



/*****Step-3)****/
dbms_output.put_line(chr(13) ||chr(10)||''||'Making Workflow Notification Mailer down as user deactivated status'||chr(13) ||chr(10)||''||'---------------------------------------------');

SELECT COMPONENT_STATUS into step3_comp_status FROM APPS.FND_SVC_COMPONENTS WHERE component_type = 'WF_MAILER';
IF (step3_comp_status='STOPPED_ERROR') OR (step3_comp_status='DEACTIVATED_USER') THEN
    dbms_output.put_line('Status of Workflow Mailer is:'||step3_comp_status);
    dbms_output.put_line('Step-3 is Completed Successfully'|| chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
ELSE
     dbms_output.put_line('Step-3 Didnt complete as expected,need to be reviewed'|| chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
END IF;



/***Step-4 :It taken care code is written at last ****/ 

/***Step-5 Has to be done at DB Node****/

/**Step-6 Put Schedule Jobs on Hold ***/


dbms_output.put_line('Keeping Schedule Jobs on Hold'|| chr(13)||chr(10)||''||'---------------------------------------------');
select count(*) into step_6_cnt from apps.fnd_concurrent_requests;
execute immediate 'create table fnd_conc_req_15092018 as select * from apps.fnd_concurrent_requests';
execute immediate 'create table apps.fnd_conc_req_15092018_b4hold as select * from apps.fnd_concurrent_requests where hold_flag='N' and phase_code='P'';

update apps.fnd_concurrent_requests set hold_flag='Y' where phase_code ='P' AND concurrent_program_id NOT IN (31556,31915,32320,32353,32584,32766,35740,39442,50035,31659,38121,32263,36201,44918);



/**Step-7 Update Workflow Table**/

dbms_output.put_line(chr(13)||chr(10)||''||chr(13)||chr(10)||''||'Updating Workflow Table'|| chr(13)||chr(10)||'');
dbms_output.put_line('Values in WF_LOCAL_USER_ROLES before update');
dbms_output.put_line('EXPIRATION_DATE	USER_END_DATE	ROLE_END_DATE	effective_end_Date');
OPEN c_step_7_WF;
LOOP
   FETCH c_step_7_WF into step_7_EXPIRATION_DATE,step_7_USER_END_DATE,step_7_ROLE_END_DATE,step_7_effective_end_Date; 
   EXIT WHEN c_step_7_WF%NOTFOUND;
   dbms_output.put_line(step_7_EXPIRATION_DATE||'====='||step_7_USER_END_DATE||'-----'||step_7_ROLE_END_DATE||'==='||step_7_effective_end_Date);

END LOOP;
ClOSE c_step_7_WF;

UPDATE applsys.WF_LOCAL_USER_ROLES SET EXPIRATION_DATE = NULL, USER_END_DATE = NULL, ROLE_END_DATE = NULL, effective_end_Date=to_date('01-01-9999','dd-mm-yyyy') WHERE expiration_date = TO_DATE('01-JAN-1950','DD-MON-YYYY')AND user_name IN (SELECT user_name FROM fnd_user WHERE end_date IS NULL or end_date >= SYSDATE);

dbms_output.put_line(chr(13)||chr(10)||''|| chr(13) ||chr(10)||''||'Values in WF_LOCAL_USER_ROLES after update'||chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
dbms_output.put_line('EXPIRATION_DATE   USER_END_DATE   ROLE_END_DATE   effective_end_Date');
OPEN c_step_7_WF;
LOOP
FETCH c_step_7_WF into step_7_EXPIRATION_DATE,step_7_USER_END_DATE,step_7_ROLE_END_DATE,step_7_effective_end_Date;
EXIT WHEN c_step_7_WF%NOTFOUND;
dbms_output.put_line(step_7_EXPIRATION_DATE||'====='||step_7_USER_END_DATE||'-----'||step_7_ROLE_END_DATE||'==='||step_7_effective_end_Date);
END LOOP;
ClOSE c_step_7_WF;


dbms_output.put_line(chr(13)||chr(10)||''|| chr(13) ||chr(10)||''||'Values in WF_USER_ROLE_ASSIGNMENTS before update'||chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
dbms_output.put_line(chr(13)||chr(10)||''|| chr(13) ||chr(10)||''||'END_DATE	USER_END_DATE	ROLE_END_DATE	effective_end_Date');
OPEN c_step_7_WF2;
LOOP
FETCH c_step_7_WF2 into step_7b_END_DATE,step_7b_USER_END_DATE,step_7b_ROLE_END_DATE,step_7b_effective_end_Date;
EXIT WHEN c_step_7_WF2%NOTFOUND;
dbms_output.put_line(step_7b_END_DATE||'====='||step_7b_USER_END_DATE||'-----'||step_7b_ROLE_END_DATE||'==='||step_7b_effective_end_Date);
END LOOP;
ClOSE c_step_7_WF2;


UPDATE applsys.WF_USER_ROLE_ASSIGNMENTS SET END_DATE = NULL, USER_END_DATE = NULL, ROLE_END_DATE = NULL, effective_end_Date=to_date('01-01-9999','dd-mm-yyyy') WHERE END_DATE  = TO_DATE('01-JAN-1950','DD-MON-YYYY')AND user_name IN (SELECT user_name FROM fnd_user WHERE end_date IS NULL or end_date >= SYSDATE);

dbms_output.put_line(chr(13)||chr(10)||''|| chr(13) ||chr(10)||''||'Values in WF_USER_ROLE_ASSIGNMENTS after update'||chr(13)||chr(10)||''|| chr(13) ||chr(10)||'');
dbms_output.put_line(chr(13)||chr(10)||''|| chr(13) ||chr(10)||''||'step_7b_END_DATE	step_7b_USER_END_DATE	step_7b_ROLE_END_DATE	step_7b_effective_end_Date');
OPEN c_step_7_WF2;
LOOP
FETCH c_step_7_WF2 into step_7b_END_DATE,step_7b_USER_END_DATE,step_7b_ROLE_END_DATE,step_7b_effective_end_Date;
EXIT WHEN c_step_7_WF2%NOTFOUND;
dbms_output.put_line(step_7b_END_DATE||'====='||step_7b_USER_END_DATE||'-----'||step_7b_ROLE_END_DATE||'==='||step_7b_effective_end_Date);
END LOOP;
ClOSE c_step_7_WF2;

dbms_output.put_line('Step-7 is completed');


/*Step-8 DB Link Creation*/

/******   Step-9 to 17 will bw ket at last


PROMPT Setting fnd_printer to NOPRINT
--update apps.fnd_printer set printer_type = 'NOPRINT' where printer_name not in ('noprint','XXIT_LANDWIDE240');
select printer_type,printer_name from apps.fnd_printer;

PROMPT Setting print_style to NOPRINT
--update apps.fnd_request_set_programs set print_style = 'NOPRINT' where printer like '%mco%';
--select print_style from apps.fnd_request_set_programs where printer like '%mco%';


PROMPT Setting mail_status to SENT 
--update apps.WF_NOTIFICATIONS set mail_status = 'SENT' where mail_status = 'MAIL';
--select mail_status from apps.WF_NOTIFICATIONS where mail_status = 'MAIL';


PROMPT Running ScriptToRemoveSmtpSettingsFromBurstingFiles.sql file
--@ScriptToRemoveSmtpSettingsFromBurstingFiles.sql
**/

/*Step-14:Reset the password for the FTP server so we don't connect to production

dbms_output.put_line('Step-14:Reset the password for the FTP server so we don't connecttion to_ production')
exec fnd_vault.put('XXIT','SFTP_PASSWORD','INVALID');
exec fnd_vault.put('XXIT','EDIHQ_PASSWORD','INVALID');*/



--step 17
PROMPT  select a.PARAMETER_NAME,b.PARAMETER_VALUE from fnd_svc_comp_param_vals_v a,FND_SVC_COMP_PARAM_VALS b where a.PARAMETER_ID=b.PARAMETER_ID and a.PARAMETER_NAME in ('TEST_ADDRESS','FROM','REPLYTO');
col PARAMETER_NAME for a15
col PARAMETER_VALUE for a50
select a.PARAMETER_NAME,b.PARAMETER_VALUE from fnd_svc_comp_param_vals_v a,FND_SVC_COMP_PARAM_VALS b where a.PARAMETER_ID=b.PARAMETER_ID and a.PARAMETER_NAME in ('TEST_ADDRESS','FROM','REPLYTO');






/*
Step-15:implemented in DIIAI.py

Step16:Update the following profile options to the following values {Need CHeck with Shaik}



Step-18 and Step 19)

Step-20 in DIIAI.py file need to check with shaik regardin =g logic

Step-21

Step-27 in DIIAI.py file


*/

dbms_output.put_line('PARAMETER_NAME	PARAMETER_VALUE');
dbms_output.put_line('---------------------------------------');
OPEN c_step_17_WFM;
LOOP 
    FETCH c_step_17_WFM into step17_PARAMETER_NAME,step17_PARAMETER_VALUE;
    EXIT when c_step_17_WFM%NOTFOUND;
    dbms_output.put_line(step17_PARAMETER_NAME||'---------'||step17_PARAMETER_VALUE);
    
END LOOP;
CLOSE c_step_17_WFM;

dbms_output.put_line( 'Selecting something');


END;
/

PROMPT Updating Profile Values to match the target env 
PROMPT -----------------------------------------------------
PROMPT 

PROMPT  select a.PARAMETER_NAME,b.PARAMETER_VALUE from fnd_svc_comp_param_vals_v a,FND_SVC_COMP_PARAM_VALS b where a.PARAMETER_ID=b.PARAMETER_ID and a.PARAMETER_NAME in ('TEST_ADDRESS','FROM','REPLYTO');
col PARAMETER_NAME for a15
col PARAMETER_VALUE for a50
select a.PARAMETER_NAME,b.PARAMETER_VALUE from fnd_svc_comp_param_vals_v a,FND_SVC_COMP_PARAM_VALS b where a.PARAMETER_ID=b.PARAMETER_ID and a.PARAMETER_NAME in ('TEST_ADDRESS','FROM','REPLYTO');


PROMPT ******** checking dba_links**************
PROMPT
set lines 200 pages 999
col OWNER for a10
col DB_LINK for a50
col HOST for a20
PROMPT SQL> SELECT OWNER,DB_LINK,HOST FROM DBA_DB_LINKS;
SELECT OWNER,DB_LINK,HOST FROM DBA_DB_LINKS;
PROMPT
PROMPT NOTE dba_links has been restored as before refresh
PROMPT
PROMPT ******************************************************
PROMPT
PROMPT ********checking dba_directories*********
PROMPT
SET lines 200
col DIRECTORY_NAME FORMAT a25
col DIRECTORY_PATH FORMAT a80
PROMPT SQL> SELECT DIRECTORY_NAME, DIRECTORY_PATH from all_directories;
SELECT DIRECTORY_NAME, DIRECTORY_PATH from all_directories;
PROMPT
PROMPT NOTE dba_directories has been restored as before refresh
PROMPT

