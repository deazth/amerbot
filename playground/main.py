from text_feedback          import WhatToFeedback
import paramiko


if __name__==  "__main__":
    print "This is the main process"
    
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
    
    finalout = "CM count\nnode1: "+node1count+"\n"+"node2: "+node2count+"\n"+"node3: "+node3count+"\n"+"node4: "+node4count
    
    print(finalout)
    
    