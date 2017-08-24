import cx_Oracle

class WhatToFeedback:
    
    def getFeedback(self, inputmsg):
    
        retval = ""
        #connect to DB
        con = cx_Oracle.connect('BILL_VIEWER/biLLvi3w@10.41.23.141/HBRMPRD')
        curr = con.cursor()
        
        if inputmsg.startswith("nova bainfo "):
            banum = inputmsg[12:]
            retval = self.getBAInfoNOVA(curr, banum)
        
        
        curr.close()
        con.close()

        
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
        
