#! /usr/bin/env python
# Runs email from the commandline.
# Still need to document and handle errors, but without errors it works!
# Could probably do some things more efficiently as well.

import smtplib, imapclient, pyzmail, pprint, datetime, imaplib

def errorCall(item):
    print 'An unexpected error occurred: '
    print item
    return

def sendEmail(myAddress, smtpObj):
    answer = 'y'
    whoTo = []
    while answer == 'y' or answer == 'Y':
        whoTo.append(raw_input('Who are you sending this message to?: '))
        answer = raw_input('Would you like to add another recipient? (y/n): ')
    subject = raw_input('What is the subject of your message?: ')
    paragraphs = []
    answer = 'y'
    while answer == 'y' or answer == 'Y':
        paragraphs.append(raw_input('Type a paragraph for the main body of your message: '))
        answer = raw_input('Would you like to add a paragraph? (y/n): ')
    message = 'Subject: ' + subject + '\n'
    sendQ = raw_input('Do you want to send your message? (y/n): ')
    if sendQ == 'N' or sendQ == 'n':
        print 'Message not sent'
        return
    for paragraph in paragraphs:
        message = message + paragraph + '\n  \n'
    success = smtpObj.sendmail(myAddress, whoTo, message)
    if not success:
        print 'Email was successfully sent'
    else:
        for key in success:
            print 'Email failed to be sent to ' + key
    return
    



def receiveEmail(myAddress, pswd, smtpObj, read = 'R'):
    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    while True:
        try:
            imapObj.login(myAddress, pswd)
            break
        except imaplib.error:
            print 'Password failed'
            password = raw_input('Re-enter Gmail PSWD: ')
    
    while True:
        print 'Here are the folders you can search through: '
        pprint.pprint(imapObj.list_folders())
        folder = raw_input('Which folder would you like to view?: ')
        try:
            junk = imapObj.select_folder(folder, readonly=False)
            
            break
        except imaplib.error:
            print 'Failed to find folder'
            answer = raw_input('Try another folder? (y/n): ')
            if answer == 'y' or answer == 'Y':
                print 'Remember to type the folder name exactly'
            else:
                return
    daysAgo = int(raw_input('From how many days ago do you want mail? (I.e.: 0,1,2,...): '))
    Date = (datetime.date.today() - datetime.timedelta(daysAgo)).ctime().split()
    unread = raw_input('Do you want only unread messages? (y/n): ')
    if unread == 'y' or unread == 'Y':
        UIDS = imapObj.search(['SINCE ' + Date[2] +'-'+ Date[1] +'-'+Date[-1], 'UNSEEN'])
    else:
        UIDS = imapObj.search(['SINCE ' + Date[2] +'-'+ Date[1] +'-'+Date[-1]])
    rawMessages = imapObj.fetch(UIDS, ['BODY[]'])
    messages = {} 
    for item in rawMessages:
        message = pyzmail.PyzMessage.factory(rawMessages[item]['BODY[]'])
        FROM = message.get_addresses('from')
        messages[item] = {'message':message,
                          'info': {'name': FROM[0][0],
                             'email':FROM[0][1],
                             'subject': message.get_subject(),
                             'to': message.get_addresses('to'),
                             'cc': message.get_addresses('cc'),
                             'bcc': message.get_addresses('bcc'),
                              }}
    printMessages(messages,Date)
    if read == 'R':
        readEmail(messages,Date)
    elif read == 'D':
        deleteEmail(imapObj)
    else:
        print 'Error, neither reading nor deleting'
    return imapObj

def printMessages(messages,Date):
    print 'You have received the following messages since '  + Date[2] +'-'+ Date[1] +'-'+Date[-1] 
    print ''
    for message in messages:
        print 'MessageID = ' + str(message)
        print '         Message Info: '
        print  messages[message]['info']
        print ''
        print ''
    return


def readEmail(messages,Date):
    while True:
        UID = int(raw_input('Enter a MessageID to read a message: '))
        message = messages[UID]['message']
        if message.text_part != None:
            print 'Text portion of the message'
            print ''
            print message.text_part.get_payload()
        if message.html_part != None:
            print 'HTML portion of the message'
            print ''
            print message.html_part.get_payload()
        answer = raw_input('Read another message? (y/n): ')
        if answer == 'n' or answer == 'N':
            break
        else:
            printMessages(messages,Date)
    return


def deleteEmail(imapObj):
    toDelete = []
    while True:
        UID = int(raw_input('Enter a MessageID to delete a message: '))
        toDelete.append(UID)
        answer = raw_input('Delete another message? (y/n): ')
        if answer == 'n' or answer == 'N':
            break
    deleted = imapObj.delete_messages(toDelete)
    expunge = imapObj.expunge()
    return
    
    
    
            
            
def quitEmail(myEmailAddress, smtpObj):
    QUIT = smtpObj.quit()
    if QUIT[0] == 221:
        print 'Quit email successfully'
        return
    else:
        errorCall(QUIT)
        return

imaplib._MAXLINE = 10000000 # Sets the the default byte size limit to 1 million
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
helloCall = smtpObj.ehlo()
if helloCall[0] == 250:
    print 'Email has been successfully called'
else:
    errorCall(helloCall)
startTls = smtpObj.starttls()
if startTls[0] == 220:
    print 'Email has been successfully started'
else:
    errorCall(startTls)
myEmailAddress = 'pinkardmichael@gmail.com'
password = raw_input('Gmail PSWD: ')
success = 0
while success != 235:
    try:
        Login = smtpObj.login(myEmailAddress,password)
        success = Login[0]
    except smtplib.SMTPAuthenticationError:
        print 'Password Failed'
        password = raw_input('Re-enter Gmail PSWD: ')

while True:
    print 'What would you like to do?'
    prompt = raw_input('E.g: send, read, delete, quit: ')
    imapObj = ''
    if prompt == 'send' or prompt == 'Send':
        sendEmail(myEmailAddress, smtpObj)
    elif prompt == 'read' or prompt == 'Read':
        imapObj = receiveEmail(myEmailAddress, password, smtpObj)
    elif prompt == 'delete' or prompt == 'Delete':
        imapObj = receiveEmail(myEmailAddress, password, smtpObj, 'D')
    elif prompt == 'quit' or prompt == 'Quit':
        quitEmail(myEmailAddress, smtpObj)
        break
if imapObj:
    imapObj.logout()


    

