from ftplib import FTP
import xml.etree.ElementTree as ET
import time
import os 

#----------------------------------GLOBALS------------------------------------------------------------------#
currentIP='10.35.73.20'
exfo_dir='/DATA/My Documents/CMAX2/'
local_bufferXML="Fiber50.xml"
#-----------------------------------------------------------------------------------------------------------#

"""--------------------------------FUNCTIONS----------------------------------------------------------------#
getResult(tmp) 
input= .xml file to overwrite, output = result of optical test as True (Pass) or False (Fail)

ftp_init(current_IP,exfo_dir) 
input= current ip of max-fip, directory where test result files are stored in max-fip
Initializes FTP connection to max-fip
output = ftp connection, list of test files in directory at time of connection

run(ftp,before)
input= ftp connection, list of test files in directory at time of connection
Checks current directory (after) with previous time iterations directory (before) for a new test result file
output=1
#---------------------------------------------------------------------------------------------------------"""

def getResult(tmp):
    tree = ET.parse(tmp)
    root=tree.getroot()
    return root[0][2][0][0].text

def ftp_init(currentIP,exfo_dir):
    try:
        ftp= FTP(currentIP)
        ftp.login()
        ftp.cwd(exfo_dir)
        before=[f for f in ftp.nlst() if '.xml' in f]
        return(ftp,before)
    except:
        print("FAIL")
        exit()

def run(ftp,before):
    while 1:
        after=[f for f in ftp.nlst() if '.xml' in f]
        added=[]
        diff=len(after)-len(before)
        if diff:
            while diff:
                added.append(after[len(before)-1+diff])
                diff=diff-1
        if added:
            for j in added:
                filename=j
                lf = open(local_bufferXML, "wb")
                ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
                lf.close()
                        
                result=getResult(local_bufferXML)
                if result == 'True':
                    print('PASSED')
                    return(1)
                elif result == 'False':
                    print('FAILED')
        before=after
        time.sleep(1)

def main():
    ftp,before=ftp_init(currentIP,exfo_dir)
    run(ftp,before)
    return(1)

if __name__ == "__main__":
    main()