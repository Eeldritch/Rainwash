'''Contains definitions for spells, as well as spell lists'''

import random

from output_mgr import cprint

def flame(monster, monster_list, player):
    '''Damages monster'''
    cprint('>You cast Flame: \n A massive gout of flame bursts forth from your hand.', 'cyan')
    for x in list(monster_list):
        cprint('>You hit the %s.' % x['Name'].lower(), 'blue')
        x['HP'] -= player.stats['Power'] + random.randint(5, 7) * 2
        if x['HP'] <= 0:
            cprint('>The %s was incinerated.' % x['Name'].lower(), 'green')
            player.stats['XP'] += x['XP']
            monster_list.remove(x)
            monster -= 1
    return monster, monster_list, player
def frost(monster, monster_list, player):
    '''Reduces monster's damage'''
    cprint('>You cast Frost: \n A creeping wave of cold spreads forward from you, freezing the \n \
           drenched ground.', 'cyan')
    for x in list(monster_list):
        cprint('>A layer of frost spreads over the %s.' % x['Name'].lower(), 'blue')
        x['Damage'] -= player.stats['Power'] + random.randint(2, 3)
        if x['Damage'] <= 0:
            cprint('>The %s freezes in place, then shatters.' % x['Name'].lower(), 'green')
            player.stats['XP'] += x['XP']
            monster_list.remove(x)
            monster -= 1
    return monster, monster_list, player
def empower(monster, monster_list, player):
    '''Enlarges monster'''
    cprint('>You fumble over the words in the text, and everything near you grows \n 50% larger.', 'cyan')
    for x in monster_list:
        cprint('>The %s becomes an empowered %s.' % (x['Name'].lower(), x['Name'].lower()), 'cyan')
        x['Damage'] += player.stats['Power'] + random.randint(4, 5)
        x['HP'] += player.stats['Power'] + random.randint(2, 3)
        x['XP'] = x['XP'] * 2
        x['Name'] = 'Empowered %s' % x['Name']
    return monster, monster_list, player
def revitalize(monster, monster_list, player):
    '''Restores player's health and grants her XP'''
    cprint('>You cast Revitalize: \n A sudden wave of energy flows through you.', 'cyan')
    player.stats['HP'] = player.stats['MaxHealth']
    player.stats['Stamina'] = player.stats['MaxStamina']
    player.stats['XP'] += player.stats['Power'] * 2
    return monster, monster_list, player
def evaporation(monsters, monster_list, player):
    '''Removes waterlogged status and damages monsters'''
    cprint('>You cast Evaporation: \n A ball of organge-white lights appears above your hand, and \
           \n it begins to suck all nearby moisture into itself,\n \
           drying you off and damaging your foes.', 'cyan')
    if 'Waterlogged' in player.active_status_effects:
        player.active_status_effects.pop('Waterlogged', None)
    for x in list(monster_list):
        x['HP'] -= player.stats['Power'] * random.randint(2, 3) + random.randint(5, 15)
        if x['HP'] <= 0:
            cprint(">The %s's eyes widen in surprise, then crack \n \
                   and explode in a burst of dust, as its body turns to sand." % x['Name'].lower(), 'green')
            player.stats['XP'] += x['XP']
            monster_list.remove(x)
            monsters -= 1
    return monsters, monster_list, player
def mirror(monsters, monster_list, player):
    '''Damages and disorients the monsters'''
    cprint('>You cast Mirror: \n You are surrounded by a shining globe of mirrors. As distant \n \
           lightning flashes, the globe amplifies it, creating a massive \n \
           explosion of light. All nearby creatures are blinded and seared \n by the light.', 'cyan')
    for x in list(monster_list):
        x['HP'] -= player.stats['Power'] * random.randint(2, 3)
        x['Damage'] -= random.randint(4, 7)
        if x['HP'] <= 0 or x['Damage'] <= 0:
            cprint('>The %s claws at its eyes, then disappears in \n a burst of light.' \
                   % x['Name'].lower(), 'green')
            player.stats['XP'] += x['XP']
            monster_list.remove(x)
            monsters -= 1
    return monsters, monster_list, player

BASIC_SPELLS = [flame, frost, empower, revitalize]
ADVANCED_SPELLS = [evaporation, mirror]
