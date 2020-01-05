from nonebot import on_command, CommandSession, permission, message
from plugins.arcaea import Arcaea
from plugins.image import AImage
import plugins.song
import time
from plugins.sql import ASQL

__plugin_name__  = 'arcp'

user = Arcaea()
user.arc_login()
db = ASQL()

def choose_rank(rank):
    rank = float(rank)
    if rank < 10:
        return 'img/rating_2.png'
    if 10 <= rank and rank < 11:
        return 'img/rating_3.png'
    if 11 <= rank and rank < 12:
        return 'img/rating_4.png'
    if 12 <= rank and rank < 12.5:
        return 'img/rating_5.png'
    if rank >= 12.5:
        return 'img/rating_6.png'

def choose_clear_type(type):
    return 'img/clear_' + str(type) + '.png'

def choose_score_type(score):
    score = int(score)
    if score < 8600000:
        return 'img/D.png'
    if 8600000 <= score and score < 8900000:
        return 'img/C.png'
    if 8900000 <= score and score < 9200000:
        return 'img/B.png'
    if 9200000 <= score and score < 9500000:
        return 'img/A.png'
    if 9500000 <= score and score < 9800000:
        return 'img/AA.png'
    if score >= 9800000:
        return 'img/EX.png'

def sc_rank(ptt, score):
    if score >= 10000000:
        return ptt + 2.00
    if score >= 9950000:
        return ptt + 1.50 + (score - 9950000.0) / 100000.0
    if score >= 9800000:
        return ptt + 1.00 + (score - 9800000.0) / 400000.0
    ptt = ptt + (score - 9500000.0) / 300000.0
    if ptt < 0:
        ptt = 0
    return ptt

def check_song(name):
    length = len(name)
    for d in plugins.song.dict:
        t = d.lower()
        if name in t[:length]:
            return d, plugins.song.dict[d][0], plugins.song.dict[d][1]
    return 'no', 'no', '0'

@message.message_preprocessor
async def _(bot: message.NoneBot, ctx: message.Context_T):
    # print(ctx)
    ctx['preprocessed'] = True
    if 'text' in ctx['message'][0]['data'].keys():
        ctx['message'][0]['data']['text'] = ctx['message'][0]['data']['text'] + ' *' + str(ctx['sender']['user_id'])

@on_command('last', only_to_me = False, permission = permission.GROUP | permission.PRIVATE)
async def get_last_song(session: CommandSession):
    stripped_arg = session.current_arg_text.split('*')[0]
    qq = session.current_arg_text.split('*')[1]
    stripped_arg = stripped_arg.strip()
    arg_list = stripped_arg.split(' ')
    print(arg_list)
    flag, friend_code = db.find_user(qq)
    if flag == False:
        return
    print('friend code')
    print(friend_code)
    ret_info = user.arc_last_song(friend_code)
    if ret_info['song_name'] == 'fail':
        print('fail')

    names = list()
    names.append('song/' + ret_info['song_name'] + '.jpg')
    names.append(choose_rank(ret_info['rank']))
    names.append('img/transparent.png')
    names.append('character/' + ret_info['character'] + '_icon.png')
    names.append(choose_clear_type(int(ret_info['clear_type'])))
    names.append(choose_score_type(ret_info['score']))

    image = AImage(names)
    img = image.create_img(ret_info)
    img.save('C:/Users/Aris/Desktop/D/CQP-xiaoi/coolqp/data/image/' + 'tmp.png')
    time.sleep(1)
    await session.send('[CQ:image, file=tmp.png]')
    
@on_command('song', only_to_me=False, permission=permission.GROUP | permission.PRIVATE)
async def get_song_by_name(session: CommandSession):
    stripped_arg = session.current_arg_text.split('*')[0]
    qq = session.current_arg_text.split('*')[1]
    stripped_arg = stripped_arg.strip()
    arg_list = stripped_arg.split(' ')
    print(arg_list)
    if len(arg_list) >= 1:
        song_name = ''
        for arg in arg_list:
            song_name = song_name + ' ' +arg

        song_name = song_name.lower()
        song_name, update_name, rank = check_song(song_name[1:])
        if song_name == 'no':
            await session.send('no song')
            return
        print(update_name)
        flag, friend_code = db.find_user(qq)
        if flag == False:
            return
        ret_info = user.arc_define_song(friend_code, update_name)
        if ret_info['song_name'] == 'fail':
            print('fail')
        if ret_info['song_name'] == 'no':
            await session.send('not played')
            return
            
        ret_info['ptt'] = str('%.2f' % sc_rank(float(rank), int(ret_info['score'])))

        names = list()
        names.append('song/' + ret_info['song_name'] + '.jpg')
        names.append(choose_rank(ret_info['rank']))
        names.append('img/transparent.png')
        names.append('character/' + ret_info['character'] + '_icon.png')
        names.append(choose_clear_type(int(ret_info['clear_type'])))
        names.append(choose_score_type(ret_info['score']))

        ret_info['song_name'] = song_name
        image = AImage(names)
        img = image.create_img(ret_info)
        img.save('C:/Users/Aris/Desktop/D/CQP-xiaoi/coolqp/data/image/' + 'tmp.png')
        time.sleep(1)
        await session.send('[CQ:image, file=tmp.png]')

@on_command('ID', only_to_me=False, permission=permission.GROUP | permission.PRIVATE)
async def bind_qq(session: CommandSession):
    stripped_arg = session.current_arg_text.split('*')[0]
    qq = session.current_arg_text.split('*')[1]
    print(qq)
    stripped_arg = stripped_arg.strip()
    arg_list = stripped_arg.split(' ')
    print(arg_list)
    if len(arg_list) == 1:
        flag, _ = db.find_user(qq)
        if flag == False:
            db.insert_user(qq, arg_list[0])
        else:
            db.update_user(qq, arg_list[0])
        db.view()
        await session.send('qq: ' + str(qq) + '\n' + 'ID: ' + str(arg_list[0]))


@on_command('delete', only_to_me=False, permission=permission.SUPERUSER)
async def delete_friend(session: CommandSession):
    stripped_arg = session.current_arg_text.split('*')[0]
    qq = session.current_arg_text.split('*')[1]
    stripped_arg = stripped_arg.strip()
    arg_list = stripped_arg.split(' ')
    print(arg_list)
    if len(arg_list) == 1:
        user.arc_delete_friend(arg_list[0])

@on_command('table', only_to_me=False, permission=permission.SUPERUSER)
async def arcaea_table(session: CommandSession):
    db.create_table()

@on_command('view', only_to_me=False, permission=permission.SUPERUSER)
async def db_view(session: CommandSession):
    db.view()

@on_command('test', only_to_me=False, permission=permission.SUPERUSER)
async def test(session: CommandSession):
    return