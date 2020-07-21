from bs4 import BeautifulSoup
import urllib.request
import time
import requests
import math

# url = urllib.request.urlopen("https://www.bsu.edu.ru/bsu/resource/schedule/groups/index.php?group=12001811")
url = 'https://www.bsu.edu.ru/bsu/resource/schedule/groups/show_schedule.php'
week = '0203202008032020'
week_int = int(week)
# soup = bs4.BeautifulSoup(url, 'lxml')
payload = {
    'group': 12001811,
    'week': int('2906202005072020')
}
s = requests.Session()
s.get(url)
r = s.post(url='https://www.bsu.edu.ru/bsu/resource/schedule/groups/show_schedule.php',
           data=payload,
           headers={'X-Requested-With': 'XMLHttpRequest'}
           )
sc = BeautifulSoup(r.text, 'lxml').prettify()
sc = BeautifulSoup(sc, 'lxml')
# print(sc)


schedule = sc.find(id='shedule')
# time = schedule.find_all(id='time').get_text()
# print(time)

time_list = [time_el.get_text(strip=True) for time_el in schedule.find_all(id='time')]
num_list = [num_el.get_text(strip=True).replace('пара', ' пара') for num_el in schedule.find_all(id='num')]
auditions = [audition.get_text(strip=True).replace(',', ' ') for audition in schedule.find_all(id='aud')]

dates = []
for date_el in schedule.find_all(class_='colspan'):
    date_el = date_el.get_text(strip=True)
    date_el_substring = date_el.split()
    date_el = date_el_substring[1] + ' ' + date_el_substring[0]
    dates.append(date_el)


lessons_sublist = [lesson_type_el.get_text(strip=True) for lesson_type_el in schedule.find_all(id='lesson')]

lessons = []
for i in range(0, len(lessons_sublist), 2):
    lessons.append(lessons_sublist[i] + ' ' + lessons_sublist[i + 1])


teachers = []
for teachers_el in schedule.find_all(id='teacher'):
    teachers_el = teachers_el.get_text(strip=True)
    teachers_el_substring = teachers_el.split('.')
    teachers.append(teachers_el_substring[1])


print(time_list)
print(num_list)
print(dates)
print(lessons)
print(teachers)
print(auditions)

def compileMessage(date, time, lesson, audition, teacher):
    for item in range(len(date)):
        print(date[item] +  ':' + '\n' + time[item] + '. ' + lesson[item] + '. ' + audition[item] + '. ' + teacher[item] + '.')
print(compileMessage(dates, time_list, lessons, auditions, teachers))