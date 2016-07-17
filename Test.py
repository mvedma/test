# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:52:09 2016

@author: mvedma
"""
import time  
import socket
import smtplib
import datetime 
fo=open("log.txt","a")
def function_sendemail():    
    fo=open("log.txt","w+")
    sender = "mreddyvedma@getwellnetwork.com"
    receiver = "mreddyvedma@getwellnetwor.com"
    message= "Movie is over or has VOD desktop has crashed"
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender,receiver,message)
        fo.write("Email send")
    except smtplib.SMTPException:
        fo.write("Error: unable to send email")
    fo.close() 
    
def function_timestamp():  
    #Generating the time stamp
    ts = time.time()
    
    #String formatting the time stamp.
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

    #Write time stamp to file.
    fo.write(st); fo.write("\n") 
   

def function_getlength():
    
    #Create TCP/IP socet:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Ouput to log file
  #  fo = open("log.txt","a")

    #Connect to socket to whihc the PLC is listening.
    server_address = ('127.0.0.1',31337)
    
    #connecting to local host on loopback address
    s.connect(server_address)

    #Sending "get_length" command to the PLC
    send_getlength ="get_length \n"
    s.sendall(send_getlength)
    time.sleep(2)
    
    #Receiving data from the PLC
    received_getlength = s.recv(2048)
        
    return received_getlength[-5:]

def function_gettime():       
        #Create TCP/IP socket.
        s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        
        #Ouput to log file
        fo = open("log.txt","a")

        #Printing Output to log file
        fo.write("Socket has been created \n")

        #Connect to socket, to which the PLC is listening.
        server_address = ('127.0.0.1',31337)

        #Printint Output to log file
        fo.write("Itiating connection \n" )

        #Connecting the Localhost on a loopback address
        s.connect(server_address)

        #Sending "Get_time" command to the  PLC
        send_gettime =  " get_time\n "
        s.sendall(send_gettime)
        time.sleep(2)

        #Receving data from the PLC    
        received_gettime = s.recv(2048)

        
    
        return received_gettime[-5:]

def function_moviestatuscheck(get_length,get_time):
    if "-1" not in get_length:
        if "-1" in get_time:
            fo.write("The movie has ended playing")
    else:
        fo.write("Playback has not started \n")    
       


 
count =1
while(True):
   function_timestamp() 
   if(count<2):
       received_getlength= function_getlength()             
       fo.write("The total run time of the movie"); fo.write("\t \t");fo.write(received_getlength[-7:])
       count += 1
   received_gettime = function_gettime()
   #Writing received data to log.txt
   fo.write("The elapsed movie time is") ; fo.write("\t \t"); fo.write(received_gettime[-5:])
   function_moviestatuscheck(received_getlength,received_gettime)    
   fo.write("===========================\n ")
   
   if "-1" in received_gettime:
       break
fo.close()


