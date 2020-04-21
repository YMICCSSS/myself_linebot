#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
當用戶關注Line@後，Line會發一個FollowEvent，

我們接受到之後，取得用戶個資，對用戶綁定自定義菜單，會回傳四個消息給用戶
"""


# In[2]:


"""

啟用伺服器基本樣板

"""

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)
# 
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, TemplateSendMessage , ImageSendMessage, FlexSendMessage, CarouselContainer
)
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent
)

from linebot.models.template import( 
    ButtonsTemplate
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# 載入基礎設定檔
secretFileContentJson=json.load(open("line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "images/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))
print(line_bot_api)
print(handler)
# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# In[3]:


'''

用戶菜單功能介紹

    用戶能透過點擊菜單，進行我方希冀之業務功能。
    
流程
    準備菜單的圖面設定檔
    讀取安全設定檔上的參數
    將菜單設定檔傳給Line
    對Line上傳菜單照片
    檢視現有的菜單
    將菜單與用戶做綁定
    將菜單與用戶解除綁定
    刪除菜單

'''


# In[4]:


'''
菜單設定檔

    設定圖面大小、按鍵名與功能
    
'''

menuRawData="""
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "主圖文選單",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 271,
        "y": 855,
        "width": 746,
        "height": 695
      },
      "action": {
        "type": "postback",
        "text": "關於創辦人",
        "data": "action2"
      }
    },
    {
      "bounds": {
        "x": 1531,
        "y": 901,
        "width": 746,
        "height": 649
      },
      "action": {
        "type": "postback",
        "text": "開始上課",
        "data": "action1"
      }
    },
    {
      "bounds": {
        "x": 1531,
        "y": 88,
        "width": 746,
        "height": 649
      },
      "action": {
        "type": "postback",
        "text": "查閱已獲得學分",
        "data": "action5"
      }
    },
    {
      "bounds": {
        "x": 252,
        "y": 97,
        "width": 775,
        "height": 639
      },
      "action": {
        "type": "postback",
        "text": "查閱畢業條件",
        "data": "action3"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 455,
        "width": 252,
        "height": 776
      },
      "action": {
        "type": "postback",
        "text": "測驗將開始",
        "data": "action4"
      }
    },
    {
      "bounds": {
        "x": 2299,
        "y": 450,
        "width": 201,
        "height": 719
      },
      "action": {
        "type": "uri",
        "uri": "https://play.famobi.com/bubble-woods"
      }
    }
  ]
}
"""


# In[5]:


'''
==============================================================
=========== 圖文選單 ==========================================
======= 如果不小心上傳太多重複的圖文選單到Line Bot上， ===========
======= 先查詢這隻Line Bot上總共有多少圖文選單，全部刪掉 =========
==============================================================
'''

# 讓 Line_bot_api 查詢，現有創建的圖文選單
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)


# In[6]:


'''

讀取安全檔案內的字串，以供後續程式碼調用

'''
import json
secretFileContentJson=json.load(open("line_secret_key",'r',encoding="utf-8"))

print(secretFileContentJson.get("channel_access_token"))
print(secretFileContentJson.get("secret_key"))
print(secretFileContentJson.get("self_user_id"))


# In[7]:


'''

用channel_access_token創建line_bot_api，預備用來跟Line進行溝通


'''

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))


# In[8]:


'''

載入前面的圖文選單設定，

並要求line_bot_api將圖文選單上傳至Line
    

'''

from linebot.models import RichMenu
import requests

menuJson=json.loads(menuRawData)

lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
print(lineRichMenuId)


# In[9]:


'''

將先前準備的菜單照片，以Post消息寄發給Line

    載入照片
    要求line_bot_api，將圖片傳到先前的圖文選單id


'''


uploadImageFile=open("001.jpg",'rb')
print(uploadImageFile)


setImageResponse = line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)

print(setImageResponse)


# In[10]:


'''

將選單綁定到特定用戶身上
    取出上面得到的菜單Id及用戶id
    要求line_bot_api告知Line，將用戶與圖文選單做綁定

'''

# https://api.line.me/v2/bot/user/{userId}/richmenu/{richMenuId}


# linkResult=line_bot_api.link_rich_menu_to_user(secretFileContentJson["self_user_id"], lineRichMenuId)

# print(linkResult)


# In[11]:


rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)


# In[12]:


# rich_menu_id = line_bot_api.get_rich_menu_id_of_user(secretFileContentJson["self_user_id"])
# print(rich_menu_id)


# In[13]:


'''

製作文字與圖片的教學訊息

'''
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# 消息清單
reply_message_list = [
    TextSendMessage(text="歡迎您進入Drama School，這個世界每天有成千上萬的影集在更新，趕快開始上課跟上大家的腳步吧!"),
    ImageSendMessage(original_content_url='https://imgur.com/vJzd18w.jpg',
    preview_image_url='https://imgur.com/vJzd18w.jpg'),
]


# In[14]:


'''

撰寫用戶關注時，我們要處理的商業邏輯

1. 取得用戶個資，並存回伺服器
2. 把先前製作好的自定義菜單，與用戶做綁定
3. 回應用戶，歡迎用的文字消息與圖片消息

'''


# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    print(user_profile)
        
     # 將用戶資訊存在檔案內
    with open("users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')
        
        
#     # 將菜單綁定在用戶身上
#     linkRichMenuId=secretFileContentJson.get("rich_menu_id")
    linkResult=line_bot_api.link_rich_menu_to_user(event.source.user_id,lineRichMenuId)

    #回覆文字消息與圖片消息
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list
    )


# In[15]:


def create_sendmessage_array_from_jsonfile(fileName):    
    #開啟檔案，轉成json
    with open(fileName, 'r', encoding='utf8') as f:
        jsonArray = json.load(f)        
    
    returnArray = []
    
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')
        
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'video':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))    


    # 回傳
    return returnArray


# In[16]:


'''
利用Line Designer 做出各種回傳訊息的.json檔案
讀取.json檔案，做出不同的SendMessage
將所有做好的SendMessage，放進字典包起來
依照User傳給我不同的文字，給他不同的回覆
'''

A_TemplateSendMessage01 = create_sendmessage_array_from_jsonfile('./JsonFiles/001.json')
#該上課啦~

A_TemplateSendMessage02 = create_sendmessage_array_from_jsonfile('./JsonFiles/002.json')
#圖文選單

A_ImageSendMessage03 = create_sendmessage_array_from_jsonfile('./JsonFiles/003.json')
#畢業條件

A_TemplateSendMessage04 = create_sendmessage_array_from_jsonfile('./JsonFiles/004.json')
#選擇要哪個測驗

A_messageSendMessage006 = create_sendmessage_array_from_jsonfile('./JsonFiles/006.json')
#恭喜獲得一學分

A_messageSendMessage007 = create_sendmessage_array_from_jsonfile('./JsonFiles/007.json')
#李屍朝鮮第一題

A_messageSendMessage008 = create_sendmessage_array_from_jsonfile('./JsonFiles/008.json')
#李屍朝鮮第二題

A_messageSendMessage009 = create_sendmessage_array_from_jsonfile('./JsonFiles/009.json')
#,答錯

A_messageSendMessage010 = create_sendmessage_array_from_jsonfile('./JsonFiles/10.json')
#愛的迫降第一題

A_messageSendMessage012 = create_sendmessage_array_from_jsonfile('./JsonFiles/12.json')
#愛的迫降第二題

A_messageSendMessage013 = create_sendmessage_array_from_jsonfile('./JsonFiles/13.json')
#想見你第一題

A_messageSendMessage014 = create_sendmessage_array_from_jsonfile('./JsonFiles/14.json')
#想見你第二題

A_messageSendMessage015 = create_sendmessage_array_from_jsonfile('./JsonFiles/15.json')
#戀愛第一題

A_messageSendMessage016 = create_sendmessage_array_from_jsonfile('./JsonFiles/16.json')
#戀愛第二題


# dic_SendMessage = {
#                     "21" : A_TextSendMessage,
#                     "傳給我ImageSendMessage" : A_ImageSendMessage,
#                     "傳給我TemplateSendMessage_ButtonsTemplate" : A_TemplateSendMessage,
#                     "傳給我FlexSendMessage_Bubble" : A_FlexSendMessage_Bubble,
#                     "傳給我FlexSendMessage_Carousel" : A_FlexSendMessage_Carousel,
#                 }  


# In[17]:


#累積學分運作
pt=0
Point="累積獲得%d學分"%(pt)
dictions={"a1":2,"a2":2,"a3":2,"a4":2,"a5":2,"a6":2,"a7":2,"a8":2}
reply_message_list1 = [TextSendMessage(text=Point)]


# In[18]:

rep = {
    "action1": A_TemplateSendMessage01,
    "action2": A_TemplateSendMessage02,
    "action3": A_ImageSendMessage03,
    "action4": A_TemplateSendMessage04,
    "action5": reply_message_list1,
    "a1":  A_messageSendMessage007,
    "test2": A_messageSendMessage009,
    "test1": A_messageSendMessage006,
    "a2": A_messageSendMessage008,
    "test4": A_messageSendMessage009,
    "test3":  A_messageSendMessage006,
    "a3": A_messageSendMessage010,
    "test6": A_messageSendMessage009,
    "test5": A_messageSendMessage006,
    "a4": A_messageSendMessage012,
    "test7": A_messageSendMessage009,
    "test6": A_messageSendMessage006,
    "a5": A_messageSendMessage013,
    "test9": A_messageSendMessage006,
    "test10": A_messageSendMessage009,
    "a6": A_messageSendMessage014,
    "test11": A_messageSendMessage006,
    "test12": A_messageSendMessage009,
    "a7": A_messageSendMessage015,
    "test13": A_messageSendMessage006,
    "test14": A_messageSendMessage009,
    "a8": A_messageSendMessage016,
    "test15": A_messageSendMessage006,
    "test16": A_messageSendMessage009,
}


# In[19]:


# def rept():
#     with open("../user_profile_business.txt", "a") as myfile:
#         myfile.write(json.dumps(vars(user_profile), sort_keys=True))
#         myfile.write('\r\n')
#         line_bot_api.reply_message(
#             event.reply_token,
#             rep.get(event.postback.data)
#         )


# In[20]:
def rept(event):
    global pt
    print('從rept顯示的pt：', pt)
    line_bot_api.reply_message(
        event.reply_token,
        rep.get(event.postback.data)
    )



@handler.add(PostbackEvent)
def handle_post_message(event):
    global pt, reply_message_list1,Point
    print('觸發PostbackEvent：',event.postback.data, '此時pt:', pt)
    user_profile = line_bot_api.get_profile(event.source.user_id)
    

    rept(event)
    print('rept之後，pt:',pt)
   # 以下為李屍朝鮮降第一題
    if (event.postback.data.find('test1') != -1):
        print("test1")
        print('dictions["a1"]:',dictions["a1"])
        print(Point)
        if dictions["a1"] == 2:
            dictions["a1"] = 3
            pt = pt + 1

            Point=("累積獲得%d學分"%(pt)) #為何要先有這行???
            rep["action5"]=[TextSendMessage(text=Point)]



    # 以下為李屍朝鮮第二題
    elif (event.postback.data.find('test3') != -1):
        print('test3')
        if dictions["a2"] == 2:
            dictions["a2"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 以下為愛的迫降第一題
    elif (event.postback.data.find('test5') != -1):
        print('test5')
        if dictions["a3"] == 2:
            dictions["a3"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 以下為愛的迫降第二題
    elif (event.postback.data.find('test7') != -1):
        print('test7')
        if dictions["a4"] == 2:
            dictions["a4"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 想見你第一題
    elif (event.postback.data.find('test9') != -1):
        print('test9')
        if dictions["a5"] == 2:
            dictions["a5"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 想見你第二題
    elif (event.postback.data.find('test11') != -1):
        print('test11')
        if dictions["a6"] == 2:
            dictions["a6"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 戀愛第一題
    elif (event.postback.data.find('test13') != -1):
        print('test13')
        if dictions["a7"] == 2:
            dictions["a7"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]

    # 戀愛第二題
    elif (event.postback.data.find('test15') != -1):
        print('test15')
        if dictions["a8"] == 2:
            dictions["a8"] = 3
            pt = pt + 1
            Point = ("累積獲得%d學分" % (pt))  # 為何要先有這行???
            rep["action5"] = [TextSendMessage(text=Point)]


    else:
        pass
    print('離開PostbackEvent，此時pt:', pt)
    return pt, reply_message_list1

# In[ ]:


'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

'''
Application 運行（heroku版）
'''

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])




