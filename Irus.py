import os
import PySimpleGUI as psg
import speech_recognition as _sr  # Speech recogniser for getting voice input
import pyttsx3  # Speech to text for irus voice
import IrusCommands as IC  # For Irus Commands
import webbrowser  # Use as browser
import random  # use for a random reply
import requests
from os import path
from bs4 import BeautifulSoup
from pathlib import Path  # user to get path
from os import walk  # For get all files

'''
 -----------------------Initialization of variables------------------------------
'''

_irus_listener = _sr.Recognizer()  # Recognise Voice 1st initialization
_engine = pyttsx3.init()  # Text to audio initialization
_engine.setProperty('rate', 150)  # Set voice a little slow
_irus_sim = open('__models__/__spacial__/__irusnamemodels__.irdata', 'r').read().split('\n')  # Irus synonyms
_email_subject_commands = open('__models__/__spacial__/__irusemailmodels__.irdata',
                               'r').read().split('\n')  # Commands for email subject
_wiki_subject_commands = open('__models__/__spacial__/__iruswikimodels__.irdata',
                              'r').read().split('\n')  # Commands for wiki subject
_google_search_models = open('__models__/__spacial__/__irusgooglemodels__.irdata',
                             'r').read().split('\n')  # Commands for google models
_web_search_models = open('__models__/__spacial__/__iruswebsearchmodels.irdata',
                          'r').read().split('\n')  # Commands for web models
_talk_models = open('__models__/__spacial__/__irustalkmodels.irdata',
                    'r').read().split('\n')  # Commands for talk models
_none_models = open('__models__/__general__/nothing.irdata',
                    'r').read().split('\n')  # Commands for talk models
_commands = ['play ', 'time', 'joke', 'shutdown', 'quit']  # Commands that valid
_greet = ['good morning', 'good evening']  # greet
_bye = ['good noon', 'good night']  # bye
_user_query_fulfil = False  # program satisfaction

# Get all user general questions
_user_file_list = next(walk('__models__'), (None, None, []))[2]
for i in _user_file_list:
    print("data generated: " + i)

# Get all user general answers
_irus_file_list = next(walk('__models__/__general__'), (None, None, []))[2]
for i in _irus_file_list:
    print(".irdata generated: " + i)

'''
 -----------------------Define all mandatory functions------------------------------
'''


def _irus_voice_reply(_text):  # get str form parameter
    _engine.say(_text)  # Say the given parameter
    _engine.runAndWait()  # Run and wait for reply (use to trigger the voice)


def _irus_listener_regular_sound_listen():
    _path = Path("__models__/__spacial__/__irusConfi__.irdata")
    try:
        with _sr.Microphone() as _voice_source:  # Get _voice_source as default microphone
            print("& -ir irus listen to source")  # Print so that user know irus is listing
            _irus_listener.adjust_for_ambient_noise(source=_voice_source,
                                                    duration=0.1)  # adjust ambient noise for faster process
            _irus_listener.energy_threshold = 10000
            _irus_listener.phrase_threshold = 0.1
            _input_voice = _irus_listener.listen(_voice_source)  # Listen from source as here _voice_source variable
            # Use google Microphone to get commands
            _user_command = _irus_listener.recognize_google(audio_data=_input_voice, language="en-IN")
            print(_user_command)  # Printing our command raw
            _user_command = _user_command.lower()  # Convert all command to lower case and then print
            # Start conditions for Irus name

            if _path.is_file():
                print("Done fin file")
                for x in _irus_sim:  # Loop through all recognisable words
                    print("Drwon in loop " + x)
                    if x in _user_command:  # If get proper
                        print("get value and done")
                        _user_final_command = _user_command.replace(x, '')  # Remove irus from word
                        print("granted: " + _user_final_command)  # Print final command
                        return _user_final_command
                    if x == 'hydrous':
                        print("Send raw")
                        return _user_command
            else:
                for x in _irus_sim:  # Loop through all recognisable words
                    if x in _user_command:  # If get proper
                        _user_final_command = _user_command.replace(x, '')  # Remove irus from word
                        print("granted: " + _user_final_command)  # Print final command
                        _irus_cong = open('__models__/__spacial__/__irusConfi__.irdata',
                                          'w+')
                        _irus_cong.close()
                        return _user_final_command



    except:  # If error occurs this statement will triggered
        pass  # Just pass for do nothing


