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
        for line in text :
            if line.find(u"Votre recherche a renvoyé") >= 0:
                parse_player = True
            if parse_player :
                for country in COUNTRIES:
                    if line.strip().startswith(country):
                        player_info["country"] = country
                        player_info["full_name"] = line.split(country)[-1].split("Signet")[0].strip()
                        player_info["ic"] = line.split("Ind. carac.")[-1].strip()
                        player_info["age"] = line.split("Age")[-1].split("Salaire")[0].strip()
                if "full_name" not in player_info.keys() and line.find("Salaire") >= 0:
                    player_info["country"] = "Unknown"
                    player_info["full_name"] = line.split("Age")[0].strip()
                    player_info["ic"] = line.split("Ind. carac.")[-1].strip()
                    player_info["age"] = line.split("Age")[-1].split("Salaire")[0].strip()
            if line.startswith(u"Équipe") and parse_player:
                player_info["height"] = line.split("Taille")[-1].split("Poids")[0].strip()
                player, created = Player.objects.get_or_create(full_name=player_info["full_name"],
                                                               #country=player_info["country"],
                                                               height=player_info["height"],
                                                               defaults=player_info)
                player.team = line.split(u"Équipe")[-1].split("Taille")[0].strip()
                player.imc = line.split(u"IMC:")[-1].split(")")[0].strip()
                player.ic = player_info["ic"]
                player.age = player_info["age"]
                if "country" in player_info.keys() :
                    player.country = country
                player.save()
            if line.strip().startswith(u"Défense") and parse_player:
                player.defense = line.split(u"Défense")[-1].split(u"Lancers francs")[0].strip()
                player.freethrow = line.split(u"Lancers francs")[-1].strip()
                player.save()
            if line.strip().startswith(u"2 points") and parse_player:
                player.twopts = line.split(u"2 points")[-1].split(u"3 points")[0].strip()
                player.threepts =line.split(u"3 points")[-1].split(u"Prix de départ")[0].strip()
                player.save()
            if line.strip().startswith(u"Dribble") and parse_player:
                player.dribbling = line.split(u"Dribble")[-1].split(u"Passe")[0].strip()
                player.passing = line.split(u"Passe")[-1].split(u"Enchère actuelle")[0].strip()
                player.save()
            if line.strip().startswith(u"Vitesse") and parse_player:
                player.speed = line.split(u"Vitesse")[-1].split(u"Jeu de jambes")[0].strip()
                player.footwork = line.split(u"Jeu de jambes")[-1].split(u"Dernière enchère")[0].strip()
                player.save()
            if line.strip().startswith(u"Rebonds") and parse_player:
                player.rebond = line.split(u"Rebonds")[-1].split(u"Expérience")[0].strip()
                player.experience = line.split(u"Expérience")[-1].split(u"Echéance")[0].strip()
                player.last_update=datetime.datetime.now()
                player.save()
                player_info = {}
                player = None
        count = Player.objects.all().count()
        return render(request,"players/submit.html",{"form":form,
                                                                 "title":"Soumission de joueurs",
                                                                 "count":count,
                                                                 "select":select,
                                                                 "last_update":last_update})

def search(request):
    last_update = Player.objects.all().order_by('-last_update')[0].last_update
    form = SearchForm()
    regexp = "\(Top\s8\s\:\s\d\d\,\d\)"
    parse_player = False
    count = Player.objects.all().count()

    player_set = []
    player = {
            "defense":"-",
            "freethrow":"-",
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
            filter = int(request.POST["filter"])
        except :
            filter = 100000
        team_name = ""
        for line in text :
            if re.match(regexp,line.strip()):
                parse_player = True
            if line.startswith(u"Saison     Événement") :
                parse_player = False
            if parse_player and line.strip() != "" and not line.startswith("Age") and not line.startswith("Taille") and line.find("%") < 0:
                for tag in NAME_TAG:
                    line = line.split(tag)[0]
                player["full_name"] = line.strip()
            if parse_player and line.startswith("Age"):
                player["age"] = line.split(u"Age:")[-1].split(u", IC:")[0].strip()
                player["ic"] = line.split(u"IC:")[-1].strip()
            if parse_player and line.startswith("Taille"):
                player["height"] = line.split(u"Taille:")[-1].split(u", IMC:")[0].strip()
                player["imc"] = line.split(u"IMC:")[-1].strip()

                if int("".join(player["ic"].split("."))) > filter:
                    try :
                        player_db = Player.objects.get(full_name = player["full_name"], height = int(player["height"]))
                    except Player.DoesNotExist:
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
                player = {            "defense":"-",
            "freethrow":"-",
            "twopts":"-",
            "threepts":"-",
            "dribbling":"-",
            "passing":"-",
            "speed":"-",
            "footwork":"-",
            "rebond":"-",
            "experience":"-",
            "last_update":"-"}
            if line.find(u"a terminé") >= 0:
                team_name = line.split(u"a terminé")[0].strip()

        return render(request,"players/show.html",{"players":player_set,
                                                               "team":team_name,
                                                               "count":count,
                                                               "select":select,
                                                               "last_update":last_update,
                                                               "filter":filter})

def single_search(request):
    last_update = Player.objects.all().order_by('-last_update')[0].last_update
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
            if request.POST["min_pass"] or request.POST["max_pass"] :
                max = int(request.POST["max_pass"]) if request.POST["max_pass"] else 30
                min = int(request.POST["min_pass"]) if request.POST["min_pass"] else 1
                query = query.filter(passing__lte=max,passing__gte=min)
            if request.POST["min_shoot"] or request.POST["max_shoot"] :
                max = int(request.POST["max_shoot"]) if request.POST["max_shoot"] else 30
                min = int(request.POST["min_shoot"]) if request.POST["min_shoot"] else 1
                query = query.filter(twopts__lte=max,twopts__gte=min)
            if request.POST["min_ftw"] or request.POST["max_ftw"] :
                max = int(request.POST["max_ftw"]) if request.POST["max_ftw"] else 30
                min = int(request.POST["min_ftw"]) if request.POST["min_ftw"] else 1
                query = query.filter(footwork__lte=max,footwork__gte=min)
            if request.POST["min_reb"] or request.POST["max_reb"] :
                max = int(request.POST["max_reb"]) if request.POST["max_reb"] else 30
                min = int(request.POST["min_reb"]) if request.POST["min_reb"] else 1
                query = query.filter(rebond__lte=max,rebond__gte=min)
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

def nt_search(request):
    form = SearchForm()
    last_update = Player.objects.all().order_by('-last_update')[0].last_update
    count = Player.objects.all().count()
    regexp = "\d+\s+\%"
    select = {"team":"",
              "search":"",
              "submit":"",
              "nt_search":"selected"
              }
    tag = u"Détails Joueurs Calendrier"
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
        for line in text :
            if line.strip().startswith(tag):
                parse_player = True
            if line.startswith(u"Toolbox") :
                parse_player = False
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
