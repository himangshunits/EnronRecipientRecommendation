##The script parses the text mails in the enron dataset folder structure and updates the mysql database with the body after initial cleaning
import os
#########f=open("C:\\Users\\sukriti\\Desktop\\sukriti\\data mining\\project\\enron_mail_20150507\\maildir\\badeer-r\\press_releases\\6_","r")
body=""
MAIL_DIR_PATH = "C:\\Users\\sukriti\\Desktop\\sukriti\\data mining\\project\\enron_rerun";
###########MAIL_DIR_PATH = "C:\\Users\\sukriti\\Desktop\\sukriti\\data mining\\project\\test";
#############3MAIL_DIR_PATH="C:\\Users\\sukriti\\Desktop\\sukriti\\data mining\\project\\test\\mail";

if not os.path.isdir(MAIL_DIR_PATH):
    raise Exception("Invalid or not found path for Enron Input: %s" % MAIL_DIR_PATH)


import mysql.connector
cnx = mysql.connector.connect(user='root', database='enron',password='root',host='localhost')
cursor = cnx.cursor();

################my_dir="C:\\Users\\sukriti\\Desktop\\sukriti\\test"
fp=open("exceptions.txt","w")
fl=open("log.txt","w")
for root, dirs, files in os.walk(MAIL_DIR_PATH):
    for file in files:
            body=""
            flag=0;select_flag=0;m_found=0;f_found=0;
            file_path=os.path.join(root, file)
            print file_path
            fl.write(file_path)
            f=open(file_path,"r");
            for line in f:
                if "Message-ID:" in line and m_found==0:
                    parts=line.split(" ")
                    message=parts[1].strip("\n")
                    m_found=1;
                if m_found==1 and f_found==0:
                    if "X-Folder:" in line:
                        parts=line.split("X-Folder: ")
                        folder_name=parts[1].replace("\\","")
                        f_found=1
                if flag==1: 	   
                    body=body+" "+line.strip("\n")
                if "X-FileName:" in line:
                     if m_found==1 and f_found==1:
                         #print line
                         flag=1
                     else:
                          fp.write(file_path)
                          fp.write("could not find headers")
                          fp.write("\n")
                          break

            if m_found==1 and f_found==1 and flag==1:
                ##print "\n data is\n" ,message,folder_name;
                ######test="testing4";
                body=body.replace("=20"," ")
                body=body.replace("= ","")
                body=body.replace("\"","")
                body=body.replace("\'","")
                try:				
                     cursor.execute("UPDATE cleaned_message_enron_test2 set body=\"%s\" where message_id=\'%s\'"%(body,message));
                     print cursor.statement;
                     fl.write(cursor.statement)
                except mysql.connector.Error as e:
                      fp.write(file_path)
                      fp.write(e.msg)
                      fp.write("\n")
                      fl.write(e.msg)
                #####cursor.execute("select body from cleaned_message where message_id=\'%s\'"%message);
                #####for body in cursor:
                #####         print body;
                cnx.commit();
fp.close();
#print body
cursor.close();
cnx.close();
