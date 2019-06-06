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

def main(name, startyear, startmonth, startday, showstart, showend, weeks=1):
    os.system('rm -r {0}*'.format(name))
    os.system('mkdir {}'.format(name))
    os.system('mkdir ./{0}/raw-audio'.format(name))

    year = '20' + startyear[-2:]
    month = int(startmonth)
    day = int(startday)

    start_time = parse_time(str(showstart))
    start_hour = start_time // 100
    start_minute = start_time % 100

    end_time = parse_time(str(showend))
    end_hour = end_time // 100
    end_minute = end_time % 100

    weeks = int(weeks)

    date_wrap = False
    if start_time > end_time:
        date_wrap = True
    
    dt = datetime(int(year), month, day, start_hour, start_minute)
    
    for i in range(weeks):
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
            os.system('scp krlxdj@garnet.krlx.org:/Volumes/Sapphire/recordings/{0}-{1:02}-{2:02}_{3:04}*.mp3 ./{4}/raw-audio/{0}-{1:02}-{2:02}_{3:04}.mp3'.format(year, month, day, time, name))
            ffmpeg_string = ffmpeg_string + '{4}/raw-audio/{0}-{1:02}-{2:02}_{3:04}.mp3|'.format(year, month, day, time, name)
        
        ffmpeg_string = ffmpeg_string.rstrip('|') + '"'
        os.system('ffmpeg -i {0} -acodec copy {1}/{1}_{2}-{3:02}-{4:02}.mp3'.format(ffmpeg_string, name, dt.year, dt.month, dt.day))

        dt += timedelta(days=7)

    os.system('rm -r {0}/raw-audio'.format(name))
    os.system('zip -r {0}.zip {0}'.format(name))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python3 {} showName startYear startMonth startDay showStartTime showEndTime [NumberOfWeeks]'.format(sys.argv[0]))
        quit()
    name = sys.argv[1]
    year = sys.argv[2]
    startmonth = sys.argv[3]
    startday = sys.argv[4]
    showstart = sys.argv[5]
    showend = sys.argv[6]
    if len(sys.argv) == 8:
        weeks = sys.argv[7]
    else:
        weeks = 1
    if len(sys.argv) > 8:
        print('Usage: python3 {} showName startYear startMonth startDay showStartTime showEndTime [NumberOfWeeks]'.format(sys.argv[0]))
        quit()
    main(name, year, startmonth, startday, showstart, showend, weeks)
