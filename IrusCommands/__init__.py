import datetime
import requests
import wikipedia
import smtplib
from email.message import EmailMessage
import pyjokes
import pywhatkit as pwk

def play(_topic):
    url = "http://www.google.com"  # demo url
    timeout = 5  # timeout time
    try:  # Try statement for internet
        requests.get(url, timeout=timeout)  # request for getting web
        pwk.playonyt(_topic)
    except (requests.ConnectionError, requests.Timeout):  # get exception
        print("No Internet Detected")  # reply that no internet detected


def date_time():
    return datetime.datetime.now().strftime('%I:%M %p')


def search_pidea(_topic, lines=2):
    try:
        return wikipedia.summary(_topic, lines)
    except:
        return None


def google(_topic):
    url = "http://www.google.com"  # demo url
    timeout = 5  # timeout time
    try:  # Try statement for internet
        requests.get(url, timeout=timeout)  # request for getting web
        return pwk.search(_topic)
    except (requests.ConnectionError, requests.Timeout):  # get exception
        print("No Internet Detected")  # reply that no internet detected



def joke():
    return pyjokes.get_joke(language='en', category='all')


def sendEmail(_receiver, _sub, _email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('aritra.irus.AI@gmail.com', 'AritraDasIrus2005')
    email = EmailMessage()
    email['From'] = 'aritra.irus.AI@gmail.com'
    email['To'] = _receiver
    email['Subject'] = _sub
    email.set_content(_email)
    server.send_message(email)

