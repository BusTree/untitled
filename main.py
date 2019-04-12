from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import matplotlib.pylab as plt
import numpy as np

## python파일의 위치
driver = webdriver.Chrome('C:\chromedriver/chromedriver')
driver.implicitly_wait(3)
driver.get('https://www.op.gg/summoner/champions/userName=KOR%20Cow')
season_xpath = ['8','7','6','5','4','3','2','1'] # 10노말 9 = 시즌1~   1 = 시즌9
season_page = ['season-2','season-3','season-4','season-5','season-6','season-7','season-11','season-13'] # 시즌 api
season_str = ['2','3','4','5','6','7','8','9']

season = []
game_win = []
game_lose = []
winsum = 0
losesum = 0
valuesum = 0
killsum =0
deathsum =0
assistsum =0
cssum =0
kdasum = 0
sortedsum =0
num = 0
final =0
final_kda =0


season_win =[]
season_lose = []
season_value =[]
season_kill = []
season_Death = []
season_Assist =[]
season_cs = []
season_kda =[]
season_sorted =[]
season_rate = []

# 전적조회
for path in season_xpath:
    el = driver.find_elements_by_xpath('//*[@id="SummonerLayoutContent"]/div[3]/div/div/div[1]/ul/li[' + path + ']/a')
    el[0].click()
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    season.append(soup)

for idx, selectSeason in enumerate(season):
    page = selectSeason.find('div', {'class':'tabItem '+season_page[idx]})
    winCount = page.find_all('div', {'class': 'Text Left'})
    loseCount = page.find_all('div', {'class': 'Text Right'})
    valueCount = page.find_all('div', {'class': 'Value'})
    killCount = page.find_all('span', {'class': 'Kill'})
    DeathCount = page.find_all('span', {'class': 'Death'})
    AssistCount = page.find_all('span', {'class': 'Assist'})
    # csCount = page.find_all('td', {'class': 'Value Cell'})
    sortedCount = page.find_all('td', {'class': 'Value Cell sorted'})

    for win in winCount:
        if win.text:
            num = int(re.findall('\d+', win.text)[0])
            winsum += num
    season_win.append(winsum)
    winsum = 0

    for lose in loseCount:
        if lose.text:
            num = int(re.findall('\d+', lose.text)[0])
            losesum += num
    season_lose.append(losesum)
    losesum = 0

    for value in valueCount:
        if value.text:
            num = int(re.findall('\d+', value.text)[0])
            valuesum += num
    season_value.append(valuesum)
    valuesum =0

    for kill in killCount:
        if kill.text:
            num = float(re.findall('\d+', kill.text)[0])
            killsum += num
    season_kill.append(killsum)
    killsum =0

    for death in DeathCount:
        if death.text:
            num = float(re.findall('\d+', death.text)[0])
            deathsum += num
    season_Death.append(deathsum)
    deathsum = 0

    for assist in AssistCount:
        if assist.text:
            num = float(re.findall('\d+', assist.text)[0])
            assistsum += num
    season_Assist.append(assistsum)
    assistsum = 0

    for sorted in sortedCount:
        if sorted.text:
            sorted = sorted.replace(',', '').strip()
            num = int(re.findall('\d+', sorted.text)[0])
            sortedsum += num
    season_sorted.append(sortedsum)
    sortedsum = 0



for idx, value in enumerate(season_kill):

    if season_Death[idx] != 0:
        num = (season_kill[idx] + season_Assist[idx]) / season_Death[idx]
        season_kda.append(num)
    else :
        season_kda.append(0)

    if season_value[idx] != 0 :
        season_rate.append(season_win[idx] / season_value[idx] * 100)
        season_rate.append(0)



#    print(str(season_str[idx]) +" : "+str(season_kda[idx]))


for idx, value in enumerate(season_str):
    season_value[idx] += season_win[idx] + season_lose[idx]
   # print(str(season_str[idx]) + " : " + str(season_value[idx]) + '판')

    # print(str(season_str[idx]) +" : "+str(season_kda[idx]))



    final += season_value[idx]
    final_kda += (round(season_kda[idx],1))/8
 #   print(str(season_str[idx])+' : kda = '+str(round(season_kda[idx],1)))
    print(season_rate[idx])






for idx, value in enumerate(season_str):
    if value == "4":
        season_value[idx] += season_win[idx] + season_lose[idx]
        season_win[idx] =0
        season_lose[idx] = 0



print("전체 게임수 : "+str(final))
print('전체시즌 평균 kda :   '+str(final_kda))
plt.bar(season_str,season_value, color="#47C83E", bottom=0, width=0.5)
plt.bar(season_str,season_lose, color="#F15F5F", bottom=0, width=0.5)
plt.bar(season_str,season_win, color="#6799FF", bottom=season_lose, width=0.5)
plt.title("Play Count")
# plt.plot(season_str, season_value)
plt.show()
