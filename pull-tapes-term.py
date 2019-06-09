import os
import sys
from datetime import *

def parse_time(input_time):
    time_list = input_time.split(':')
    time = 0
    pm = False
    for chunk in time_list:
        for character in chunk:
            if character.isdigit() == False:
                if character.lower() == 'p':
                    pm = True
    for i in range(len(time_list)):
        chunk = time_list[i]
        if len(chunk) <= 2:
            numbers = chunk
        else:
            numbers = ''
            for character in chunk:
                if character.isdigit() == True:
                    numbers = numbers + character
                else:
                    if character.lower() == 'a':
                        time += 0
                    if character.lower() == 'p':
                        time += 1200
        if len(numbers) <= 2:
            if i == 0:
                time += int(numbers)*100
                if int(numbers) == 12 and pm == False:
                    time -= int(numbers)*100
            else:
                time += int(numbers)
        else:
            time += int(numbers)
    return time

def main(name, term, year, day_of_week, showstart, showend):
    termID = year[-2:] + term[0].upper()
    os.system('rm -r {0}_{1}*'.format(name, termID))
    os.system('mkdir {0}_{1}'.format(name, termID))
    os.system('mkdir ./{0}_{1}/raw-audio'.format(name, termID))

    term_dict = {'F':9, 'W':1, 'S':4}
    day_dict = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}

    term = term[0].upper()
    year = '20' + year[-2:]
    month = term_dict[term]
    day = day_of_week[:3].lower()
    weekday = day_dict[day]

    start_time = parse_time(str(showstart))
    start_hour = start_time // 100
    start_minute = start_time % 100

    end_time = parse_time(str(showend))
    end_hour = end_time // 100
    end_minute = end_time % 100

    date_wrap = False
    if start_time > end_time:
        date_wrap = True
    
    dt = datetime(int(year), month, 1, start_hour, start_minute)
    while dt.weekday() != weekday:
        dt += timedelta(days=1)
    
    for i in range(13):
        times = []
        start_dt = datetime(dt.year, dt.month, dt.day, start_hour, start_minute)
        end_dt = datetime(dt.year, dt.month, dt.day, end_hour, end_minute)
        if date_wrap:
            end_dt += timedelta(days=1)
        while start_dt < end_dt:
            times.append(datetime(start_dt.year, start_dt.month, start_dt.day, start_dt.hour, start_dt.minute))
            start_dt += timedelta(seconds=1800)
    
        ffmpeg_string = '"concat:'
        for tape in times:
            year = tape.year
            month = tape.month
            day = tape.day
            time = tape.hour*100 + tape.minute
            os.system('scp krlxdj@garnet.krlx.org:/Volumes/Sapphire/recordings/{0}-{1:02}-{2:02}_{3:04}*.mp3 ./{4}_{5}/raw-audio/{0}-{1:02}-{2:02}_{3:04}.mp3'.format(year, month, day, time, name, termID))
            ffmpeg_string = ffmpeg_string + '{4}_{5}/raw-audio/{0}-{1:02}-{2:02}_{3:04}.mp3|'.format(year, month, day, time, name, termID)
        
        ffmpeg_string = ffmpeg_string.rstrip('|') + '"'
        os.system('ffmpeg -i {0} -acodec copy {1}_{5}/{1}_{2}-{3:02}-{4:02}.mp3'.format(ffmpeg_string, name, dt.year, dt.month, dt.day, termID))

        dt += timedelta(days=7)

    os.system('rm -r {0}_{1}/raw-audio'.format(name, termID))
    os.system('zip -r {0}_{1}.zip {0}_{1}'.format(name, termID))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python3 {} showName Term(F/W/S) Year DayOfWeek(Mon/Tue/...) showStartTime showEndTime'.format(sys.argv[0]))
        quit()
    name = sys.argv[1]
    term = sys.argv[2]
    year = sys.argv[3]
    day_of_week = sys.argv[4]
    showstart = sys.argv[5]
    showend = sys.argv[6]
    if len(sys.argv) > 7:
        print('Usage: python3 {} showName Term(F/W/S) Year DayOfWeek(Mon/Tue/...) showStartTime showEndTime'.format(sys.argv[0]))
        quit()
    main(name, term, year, day_of_week, showstart, showend)
