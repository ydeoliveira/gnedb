# Create your views here.
#encoding:utf-8
import re
import datetime

from django.shortcuts import render
from django.db.models import Max
#from django.views.generic.simple import direct_to_template

from players.forms import SubmitForm, PlayerSearch, SearchForm
from players.models import Player
from players.constants import COUNTRIES

NAME_TAG = [u"Sur le marché", "Equipe nationale", "En attente d'offres", u"Blessé", u"Ce joueur fait partie d'un Hall of Fame"]

def submit(request):
    form = SubmitForm()
    parse_player = False
    player = None
    player_info = {}
    select = {"team":"",
              "search":"",
              "submit":"selected"
              }
    last_update = Player.objects.all().aggregate(Max('last_update'))['last_update__max']
    #last_update = Player.objects.all().order_by('-last_update')[0].last_update
    if request.method == "GET":
        count = Player.objects.all().count()
        return render(request,"players/submit.html",{"form":form,
                                                                 "title":"Soumission de joueurs",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})
    else :
        text = request.POST["liste"].split("\n")
        player_data = None
        for line in text :
            if line.find(u"Tout Recommencer") >= 0:
                parse_player = True
                player_data = {}
                continue
            if parse_player :
                if "full_name" not in player_data.keys() :
                    player_data["full_name"] = line.strip()
                    print("player {0}".format(player_data["full_name"]))
                if line.startswith('ATTAQUE') and parse_player:
                    expression = "ATTAQUE.*?Nationalité\:\t(?P<country>[\w\,\-\s]+)\sÂge:\t(?P<age>\d{2})\sTaille:\t(?P<height>\d{3})cm\sPoids:\t\d+kg\sSalaire:\t\$\d+\,\d+\sPosition:\t(?P<position>[\w\/]+)\sEnergy"
                    p = re.compile(expression)
                    m = p.match(line)
                    player_data['country'] = m.group('country').strip()
                    player_data['age'] = m.group('age').strip()
                    player_data['height'] = m.group('height').strip()
                    player_data['position'] = m.group('position').strip()
                    
                if line.startswith(' Défense:') and parse_player:
                    expression = " Défense:\t(?P<defense>\d{1,2})\sTir:\t(?P<shot>\d{1,2})\sVitesse:\t(?P<speed>\d{1,2})\sDribble:\t(?P<dribbling>\d{1,2})\sForce:\t(?P<straight>\d{1,2})\sMouvements de Poste:\t(?P<postmove>\d{1,2})\sExpérience:\t(?P<experience>\d{1,2})"
                    p = re.compile(expression)
                    m = p.match(line)
                    player_data['defense'] = m.group('defense').strip()
                    player_data['shot'] = m.group('shot').strip()
                    player_data['speed'] = m.group('speed').strip()
                    player_data['dribbling'] = m.group('dribbling').strip()
                    player_data['straight'] = m.group('straight').strip()
                    player_data['postmove'] = m.group('postmove').strip()
                    player_data['experience'] = m.group('experience').strip()
                if line.startswith(u"Prix:") and parse_player:
                    Player.objects.update_or_create(full_name=player_data['full_name'],height=player_data['height'],defaults=player_data)
                    player_data = {}
                
        count = Player.objects.all().count()
        last_update = Player.objects.all().aggregate(Max('last_update'))['last_update__max']
        return render(request,"players/submit.html",{"form":form,
                                                                 "title":"Soumission de joueurs",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})

