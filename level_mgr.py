"""Manages leveling up and class choices"""

import random

def level_check(player, levels):
    """Levels up the player as necessary, per the XP chart"""
    if player.stats['XP'] >= levels[player.stats['Level'] + 1]:
        player.stats['Level'] += 1
        stat_up = random.choice(['MaxHealth', 'Damage', 'MaxStamina', 'Defense', 'Power'])
        player.stats[stat_up] += player.stats['Level']
        player.stats['Health'] = player.stats['MaxHealth']
        player.stats['Stamina'] = player.stats['MaxStamina']
        if stat_up == 'MaxHealth':
            print('>You have become more used to this harsh, rainy environment.\n Your health improves.')
        if stat_up == 'Damage':
            print('>Your time spent fighting has paid off. You handle yourself far more \n confidently in combat.')
        if stat_up == 'MaxStamina':
            print('>Trudging, running, and jumping through the muck has become second nature to \n you, and you can move, run, and fight longer without tiring.')
        if stat_up == 'Defense':
            print('>Your weapons, fists, and arrows are a frustrating barrage for any enemy to \n penetrate. You are better able to defend yourself.')
        if stat_up == 'Power':
            print('>Days spent in this magical fallout zone have worn off on you. \n The patterns of the universe seem somehow... clearer.')
        player = level_up_choices(player)
    return player
def level_up_choices(player):
    """Provides choices to make during the level up process"""
    if player.stats['Level'] == 2:
        print('>You have quickly developed a style of survival, and begin to identify your \
              strengths and weaknesses. Are you: \n Burly? \n Metabolic? \n or Stealthy?')
        while True:
            passive = input(': ')
            passive = passive.upper()
            if passive in ['BURLY', 'METABOLIC', 'STEALTHY']:
                if passive == 'BURLY':
                    player.defaults['InvHoldLen'] = 15
                    player.stats['Damage'] += 5
                if passive == 'METABOLIC':
                    player.defaults['RestSick'] = 7
                    player.stats['Health'] += 5
                if passive == 'STEALTHY':
                    player.defaults['PrlngStlth'] = 4
                    player.defaults['SnkStm'] = 2
                break
            else:
                print('Invalid option.')
        print('>Are you: \n Thin-Skinned? \n Weak-Hearted? \n or Near-Sighted?')
        while True:
            passive = input(': ')
            passive = passive.upper()
            if passive in ['THIN-SKINNED', 'WEAK-HEARTED', 'NEAR-SIGHTED']:
                if passive == ('THIN-SKINNED'):
                    player.defaults['BleedChance'] = 25
                    player.defaults['DeathHealth'] = 1
                if passive == ('WEAK-HEARTED'):
                    player.defaults['WlkngStamLoss'] = 2
                    player.defaults['FtgueRate'] = 2
                if passive == ('NEAR-SIGHTED'):
                    player.defaults['MissChance'] = 4
                    player.defaults['AltrChance'] = 0
                break
            else:
                print('Invalid option.')
        active = random.choice(['DODGE', 'CHARGE', 'CLEAVE'])
        print('>Additionally, you have learned a new combat skill. You can now use the %s \
              ability.' % active.title())
        player.learned_commands.append(active)
    elif player.stats['Level'] in [5, 11, 15]:
        print('>You have further fleshed out your combat style.')
        if player.stats['Level'] == 5:
            print('Are you: \n Muscled? \n Spritely? \n Tactical? \n Brutal? \n or Sneaky?')
            while True:
                passive = input(': ')
                passive = passive.upper()
                if passive in ['MUSCLED', 'SPRITELY', 'TACTICAL', 'BRUTAL', 'SNEAKY']:
                    if passive == 'MUSCLED':
                        player.defaults['EffDmg'] = 10
                        player.stats['Damage'] += 7
                    if passive == 'SPRITELY':
                        player.defaults['MealMod'] = 10
                        player.defaults['FtgueThrshld'] = 15
                    if passive == 'TACTICAL':
                        player.defaults['MaxDmgMod'] = 15
                        player.defaults['DefStamMod'] = 5
                    if passive == 'BRUTAL':
                        player.defaults['StamModXtra'] = 10
                        player.stats['Damage'] += 7
                    if passive == 'SNEAKY':
                        player.defaults['SnkAtkMult'] = 5
                        player.defaults['SnkStm'] = 1
                    break
                else:
                    print('Invalid option.')
            active = random.choice(['RAGE', 'PARRY', 'SUICIDAL BLOW'])
            print('>You have learned a new combat skill. You can now use the %s ability.' \
                  % active.title())
            player.learned_commands.append(active)
        if player.stats['Level'] == 11:
            active = random.choice(['MEDITATE', 'DANCE', 'SCROLLBIND'])
            print('>You have learned a new skill. You can now use the %s ability.' % active.title())
            player.learned_commands.append(active)
        if player.stats['Level'] == 15:
            print('Are you: \n Glorious? \n Tireless? \n or Prosperous?')
            while True:
                passive = input(': ')
                passive = passive.upper()
                if passive in ['GLORIOUS', 'TIRELESS', 'PROSPEROUS']:
                    if passive == 'GLORIOUS':
                        player.defaults['KillHealChance'] = 3
                        player.defaults['KillHealth'] = 20
                    if passive == 'TIRELESS':
                        player.defaults['AtkStam'] = 0
                        player.defaults['WlkngStamLoss'] = 0
                        player.defaults['SnkStm'] = 0
                    if passive == 'PROSPEROUS':
                        player.defaults['AltrChance'] = 10
                        player.defaults['ContnrBtmRng'] = 0
                        player.defaults['MaxGold'] = 100
                    break
                else:
                    print('Invalid option.')
            active = random.choice(['DEATHSTRIKE', 'MINDSTRIKE', 'BODYSTRIKE'])
            print('>Additionally, you have learned how to sacrifice your very essence in order \
                  to perform the devastating %s.' % active.title())
            player.learned_commands.append(active)
    return player