def _irus_query_listener():  # This is for data listen
    try:
        with _sr.Microphone() as _voice_source:  # Get _voice_source as default microphone
            print("& -ir irus listen to source")  # Print so that user know irus is listing
            _irus_listener.adjust_for_ambient_noise(source=_voice_source,
                                                    duration=0.5)  # adjust ambient noise for faster process
            _input_voice = _irus_listener.listen(_voice_source)  # Listen from source as here _voice_source variable
            # Use google Microphone to get commands
            _user_data = _irus_listener.recognize_google(audio_data=_input_voice, language="en-IN")
            print(_user_data)  # Printing our command raw
            _user_data = _user_data.lower()  # Convert all command to lower case and then print
            return _user_data  # Return data to user

    except:  # If error occurs this statement will triggered
        pass  # Just pass for do nothing


def irusEmailSender():  # Collect all data and return
    _irus_voice_reply("Whom?")  # say whom?
    _receiver = _irus_query_listener()  # Get the receiver query
    _user_path = Path("data\\" + _receiver + ".irdata")  # Get user path
    if not _user_path.is_file():  # If no data available
        _irus_voice_reply("No email found with that name. Please write the email down")  # ask for email
        _address = input("Email address [don't need to include @gmail.com]: ")
        print(_address)
        _irus_voice_reply("Do you want to save this email with name " + _receiver + "?")
        _check_ans = _irus_query_listener()

        if 'yes' in _check_ans or 'ok' in _check_ans or 'save' in _check_ans:
            _file_data = open('data\\' + _receiver + '.irdata', 'w+').write(_address + "@gmail.com")
            _irus_voice_reply("email saved as the name of " + _receiver)
        else:
            _irus_voice_reply("Ok.")

        _receiver = _address + "@gmail.com"
    else:
        _receiver_profile = open("data\\" + _receiver + ".irdata", 'r')  # Open profile data
        _email_data = _receiver_profile.read()
        if _email_data is None:
            _irus_voice_reply("No email found with that name. Please write the email down")  # ask for email
            _address = input("Email address [don't need to include @gmail.com]: ")  # Get email address
            _irus_voice_reply("Do you want to save this email with name " + _receiver + "?")  # replay user to get order
            _check_ans = _irus_query_listener()  # check irus voice coord

            if 'yes' in _check_ans or 'ok' in _check_ans or 'save' in _check_ans:  # check for positive words
                _file_data = open('data\\' + _receiver + ".irdata", 'w') \
                    .write(_address + "@gmail.com")  # get irus data as irdata
                _irus_voice_reply("email saved as the name of " + _receiver)  # reply with voice
            else:  # else reply ok
                _irus_voice_reply("Ok.")  # reply for ok

            _receiver = _address + "@gmail.com"  # add .gmail.com
        else:
            _receiver = _email_data  # set email data as receiver

    _irus_voice_reply("Subject?")  # say Subject
    _sub = _irus_query_listener()  # Get the subject query
    _irus_voice_reply("email?")  # say email
    _mail = _irus_query_listener()  # get the actual mail query
    _irus_voice_reply("Do you conform this email?")  # Conform to send email
    _confirm = _irus_query_listener()  # get reply
    if 'yes' in _confirm or 'ok' in _confirm or 'conform' in _confirm:  # check for yes or no
        _irus_voice_reply("Email proceed")  # reply that email is proceed
        return _receiver, _sub, _mail  # Return all
    else:
        _irus_voice_reply("email canceled")  # reply that email failed
        _receiver, _sub, _mail = None, None, None  # initialize all to none
        return _receiver, _sub, _mail  # Return all


def _get_Assistant_google(_query):
    URL = "https://www.google.co.in/search?q=" + _query

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36'}

    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        results = soup.find(class_='Z0LcW').get_text()
        return results
    except:
        return None


