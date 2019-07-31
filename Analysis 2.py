import email
import os
import imaplib
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

if(os.path.isfile("SentimentScores.txt")=='True'):
    f = open("SentimentScores.txt","a")
else:
    f = open("SentimentScores.txt","w")
    f.write("Following are the polarity scores:\n")

analyser = SentimentIntensityAnalyzer() #object for sentiment analysis
def print_sentiment_scores(sentence):    #function for the actual analysis
    snt = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(snt))+"\n\n")
    score = str(snt)
    f.write("Message: "+sentence + "\nPolarity Score: " + score + "\n\n")

username = 'testrest024@gmail.com' #username of support mail ID
password = 'abc71421'              #password of support mail ID

mail = imaplib.IMAP4_SSL("imap.gmail.com")  #sets imap server
mail.login(username, password)              #log into support email ID
mail.select("inbox")  #selecting folder inside mail ID
result, data = mail.uid('search', None, "ALL") #selects all the emails
inbox_item_list = data[0].split()    #splitting the mails from each other

# Iterating through mails and printing them with their sentiment scores
for item in inbox_item_list:
    result2, email_data = mail.uid('fetch', item, '(RFC822)')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    to_= email_message['To']
    from_ = email_message['From']
    subject_ = email_message['Subject']
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        if not filename:
            ext = '.html'
            filename = 'msg-part-%08d%s' %(counter, ext)
        counter += 1        
        content_type = part.get_content_type()        
      
        if "plain" in content_type:  #checks if mail is plain text or not
            print("From:" + from_)
            print("To: " + to_)
            print("Subject: " + subject_)            
            text = part.get_payload()            
            print_sentiment_scores(text)  #message with sentiment         
            print("\n\n")
            pass                    
f.close()