def player_type_choice():
    """Defines the class of the player"""
    print(">Type one of the following classes to learn more about it. Follow the \n prompts to choose a class. "
          "Hunter, Prince, Farmer, Traveller")
    while True:
        choice = input("Class: ")
        if choice == "Hunter":
            #print ("The Hunter. \n Many years of fresh air and life in the woods \n have made you healthy and robust. When the storm washed away \n your hunting grounds, you left to find healthier forests. \n """What you lack in weapon skills and \n stamina you make up for in your superior health.")
            print("Low stamina, low damage, high health. Good low-level, \n harder high-level.")
            accept = input("Type \"Choose\" to choose this class. Type \"Back\" to \n pick a new one. \n : ")
            if accept.upper() == "CHOOSE":
                player_stats = {"Health": 50,
                                "MaxHealth": 50,
                                "Damage": 15,
                                "Stamina": 25,
                                "MaxStamina": 25,
                                "Fatigue": 0,
                                "Defense": 5,
                                "Power": 5,
                               }
                player_class = "Hunter"
                break
        if choice == "Prince":
            #print ("The Prince. \n You have lived a life of luxury, free from the troubles \n of commoners. Your kingdom destroyed by the storm, you chose to \n leave and be the hero you always desired to be. \n Though you lack the experience that comes from hard work, \n your many days of fencing and dueling make you well suited for \n battle.")
            print("Low stamina, low health, high damage. Very difficult! For experienced \n \
                  players only.")
            accept = input("Type \"Choose\" to choose this class. Type \"Back\" to \n pick a new one. \n : ")
            if accept.upper() == "CHOOSE":
                player_stats = {"Health": 30,
                                "MaxHealth": 30,
                                "Damage": 45,
                                "Stamina": 25,
                                "MaxStamina": 25,
                                "Fatigue": 0,
                                "Defense": 5,
                                "Power": 10,
                               }
                player_class = "Prince"
                break
        if choice == "Farmer":
            #print ("The Farmer. \n After years of hardships, you were spurred to action as \n the last of your land is washed away by the storm. You can \n endure considerably more than most people.")
            print("Low health, OK damage, good stamina. A good class in the long run.")
            accept = input("Type \"Choose\" to choose this class. Type \"Back\" to \n pick a new one. \n : ")
            if accept.upper() == "CHOOSE":
                player_stats = {"Health": 37,
                                "MaxHealth": 37,
                                "Damage": 15,
                                "Stamina": 40,
                                "MaxStamina": 40,
                                "Fatigue": 0,
                                "Defense": 6,
                                "Power": 5,
                               }
                player_class = "Farmer"
                break
        if choice == "Traveller":
            #print ("The Traveller. \n Years on the road have led you on adventures nearly every day. \n Now that the roads have been washed away, your next adventure will be this \n one. You are a well-balanced fighter, survivor, and endurer, but you do not \n excel in any particular thing.")
            print("Well-balanced. Good for experimenting or developing \n your own play style.")
            accept = input("Type \"Choose\" to choose this class. Type \"Back\" to \n pick a new one. \n : ")
            if accept.upper() == "CHOOSE":
                player_stats = {"Health": 40,
                                "MaxHealth": 40,
                                "Damage": 20,
                                "Stamina": 30,
                                "MaxStamina": 30,
                                "Fatigue": 0,
                                "Defense": 5,
                                "Power": 5,
                               }
                player_class = "Traveller"
                break
    return player_stats, player_class