def temp():
    URL = "https://www.google.co.in/search?q=current+temperature&sxsrf=AOaemvKGB_s9sxd4Vtsv-OP81XfyfrmLOg" \
          "%3A1642762872426&source=hp&ei=eJLqYcf8F5iP2roPy82w0AY&iflsig=ALs-wAMAAAAAYeqgiN_yE3Aw0LmhC1l9rfndVwSjnqvp" \
          "&oq=current+&gs_lcp" \
          "=Cgdnd3Mtd2l6EAMYADIHCCMQJxCdAjIECAAQQzIECAAQQzIECAAQQzIKCAAQsQMQyQMQQzIFCAAQkgMyBQgAEJIDMgQIABBDMgcIABCxAxBDMgcIABCxAxBDOg0ILhDHARDRAxDqAhAnOgcIIxDqAhAnOgUIABCABDoKCC4QxwEQowIQQzoICAAQgAQQsQM6CwguEIAEELEDEIMBOgUILhCABDoLCAAQgAQQsQMQgwE6CggjEMkDECcQnQI6BAguEEM6CggAEIAEEIcCEBQ6BwgAEMkDEENQvgVY3A1gxBdoAHAAeAGAAZUFiAHvFZIBCzAuNC4yLjEuMC4ymAEAoAEBsAEK&sclient=gws-wiz "

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36'}

    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        results = soup.find(class_='wob_t q8U8x').get_text()
        return results
    except:
        return None


def weather():
    URL = "https://www.google.com/search?q=how+is+today+weather"

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36'}

    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        results = soup.find(class_='wob_dcp').get_text()
        return results
    except:
        return None


