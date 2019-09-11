# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Dynamic_Email():
    
    
    def __init__ (self,Template,sqlconnection,script):
        
        self.email_file=Template
        
        self.sqlconnection=sqlconnection
        
        self.script = script
        
        self.file = Template
        
        self.email_template = []
        
        self.Contact_list = {}
        
        self.Names = []
        
        self.sqltable = []
        
        
    def connection (self):
        
        # this function connects to sql, and creates a table called sqltable
        
        import pandas.io.sql
        import pyodbc
        con = pyodbc.connect(self.sqlconnection)
        sql = self.script
        self.sqltable = pandas.io.sql.read_sql(sql,con)
        
        
    def get_contacts (self):
        
        #this function is for stripping out email and name information from the data
        #all this is stored in a dictionary called Contact list
        
        for name, email in zip(self.sqltable.FirstName,self.sqltable.Email):
    
            self.Contact_list[name]= email
        
        
    
        
    def Email_temp(self):
        
         # this function is where we read the HTML email template, modify, and attach documents 
         # to the email body
         
        self.email_template = open(self.file).read()
        
        
        
    def send_email(self):
        
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        
        
  
        
        for name, email in self.Contact_list.items():
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = self.email_template.format(name)

            # setup the parameters of the message
            msg['From']= 'Muchigi.kimari@mckesson.com'
            msg['To']=email
            msg['Subject']="This is TEST"

            # add in the message body
            msg.attach(MIMEText(message, 'html'))
           # msg.attach(MIMEText(message, 'plain'))
            
            # set up the SMTP server
            s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
            s.starttls()
            s.login('Muchigi.kimari@mckesson.com', 'Rading37')

            # send the message via the server set up earlier.
            s.send_message(msg)
        
        
if __name__ == "__main__":
    
    connections = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:zterraformation.database.windows.net;DATABASE=CloudAnalytics;UID=CloudAnalytics;PWD=!@#$ILCADY1317'

    Script = """SELECT DISTINCT  FirstName, 
                Dim_EmployeeData.EID, 
                SubscriptionID, 
                CASE WHEN Dim_EmployeeData.EID = 'e7vsisr' THEN 'jay.moors@mckesson.com'
                ELSE 'muchigi.kimari@mckesson.com' END AS Email
                FROM Fact_RoleAssignments_RG
                INNER JOIN Dim_EmployeeData
                ON Fact_RoleAssignments_RG.EID = Dim_EmployeeData.EID"""

    temp = 'C:\Cloud Analytics\Email_template.txt'
    
    Y = Dynamic_Email (Template = temp, sqlconnection = connections,script = Script)
    
    Y.connection()

    Y.get_contacts()
    
    Y.Email_temp()
    
    #Y.send_email()
