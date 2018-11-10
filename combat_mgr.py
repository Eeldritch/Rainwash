"""Manage combat"""

import random

import status_effects
import output_mgr

from output_mgr import cprint

def monster_attack(monster, monsters, monster_list, monster_list_count, player):
    """Calculates damage from monster attack"""
    vowels = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
    damage = random.randint(1, monster['Damage']+player.stats['Level'])
    player_death = False
    if player.stats['TempDef'] > 0:
        effective_damage = damage - random.randint(int(round(player.stats['Defense']/2)),
                                                   player.stats['Defense']+player.stats['TempDef'])
        player.stats['TempDef'] -= 1
    else:
        effective_damage = damage - (random.randint(round(player.stats['Defense']/2),
                                                    player.stats['Defense']))
    if effective_damage >= player.defaults['EffDmg']:
        if player.stats['TempHealth'] > 0:
            player.stats['TempHealth'] -= damage
            if player.stats['TempHealth'] < 0:
                player.stats['Health'] -= abs(player.stats['TempHealth'])
                player.stats['TempHealth'] = 0
        else:
            player.stats['Health'] -= damage
        if monster_list_count[monster['Name']] != 1:
            if monster['Name'][0] in vowels:
                print('>You were attacked by an %s.' % monster['Name'].lower())
            else:
                print('>You were attacked by a %s.' % monster['Name'].lower())
        else:
            print('You were attacked by the %s.' % monster['Name'].lower())
        bleeding_chance = random.randint(1, player.defaults['BleedChance'])
        if bleeding_chance >= 20 and "Bleeding" not in player.active_status_effects:
            print('>You begin to bleed from a gash in your side.')
            player.active_status_effects['Bleeding'] = {'Command': status_effects.bleeding, 'Stack': 1}
        player = output_mgr.do_dmg_text(player)
        retaliation_damage = random.randint(0, player.equipped['Armor']['Retaliation'])
        if retaliation_damage > 0:
            print('>The %s is burnt by your %s.' %
                  (monster['Name'].lower(), player.equipped['Armor']['Name'].lower()))
            monster['HP'] -= retaliation_damage
            if monster['HP'] <= 0:
                print('>The %s dies.' % monster['Name'].lower())
                monster_list.remove(monster)
                monster -= 1
    else:
        glancing_hit = random.choice([True, False])
        if glancing_hit is True:
            player.stats['Health'] -= player.defaults['GlncngBlwDmg(Plyr)']
            print(">The %s's hit barely grazed you." % monster['Name'].lower())
            player = output_mgr.do_dmg_text(player)
        else:
            if damage > player.defaults['BlckingThrshld']:
                print(">You blocked the %s's attack." % monster['Name'].lower())
            else:
                print('>The %s failed to hit you.' % monster['Name'].lower())
    if monster['Epic'] is True:
        epic_action = random.randint(player.defaults['EpicActnChance'], 4)
        do_epic_action = bool(epic_action == 4)
    if monster['Epic'] is False:
        do_epic_action = False
    return player, do_epic_action, monster, monsters, monster_list, player_death

def do_epic_skill(epic_skills, player, monster, monsters, monster_list):
    """Handles epic skills performed by enemies"""
    skill_type = {
        'Undead': [epic_skills['Siphon'], epic_skills['SummonUndead']],
        'Spider': [epic_skills['Poison'], epic_skills['SummonSpider']],
        'Water': [epic_skills['Siphon'], epic_skills['Soak']],
        'Shadow': [epic_skills['PhaseIn'], epic_skills['PhaseOut'], epic_skills['SummonUndead']],
        'Lightning': [epic_skills['Flash'], epic_skills['LightningBlast']],
        'Thunder': [epic_skills['Thunder']],
    }
    skill_choice = random.choice(skill_type[monster['EpicType']])
    player, monster, monsters, monster_list = skill_choice(status_effects, player, monster, monsters, monster_list)
    return player, monster, monsters, monster_list

def do_player_attack(monster, player):
    """Calculates damage of player attack"""
    if player.stats['Stamina'] <= 0:
        cprint('>You are tiring... Your arms feel weak and your attacks begin to fail.', 'red')
        stamina_mod = player.stats['Stamina']
    if player.stats['Stamina'] == player.stats['MaxStamina']:
        stamina_mod = player.stats['Stamina']
    else:
        stamina_mod = player.defaults['DefStamMod']
    hit_true = random.randint(0, player.stats['Level']+player.defaults['MaxDmgMod'])
    if hit_true <= player.defaults['MissChance']:
        print('>You fail to hit the %s.' % monster['Name'].lower())
        hit = False
        if player.stats['Sneaking'] is True:
            cprint('>The %s sees you!' % monster['Name'].lower(), 'yellow')
            player.stats['Sneaking'] = False
    else:
        damage = random.randint(1, player.stats['Damage'])
        if player.stats['TempDamage'] > 0:
            damage += player.stats['TempDamage']
            player.stats['TempDamage'] = 0
        if player.stats['Sneaking'] is True:
            damage = damage*player.defaults['SnkAtkMult']
            print('>You sneak up on the %s.' % monster['Name'].lower())
            print('>You stop sneaking.')
            player.stats['Sneaking'] = False
        monster['HP'] -= damage + stamina_mod + player.defaults['StamModXtra']
        cprint('>You hit the %s.' % monster['Name'].lower(), 'blue')
        hit = True
    return monster, hit, player
