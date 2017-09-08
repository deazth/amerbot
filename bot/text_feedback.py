import cx_Oracle
import paramiko

class WhatToFeedback:
    
    def getFeedback(self, inputmsg):
    
        retval = ""
        #connect to DB
        
        
        if inputmsg.startswith("nova bainfo "):
            con = cx_Oracle.connect('BILL_VIEWER/biLLvi3w@10.41.23.141/HBRMPRD')
            curr = con.cursor()
            banum = inputmsg[12:]
            retval = self.getBAInfoNOVA(curr, banum)
            curr.close()
            con.close()
            
        elif inputmsg == 'nova cmcount':
            retval = self.getCMCountNOVA()
        
        return retval
        
    
    def getBAInfoNOVA(self, cursor, banumber):
    
        print "searching for %s" % banumber
    
        retstr = "BA# not found: %s" % banumber
        
        cursor.execute("""select tan.last_name, nvl(tb.total_due, 0) lbilldue, tbi.pending_recv
            , decode(ta.status, 10100, 'Live', 10102, 'Suspend', 'Final') accstatus
            , decode(nvl(tb.end_t, 0), 0, 'no bill yet', to_char(pin.unix_ora_ts_conv(tb.end_t), 'dd/MM/yyyy')) bdate
            from pin.account_t ta, pin.account_nameinfo_t tan, pin.billinfo_t tbi
            , pin.bill_t tb where ta.account_no = :bano and ta.poid_id0 = tan.obj_id0
            and ta.poid_Id0 = tbi.account_obj_Id0
            and tbi.last_bill_obj_Id0 = tb.poid_Id0(+) """, {'bano' : str(banumber)})
        
        rowcount = 0
        
        for rlname, rlbdue, rprcv, raccstt, rbdate in cursor:
            rowcount = 1
            retstr = """BA# {0}
Name: {1}
Acc Status: {2}
Latest Bill Amt: {3} ({4})
Pending Revc: {5}""".format(banumber, rlname, raccstt, rlbdue, rbdate, rprcv)
            break
            
        return retstr
        
        
    def getCMCountNOVA(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect("10.41.24.22", username="pin", password="novapin123")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -ef | grep /app/brm/base/bin/cm | wc -l")
        node1count = ssh_stdout.read().split('\n', 1)[0]
        ssh.close()
        
        ssh.connect("10.41.24.23", username="pin", password="novapin123")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -ef | grep /app/brm/base/bin/cm | wc -l")
        node2count = ssh_stdout.read().split('\n', 1)[0]
        ssh.close()
        
        ssh.connect("10.41.24.194", username="pin", password="novapin123")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -ef | grep /app/brm/base/bin/cm | wc -l")
        node3count = ssh_stdout.read().split('\n', 1)[0]
        ssh.close()
        
        ssh.connect("10.41.24.250", username="pin", password="novapin123")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -ef | grep /app/brm/base/bin/cm | wc -l")
        node4count = ssh_stdout.read().split('\n', 1)[0]
        ssh.close()
        
        return "CM count\nnode1: "+node1count+"\n"+"node2: "+node2count+"\n"+"node3: "+node3count+"\n"+"node4: "+node4count
        
