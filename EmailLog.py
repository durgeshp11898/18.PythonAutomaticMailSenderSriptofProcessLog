import os
from sys import *
import psutil
import time
import smtplib
import urllib3.request
import urllib.request as ur
import schedule
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
       # urllib3.request.urlopen('http://216.58.192.142',timeout=1)
       s = ur.urlopen("http://www.google.com",timeout=1)
       print(s)
       return True
    except ur.URLError as err:
        print("Internet is Not Connected")
        return False

def MailSender(filename,time):
    try:
        fromaddr = 'dullu.milu@gmail.com'
        toaddr = 'durgeshpawar077@gmail.com'

        msg=MIMEMultipart()

        msg['From']=fromaddr

        msg['To']=toaddr

        body=""" Hello %s,
        Welcome to our Auto-Genarated Mail System.
        Plese find attached document which contais Log of Running Process.
        Log file is Created at: %s.

        This is Auto-Genarated Mail,

        Thanks & Regards,
        Durgesh K. Pawar.
        """%(toaddr,time)
        
        Subject="""
         Durgesh Pawar Process Log Genarated at: %s"""%(time)

        msg['Subject']=Subject

        msg.attach(MIMEText(body,'plain'))

        attachment=open(filename,"rb")

        p=MIMEBase('application','octet-stram')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)
        
        p.add_header('content-Diposition',"attachment; filename=%s"%filename)

        msg.attach(p)

        s=smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,"Ashu@1999")

        text=msg.as_string()
        
        s.sendmail(fromaddr,toaddr,text)
        
        s.quit()

        print("Log File Succesfully Sent through Mail")

    except Exception as E:
        print("Unble to send Mail.",E)

def ProcessLog(log_dir= 'DIR'): 
    listprocess=[]

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator="-"*80
    log_path=os.path.join(log_dir,"DurgeshLog%s.log"%(time.ctime()))
    f=open(log_path,'w')
    f.write(separator+"\n")
    f.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo=proc.as_dict(attrs=['pid','name','username'])
            vms=proc.memory_info().vms/(1024*1024)
            pinfo['vms']=vms
            listprocess.append(pinfo)
        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    for element in listprocess:
        f.write("%s\n"%element)

    print("Log File is SucessFully Genarated at Location %s"%(log_path))

    connected=is_connected()

    if connected:
        startTime=time.time()
        MailSender(log_path,time.ctime())
        endTime=time.time()
        
        print('Took %s seconds to send Mail'%(endTime-startTime))

    else:
        print("There is No Internet Connecetion")
    


def main():

    print(".....EMAIL PROCESS LOG SENDER.....")
    
    print("Application Name: "+argv[0])
   
    connected=is_connected()
    print("Connection is on",connected)

    try:
        schedule.every(int(argv[1])).minutes.do(ProcessLog)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except ValueError:
        print("Error Invlaid Datatype of Input")

    except Exception as E:
        print("Error : Invalid Input",E)


if __name__=="__main__":
    main()
