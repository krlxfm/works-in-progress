import sys
import csv

# Format:
# name,startDate,startTime,endDate,endTime,login,password

login_dict = {}

reader = csv.reader(sys.stdin)
for row in reader:
    login = row[5]
    if login not in login_dict:
        login_dict[login] = []
    login_dict[login].append(','.join(row))

for login in login_dict:
    if len(login_dict[login]) > 1:
        print(f'\nLogin: {login}\nShows:')
        for entry in login_dict[login]:
            print(entry)

