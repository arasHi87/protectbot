# -*- coding: utf-8 -*-
from linepy import *
from akad.ttypes import Message
from datetime import datetime
import json,sys,atexit,time,codecs,timeit
botStart = time.time()
cl = LINE()
channelToken = cl.getChannelResult()
cl.log("Auth Token : " + str(cl.authToken))
print ("======登入成功=====")
oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
clMID = cl.profile.mid
KAC=[cl]
admin=['u85ee80cfb293599510d0c17ab25a5c98', 'u72e36ec4d3a1c6b3b5b4a3654eead14a', 'u8efc93824990b63d86eebb930ab97360',clMID]
msg_dict = {}
bl = [""]
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            GS = group.creator.mid
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in settings['bot'] or op.param2 == GS:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
                    invsend = 0
                    cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "你沒有權限開啟網址!")
                    cl.kickoutFromGroup(op.param1,[op.param2])
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            GS = group.creator.mid
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if settings["inviteprotect"] == True:
                if op.param2 in admin or op.param2 in settings['bot'] or op.param2 == GS:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            if settings["autoJoin"] == True:
                if op.param2 in admin or op.param2 in settings['bot']:
                    print ("進入群組: " + str(group.name))
                    cl.acceptGroupInvitation(op.param1)
                    try:
                        mc = ""
                        for mi_d in settings["bot"]:
                            cl.findAndAddContactsByMid(mi_d)
                            cl.inviteIntoGroup(msg.to,[mi_d])
                    except:
                        pass
                pass
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if settings["protect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    if contact2.mid in admin:
                        cl.findAndAddContactsByMid(op.param3)
                        cl.inviteIntoGroup(op.param1,[op.param3])
        if op.type == 24:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin:
                if msg.text in ["kickban"]:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in settings["blacklist"]:
                            matched_list+=filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            print ("1")
                            cl.sendMessage(to, "沒有黑名單")
                            return
                        for jj in matched_list:
                            cl.kickoutFromGroup(to, [jj])
                            cl.sendMessage(to, "黑名單已踢除")
                elif msg.text in ["speed"]:
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    start = time.time()
                    cl.sendMessage(to,'處理速度\n' + str1 + '秒')
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,'指令反應\n' + format(str(elapsed_time)) + '秒')
                elif text.lower() == 'in':
                    gid = user['gid']
                    url = user['url']
                    acceptGroupInvitationByTicket(gid, url)
        if op.type == 26:
            try:
                msg = op.message
                if msg.toType == 0:
                    cl.log("[%s]"%(msg._from)+msg.text)
                else:
                    cl.log("[%s]"%(msg.to)+msg.text)
                if msg.contentType == 0:
                    msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
            except Exception as e:
                print(e)
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)