import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import datetime
import re
import time
from datetime import date


filename="NBADiamondMine.csv"
f=open(filename,"w")
headers="#, Date, Away Team, 1Q, 2Q, 3Q, 4Q, Total, Home Team, 1Q, 2Q, 3Q, 4Q, Total, Game Total, Over/Under, Result, Favorite, Spread, Home Pts/G, Home Opp Pts/G, Home SRS, Home Pace, Home Off Rat, Home Def Rat, Away Pts/G, Away Opp Pts/G, Away SRS, Away Pace, Away Off Rat, Away Def Rat\n"
f.write(headers)

teamList=list(range(0,30))
teamList[0]="ATL"
teamList[1]="BOS"
teamList[2]="BRK"
teamList[3]="CHI"
teamList[4]="CHO"
teamList[5]="CLE"
teamList[6]="DAL"
teamList[7]="DEN"
teamList[8]="DET"
teamList[9]="GSW"
teamList[10]="HOU"
teamList[11]="IND"
teamList[12]="LAC"
teamList[13]="LAL"
teamList[14]="MEM"
teamList[15]="MIA"
teamList[16]="MIL"
teamList[17]="MIN"
teamList[18]="NOP"
teamList[19]="NYK"
teamList[20]="OKC"
teamList[21]="ORL"
teamList[22]="PHI"
teamList[23]="PHO"
teamList[24]="POR"
teamList[25]="SAC"
teamList[26]="SAS"
teamList[27]="TOR"
teamList[28]="UTA"
teamList[29]="WAS"

df=pd.DataFrame(columns=["Team", "Pts/Game","Opp Pts/Game", "SRS", "Pace", "Off Rating", "Def Rating"])
i=0

print("Pumping Basketballs")


for team in teamList:
    statsURL="https://www.basketball-reference.com/teams/"+str(team)+"/2018.html"
    uClient2=uReq(statsURL)
    stats_html=uClient2.read()
    uClient2.close()
    statsSoup=soup(stats_html, "html.parser")
    listofStats=statsSoup.findAll("p")
    ptsGame=listofStats[7].text.split(" ")[7]
    oppPts=listofStats[7].text.split(" ")[24]
    SRS=listofStats[8].text.split(" ")[1]
    pace=listofStats[8].text.split(" ")[17]
    offRating=listofStats[9].text.split(" ")[2]
    defRating=listofStats[9].text.split(" ")[13]
    df.loc[i]=[team, ptsGame, oppPts, SRS, pace, offRating, defRating]
    i=i+1

print("Putting Up Nets")
print(df)


number=1
stringDate="10-17-2017"
dateObject=datetime.datetime.strptime(stringDate,"%m-%d-%Y")
stopDate=datetime.datetime.today()-datetime.timedelta(days=1)
hold=0