if __name__ == '__main__':
    while True:
        _user_query_fulfil = False
        _cmd = _irus_listener_regular_sound_listen()  # Getting commands from user
        if _cmd is not None:  # Check commands for not null
            print("Command: " + _cmd)
            if _commands[0] in _cmd:  # Check play word from command
                _cmd = _cmd.replace('play', '')  # Replace 'play' from the command to play video or audio
                _irus_voice_reply("Playing " + _cmd)  # reply from irus
                IC.play(_topic=_cmd)  # Play the topic which received from user

            elif _commands[1] in _cmd:  # Check time word from command
                _time = IC.date_time()  # Collect system time from datetime package
                _irus_voice_reply("Current Time is " + _time)  # Reply from irus

            elif _commands[2] in _cmd:  # check for joke in command
                joke = IC.joke()  # get joke
                print("You might find this funny " + joke)  # Print the joke
                _irus_voice_reply("You might find this funny: " + joke)  # Say the joke

            elif _commands[3] in _cmd:  # check for shut down
                _irus_voice_reply("Irus service, shutting down")  # shut down irus
                break  # close the loop

            elif _commands[4] in _cmd:
                _irus_voice_reply('ok')
                os.system("wmic process where name='Chrome.exe' delete")

            else:  # if none of the commands given irus search for wiki or google
                for i in _greet:
                    if i in _cmd:
                        temp = temp()
                        weather = weather()
                        print(temp + weather)
                        _irus_voice_reply(
                            i + 'sir. today is ' + temp + 'degree celsius temperature and' + weather + ', What are '
                                                                                                       'todays plan?')
                        _user_query_fulfil = True
                        break
                    if i == i[-1]:
                        _user_query_fulfil = False
                        break

                for i in _bye:
                    if not _user_query_fulfil:
                        if i in _cmd:
                            _irus_voice_reply(i + 'sir')
                            _user_query_fulfil = True
                            break
                        if i == i[-1]:
                            _user_query_fulfil = False
                            break

                for i in _user_file_list:
                    if not _user_query_fulfil:
                        _qr_data = open('__models__/' + i, 'r').read().split('\n')
                        for _data in _qr_data:
                            if _data in _cmd:
                                _reply_query = open('__models__/__general__/' + i + '.irdata', 'r').read().split('\n')
                                _reply = random.choice(_reply_query)
                                print(_reply)
                                _irus_voice_reply(_reply)
                                _user_query_fulfil = True
                                break
                            if i == i[-1]:
                                _user_query_fulfil = False
                                break

                for i in _google_search_models:
                    if not _user_query_fulfil:
                        if i in _cmd:
                            cmd = _cmd.replace(i, '')  # try a google search
                            try:
                                result = _get_Assistant_google(_cmd)
                                _irus_voice_reply(result)
                                _user_query_fulfil = True
                            except:
                                _user_query_fulfil = False
                            break
                        if i == i[-1]:  # If i is not in method
                            _user_query_fulfil = False
                            break

                for i in _wiki_subject_commands:  # loop thorough all commands that can wiki
                    if not _user_query_fulfil:
                        if i in _cmd:  # If get the wiki command
                            _cmd = _cmd.replace(i + "is", '')  # replace the constant command get from loop to null
                            _info = IC.search_pidea(_cmd)  # Search on wikipedia using wiki
                            if _info is None:  # If nothing found in wiki
                                _irus_voice_reply(
                                    "Nothing found in Wikipedia. Trying a google search"
                                )  # Tell user that nothing is found
                                _user_query_fulfil = True
                                IC.google(_cmd)  # search topic in google
                                _irus_voice_reply("Here is what I found")  # tell user that irus find
                                break
                            else:
                                _irus_voice_reply("According to Wikipedia in summery: " +
                                                  _info)  # reply the info with voice
                                print("WIKI: " + _info)
                                _user_query_fulfil = True
                                break  # break the loop when find the confident result

                        if i == i[-1]:
                            _user_query_fulfil = False
                            break

                for i in _google_search_models:
                    if not _user_query_fulfil:
                        if i in _cmd:
                            cmd = _cmd.replace(i, '')  # try a google search
                            _info = IC.google(_cmd)  # Get info from google
                            _irus_voice_reply("here is what i found")  # replay that she found something
                            break
                        if i == i[-1]:  # If i is not in method
                            _user_query_fulfil = False
                            break

                for i in _web_search_models:  # search for web commands
                    if not _user_query_fulfil:
                        if i in _cmd:
                            _cmd = _cmd.replace(i, '')  # replace again
                            if 'https' in _cmd:  # If get https that means user is calling full website link
                                webbrowser.open_new_tab(_cmd)  # Open site in web browser
                                _irus_voice_reply("Opening " + _cmd + " from browser")  # Reply with voice
                            else:
                                _irus_voice_reply("Opening " + _cmd + " from web browser")  # else just reply
                                webbrowser.open_new_tab(_cmd
                                                        + ".com")  # get with home page by ex: https://www.google.com
                            _user_query_fulfil = True
                            break
                        if i == i[-1]:
                            _user_query_fulfil = False
                            break

                for i in _talk_models:
                    if not _user_query_fulfil:
                        if i in _cmd:
                            _cmd = _cmd.replace(i, '')  # replace word
                            _irus_voice_reply(_cmd)  # reply with voice
                            _user_query_fulfil = True
                            break  # break the loop
                        if i == i[-1]:
                            _user_query_fulfil = False
                            break  # break the loop

                for i in _email_subject_commands:
                    if not _user_query_fulfil:
                        if i in _cmd:
                            _cmd = _cmd.replace(i, '')  # Replace word from command
                            receiver, subject, mail = irusEmailSender()  # Get three query and initialize in variables
                            if receiver is None:  # if email canceled by user
                                _user_query_fulfil = True
                            else:
                                IC.sendEmail(_receiver=receiver, _sub=subject, _email=mail)  # send email to person
                                _irus_voice_reply("Email send successfully")  # say that email send
                                _user_query_fulfil = True
                            break  # break the loop
                        if i == i[-1]:
                            _user_query_fulfil = False
                            break  # break the loop

                if not _user_query_fulfil:
                    _user_query_fulfil = True
                    _irus_voice_reply("I can't understand a single word you say, Do you want me to try a google "
                                      "search about this?")

                    _check = _irus_query_listener()  # check the reply query
                    if _check is not None:
                        if 'yes' in _check or 'ok' in _check or 'search' in _check:  # if user want for search
                            _irus_voice_reply("Ok")  # irus say ok
                            try:
                                result = _get_Assistant_google(_cmd)
                                _irus_voice_reply(result)
                            except:
                                IC.google(_cmd)  # google about user command
                                _irus_voice_reply("Here is what i found")  # Replay that she found
                        else:
                            _irus_voice_reply("Ok")  # just say ok and continue the loop
        else:
            _irus_voice_reply(random.choice(_none_models))
            


'''
 -------------------------About ------------------------------
'''

'''
    This code is using IrusCommands Python package and also smtplib, pywhatkit, wikipedia and also much more.
    This code it self using SpeechRecognition and python library text to speech (pyttsx3) for getting the voice
        and reply by voice.
    Also it use many python pre-build libraries for external in internal functions  
'''

"""

:parameter Author Aritra Das

"""
