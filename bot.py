from requests import get
from re import findall
import os
import glob
from rubika import Bot
import requests
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import random
import urllib
import io

bot = Bot("zedhtbbycrofhyyjlloblimbztbzwrxn")
target = "g0CS6bm01fad226569c53de827d7c55a"

# created By Sajad & morteza

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "It is forbidden to put a link in the group"

	if coun == 1:
		bot.sendMessage(target, "🔹 Dear user, [ @"+user+" ] "+haslink+" \n  you have received (1/3) of the warning 🔹 .")
	elif coun == 2:
		bot.sendMessage(target, "🔹 Dear user, [ @"+user+" ] "+haslink+" \n  you have received (2/3) of the warning 🔹 .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 🔹 Dear user, [ @"+user+" ] \n you will be fired from the group for receiving (3) warnings 🔹 .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!stop" or msg.get("text") == "خاموش" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "✅  ᵀᴴᴱ ᴿᴼᴮᴼᵀ ᴵˢ ᴺᴼᵂ ᴼᶠᶠ", message_id=msg.get("message_id"))
							except:
								print("err off bot")
								
						elif msg.get("text") == "!restart" or msg.get("text") == "ریستارت" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "Restarting ...", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ᵀᴴᴱ ᴿᴼᴮᴼᵀ ᵂᴬˢ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴿᴱˢᵀᴬᴿᵀᴱᴰ!", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
								
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" ᴿᴱᶜᴱᴺᵀ ᴹᴱˢˢᴬᴳᴱ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴰᴱᴸᴱᵀᴱᴰ", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ ᴹᴱˢˢᴬᴳᴱ ᴰᴱᴸᴱᵀᴱᴰ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ ᴾᴸᴱᴬˢᴱ ᴱᴺᵀᴱᴿ ᵀᴴᴱ ᶜᴼᴹᴹᴬᴺᴰ ᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("بن") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ ᵀᴴᴱ ᵁˢᴱᴿ ᵂᴬˢ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴱˣᴾᴱᴸᴸᴱᴰ ᶠᴿᴼᴹ ᵀᴴᴱ ᴳᴿᴼᵁᴾ", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ ᵀᴴᴱ ᵁˢᴱᴿ ᴵˢ ᴬᴺ ᴬᴰᴹᴵᴺ", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ ᵀᴴᴱ ᵁˢᴱᴿ ᵂᴬˢ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴱˣᴾᴱᴸᴸᴱᴰ ᶠᴿᴼᴹ ᵀᴴᴱ ᴳᴿᴼᵁᴾ", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ ᵂᴿᴼᴺᴳ ᶜᴼᴹᴹᴬᴺᴰ", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ ᵁˢᴱᴿ ᴵˢ ᴸᴵᴹᴵᵀᴱᴰ", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ ᵁˢᴱᴿ ᴵˢ ᴸᴵᴹᴵᵀᴱᴰ", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "دستورات":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت دستورات") and msg.get("author_object_guid") in admins:
							try:
								rules = open("help.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "ᴿᴬᴮᴬᵀ ᴿᵁᴸᴱˢ ᴴᴬⱽᴱ ᴮᴱᴱᴺ ᵁᴾᴰᴬᵀᴱᴰ!", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "ᵀᴴᴱᴿᴱ ᵂᴬˢ ᴬ ᴾᴿᴼᴮᴸᴱᴹ, ᵀᴿᵞ ᴬᴳᴬᴵᴺ!", message_id=msg.get("message_id"))
								
						elif msg["text"].startswith("!number") or msg["text"].startswith("بشمار"):
							try:
								response = get(f"http://api.codebazan.ir/adad/?text={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("زمان"):
							try:
								response = get("https://api.codebazan.ir/time-date/?td=all").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
								
						elif msg.get("text") == "ساعت":
							try:
								bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))
							except:
								print("err time answer")
						
						elif msg.get("text") == "!date":
							try:
								bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))
							except:
								print("err date")
								
						elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ᴰᴱᴸᴱᵀᴱᴰ ...", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("!cal") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "ᵁᴺᶠᴼᴿᵀᵁᴺᴬᵀᴱᴸᵞ ᵞᴼᵁᴿ ᴼᴿᴰᴱᴿ ᴵˢ ᵂᴿᴼᴺᴳ!" ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
                                
						elif msg.get("text").startswith("اصل") or msg.get("text").startswith("اصل بده") or msg.get("text").startswith("اصل بشوت") or msg.get("text").startswith("اصل بد") or msg.get("text").startswith("اصل میدی") or msg.get("text").startswith("اصل میدی اشنا شیم"):
							try:
								bot.sendMessage(target,'بات الیاس هسم' ,message_id=msg.get("message_id"))
							except:
								print("err asll")

						elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "اره نفسم تو خوبی ؟", message_id=msg.get("message_id"))
							except:
								print("err khobi")
								
						elif msg.get("text").startswith("چه خبر") or msg.get("text").startswith("چخبر"):
							try:
								bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
							except:
								print("err CheKhabar")
                                
						elif msg.get("text").startswith("بیا پی") or msg.get("text").startswith("بیا پیوی"):
							try:
								bot.sendMessage(target, "حله", message_id=msg.get("message_id"))
							except:
								print("err biya pv")
                                
						elif msg.get("text").startswith("اها") or msg.get("text").startswith("عاها"):
							try:
								bot.sendMessage(target, "بعله", message_id=msg.get("message_id"))
							except:
								print("err kossheryek")
                                
		           
						elif msg.get("text").startswith("خبید") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "حله", message_id=msg.get("message_id"))
							except:
								print("err kossherpang")
                                
						elif msg.get("text").startswith("مرسی") or msg.get("text").startswith("مرس"):
							try:
								bot.sendMessage(target, "خواهش میکنم", message_id=msg.get("message_id"))
							except:
								print("err kosshershish")
                                
						elif msg.get("text").startswith("ممنون") or msg.get("text").startswith("خیلی ممنون"):
							try:
								bot.sendMessage(target, "Thankyou very much 😇", message_id=msg.get("message_id"))
							except:
								print("err kossherhaf")
                                
						elif msg.get("text").startswith("مرسی ممنون") or msg.get("text").startswith("ملسی"):
							try:
								bot.sendMessage(target, "جواب دادنت وظیفه بود😆", message_id=msg.get("message_id"))
							except:
								print("err kossherhash")
                                
						            
						elif msg.get("text").startswith("فعلا") or msg.get("text").startswith("فعلن"):
							try:
								bot.sendMessage(target, "بای بای", message_id=msg.get("message_id"))
							except:
								print("err sise")
                                
						elif msg.get("text").startswith("الیاس") or msg.get("text").startswith("الی"):
							try:
								bot.sendMessage(target, "جونم", message_id=msg.get("message_id"))
							except:
								print("err sichar")
                                
						
                                
						elif msg.get("text").startswith("🗿") or msg.get("text").startswith("🗿🗿"):
							try:
								bot.sendMessage(target, "مراپ و معرفت سید", message_id=msg.get("message_id"))
							except:
								print("err sihash")
                                
						
						elif msg.get("text").startswith("سلاپ") or msg.get("text").startswith("سلاپ"):
							try:
								bot.sendMessage(target, "سلام 😐", message_id=msg.get("message_id"))
							except:
								print("err chel")
                                
						elif msg.get("text").startswith("جیگرم") or msg.get("text").startswith("جیگر"):
							try:
								bot.sendMessage(target, "گمشو نبینمت😐بات قهرم", message_id=msg.get("message_id"))
							except:
								print("err celyek")
                                
						elif msg.get("text").startswith("😂❤") or msg.get("text").startswith("❤😂"):
							try:
								bot.sendMessage(target, "❤💋😛", message_id=msg.get("message_id"))
							except:
								print("err cheldo")
                                
						elif msg.get("text").startswith("😐💔") or msg.get("text").startswith("💔😐"):
							try:
								bot.sendMessage(target, "ها چته😐", message_id=msg.get("message_id"))
							except:
								print("err chelse")
                                
						elif msg.get("text").startswith("حاجی") or msg.get("text").startswith("حجی"):
							try:
								bot.sendMessage(target, "جان حاجی حاجی قربونت بره امر کن جیگر 😐", message_id=msg.get("message_id"))
							except:
								print("err chelchar")
                                
						elif msg.get("text").startswith("دعوا") or msg.get("text").startswith("دعوا باز"):
							try:
								bot.sendMessage(target, "هروز دعوا هس😂", message_id=msg.get("message_id"))
							except:
								print("err chelpang")
                                
						       
						elif msg.get("text").startswith("بات") or msg.get("text").startswith("بات"):
							try:
								bot.sendMessage(target, "بگو عزیزم🙂چیکارم داری دورت بگردم؟🙃💋", message_id=msg.get("message_id"))
							except:
								print("err chelnoh")
                                
						 
						elif msg.get("text").startswith("کوفت") or msg.get("text").startswith("کوفت"):
							try:
								bot.sendMessage(target, "ک= کل وجودم  و=واقعا  ف=فدای  ت=تو🥲💜", message_id=msg.get("message_id"))
							except:
								print("err pdo")
                                
						
						elif msg.get("text").startswith("💙") or msg.get("text").startswith("💙"):
							try:
								bot.sendMessage(target, "😉❤میدونم رفیقمی", message_id=msg.get("message_id"))
							except:
								print("err pchar")
                                
						elif msg.get("text").startswith("❤") or msg.get("text").startswith("❤"):
							try:
								bot.sendMessage(target, "میدونم عاشقمی🥺❤", message_id=msg.get("message_id"))
							except:
								print("err phaf")
                                
						                    
						elif msg.get("text").startswith("بوس بده") or msg.get("text").startswith("بوس"):
							try:
								bot.sendMessage(target, "💋💋🥰☺💋🫀", message_id=msg.get("message_id"))
							except:
								print("err shehash")
                                
						      
						elif msg.get("text").startswith("چایی") or msg.get("text").startswith("چای"):
							try:
								bot.sendMessage(target, "بفرما چایی😝☕️", message_id=msg.get("message_id"))
							except:
								print("err haftad")
                                
						     
						elif msg.get("text").startswith("ربات کیه") or msg.get("text").startswith("ربات کیه"):
							try:
								bot.sendMessage(target, "ربات الی جون", message_id=msg.get("message_id"))
							except:
								print("err hafch")
                                
						elif msg.get("text").startswith("سازندت کیه") or msg.get("text").startswith("سازنده"):
							try:
								bot.sendMessage(target, "@Elyas_rr2", message_id=msg.get("message_id"))
							except:
								print("err hafpang")
                                
						       
						elif msg.get("text").startswith("لینک") or msg.get("text").startswith("لینک گپ"):
							try:
								bot.sendMessage(target, "از مدیر گپ بگیر ", message_id=msg.get("message_id"))
							except:
								print("err hshch")
                                
						
		           
						elif msg.get("text").startswith("😕") or msg.get("text").startswith("😕"):
							try:
								bot.sendMessage(target, "خوبی؟", message_id=msg.get("message_id"))
							except:
								print("err nash")
                                
						             
						elif msg.get("text").startswith("هعی") or msg.get("text").startswith("هعپ"):
							try:
								bot.sendMessage(target, "درست میشه هر مشکلی هست نگران نباش😌❣", message_id=msg.get("message_id"))
							except:
								print("err nash")
                                
						        
						elif msg.get("text").startswith("عاشقتم") or msg.get("text").startswith("عاشقتم"):
							try:
								bot.sendMessage(target, "منم همینطور", message_id=msg.get("message_id"))
							except:
								print("err nano")
                                
						elif msg.get("text").startswith("حوصله ندارم") or msg.get("text").startswith("حصلم"):
							try:
								bot.sendMessage(target, "چرا؟", message_id=msg.get("message_id"))
							except:
								print("err sad")
                                
						
						elif msg.get("text") == "تست":
							try:
								bot.sendMessage(target, "ᵀᴴᴱ ᴿᴼᴮᴼᵀ ᴵˢ ᴺᴼᵂ ᴬᶜᵀᴵⱽᴱ ✅", message_id=msg.get("message_id"))
							except:
								print("err test bot")
								
						elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.pin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴾᴵᴺᴺᴱᴰ!", message_id=msg.get("message_id"))
							except:
								print("err pin")
								
						elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.unpin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ᴿᴱᴹᴼⱽᴱᴰ ᶠᴿᴼᴹ ᵀᴴᴱ ᴾᴵᴺ!", message_id=msg.get("message_id"))
							except:
								print("err unpin")
								
						elif msg.get("text").startswith("!trans"):
							try:
								responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
								al = [responser["result"]]
								bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴱᴺᵀᴱᴿ ᵀᴴᴱ ᶜᴼᴹᴹᴬᴺᴰ ᶜᴼᴿᴿᴱᶜᵀᴸᵞ 😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("!font"):
							try:
								response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
								bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴱᴺᵀᴱᴿ ᵀᴴᴱ ᶜᴼᴹᴹᴬᴺᴰ ᶜᴼᴿᴿᴱᶜᵀᴸᵞ 😁", message_id=msg["message_id"])
						
						elif msg.get("text").startswith("جوک") or msg.get("text").startswith("jok") or msg.get("text").startswith("!jok"):
							try:
								response = get("https://api.codebazan.ir/jok/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("ذکر") or msg.get("text").startswith("zekr") or msg.get("text").startswith("!zekr"):
							try:
								response = get("http://api.codebazan.ir/zekr/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("حدیث") or msg.get("text").startswith("hadis") or msg.get("text").startswith("!hadis"):
							try:
								response = get("http://api.codebazan.ir/hadis/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("بیو") or msg.get("text").startswith("bio") or msg.get("text").startswith("!bio"):
							try:
								response = get("https://api.codebazan.ir/bio/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg["text"].startswith("!weather"):
							try:
								response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("دیالوگ"):
							try:
								response = get("http://api.codebazan.ir/dialog/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("دانستنی"):
							try:
								response = get("http://api.codebazan.ir/danestani/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])
                                
						elif msg.get("text").startswith("همسر"):
							try:
								response = get("https://api.codebazan.ir/name/?type=json").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])	
								
						elif msg.get("text").startswith("پ ن پ") or msg.get("text").startswith("!pa-na-pa") or msg.get("text").startswith("په نه په"):
							try:
								response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("الکی مثلا") or msg.get("text").startswith("!alaki-masalan"):
							try:
								response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("داستان") or msg.get("text").startswith("!dastan"):
							try:
								response = get("http://api.codebazan.ir/dastan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("!ping"):
							try:
								responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
								
						elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
							
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "✅ Rules updated", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg.get("message_id"))

						elif msg.get("text") == "حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!speak" or msg.get("text") == "ویس" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'Your message has no text or caption',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "برداشتن حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ The user is an admin", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ The user is an admin", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ Please enter the command correctly", message_id=msg.get("message_id"))



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 The group was locked", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 The group is now open", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "!start" or msg.get("text") == "روشن" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "The robot was successfully lit!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"️ User {user} Successfully removed from the group.", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hi {user} Dear 😘🌹\n • Welcome to the {name} group 😍❤️\nPlease follow the rules.\n 💎 Send the word (rules) to see enough rules! ", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Bye {user} 👋 ", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Leave member Answer")
							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hi {user} Dear 😘🌹\n • Welcome to the {name} group 😍❤️\nPlease follow the rules.\n 💎 Send the word (rules) to see enough rules!", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
