import requests
import json
from datetime import date, timedelta
import time 
rate = 2.05
redirectAPI = 'Enter your Redirect.com API key here'
URL = 'https://panel.zeropark.com/api/publisher/stats/targets?endDate=' + time.strftime('%d/%m/%Y') + '&interval=CUSTOM&limit=9000&sortOrder=DESC&startDate=' + (date.today() - timedelta(2)).strftime('%d/%m/%Y')
LOGIN_URL = 'https://panel.zeropark.com/signin?referer=/' # Or whatever the login request url is
payload = { 'password': 'ZeroPark Publisher Account Password', 'email': 'ZeroPark Publisher Account Password'}
while True:
     time.sleep(0.1)
     s = requests.Session()
     try: 
         response = s.post(LOGIN_URL, data=payload)
         targets = s.get(URL)
         targetsList = json.loads(targets.content)['elements']
         visits = s.get('http://api.theparkingplace.com/api/campaignreporting?apikey=' + redirectAPI + '&startdate=' + (date.today() - timedelta(2)).strftime('%m/%d/%Y') + '&enddate=' + time.strftime('%m/%d/%Y') + '&format=json')
     except Exception as e:
         print e
     visit = {}
     cost = {}
     for v in json.loads(visits.content)['results']['result']:
         
         visit[(str)(v['campaignname'].lower())] = (float)(v['total_visitors'])
         cost[(str)(v['campaignname'].lower())] = (float)(v['cost'])
     cancel = False
     for value in targetsList:
         with open("results.txt") as fp:
             if value['sellableVisits'] > 5:
                 for i, line in enumerate(fp):
                     if line[0:line.index(',')].lower() == value['targetAddress']:
                         print value['targetAddress']
                         
                         if (value['revenue'] != 0.00):
                             try:
                                 cpm = 1000 * (value['revenue'] / visit[value['targetAddress']])
                                 print 'Rev: $' + (str)(value['revenue']) + ', cpm calculated perfectly at ' + (str) (cpm) + " with " + (str) (value['sellableVisits']) + " sellable and " + (str)(value['soldVisits']) + " sold."
                             except Exception as e:
                                 cpm = value['cpm'] / 1.5
                                 print 'Rev: $' + (str)(value['revenue']) + ', cpm calculted imperfectly, guess is ' + (str) (cpm) + " with " + (str) (value['sellableVisits']) + " sellable and " + (str) (value['soldVisits']) + " sold."
                         else:
                             cpm = value['cpm'] / 1.5
                             print 'Rev=0.00, cpm calculted imperfectly, guess is ' + (str) (cpm) + " with " + (str) (value['sellableVisits']) + " sellable and " + (str) (value['soldVisits']) + " sold."
                        
                         cpm2 = value['cpm']
                         if cpm2 < cpm:
                             cpm = cpm2
                         if cpm == 0.0:
                             cpm
                             if value['sellableVisits'] > 1000:
                                 cpm = 0.1
                             else:
                                 cpm = 0.2
                         bid = (cpm / rate)
                         if (bid < .2 and cpm >= .23):
                             bid = .21
                             if value['revenue'] == 0.00 and value['sellableVisits'] < 1000:
                                 bid = .5
                         elif (bid < .2 and cpm >= .21 and cpm <= .23):
                             bid = .2
                         elif (bid < .2 and cpm < .2):
                            bid = .01
                         if value['targetAddress'] == 'us-scraps' and bid <= 4.25:
                             print 'us scraps bid should be ' + (str)(bid)
                             bid = bid * 1.3
                         if (value['targetAddress'] == 'us-2' or value['targetAddress'] == 'ca-2' or value['targetAddress'] == 'uk-2') and bid <= 2:
                             print 'us/ca/uk 2 bid should be ' + (str)(bid)
                             bid = bid * 1.3
                         try:
                             if (float)(cost[value['targetAddress']]) > .4:
                                 print 'bid set at ' + (str)(bid)
                                 URL2 = 'http://api.theparkingplace.com/api/editcampaign?apikey=' + redirectAPI + '&format=json&max_bid=' + (str) (bid) + '&id='  + line[line.index(',') + 1:len(line)]
                                 try:
                                     optimize = s.get(URL2)
                                     #print optimize.content
                                 except Exception as e:
                                    print e
                             else:
                                 bid = bid * rate * .75   
                                 print 'bid adjusted up, set at ' + (str)(bid)
                                 URL2 = 'http://api.theparkingplace.com/api/editcampaign?apikey=' + redirectAPI + '&format=json&max_bid=' + (str) (bid) + '&id='  + line[line.index(',') + 1:len(line)]
                                 try:
                                     optimize = s.get(URL2)
                                     #print optimize.content
                                 except Exception as e:
                                    print e
                         except Exception as e:
                             print 'NO COST INFO bid set at ' + (str)(bid)
                             URL2 = 'http://api.theparkingplace.com/api/editcampaign?apikey=' + redirectAPI + '&format=json&max_bid=' + (str) (bid) + '&id='  + line[line.index(',') + 1:len(line)]
                             try:
                                 optimize = s.get(URL2)
                                 #print optimize.content
                             except Exception as e:
                                print e
         if cancel == True:
             with open("results.txt") as fp:
                 for i, line in enumerate(fp):
                     if line[0:line.index(',')].lower() == value['targetAddress']:
                         URL2 = 'http://api.theparkingplace.com/api/pausecampaign?apikey=' + redirectAPI + '&format=json&id='  + line[line.index(',') + 1:len(line)]    
                         try:
                             pause = s.get(URL2)
                             #print pause.content
                         except Exception as e:
                             print e
     print 'Done loop'
     time.sleep(60 * 15)
