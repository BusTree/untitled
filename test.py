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
# season_xpath = ['10','9','8','7','6','5','4','3','2','1'] # 10노말 9 = 시즌1~   1 = 시즌9
season_xpath = ['10','9','8','7','6','5','4','3','2','1'] # 10노말 9 = 시즌1~   1 = 시즌9
season_page = ['normal','season-1','season-2','season-3','season-4','season-5','season-6','season-7','season-11','season-13'] # 시즌 api
season_str = ['normal','1','2','3','4','5','6','7','8','9']

season = []
game_win = []
game_lose = []
winsum = 0
losesum = 0
valuesum = 0
season_win =[]
season_lose = []
season_value =[]
num = 0
final =0
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
        if value:
            num = int(re.findall('\d+', value.text)[0])
            valuesum += num
    season_value.append(valuesum)
    valuesum =0



print(season_win)
print(season_lose)


print('')

for idx, value in enumerate(season_str):
    season_value[idx] += season_win[idx] + season_lose[idx]
    print(str(season_str[idx]) + " : " + str(season_value[idx]) + '판')
    final += season_value[idx]

for idx, value in enumerate(season_str):
    if value == "4":
        season_value[idx] += season_win[idx] + season_lose[idx]
        season_win[idx] =0
        season_lose[idx] = 0

print("전체 게임수 : "+str(final))
plt.bar(season_str,season_value, color="#47C83E", bottom=0, width=0.5)
plt.bar(season_str,season_lose, color="#F15F5F", bottom=0, width=0.5)
plt.bar(season_str,season_win, color="#6799FF", bottom=season_lose, width=0.5)
plt.title("Play Count")
# plt.plot(season_str, season_value)
plt.show()