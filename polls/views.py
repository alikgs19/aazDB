# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import unicodedata
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import pymssql
import json

config = { 'SERVERIP' : '192.168.1.8',
           'PASSWORD' : 'kgsali1234',
           'USER' : 'alikgs',
           'DATABASE' : 'FootsiDB',
           'SERVERPORT' : 1433}

def donothing(request):
    return render(request, 'polls/index.html')




def playmatch(request):

    conn = pymssql.connect(server= config['SERVERIP'], port= config['SERVERPORT'], user=config['USER'],
                           password=config['PASSWORD'], database=config['DATABASE'])
    cursor = conn.cursor()

    homeKey = request.GET.get('homeKey', '')
    guestKey = request.GET.get('guestKey', '')

    strHomeKey = unicodedata.normalize('NFKD', homeKey).encode('ascii','ignore')
    strGuestKey = unicodedata.normalize('NFKD', guestKey).encode('ascii', 'ignore')
    # cursor.callproc('doMatch', (strHomeKey, strGuestKey))
    cursor.callproc('doMatch', ('6'.unicode('utf8'), '5'))
    result = cursor.fetchall()

    response = {}
    response['response'] = result[0]

    return JsonResponse(response)

def getteams(self):
    conn = pymssql.connect(server=config['SERVERIP'], port=config['SERVERPORT'], user=config['USER'],
                           password=config['PASSWORD'], database=config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM club")
    response = {}
    result = []

    for row in cursor.fetchall():
        tempres = {}
        tempres['budget'] = row[0]
        tempres['name'] = row[1]
        tempres['key'] = row[2]
        tempres['stadium'] = row[3]

        result.append(tempres)

    response['clubslist'] = result

    cursor.execute("SELECT league.")
    return JsonResponse(response)



def getclubinfo(request):
    conn = pymssql.connect(server=config['SERVERIP'], port=config['SERVERPORT'], user=config['USER'],
                           password=config['PASSWORD'], database=config['DATABASE'])
    response = {}


    cursor = conn.cursor()
    cursor.execute("SELECT stadium.*"
                   " FROM stadium INNER JOIN club ON stadium.[key] = club.stadium "
                   "WHERE club.[key] = %s", (request.GET.get('clubKey', '')))

    stadium = cursor.fetchall()[0]

    stadiumInfo = {}
    stadiumInfo['key'] = stadium[0]
    stadiumInfo['capacity'] = stadium[1]
    stadiumInfo['feild'] = stadium[2]
    stadiumInfo['name'] = stadium[3]
    stadiumInfo['price'] = stadium[4]
    stadiumInfo['wc'] = stadium[5]

    response['stadiumInfo'] = stadiumInfo

    cursor.execute("SELECT * FROM club WHERE club.[key] = %s", (request.GET.get('clubKey', '')))
    clubInfo = cursor.fetchall()
    clubInfoObject = {}
    clubInfoObject['budget'] = clubInfo[0][0]
    clubInfoObject['name'] = clubInfo[0][1]
    clubInfoObject['key'] = clubInfo[0][2]
    clubInfoObject['stadium'] = clubInfo[0][3]

    response['clubInfo'] = clubInfoObject

    cursor.execute("SELECT * FROM match INNER JOIN club ON club.[key] = match.host OR club.[key] = match.guest "
                   "WHERE club.[key] = %s", (request.GET.get('clubKey', '')))
    clubMatchs = cursor.fetchall()

    response['clubMatchs'] = []
    for match in clubMatchs:
        matchInfoObject = {}
        matchInfoObject['key'] = match[0]

        cursor.execute("SELECT club.name FROM club WHERE club.[key] = %s", (match[1]))
        hostClubName = cursor.fetchall()[0]
        matchInfoObject['host'] = hostClubName[0]

        cursor.execute("SELECT club.name FROM club WHERE club.[key] = %s", (match[2]))
        guestClubName = cursor.fetchall()[0]
        matchInfoObject['guest'] = guestClubName[0]

        matchInfoObject['time'] = match[3]

        matchInfoObject['score'] = match[4]

        cursor.execute("SELECT league.name FROM league WHERE league.[key] = %s", (match[5]))
        leagueName = cursor.fetchall()[0]
        matchInfoObject['leagueName'] = leagueName
        response['clubMatchs'].append(matchInfoObject)



    return JsonResponse(response)