while(dateObject<stopDate): 
      oddsURL="http://www.vegasinsider.com/nba/scoreboard/scores.cfm/game_date/"+str(stringDate)
      uClient=uReq(oddsURL)
      odds_html=uClient.read()
      uClient.close()
      oddsSoup=soup(odds_html, "html.parser")
      listofGames=oddsSoup.findAll("td",{"class":"sportPicksBorder"})
      #game=listofGames[0]
      for game in listofGames:
          #teamContainer=game.b.text
          #teams=teamContainer.split("@")
          #awayTeam=teams[0].strip()
          awayScoresContainer=game.findAll("td",{"class":"sportPicksBorderL2"})
          print(stringDate)
          awayTeamString=awayScoresContainer[2].text.strip().split("\n")[1]
          awayTeam=awayTeamString[:3]
          away1Q=awayScoresContainer[4].text.strip()
          away2Q=awayScoresContainer[5].text.strip()
          away3Q=awayScoresContainer[6].text.strip()
          away4Q=awayScoresContainer[7].text.strip()
          awayTotal=awayScoresContainer[-1].text.strip()
          #homeTeam=teams[1].strip()
          homeScoresContainer=game.findAll("td",{"class":"sportPicksBorderL"})
          newRowIndicator=int(len(homeScoresContainer)/2+1)
          homeTeamScrap=homeScoresContainer[newRowIndicator-1].text.strip().split("\n")[1]
          homeTeam=homeTeamScrap.split(" ")[0]
          home1Q=homeScoresContainer[newRowIndicator+1].text.strip()
          home2Q=homeScoresContainer[newRowIndicator+2].text.strip()
          home3Q=homeScoresContainer[newRowIndicator+3].text.strip()
          home4Q=homeScoresContainer[newRowIndicator+4].text.strip()
          homeTotal=homeScoresContainer[-1].text.strip()
          oddsSpace1=awayScoresContainer[3].text.strip()
          oddsSpace2=homeScoresContainer[int(1+len(homeScoresContainer)/2)].text.strip()
          oddsBucket=[oddsSpace1,oddsSpace2]
          if oddsBucket[0][0]=="-":
              spread=oddsBucket[0]
              favorite=awayTeam
              overUnder=oddsBucket[1]
          else:
              spread=oddsBucket[1]
              favorite=homeTeam
              overUnder=oddsBucket[0]
          if homeTeam=="UTH":
                homeTeam="UTA"
          else:
                hold=0
          if homeTeam=="CHA":
                homeTeam="CHO"
          else:
                hold=0
          if homeTeam=="BKN":
                homeTeam="BRK"
          else:
                hold=0
          if homeTeam=="NOR":
                homeTeam="NOP"
          else:
                hold=0
          if awayTeam=="UTH":
                awayTeam="UTA"
          else:
                hold=0
          if awayTeam=="CHA":
                awayTeam="CHO"
          else:
                hold=0
          if awayTeam=="BKN":
                awayTeam="BRK"
          else:
                hold=0
          if awayTeam=="NOR":
                awayTeam="NOP"
          else:
                hold=0
          #print(homeTeam)
          #print(awayTeam)
          homePtsGame=df.loc[df["Team"]==homeTeam]["Pts/Game"].values[0]
          homeOppPts=df.loc[df["Team"]==homeTeam]["Opp Pts/Game"].values[0]
          homeSRS=df.loc[df["Team"]==homeTeam]["SRS"].values[0]
          homePace=df.loc[df["Team"]==homeTeam]["Pace"].values[0]
          homeoffRating=df.loc[df["Team"]==homeTeam]["Off Rating"].values[0]
          homedefRating=df.loc[df["Team"]==homeTeam]["Def Rating"].values[0]
          awayPtsGame=df.loc[df["Team"]==awayTeam]["Pts/Game"].values[0]
          awayOppPts=df.loc[df["Team"]==awayTeam]["Opp Pts/Game"].values[0]
          awaySRS=df.loc[df["Team"]==awayTeam]["SRS"].values[0]
          awayPace=df.loc[df["Team"]==awayTeam]["Pace"].values[0]
          awayoffRating=df.loc[df["Team"]==awayTeam]["Off Rating"].values[0]
          awaydefRating=df.loc[df["Team"]==awayTeam]["Def Rating"].values[0]
          date=stringDate
          gameTotal=int(awayTotal)+int(homeTotal)
          number=number+1
          if gameTotal>float(overUnder):
              result="Over"
          else:
              result="Under"
          f.write(str(number)+","+date+","+awayTeam+","+away1Q+","+away2Q+","+away3Q+","+away4Q+","+awayTotal+","+homeTeam+","+home1Q+","+home2Q+","+home3Q+","+home4Q+","+homeTotal+","+str(gameTotal)+","+overUnder+","+result+","+favorite+","+str(spread)+","+homePtsGame+","+homeOppPts+","+homeSRS+","+homePace+","+homeoffRating+","+homedefRating+","+awayPtsGame+","+awayOppPts+","+awaySRS+","+awayPace+","+awayoffRating+","+awaydefRating+"\n")
      dateObject=dateObject+datetime.timedelta(days=1)
      stringDate=datetime.datetime.strftime(dateObject,"%m-%d-%Y")


f.close()
print("Done")
      
      
      
      



