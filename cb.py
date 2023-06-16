from aiogram import Bot, Dispatcher, executor, types
from config_reader import config



bot=Bot(token=config.bot_token.get_secret_value())

dp=Dispatcher(bot)

def readFileOrCreateNew(fileName):
    try:
        rfile=open(fileName,'r')
    except IOError:
        rfile=open(fileName,'w')
        rfile.close()
        rfile=open(fileName,'r')
    lines = [line.strip() for line in rfile]
    rfile.close
    return lines


lines            =readFileOrCreateNew('chatID.txt')           #read list of chats
admins           =readFileOrCreateNew('adminsID.txt')         #read list of active admin
adminsNew        =readFileOrCreateNew('adminsNewID.txt')      #read list of admins applicant
applicantNew     =readFileOrCreateNew('newApplicantID.txt')   #read list of new job applicant

ADMIN_MENU=".\nМожешь добавлять меня в любые группы.\nПо команде /sendall отправлю сообщение во все группы в которые был добавлен ранее.\n /updatenews обновит новость для рассылки. Формат: \n/updatenews Какая-то новость\n/shownews покажет текущую сохраненную новость.\n/showApplicants покажет список желающих поджобать, а /clearApplicants очистит его, будь внимателен."
WORKER_MENU=".\nХочешь работать у нас? Жми /wantjob и наш менеджер свяжется с тобой!"

#read string with news message
try:
    news_file=open('chatNews.txt','r', encoding="utf-8")
except IOError:
    news_file=open('chatNews.txt','w', encoding="utf-8")
    news_file.write("Какие-то новости для группы\nОбновить можно через бот и его команду /updatenews.")
    news_file.close()
    news_file=open('chatNews.txt','r', encoding="utf-8")
news=news_file.read()
news_file.close


def NotElInArr(arr,ell):
    for cEl in arr:
        if str(cEl) == str(ell):
            return(False)
    return(True)


def addChatID(newID):
    db_file=open('chatID.txt','w')
    if NotElInArr(lines,newID):
        lines.append(newID)
    for lineEl in lines:
        db_file.write(str(lineEl)+"\n")
    db_file.close()

def addAdminNewID(newAdminID):
    adminsNew_file=open('adminsNewID.txt','w')
    if NotElInArr(adminsNew,newAdminID):
        adminsNew.append(newAdminID)
    for lineEl in adminsNew:
        adminsNew_file.write(str(lineEl)+"\n")
    adminsNew_file.close()


def addApplicationNewID(newApplicationID):
    applicantNew_file=open('newApplicantID.txt','w')
    if NotElInArr(applicantNew,newApplicationID):
        applicantNew.append(newApplicationID)
    for lineEl in applicantNew:
        applicantNew_file.write(str(lineEl)+"\n")
    applicantNew_file.close()


def clearApplicantsFN():
    applicantNew_file=open('newApplicantID.txt','w')
    #applicantNew_file.write("")
    applicantNew_file.close()
    global applicantNew
    applicantNew.clear()



def updateNews(newNews):
    news_file=open('chatNews.txt','w', encoding="utf-8")
    news_file.write(newNews)
    news_file.close()



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if NotElInArr(admins,message.from_user.id) == False:
            await bot.send_message(message.from_user.id,"Приветы, "+message.from_user.full_name+ADMIN_MENU)
        else:
            await bot.send_message(message.from_user.id,"Привет, "+message.from_user.full_name+WORKER_MENU)


@dp.message_handler(commands=['updatenews'])
async def updatenews(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False):
        text=message.text[12:]
        if text!="":
            print("News updated.")
            updateNews(text)
            global news
            news=text
            await message.reply("Новость успешно изменена на: "+news)
        else:
            await message.reply("Новость не может быть пустой. Пример команды: \n/updatenews Какая-то новость.")

@dp.message_handler(commands=['shownews'])
async def shownews(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False):
        await bot.send_message(message.from_user.id,news)
        await bot.send_message(message.from_user.id,message.from_user.full_name+ADMIN_MENU)



@dp.message_handler(commands=['clearApplicants'])
async def clearApplicants(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False):
        clearApplicantsFN()
        await bot.send_message(message.from_user.id,"Список пуст.")
        await bot.send_message(message.from_user.id,message.from_user.full_name+ADMIN_MENU)




@dp.message_handler(commands=['showApplicants'])
async def showApplicants(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False):
        rep=""
        for applicant in applicantNew:
            rep=rep+"\n"+str(applicant)
        await bot.send_message(message.from_user.id,rep)
        await bot.send_message(message.from_user.id,message.from_user.full_name+ADMIN_MENU)


@dp.message_handler(commands=['viewgroups'])
async def viewgroups(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False):
        rep=""
        for group in lines:
            rep=rep+"\ntg://group?id="+str(group)
        await bot.send_message(message.from_user.id,rep)
        await bot.send_message(message.from_user.id,message.from_user.full_name+ADMIN_MENU)





@dp.message_handler(commands=['godmode'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        text=message.text[9:]
        if text=="123":
            print("Someone whant to be a god:"+str(message.from_user.id))
            addAdminNewID(message.from_user.id)


@dp.message_handler(commands=['wantjob'])
async def start(message: types.Message):
    if message.chat.type == 'private':
            #addApplicationNewID(message.from_user.url)
            addApplicationNewID(message.from_user.mention)
            await bot.send_message(message.from_user.id,"Спасибо за заявку, "+message.from_user.full_name+". Наш менеджер свяжется с вами в ближайшее время.")
            await bot.send_message(message.from_user.id,message.from_user.full_name+WORKER_MENU)





@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:
            await message.reply("Спасибо за добавление в группу.\nБуду иногда присылать инофрмацию.")
            print("Edded in new group:"+str(message.chat.id))
            addChatID(message.chat.id)
            
            
@dp.message_handler(commands=['sendall'])
async def start(message: types.Message):
    if (message.chat.type == 'private' and NotElInArr(admins,message.from_user.id) == False ):
        for lineEl in lines:
            await bot.send_message(lineEl,news)
            await bot.send_message(message.from_user.id,message.from_user.full_name+ADMIN_MENU)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
