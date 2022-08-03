# http requests
import requests 
# Web Scraping
from bs4 import BeautifulSoup
# send the email
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime

# get the date and time
now = datetime.datetime.now()

# email content placeholder
content = ' '

# extracting Hacker News Stories

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    #<b>= bold text
    cnt +=('<b>HN Top Stories:<b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    #find all the class title values and index them 
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        #capture all the title tages except more 
        cnt += ((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else '')
        #print (tag.prettyify)# find all ('span', attrs={'class':sitestr})
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

#lets send email

print('Composing Email... ')

# update your email details

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT =  # your port number
FROM = # your from email id
TO = # your to email ids # can be a list
PASS =  # your emails password

# fp = open(file_name, 'rb')
# create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

#msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-'+ str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print("Initiating Server...")

server = smtplib.SMTP(SERVER,PORT)
#server = smtplib.SMT_SSL('smtp.gmail.com',465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()

