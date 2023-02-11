import sqlite3
import pymysql
from Time import weekdaysRus
from loader import bot, dp
import messages
import keyboards
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

    async def check_connect(self):
        try:
            await self.conn.cursor()

        except Exception as ex:
            self.conn = await pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db=self.databaseName,
                                        charset=self.charset,
                                        port=self.port)

    async def user_exists(self, tg_id):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"SELECT EXISTS(SELECT id FROM student WHERE tg_id = {tg_id})")
        ans = self.cur.fetchone()[0]
        await print(ans)
        await self.cur.close()
        if ans == 1:
            return True
        else:
            return False


    async def get_user_id(self, tg_id):
        await self.check_connect()
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
        ans = await self.cur.fetchone()[0]
        self.cur.close()
        return ans


    async def get_user_name(self, tg_id):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
        ans = await self.cur.fetchone()[2]
        await self.cur.close()
        return ans


    async def get_user_group(self, tg_id):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"SELECT * FROM student WHERE tg_id = {tg_id}")
        await self.cur.close()
        ans = await self.cur.fetchone()[3]
        return ans


    # def confirm(self):
    #     print(message.text.lower())
    #     return message.text.lower() == 'да'

    async def change_user_group(self, tg_id, group_number):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"""UPDATE student\
                        SET `group_number` = '{group_number}' \
                        WHERE `tg_id` = {tg_id}""")
        await self.cur.close()
        return self.conn.commit()


    async def get_tt_tomorrow(self, group_number, weekday):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        if weekday == "Sunday":
            await self.cur.close()
            return "Завтра пар нет)"
        else:
            await self.cur.execute(
                f"""SELECT * FROM `timetable` WHERE `group_number` = "{group_number}" AND `weekday` = "{weekday}" """)
            await self.cur.close()
            return f"Вот твое расписание\n{self.cur.fetchone()[3]}"

    async def get_tt_today(self, group_number, weekday):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        if weekday == "Sunday":
            await self.cur.close()
            return "Сегодня пар нет)"
        else:
            await self.cur.execute(
                f"""SELECT * FROM `timetable` WHERE `group_number` = "{group_number}" AND `weekday` = "{weekday}" """)
            await self.cur.close()
            return f"Вот твое расписание\n{self.cur.fetchone()[3]}"


    async def get_tt_week(self, group_number):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        mes = ''
        ind = 0
        await self.cur.execute(f"""SELECT * FROM timetable WHERE group_number = "{group_number}" """)
        for weekday_ind in self.cur.fetchall():
            mes += f"{weekdaysRus[ind]}\n{weekday_ind[3]}\n\n"
            ind += 1
        await self.cur.close()
        return mes

    async def get_tt_lecther(self, lecturer_name):
        if await lecturer_name.text == 'Назад':
            await lecturer_name.answer(lecturer_name.chat.id, messages.FUNCTION_MESSAGE.format(lecturer_name.from_user.id, bot.get_me()),
                             parse_mode='html', reply_markup=keyboards.functions)
        return 0

        self.cur = await self.conn.cursor()
        temp_name = lecturer_name.text[::-1][::-1]
        last_name = temp_name.split()[0].lower()
        if last_name in messages.lecturers_lastnames or lecturer_name.text.lower() in messages.lecturers_names:

            tt_monday = "Понедельник\n"
            tt_tuesday = "Вторник\n"
            tt_wednesday = "Среда\n"
            tt_thursday = "Четверг\n"
            tt_friday = "Пятница\n"
            tt_saturday = "Суббота\n"
            await self.cur.execute(f"""SELECT * FROM `timetable_lecturers` WHERE `lecturer_name` like "%{lecturer_name.text}%" """)
            all = await self.cur.fetchall()
            for ind in range(8):
                tt_monday += f"{ind + 1} пара - {all[ind][3]} : {all[ind][4]}\n" * bool(all[ind][3])
                tt_tuesday += f"{ind + 1} пара - {all[ind][5]} : {all[ind][6]}\n" * bool(all[ind][5])
                tt_wednesday += f"{ind + 1} пара - {all[ind][7]} : {all[ind][8]}\n" * bool(all[ind][7])
                tt_thursday += f"{ind + 1} пара - {all[ind][9]} : {all[ind][10]}\n" * bool(all[ind][9])
                tt_friday += f"{ind + 1} пара - {all[ind][11]} : {all[ind][12]}\n" * bool(all[ind][11])
                tt_saturday += f"{ind + 1} пара - {all[ind][13]} : {all[ind][14]}\n" * bool(all[ind][13])
            #print(tt_monday, tt_tuesday, tt_wednesday, tt_thursday, tt_friday, tt_saturday)

            ans = tt_monday + (((int(not (bool(tt_monday)))) * ' Пар нет') + '\n' + tt_tuesday + ((int(not (bool(tt_tuesday)))) * ' Пар нет') + '\n' +
                    tt_wednesday + ((int(not (bool(tt_wednesday)))) * ' Пар нет') + '\n' + tt_thursday + ((int(not (bool(tt_thursday))) * ' Пар нет')) + '\n' +
                    tt_friday + (int(not (bool(tt_friday))) * ' Пар нет') + '\n' + tt_saturday + ((int(not (bool(tt_saturday[8:])))) * ' Пар нет'))
            await bot.send_message(lecturer_name.chat.id, ans, reply_markup=keyboards.markupFunc)
            await self.cur.close()
            return tt_monday
        else:
            await self.cur.close()
            if lecturer_name != 'Отменить':
                msg = await bot.send_message(lecturer_name.chat.id, "Проверьте правильность ввода")
                await bot.register_next_step_handler(msg, self.get_tt_lecther)

    async def get_tt(self, group_number):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"""SELECT * FROM `timetable` WHERE `group_number`="{group_number}" """)
        await self.cur.close()

    async def get_subjects(self, group_number):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"""SELECT * FROM `timetable` WHERE `group_number`="{group_number}" """)
        ans = []
        lec3 = set()
        for i in await self.cur.fetchall():
            lec = i[3]
            lec = lec.split('• ')[1:]
            lec1 = []
            for j in range(len(lec)):
                lec1.append(lec[j].split(" - ")[1])
            for k in lec1:
                lec3.add(k.split(',')[0])

        for m in lec3:
            ans.append(m)
        return ans

    async def add_user(self, id, tg_id, user_name, group_number):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(
            f"""INSERT INTO `student` (id, tg_id, user_name, group_number) VALUES (%d, %d,\'%s\', \'%s\');""" % (
                id, tg_id, user_name, group_number,))
        await self.cur.close()
        return self.conn.commit()


    async def add_tt(self, id, group_number, weekday, timetable):
        await self.check_connect()
        self.cur = await self.conn.cursor()
        await self.cur.execute(f"""UPDATE timetable (id, group_number, weekday, timetable) VALUES (%d, \'%s\',
        \'%s\',\'%s\');""" % (id, group_number, weekday, timetable,))
        await self.cur.close()
        return self.conn.commit()

    async def wakeup(self):

        #await self.check_connect()

        self.cur = await self.conn.cursor()
        await print("UUUP!")
        await self.cur.close()


    async def db_close(self):
        await self.conn.close()


