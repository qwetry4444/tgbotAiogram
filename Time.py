import time
import datetime
# from DataBaseCreate import bot_DataBase

weekdaysRus = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

def switchWeekday(number):
    number = number % 7
    if number == 0:
        return "Monday"
    if number == 1:
        return "Tuesday"
    if number == 2:
        return "Wednesday"
    if number == 3:
        return "Thursday"
    if number == 4:
        return "Friday"
    if number == 5:
        return "Saturday"
    if number == 6:
        return "Sunday"

lTime = time.localtime()


def get_ch_zn():
    weekNumber = datetime.date(lTime[0], lTime[1], lTime[2]).isocalendar()[1]
    if weekNumber % 2 == 1:
        ch_zn = 'Числитель'
    elif weekNumber % 2 == 0:
        ch_zn = 'Знаменатель'
    return ch_zn


def convertMin(min):
    hour = min % 60
    min -= (hour * 60)
    return f"{hour}ч. {min}м."

hour = lTime[3]
min = lTime[4]

min += hour * 60

def tt_Time():
    lTime = time.localtime()
    hour = lTime[3]
    min = lTime[4]
    min += hour * 60
    if min < 450:
        return f"Сейчас пар нет.\nДо начала первой пары {(510 - min) // 60}ч. {min % 60}м."
    if 450 <= min < 510:
        return f"Сейчас пар нет.\nДо начала первой пары {510 - min}м."
    if 510 <= min <= 590:
        return f"Сейчас идет первая пара.\nДо перерыва {590 - min}м."
    if 590 < min < 600:
        return f"Сейчас идет перерыв.\nДо начала второй пары {600-min}м."
    if 600 <= min <= 680:
        return f"Сейчас идет вторая пара.\nДо перерыва {680 - min}м."
    if 680 < min < 690:
        return f"Сейчас идет перерыв.\nДо начала третьей пары {690 - min}м."
    if 690 <= min <= 770:
        return f"Сейчас идет третья пара.\nДо перерыва {770 - min}м."
    if 770 < min < 800:
        return f"Сейчас идет перерыв.\nДо начала четвертой пары {800 - min}м."
    if 800 <= min <= 880:
        return f"Сейчас идет четвертая пара.\nДо перерыва {880 - min}м."
    if 880 < min < 890:
        return f"Сейчас идет перерыв.\nДо начала пятой пары {890 - min}м."
    if 890 <= min <= 970:
        return f"Сейчас идет пятая пара.\nДо перерыва {970 - min}м."
    if 970 < min < 980:
        return f"Сейчас идет перерыв.\nДо начала шестой пары {980 - min}м."
    if 970 <= min <= 1050:
        return f"Сейчас идет шестая пара.\nДо перерыва {1050 - min}м."
    if 1050 < min < 1060:
        return f"Сейчас идет перерыв.\nДо начала седьмой пары {1060 - min}м."
    if 1060 <= min <= 1140:
        return f"Сейчас идет седьмая пара.\nДо перерыва {1140 - min}м."
    if 1140 < min < 1150:
        return f"Сейчас идет перерыв.\nДо начала восьмой пары {1150 - min}м."
    if 1150 <= min <= 1230:
        return f"Сейчас идет восьмая пара.\nДо перерыва {1230 - min}м."
    if min > 1230:
        return f"На сегодня пары закончились!\nДо начала первой пары {(1440 - min + 510) // 60}ч. {(1440 - min + 510) % 60}м."


# def uptime():
#     while True:
#         bot_DataBase.wakeup()
#         time.sleep(480)

