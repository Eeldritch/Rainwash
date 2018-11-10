"""Contains definitions for epic skills"""

import random

import status_effects

from output_mgr import cprint

def siphon(player, epic_monster, monsters, monster_list):
    """Siphons health from the player to epic_monster"""
    cprint(">The %s siphons off a little bit of your health." % epic_monster['Name'].lower(), 'magenta')
    health_siphon = random.randint(1, 5)
    player.stats["Health"] -= health_siphon
    epic_monster["HP"] += health_siphon
    if epic_monster["HP"] > epic_monster["MaxHP"]:
        epic_monster["HP"] = epic_monster["MaxHP"]
    return player, epic_monster, monsters, monster_list
def summon_undead(player, epic_monster, monsters, monster_list):
    """Summons two zombie minions"""
    cprint(">The %s raises its arms, and two \n zombies rise from the earth." % \
          epic_monster['Name'].lower(), 'magenta')
    monsters += 2
    monster_list.append({"Name": ("Zombie"), "HP": (12), "MaxHP": (12),
                         "Damage": (3), "Carries": [], "XP": (11),
                         "Epic": (False)})
    monster_list.append({"Name": ("Zombie"), "HP": (12), "MaxHP": (12),
                         "Damage": (3), "Carries": [], "XP": (11),
                         "Epic": (False)})
    return player, epic_monster, monsters, monster_list
def summon_nature(player, epic_monster, monsters, monster_list):
    """Summons two wolf minions"""
    cprint(">The %s cries out, and two wolves \n rush to its aid." % epic_monster['Name'].lower(), 'magenta')
    monsters += 2
    monster_list.append({"Name": ("Wolf"), "HP": (12), "MaxHP": (12),
                         "Damage": (3), "Carries": [], "XP": (11),
                         "Epic": (False)})
    monster_list.append({"Name": ("Wolf"), "HP": (12), "MaxHP": (12),
                         "Damage": (3), "Carries": [], "XP": (11),
                         "Epic": (False)})
    return player, epic_monster, monsters, monster_list
def poison(player, epic_monster, monsters, monster_list):
    """Poisons the player"""
    cprint(">The %s spits a yellow-green globule onto you, \n \
          and a burning spreads through your body." % epic_monster['Name'].lower(), 'magenta')
    player.active_status_effects["Poisoned"]={"Command": status_effects.poisoned, "Stack": 1}
    return player.stats, player.defaults, epic_monster, monsters, monster_list, player.active_status_effects
def summon_spider(player, epic_monster, monsters, monster_list):
    """Summons three baby spiders of the same type as epic_monster"""
    cprint(">The %s makes a clicking noise, \n \
          and three of its young come to its aid." % epic_monster['Name'].lower(), 'magenta')
    monsters += 3
    monster_list.append({"Name": ("Baby " + epic_monster["Name"].title()),
                         "HP": (8), "MaxHP": (8), "Damage": (3),
                         "Carries": [], "XP": (7), "Epic": (False)})
    monster_list.append({"Name": ("Baby " + epic_monster["Name"].title()),
                         "HP": (8), "MaxHP": (8), "Damage": (3),
                         "Carries": [], "XP": (7), "Epic": (False)})
    monster_list.append({"Name": ("Baby " + epic_monster["Name"].title()),
                         "HP": (8), "MaxHP": (8), "Damage": (3),
                         "Carries": [], "XP": (7), "Epic": (False)})
    return player, epic_monster, monsters, monster_list
def soak(player, epic_monster, monsters, monster_list):
    """Damages and waterlogs the player"""
    cprint(">The %s sends forth a blast of \n frigid water, soaking you to the bone and \
          freezing your limbs." % epic_monster['Name'].lower(), 'magenta')
    player.active_status_effects["Waterlogged"] = {"Command": status_effects.waterlogged, "Stack": 3}
    player.stats["Damage"] -= random.randint(1, 6)
    return player, epic_monster, monsters, monster_list
def phase_in(player, epic_monster, monsters, monster_list):
    """Increases epic_monster's health, but lowers its dodge chance"""
    cprint(">The %s gathers wisps of the stormclouds \n above into its body, becoming stronger \
          and more uniform." % epic_monster['Name'].lower(), 'magenta')
    epic_monster["HP"] += 10
    player.defaults["MissChance"] -= 1
    return player.stats, player.defaults, epic_monster, monsters, monster_list, \
           player.active_status_effects
def phase_out(player, epic_monster, monsters, monster_list):
    """Decreases epic_monster's healht, but increases its dodge chance"""
    cprint(">The %s raises its arms and... thins, \n \
          becoming less corporeal but weaker." % epic_monster['Name'].lower(), 'magenta')
    player.defaults["MissChance"] += 1
    return player.stats, player.defaults, epic_monster, monsters, monster_list, \
           player.active_status_effects
def flash(player, epic_monster, monsters, monster_list):
    """Increases the player's miss chance"""
    cprint(">The %s shines in a blindingly bright flash \n \
          of light, damaging your eyesight." % epic_monster['Name'].lower(), 'magenta')
    player.defaults["MissChance"] += 1
    return player.stats, player.defaults, epic_monster, monsters, monster_list, \
           player.active_status_effects
def lightning_blast(player, epic_monster, monsters, monster_list):
    """Damages the player, and her maximum health"""
    cprint(">The %s raises an arm and sends a crackling \n \
          bolt of energy towards you." % epic_monster['Name'].lower(), 'magenta')
    player.stats["Health"] -= random.randint(1, player.stats["MaxHealth"])
    player.stats["MaxHealth"] -= random.randint(1, 4)
    return player, epic_monster, monsters, monster_list
def thunder(player, epic_monster, monsters, monster_list):
    """Damages the player"""
    cprint(">The %s begins to pound and pulsate, \n \
          and the world is drowned out by a terrifying roar." % epic_monster['Name'].lower(), 'magenta')
    player.stats["Health"] -= player.stats["Power"]
    return player, epic_monster, monsters, monster_list
