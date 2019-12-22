import json

from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
app = Flask(__name__)

@app.route("/")
def home():
    return "hi"

@app.route("/index")
def index():
    return render_template('login.html', message='')

urls = '''
https://www.google.com/
https://www.yahoo.com/
https://www.foxnews.com/politics/aoc-squad-news-conference-trump-call-go-back-home
'''
datafromjs = urls

@app.route('/login', methods=['GET', 'POST'])
def login():
   message = None
   if request.method == 'GET':
        datafromjs = request.args.get('mydata')
        print(datafromjs)
        # Add Summarization and Bias code here.
        news = []
        for url in datafromjs.strip().split("\n"):
            s = 0
            b = 0
            try:
                s = round(subjectivity(url),4)
                b = round(polarity(url),4)
            except Exception as e:
                s = 'retrieval error: '+ str(e)
                b = 'retrieval error: '+ str(e)
                pass
            resplist = []
            resplist.append(url)
            resplist.append(s)
            resplist.append(b)
            news.append(resplist)

        resp = make_response('{"response": '+json.dumps(news)+'}')
        resp.headers['Content-Type'] = "application/json"
        print(resp)
        return resp



#https://medium.com/fintechexplained/nlp-python-data-extraction-from-social-media-emails-images-documents-web-pages-58d2f148f5f4
#https://textblob.readthedocs.io/en/dev/
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#https://www.datacamp.com/community/tutorials/web-scraping-using-python
#https://stackoverflow.com/questions/8554035/remove-all-javascript-tags-and-style-tags-from-html-with-python-and-the-lxml-mod
#https://planspace.org/20150607-textblob_sentiment/
#https://www.aclweb.org/anthology/D17-1058.pdf

from textblob import TextBlob
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree
import lxml.html

def remove_javascript(txt_str):
    root = lxml.html.document_fromstring(txt_str)
    txtels = root.xpath("//*[local-name()!='script' and local-name() != 'style']/text()")
    return " ".join(txtels)

# Each word in the lexicon has scores for:
# 1) polarity: negative vs. positive    (-1.0 => +1.0)
# 2) subjectivity: objective vs. subjective (+0.0 => +1.0)

def subjectivity(url):
    html = urlopen(url).read()
    html = remove_javascript(html)
    soup = BeautifulSoup(html, "lxml")
    soup.get_text()
    return TextBlob(soup.text).sentiment.subjectivity

def polarity(url):
    html = urlopen(url).read()
    html = remove_javascript(html)
    soup = BeautifulSoup(html, "lxml")
    soup.get_text()
    return TextBlob(soup.text).sentiment.polarity

if __name__ == "__main__":
    app.run(debug = True)
