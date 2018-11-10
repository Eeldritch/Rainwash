'''Contains definitions for status effects'''

import random

def sickened(player):
    '''Nausea-based sickness, food poisoning, etc.'''
    stack = player.active_status_effects['Sickened']['Stack']
    get_sick = random.randint(1, 3)
    if stack <= 0:
        print('>You are no longer sickened.')
        effects_to_remove = 'Sickened'
        get_sick = 0
    else:
        effects_to_remove = None
    if get_sick == 3:
        if stack == 1:
            print('>A wave of nausea rushes over you.')
            stack += 1
            player.stats['Stamina'] -= 3
        elif stack == 2:
            print('>You double over from a cramp in your gut.')
            stack += 1
            player.stats['Stamina'] -= 3
            player.stats['Health'] -= 1
        elif stack == 3:
            print('>Nausea overpowers you, and you hurl on the ground.')
            stack += 1
            player.stats['Stamina'] -= 3
            player.stats['Health'] -= 1
        elif stack > 3:
            print('>Whatever ails you is beginning to do permanent damage. \n \
                  You feel your arms grow weak...')
            stack += 1
            player.stats['Damage'] -= 1
            if player.stats['Damage'] < 0:
                player.stats['Damage'] = 0
            player.stats['Stamina'] -= 3
            player.stats['Health'] -= 1
    if get_sick == 1:
        stack -= 1
        print('>Some of the pressure in your gut seems to be relieved.')
    player.active_status_effects['Sickened']['Stack'] = stack
    return player, effects_to_remove

def poisoned(player):
    '''Venoms from spiders and epic effects'''
    stack = player.active_status_effects['Poisoned']['Stack']
    get_poison = random.randint(1, 4)
    if stack <= 0:
        print('>You are no longer poisoned.')
        effects_to_remove = 'Poisoned'
        get_poison = 0
    else:
        effects_to_remove = None
    if get_poison >= 2:
        if stack == 1:
            print('>Your blood feels as if it is boiling as poison \n rages through you.')
            stack += 1
            player.stats['Health'] -= 1
        elif stack == 2:
            print('>You scream in pain as the poison courses through your heart.')
            stack += 1
            player.stats['Health'] -= 2
        elif stack > 2 and stack < 5:
            print('>Your body fails as the poison destroys it.')
            stack += 1
            player.stats['Health'] -= 2
            player.stats['Damage'] -= 2
            player.stats['MaxHealth'] -= 1
            player.stats['MaxStamina'] -= 1
        elif stack == 5:
            print('>As the poison reaches the farthest corners of your body, you die.')
            player.stats['Health'] = 0
    if get_poison == 1:
        stack -= 1
        print('>Somehow, your body recovers a little bit from the poison.')
    player.active_status_effects['Poisoned']['Stack'] = stack
    return player, effects_to_remove

def waterlogged(player):
    '''The repercussions of prolonged water exposure'''
    stack = player.active_status_effects['Waterlogged']['Stack']
    get_waterlogged = random.randint(1, 4)
    if stack <= 0:
        print('>You manage to completely dry off. You feel much better.')
        effects_to_remove = 'Waterlogged'
        get_waterlogged = 0
    else:
        effects_to_remove = None
    if get_waterlogged == 4:
        if stack == 1:
            print(">You are soaked to the bone. You can't seem to shake the chill that has \n seeped under your skin.")
            stack += 1
            player.stats['Stamina'] -= 2
        elif stack == 2:
            print('>Your skin is wrinkling and uncontrollable shivering wracks your body.')
            stack += 1
            player.stats['Stamina'] -= 2
            player.stats['Health'] -= 1
        elif stack == 3:
            print(">You can't focus. Your whole body is numb. You desperately fight the lethargy.")
            player.stats['Stamina'] -= 1
            player.stats['Health'] -= 2
            player.stats['Damage'] -= 1
    if get_waterlogged == 1:
        stack -= 1
        print('>You dry off a bit, and some of the cold leaves your body.')
    if get_waterlogged in [2, 3]:
        player.stats['Stamina'] -= 1
    player.active_status_effects['Waterlogged']['Stack'] = stack
    return player, effects_to_remove

def bleeding(player):
    '''Bleeding from particularly nasty wounds'''
    stack = player.active_status_effects['Bleeding']['Stack']
    increased_bleeding = random.randint(1, 3)
    if stack <= 0:
        print('>You finally stop the bleeding, and you feel a bit more \n level-headed. \
              Nevertheless, you need rest.')
        player.stats['Stamina'] = -1
        effects_to_remove = 'Bleeding'
        increased_bleeding = 0
    else:
        effects_to_remove = None
    if increased_bleeding == 3:
        if stack == 1:
            print('>Hot blood soaks through your clothes, and you stagger from \n your wounds.')
            stack += 1
            player.stats['Health'] -= 2
        elif stack == 2:
            print('>Your blood loss worsens. Your vision blurs and you stumble.')
            stack += 1
            player.stats['Health'] -= 2
            player.stats['Damage'] -= 1
            player.stats['Stamina'] -= 3
        elif stack == 3:
            print('>You have lost too much blood. You desperately cling to consciousness.')
            player.stats['Health'] -= 2
            player.stats['Damage'] -= 1
            player.stats['Stamina'] -= 5
    if increased_bleeding == 1:
        stack -= 1
        print('>You are able to stop some of the bleeding from your wounds.')
    if increased_bleeding == 2:
        print('>You are suffering from blood loss.')
        player.stats['Health'] -= 1
        player.stats['Stamina'] -= 1
    player.active_status_effects['Bleeding']['Stack'] = stack
    return player, effects_to_remove

def invigorating(player):
    '''From a bard's Invigorating Song'''
    stack = player.active_status_effects['Invigorating Song']['Stack']
    if stack == 10:
        print('>The Invigorating Song makes you feel healthy and strong.')
        player.stats['MaxHealth'] += 10
        player.stats['Health'] += 10
        stack -= 1
        effects_to_remove = None
    if stack == 0:
        print('>The effects of the Invigorating Song have worn off.')
        player.stats['MaxHealth'] -= 10
        player.stats['Health'] -= 10
        effects_to_remove = 'Invigorating Song'
    else:
        print('>You benefit from the Invigorating Song.')
        player.active_status_effects['Song of Courage']['Stack'] -= 1
        effects_to_remove = None
    player.active_status_effects['Invigorating Song']['Stack'] = stack
    return player, effects_to_remove

def strengthening(player):
    '''From a bard's Strengthening Song'''
    stack = player.active_status_effects['Strengthening Song']['Stack']
    if stack == 0:
        print('>The Strengthening Song has worn off.')
        player.stats['Damage'] -= 10
        effects_to_remove = 'Strengthening Song'
    else:
        print('>The Strengthening Song makes you feel strong and powerful, \n \
              as if you could defeat any foe.')
        player.stats['Damage'] += 1
        player.active_status_effects['Song of Courage']['Stack'] -= 1
        effects_to_remove = None
    return player, effects_to_remove

def encouragement(player):
    '''From a bard's Song of Courage'''
    stack = player.active_status_effects['Song of Courage']['Stack']
    if stack == 0:
        print('>The Song of Courage has faded from your ears, \n \
              and some of your old fears return...')
        player.stats['Defense'] -= 20
        effects_to_remove = 'Song of Courage'
    else:
        print('>The Song of Courage resonates in your mind, hardening your resolve. \n \
              You handle yourself with calm, calculating confidence.')
        player.stats['Defense'] += 2
        player.active_status_effects['Song of Courage']['Stack'] -= 1
        effects_to_remove = None
    return player, effects_to_remove
