# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from flask import Flask, request, render_template
import datetime, requests, json

app = Flask(__name__)
file_in = "./sensor_in.csv"
file_out = "./sensor_out.csv"
file_exist = "./sensor_exist.csv"
port_num = 17104
SCOPES = ['https://www.googleapis.com/auth/calendar']

#Googleカレンダーの登録
def calendar(login,logout):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    formatin = datetime.datetime.strptime(login, '%Y/%m/%d,%H:%M:%S').isoformat()
    formatout = datetime.datetime.strptime(logout, '%Y/%m/%d,%H:%M:%S').isoformat()
    event_dict = {
        'summary': '研究',
        'start':{
            'dateTime': '2020-04-25T18:00:00',
            'timeZone': 'Japan',
        },
        'end':{
            'dateTime': '2020-04-25T22:00:00',
            'timeZone': 'Japan',
        },
    }

    event_dict['start']['dateTime'] = formatin
    event_dict['end']['dateTime'] = formatout

    event_dict = service.events().insert(calendarId='i0jd8eh63v2b10sqqtcm1smr3s@calendar.google.com',
    body=event_dict).execute()

    print(event_dict['id'])


#滞在時間の計算
def calc_time(start,end):
    starttime = datetime.datetime.strptime(start, '%Y/%m/%d,%H:%M:%S')
    endtime = datetime.datetime.strptime(end, '%Y/%m/%d,%H:%M:%S')
    
    total = endtime - starttime
    total_seconds = total.total_seconds()
    print(total_seconds)

    return int(total_seconds/60)
 

#slackにお褒めの言葉を投稿
def slack(flag,record):
    url = "T010V4PKESJ/B012M909PLY/177F8n5PrfYi6k8Mw0bga7o8" 

    if flag == 1:
        requests.post(url, data = json.dumps({
            'text': u"出席を確認！来れてすごい！！！",
        }))
    elif record > 180:
        requests.post(url, data = json.dumps({
            'text': u"3時間越え！もはや天才！！！！",
        }))
    elif record > 120:
        requests.post(url, data = json.dumps({
            'text': u"2時間以上だ！たまには休憩も必要だよ！",
        }))
    elif record > 60:
        requests.post(url, data = json.dumps({
            'text': u"お疲れ様！集中できたみたいじゃん！",
        }))
    elif record > 30:
        requests.post(url, data = json.dumps({
            'text': u"お疲れ様！進捗はどうかな？",
        }))
    else:
        requests.post(url, data = json.dumps({
            'text': u"お疲れ様！来たことに意義があるよね！",
        }))


@app.route('/', methods = ['GET'])
def get_html():
    return render_template('./index.html')


#ゲートウェイからデータ受信
@app.route('/exist', methods = ['POST'])
def update_exist():
    strlog = ""
    date = request.form["date"]
    time = request.form["time"]
    exist = request.form["exist"]
    try:
        exist_int = int(exist)

        if exist_int == 1:
            f = open(file_in, 'w')
            f.write(date + "," + time)
            slack(exist_int,0)
        else:
            f = open(file_out, 'w')
            f.write(date + "," + time)
            login = get_login()
            print(login)
            logout = date + "," + time
            #calendar(login,logout)
            record = calc_time(login,logout)
            print(record)
            slack(exist_int,record)
        return "succeeded to write"
    except Exception as e:
        print(e)
        return "failed to write"
    finally:
        f.close()

#開始した時間データを返す
@app.route('/login', methods = ['GET'])
def get_login():
    login = "0"
    try:
        f = open(file_in, 'r')
        for row in f:
            login = row
    except Exception as e:
        print("can not open:sensor_in")
        return e
    finally:
        f.close()
        return login

#終了した時間データを返す
@app.route('/logout', methods = ['GET'])
def get_logout():
    logout = "0"
    try:
        f = open(file_out, 'r')
        for row in f:
            logout = row
    except Exception as e:
        print("can not open:sensor_out")
        return e
    finally:
        f.close()
        return logout


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_num)