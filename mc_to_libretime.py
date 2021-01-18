import os
import sys
import datetime
import csv
import mysql.connector as mysql
import random

from data_krlx_org_credentials import USER, PASSWORD

HOST = 'data.krlx.org'
DATABASE = 'krlx_missioncontrol'

WEEKDAY_DICT = {
        'monday':       0,
        'tuesday':      1,
        'wednesday':    2,
        'thursday':     3,
        'friday':       4,
        'saturday':     5,
        'sunday':       6}

def get_term_id(show_id):
    term_id = ''
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"SELECT shows.term_id FROM shows WHERE shows.id='{show_id}'")
    rows = cursor.fetchall()
    for row in rows:
        term_id = row[0]
    cursor.close()
    conn.close()
    return term_id

def get_on_air_date(term_id):
    on_air = ''
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"SELECT terms.on_air FROM terms WHERE terms.id='{term_id}'")
    rows = cursor.fetchall()
    for row in rows:
        on_air = row[0]
    cursor.close()
    conn.close()
    return on_air

def get_show_dict(term_id):
    show_dict = {}

    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"SELECT shows.id, users.name, users.email FROM users, show_user, shows WHERE shows.term_id='{term_id}' AND show_user.show_id=shows.id AND users.id=show_user.user_id")
    rows = cursor.fetchall()

    for row in rows:
        id, user, email = row
        if id not in show_dict:
            show_dict[id] = {'users': [], 'emails': []}
        show_dict[id]['users'].append(user)
        show_dict[id]['emails'].append(email)

    cursor.close()
    conn.close()
    return show_dict

def get_djs_from_id(show_id):
    users = []
    emails = []

    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"SELECT users.name, users.email FROM users, show_user WHERE show_user.show_id='{show_id}' AND users.id=show_user.user_id")
    rows = cursor.fetchall()

    for row in rows:
        users.append(row[0])
        emails.append(row[1])

    cursor.close()
    conn.close()
    return users, emails

def get_start_date(on_air, weekday):
    difference = WEEKDAY_DICT[weekday.lower()] - on_air.weekday() % 7
    return on_air.date() + datetime.timedelta(days=difference)

def invalid_term_id(term_id):
    print('ERROR: invalid term ID. Must be of the form 2021-WI, 2019-FA, 2018-SP.', file=sys.stderr)
    exit(2)

def check_argv():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print(f'ERROR: File not found: {sys.argv[0]}', file=sys.stderr)
        exit(1)

def main():
    check_argv()

    '''
    term_id = input('Please input term ID (of the form 2021-WI, 2019-FA, 2018-SP): ')
    components = term_id.split('-')
    if len(components) != 2:
        invalid_term_id(term_id)
    elif len(components[0]) != 4 and not components[0].isnumeric():
        invalid_term_id(term_id)
    elif components[1] not in ['FA', 'WI', 'SP']:
        invalid_term_id(term_id)
    on_air = get_on_air_date(term_id)
    '''

    on_air = None
    show_dict = None

    out_list = []

    with open(sys.argv[1]) as infile:
        reader = csv.reader(infile)
        for row in reader:
            # format given:
            # id,title,djs,day,start,end,flags
            # eventually want:
            # name,startDate,startTime,endDate,endTime,login,password
            if 'id' in row and 'title' in row:
                continue    # this is probably the header

            id, title, djs, day, start, end, flags = row

            if on_air == None:
                term_id = get_term_id(id)
                on_air = get_on_air_date(term_id)
                show_dict = get_show_dict(term_id)

            if not (day and start and end):
                continue    # show not assigned a time

            name = title
            startDate = get_start_date(on_air, day.lower())
            startTime = start
            endDate = startDate if end > start else startDate + datetime.timedelta(days=1)
            endTime = end
            login = show_dict[id]['emails'][0].split('@')[0]
            password = '{:08}'.format(random.randrange(0, 100000000))

            out_list.append([name, startDate, startTime, endDate, endTime, login, password])

    writer = csv.writer(sys.stdout)
    header = ['name', 'startDate', 'startTime', 'endDate', 'endTime', 'login', 'password']
    writer.writerow(header)
    for row in out_list:
        writer.writerow(row)


if __name__ == '__main__':
    main()