def search(request):
    last_update = Player.objects.all().aggregate(Max('last_update'))['last_update__max']
    form = SearchForm()
    regexp = "\(Top\s8\s\:\s\d\d\,\d\)"
    parse_player = False
    count = Player.objects.all().count()

    player_set = []
    player = {
            "defense":"-",
            "shoot":"-",
            "twopts":"-",
            "threepts":"-",
            "dribbling":"-",
            "passing":"-",
            "speed":"-",
            "footwork":"-",
            "rebond":"-",
            "experience":"-",
            "last_update":"-"
              }
    select = {"team":"selected",
              "search":"",
              "submit":""
              }
    if request.method == "GET":
        return render(request,"players/submit.html",{"form":form,
                                                                 "title":"Recherche de joueurs",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})
    else :
        text = request.POST["liste"].split("\n")
        try:
            filter_age = int(request.POST["filter"])
        except :
            filter_age = 21
        team_name = ""

        player = {}
        for line in text :
            if line.strip().startswith("ANALYSE D'EQUIPE"):
                parse_player = True
            if line.startswith(u"webelinx") :
                parse_player = False
            if line.startswith(COUNTRIES) and parse_player:
                print(line)
                for country in COUNTRIES :
                    expression = "{0}\s(?P<full_name>.*)".format(country)
                    p = re.compile(expression)
                    m = p.match(line)
                    if m :
                        player["full_name"] = m.group('full_name').strip()
                        break
            if line.startswith('Âge:') and parse_player:
                expression = "Âge:\s+(?P<age>\d{2})\sTaille:\s(?P<height>\d{3})cm\sPosition:\s(?P<position>[\w\/]+)"
                p = re.compile(expression)
                m = p.match(line)
                player["age"] = m.group('age').strip()
                player["height"] = m.group('height').strip()
                player["position"] = m.group('position').strip()
                if int(player["age"]) < filter_age :
                    player = {}
                    continue
                try :
                    player_db = Player.objects.get(full_name = player["full_name"], height = int(player["height"]))
                    player["defense"] = player_db.defense
                    player["shot"] = player_db.shot
                    player["speed"] = player_db.speed
                    player["dribbling"] = player_db.dribbling
                    player["straight"] = player_db.straight
                    player["postmove"] = player_db.postmove
                    player["experience"] = player_db.experience
                    player["last_update"] = player_db.last_update
                except Player.DoesNotExist:
                    player["defense"] = "-"
                    player["shot"] = "-"
                    player["speed"] = "-"
                    player["dribbling"] = "-"
                    player["straight"] = "-"
                    player["postmove"] = "-"
                    player["experience"] = "-"
                    player["last_update"] = "-"
 
                player_set.append(player)
                player = {}

        sorted_players = sorted(player_set, key=lambda k: k['height'])
        return render(request,"players/show.html",{"players":sorted_players,
                                                               "team":team_name,
                                                               "count":count,
                                                               "select":select,
                                                               "last_update":last_update,
                                                               "filter":filter})

def single_search(request):
    last_update = Player.objects.all().aggregate(Max('last_update'))['last_update__max']
    select = {"team":"",
              "search":"selected",
              "submit":""
              }
    count = Player.objects.all().count()
    form = PlayerSearch()
    if request.method == "GET":

        return render(request,"players/player.html",{"form":form,
                                                                 "title":"Rechercher un joueur",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})
    else:
        form = PlayerSearch(data=request.POST)
        if form.is_valid():
            query = Player.objects.all()
            
            if request.POST["name"] :
                player_name = request.POST["name"]
                query = query.filter(full_name__icontains = player_name)
            if request.POST["min_age"] or request.POST["max_age"] :
                max = int(request.POST["max_age"]) if request.POST["max_age"] else 1000
                min = int(request.POST["min_age"]) if request.POST["min_age"] else 0
                query = query.filter(age__lte=max,age__gte=min)
            if request.POST["min_height"] or request.POST["max_height"] :
                max = int(request.POST["max_height"]) if request.POST["max_height"] else 1000
                min = int(request.POST["min_height"]) if request.POST["min_height"] else 0
                query = query.filter(height__lte=max,height__gte=min)
            if request.POST["min_def"] or request.POST["max_def"] :
                max = int(request.POST["max_def"]) if request.POST["max_def"] else 30
                min = int(request.POST["min_def"]) if request.POST["min_def"] else 1
                query = query.filter(defense__lte=max,defense__gte=min)
            if request.POST["min_speed"] or request.POST["max_speed"] :
                max = int(request.POST["max_speed"]) if request.POST["max_speed"] else 30
                min = int(request.POST["min_speed"]) if request.POST["min_speed"] else 1
                query = query.filter(speed__lte=max,speed__gte=min)
            if request.POST["min_drib"] or request.POST["max_drib"] :
                max = int(request.POST["max_drib"]) if request.POST["max_drib"] else 30
                min = int(request.POST["min_drib"]) if request.POST["min_drib"] else 1
                query = query.filter(dribbling__lte=max,dribbling__gte=min)
            if request.POST["min_str"] or request.POST["max_str"] :
                max = int(request.POST["max_str"]) if request.POST["max_str"] else 30
                min = int(request.POST["min_str"]) if request.POST["min_str"] else 1
                query = query.filter(straight__lte=max,straight__gte=min)
            if request.POST["min_shoot"] or request.POST["max_shoot"] :
                max = int(request.POST["max_shoot"]) if request.POST["max_shoot"] else 30
                min = int(request.POST["min_shoot"]) if request.POST["min_shoot"] else 1
                query = query.filter(shot__lte=max,shot__gte=min)
            if request.POST["min_ftw"] or request.POST["max_ftw"] :
                max = int(request.POST["max_ftw"]) if request.POST["max_ftw"] else 30
                min = int(request.POST["min_ftw"]) if request.POST["min_ftw"] else 1
                query = query.filter(postmove__lte=max,postmove__gte=min)
            if request.POST["min_xp"] or request.POST["max_xp"] :
                max = int(request.POST["max_xp"]) if request.POST["max_xp"] else 30
                min = int(request.POST["min_xp"]) if request.POST["min_xp"] else 1
                query = query.filter(experience__lte=max,experience__gte=min)

            if request.POST["sort1"] != ''  and request.POST["sort2"] !='' :
                query = query.order_by(request.POST["sort1"],request.POST["sort2"])
            elif request.POST["sort1"] != '':
                query = query.order_by(request.POST["sort1"])
            elif request.POST["sort2"] != '':
                query = query.order_by(request.POST["sort2"])

            title = "%i joueurs trouvés"%len(query)
            return render(request,"players/player.html",{"title":title,
                                                                     "players":query,
                                                                     "count":count,
                                                                     "select":select,
                                                                     "form":form,
                                                                 "last_update":last_update})
        else :
            return render(request,"players/player.html",{"form":form,
                                                                 "title":"Rechercher un joueur",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})

