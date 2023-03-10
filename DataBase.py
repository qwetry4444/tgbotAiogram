import sqlite3
import pymysql
from Time import weekdaysRus
from loader import bot, dp
import messages
import keyboards
import aiogram
from asyncpg import Connection, Record
from aiogram import types
import asyncio
import logging

class DataBase:
    def __init__(self, host, user, password, databaseName, charset, port):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=databaseName,
                                    charset=charset,
                                    port=port)

    # async def check_connect(self):
    #     try:
    #         await self.conn.cursor()
    #
    #     except Exception as ex:
    #         self.conn = await pymysql.connect(host=self.host,
    #                                     user=self.user,
    #                                     password=self.password,
    #                                     db=self.databaseName,
    #                                     charset=self.charset,
    #                                     port=self.port)
    USER_EXISTS = "SELECT EXISTS(SELECT id FROM student WHERE tg_id = $1"
    GET_USER_ID = "SELECT * FROM student WHERE tg_id = $1"
    GET_USER_NAME = "SELECT * FROM student WHERE tg_id = $1"
    GET_USER_GROUP = "SELECT * FROM student WHERE tg_id = $1"
    CHANGE_USER_GROUP = "UPDATE student SET group_number = $1 WHERE tg_id = $2"
    GET_TT_TOMORROW = "SELECT * FROM timetable WHERE group_number = $1 AND weekday = $2"
    GET_TT_TODAY = "SELECT * FROM timetable WHERE group_number = $1 AND weekday = $2 "
    GET_TT_WEEK = "SELECT * FROM timetable WHERE group_number = $1"
    GET_TT_LECTHER = "SELECT * FROM `timetable_lecturers` WHERE `lecturer_name` like $1"
    GET_TT = "SELECT * FROM timetable WHERE group_number = $1"
    GET_SUBJECTS = "SELECT * FROM timetable WHERE group_number = $1"
    ADD_USER = "INSERT INTO student (id, tg_id, user_name, group_number) VALUES ($1, $2, $3, $4)"

    async def user_exists(self, tg_id):
        with self.conn.cursor as cur:
            await cur.execute(f"SELECT EXISTS(SELECT id FROM student WHERE tg_id = {tg_id})")
            ans = await cur.fetchone()[0]
            print(ans)
            if await ans == 1:
                return True
            else:
                return False

    async def get_user_id(self, tg_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
            ans = cur.fetchone()[0]

            return ans

    async def get_user_name(self, tg_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
            ans = self.cur.fetchone()[2]

            return ans

    async def get_user_group(self, tg_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
            ans = cur.fetchone()[3]
            return ans


    # def confirm(self):
    #     print(message.text.lower())
    #     return message.text.lower() == '????'

    async def change_user_group(self, message, tg_id, group_number):
        with self.conn.cursor() as cur:
            cur.execute(f"""UPDATE student\
                            SET `group_number` = '{group_number}' \
                            WHERE `tg_id` = {tg_id}""")
            await bot.send_message(message.chat.id, f"{messages.GROUP_NUMBER_CHANGED}{group_number}", reply_markup=keyboards.start)

            return self.conn.commit()


    def get_tt_tomorrow(self, group_number, weekday):
        with self.conn.cursor() as cur:
            if weekday == "Sunday":
                return "???????????? ?????? ??????)"
            else:
                cur.execute(
                    f"""SELECT * FROM `timetable` WHERE `group_number` = "{group_number}" AND `weekday` = "{weekday}" """)
                ans = f"?????? ???????? ????????????????????\n{cur.fetchone()[3]}"
                return ans

    def get_tt_today(self, group_number, weekday):
        with self.conn.cursor() as cur:
            if weekday == "Sunday":
                return "?????????????? ?????? ??????)"
            else:
                cur.execute(
                    f"""SELECT * FROM `timetable` WHERE `group_number` = "{group_number}" AND `weekday` = "{weekday}" """)
                return f"?????? ???????? ????????????????????\n{cur.fetchone()[3]}"


    def get_tt_week(self, group_number):
        with self.conn.cursor() as cur:
            mes = '1'
            ind = 0
            cur.execute(f"""SELECT * FROM timetable WHERE group_number = "{group_number}" """)
            for weekday_ind in cur.fetchall():
                mes += f"{weekdaysRus[ind]}\n{weekday_ind[3]}\n\n"
                ind += 1
            return mes

    def get_tt_lecther(self, lecturer_name):
        with self.conn.cursor() as cur:
            temp_name = lecturer_name.text[::-1][::-1]
            last_name = temp_name.split()[0].lower()
            if last_name in messages.lecturers_lastnames or lecturer_name.text.lower() in messages.lecturers_names:

                tt_monday = "??????????????????????\n"
                tt_tuesday = "??????????????\n"
                tt_wednesday = "??????????\n"
                tt_thursday = "??????????????\n"
                tt_friday = "??????????????\n"
                tt_saturday = "??????????????\n"
                cur.execute(f"""SELECT * FROM `timetable_lecturers` WHERE `lecturer_name` like "%{lecturer_name.text}%" """)
                all = cur.fetchall()
                for ind in range(8):
                    tt_monday += f"{ind + 1} ???????? - {all[ind][3]} : {all[ind][4]}\n" * bool(all[ind][3])
                    tt_tuesday += f"{ind + 1} ???????? - {all[ind][5]} : {all[ind][6]}\n" * bool(all[ind][5])
                    tt_wednesday += f"{ind + 1} ???????? - {all[ind][7]} : {all[ind][8]}\n" * bool(all[ind][7])
                    tt_thursday += f"{ind + 1} ???????? - {all[ind][9]} : {all[ind][10]}\n" * bool(all[ind][9])
                    tt_friday += f"{ind + 1} ???????? - {all[ind][11]} : {all[ind][12]}\n" * bool(all[ind][11])
                    tt_saturday += f"{ind + 1} ???????? - {all[ind][13]} : {all[ind][14]}\n" * bool(all[ind][13])
                #print(tt_monday, tt_tuesday, tt_wednesday, tt_thursday, tt_friday, tt_saturday)

                ans = tt_monday + (((int(not (bool(tt_monday)))) * ' ?????? ??????') + '\n' + tt_tuesday + ((int(not (bool(tt_tuesday)))) * ' ?????? ??????') + '\n' +
                        tt_wednesday + ((int(not (bool(tt_wednesday)))) * ' ?????? ??????') + '\n' + tt_thursday + ((int(not (bool(tt_thursday))) * ' ?????? ??????')) + '\n' +
                        tt_friday + (int(not (bool(tt_friday))) * ' ?????? ??????') + '\n' + tt_saturday + ((int(not (bool(tt_saturday[8:])))) * ' ?????? ??????'))
                return ans


    async def get_tt(self, group_number):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM `timetable` WHERE `group_number`="{group_number}" """)


    async def get_subjects(self, group_number):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM `timetable` WHERE `group_number`="{group_number}" """)
            ans = []
            lec3 = set()
            for i in cur.fetchall():
                lec = i[3]
                lec = lec.split('??? ')[1:]
                lec1 = []
                for j in range(len(lec)):
                    lec1.append(lec[j].split(" - ")[1])
                for k in lec1:
                    lec3.add(k.split(',')[0])
            for m in lec3:
                ans.append(m)
            return ans

    async def add_user(self, id, tg_id, user_name, group_number):
        with self.conn.cursor() as cur:
            cur.execute(
                f"""INSERT INTO `student` (id, tg_id, user_name, group_number) VALUES (%d, %d,\'%s\', \'%s\');""" % (
                    id, tg_id, user_name, group_number,))
            return self.conn.commit()


    async def add_tt(self, id, group_number, weekday, timetable):
        with self.conn.cursor() as cur:
            cur.execute(f"""UPDATE timetable (id, group_number, weekday, timetable) VALUES (%d, \'%s\',
            \'%s\',\'%s\');""" % (id, group_number, weekday, timetable,))

            return self.conn.commit()

    async def wakeup(self):
        with self.conn.cursor() as cur:
            print("UUUP!")


