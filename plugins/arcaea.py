import requests
import urllib3
from bs4 import BeautifulSoup
import time
import json

class Arcaea(object):
    session = ''
    access_token = ''
    token_type = ''

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.session()

    def arc_login(self):
        url = 'https://arcapi.lowiro.com/8/auth/login'
        Headers = {
            'Accept': '*/*',
            'Authorization': 'Basic UmVzdGFydDA0OlJldml2ZTkwMDA=',
            'AppVersion': '2.4.7',
            'Accept-Language': 'zh-cn',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'DeviceId': '81C9D5E3-A3A0-4161-9CF9-9511F5625D2B',
            'User-Agent': 'Arc-mobile/2.4.7.0 CFNetwork/1107.1 Darwin/19.0.0',
            'Content-Length': '29',
            'Connection': 'keep-alive'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        response = self.session.post(url, headers=Headers, data=data, verify=False)
        soup = BeautifulSoup(response.content, features="html.parser")
        dict = json.loads(soup.get_text())
        print(dict)
        self.access_token = dict["access_token"]
        self.token_type = dict["token_type"]

    def arc_add_friend(self, friend_code):
        url = 'https://arcapi.lowiro.com/8/friend/me/add'
        Headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Arc-mobile/2.4.7.0 CFNetwork/1107.1 Darwin/19.0.0',
            'Content-Length': '21',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'Authorization': self.token_type + ' ' + self.access_token,
            'Accept-Encoding': 'gzip, deflate, br',
            'AppVersion': '2.4.7'
        }
        data = {
            'friend_code': friend_code
        }
        response = self.session.post(url, headers=Headers, data=data, verify=False)
        soup = BeautifulSoup(response.content, features="html.parser")
        dict = json.loads(soup.get_text())
        print('add')
        print(dict)
        if dict['success'] == False:
            return 'fail', { 'song_name': 'fail' }, '0'
        info = dict['value']['friends'][0]
        info_score = info['recent_score'][0]
        ret_info = {}
        ret_info['character'] = str(info['character'])
        ret_info['name'] = str(info['name'])
        ret_info['clear_type'] = str(info_score['clear_type'])
        ret_info['rank'] = str(float(info['rating']) / 100.0)
        ret_info['song_name'] = str(info_score['song_id'])
        ret_info['score'] = str(info_score['score'])
        ret_info['pure'] = str(info_score['perfect_count']) + ' (' + str(info_score['shiny_perfect_count']) + ')'
        ret_info['far'] = str(info_score['near_count'])
        ret_info['miss'] = str(info_score['miss_count'])
        ret_info['ptt'] = str('%.2f' % info_score['rating'])
        ret_info['difficulty'] = str(info_score['difficulty'])
        unix_time = info_score['time_played'] / 1000
        unix_time = time.localtime(unix_time)
        unix_time = time.strftime('%Y/%m/%d', unix_time)
        ret_info['date'] = str(unix_time)
        friend_id = str(info['user_id'])

        return 'success', ret_info, friend_id

    def arc_delete_friend(self, friend_id):
        url = 'https://arcapi.lowiro.com/8/friend/me/delete'
        Headers = {
            'Host': 'arcapi.lowiro.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Arc-mobile/2.4.7.0 CFNetwork/1107.1 Darwin/19.0.0',
            'Content-Length': '17',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'Authorization': self.token_type + ' ' + self.access_token,
            'Accept-Encoding': 'gzip, deflate, br',
            'AppVersion': '2.4.7'
        }
        data = {
            'friend_id': friend_id
        }
        response = self.session.post(url, headers=Headers, data=data, verify=False)
        soup = BeautifulSoup(response.content, features="html.parser")
        dict = json.loads(soup.get_text())
        print('delete')
        print(dict)

    def arc_find_song(self, song_id):
        url = 'https://arcapi.lowiro.com/8/score/song/friend?song_id=' + song_id + '&difficulty=2&start=0&limit=11' 
        Headers = {
            'Host': 'arcapi.lowiro.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Arc-mobile/2.4.7.0 CFNetwork/1107.1 Darwin/19.0.0',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'Authorization': self.token_type + ' ' + self.access_token,
            'Accept-Encoding': 'gzip, deflate, br',
            'AppVersion': '2.4.7'
        }
        response = self.session.get(url, headers=Headers, verify=False)
        soup = BeautifulSoup(response.content, features="html.parser")
        dict = json.loads(soup.get_text())
        print('find')
        print(dict)
        if len(dict['value']) == 0:
            return { 'song_name': 'no' }
        info = dict['value'][0]
        ret_info = {}
        ret_info['character'] = str(info['character'])
        ret_info['name'] = str(info['name'])
        ret_info['clear_type'] = str(info['clear_type'])
        ret_info['name'] = str(info['name'])
        ret_info['song_name'] = str(info['song_id'])
        ret_info['score'] = str(info['score'])
        ret_info['pure'] = str(info['perfect_count']) + '(' + str(info['shiny_perfect_count']) + ')'
        ret_info['far'] = str(info['near_count'])
        ret_info['miss'] = str(info['miss_count'])
        unix_time = info['time_played'] / 1000
        unix_time = time.localtime(unix_time)
        unix_time = time.strftime('%Y/%m/%d', unix_time)
        ret_info['date'] = str(unix_time)
        ret_info['difficulty'] = str(info['difficulty'])
        return ret_info

    def arc_last_song(self, friend_code):
        success_code, ret_info, friend_id = self.arc_add_friend(friend_code)
        time.sleep(0.1)
        if success_code == 'fail':
            return { 'song_name': 'fail' }
        print(ret_info)
        #for it in ret_info:
        #    print(it, ret_info[it])
        #print('\n')
        time.sleep(0.1)
        self.arc_delete_friend(friend_id)
        return ret_info


    def arc_define_song(self, friend_code, song_id):
        success_code, ret_info, friend_id = self.arc_add_friend(friend_code)
        time.sleep(0.1)
        print(success_code)
        if success_code == 'fail':
            return { 'song_name': 'fail' }
        rank = ret_info['rank']
        ret_info = self.arc_find_song(song_id)
        ret_info['rank'] = rank
        time.sleep(0.1)
        self.arc_delete_friend(friend_id)
        return ret_info