"""def nt_search(request):
    form = SearchForm()
    last_update = Player.objects.all().order_by('-last_update')[0].last_update
    count = Player.objects.all().count()
    regexp = "\d+\s+\%"
    select = {"team":"",
              "search":"",
              "submit":"",
              "nt_search":"selected"
              }
    tag = u"ANALYSE D'EQUIPE"
    parse_player = False
    player_set = []
    if request.method == "GET":
        return render(request,"players/submit.html",{"form":form,
                                                                 "title":"Recherche de joueurs NT",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})
    else :
        text = request.POST["liste"].split("\n")
        player = {}
        for line in text :
            if line.strip().startswith(tag):
                parse_player = True
            if line.startswith(u"webelinx") :
                parse_player = False
            if line.startswith(COUNTRIES) and parse_player:
                for country in COUNTRIES :
                    expression = "{0}\s(?P<full_name>.*)".format(country)
                    p = re.compile(expression)
                    m = p.match(line)
                    player["full_name"] = m.group('full_name').strip()
            if line.startswith('Âge:') and parse_player:
                expression = "Âge:\s+(?<age>\d{2})\sTaille:\s(?<height{3}>)cm\sPosition:\(?P<position>[\w\/]+)"
            
            if parse_player is True and not line.startswith("Age") and not line.startswith("Taille") and not line.startswith("Team") and not re.match(regexp,line.strip()) :
                player = {}
                player["full_name"] = line.strip()
            if parse_player is True and line.startswith("Age") :
                player["age"] = int(line.split(',')[0].split(':')[1].strip())
                player["ic"] = line.split(',')[1].split(':')[1].strip()
            if parse_player is True and line.startswith("Taille") :
                player["height"] = int(line.split(',')[0].split(':')[1].strip())
                player["imc"] = line.split(',')[1].split(':')[1].strip()
                try :
                    player_db = Player.objects.get(full_name = player["full_name"], height = player["height"])
                except Player.DoesNotExist:
                    player["defense"] = "-"
                    player["freethrow"]="-"
                    player["twopts"]="-"
                    player["threepts"]="-"
                    player["dribbling"]="-"
                    player["passing"]="-"
                    player["speed"]="-"
                    player["footwork"]="-"
                    player["rebond"]="-"
                    player["experience"]="-"
                    player["last_update"]="-"
                    if not player_set :
                        player_set.append(player)
                    else :
                        for p in player_set:
                            if type(p).__name__ == 'dict' :
                                if int(p["height"]) > int(player["height"]):
                                    player_set.insert(player_set.index(p), player)
                                    break
                                elif player_set.index(p)+1 == len(player_set):
                                    player_set.insert(player_set.index(p)+1, player)
                                    break
                            else:
                                if int(p.height) > int(player["height"]):
                                    player_set.insert(player_set.index(p), player)
                                    break
                                elif player_set.index(p)+1 == len(player_set):
                                    player_set.insert(player_set.index(p)+1, player)
                                    break
                else :
                    if not player_set :
                        player_set.append(player_db)
                    else :
                        for p in player_set:
                            if type(p).__name__ == 'dict' :
                                if int(p["height"]) > int(player_db.height):
                                    player_set.insert(player_set.index(p), player_db)
                                    break
                                elif player_set.index(p)+1 == len(player_set):
                                    player_set.insert(player_set.index(p)+1, player_db)
                                    break
                            else :
                                if int(p.height) > int(player_db.height):
                                    player_set.insert(player_set.index(p), player_db)
                                    break
                                elif player_set.index(p)+1 == len(player_set):
                                    player_set.insert(player_set.index(p)+1, player_db)
                                    break
        return render(request,"players/show.html",{"players":player_set,
                                                               "count":count,
                                                               "select":select,
                                                               "last_update":last_update,
                                                               })
"""
