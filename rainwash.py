def main():
    import math
    import os
    import random
    import re
    import smtplib
    import sys
    import shelve
    import time
    import zipfile

    import combat_mgr
    import gen_mgr
    import inv_mgr
    import status_effects
    import save_mgr
    import dicts
    import output_mgr
    import level_mgr
    import map_mgr
    import spells
    import crafting_mgr

    from dicts import TRAVELLERS as travellers
    from output_mgr import cprint
###
    from dbm import dumb
    from smtplib import SMTPAuthenticationError
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from email import encoders
    from collections import Counter

    save_data = shelve.open('save_data')
    if save_data['SaveActive'] is False:
        if save_data['Email'] is None:
            print('A valid email is required. Please run Setup.')
            sys.exit('Invalid email!')
        class PlayerStruct:
            def __init__(self, stats, pclass):
                self.stats = stats
                self.pclass = pclass
                self.stats['XP'] = 0
                self.stats['Hunger'] = 0
                self.stats['Insanity'] = 0
                self.stats['Sneaking'] = False
                self.stats['TempHealth'] = 0
                self.stats['TempDamage'] = 0
                self.stats['TempDef'] = 0
                self.stats['Level'] = 1
            learned_commands = []
            inventory = ['Musty Spellbook', 'Strike-Stone', 'Bandage Roll', 'Raw Venison Steak',
                         'Red Apple', 'Red Apple']
            equipped = {'Weapon': {'Name': 'Pointed Stick', 'Type': 'Weapon', 'Bonus': 0,
                                   'BonusType': 'Add', 'Power': 0, 'Defense': 0, 'Stamina': 0},
                        'Armor': {'Name': 'Soaked Tunic', 'Bonus': 0, 'Retaliation': 0,
                                  'Damage': 0, 'Stamina': 0, 'Power': 0, 'SentenceStructure': ' a',
                                  'Type': 'Armor'}}
            actions = {'Attacks': 0, 'Explorations': 0, 'Kills': 0, 'EpicKills': 0,
                       'MonsterTypes': 0, 'Hidden': 0, 'Eaten': 0, 'TravellersEncountered': 0,
                       'Spells': 0, 'Slept': 0, 'Waterlogged': 0, 'Poisoned': 0, 'Cooked': 0,
                       'Crafted': 0, 'FiresLit': 0, 'Blocked': 0, 'Foraged': 0, 'Misses': 0}
            gold = 0
            active_status_effects = {}
            defaults = dicts.player_defaults
        t1, t2 = level_mgr.player_type_choice()
        player = PlayerStruct(t1, t2)
        local_map, container_map, item_map, x_coord, \
        y_coord, coords, monster_list, monsters, monster_queue, container_map_queue, \
        things_changed, fire_lit, \
        container, item, variant, variant_chosen = save_mgr.save_primer()
        item_map[coords] = []
        biome_choice = random.randint(1, 100)
        biome_choice = str(biome_choice)
        biome = gen_mgr.get_biome(biome_choice)
        local_map[coords] = biome
        things_changed.append(1)
        for x in travellers:
            travellers[x]['XCoord'] = 0
            travellers[x]['YCoord'] = 1
            travellers[x]['Coords'] = '%s, %s' % (str(travellers[x]['XCoord']), str(travellers[x]['YCoord']))
        travellers_here = ()
        output_mgr.area_status(things_changed, biome, dicts.CONTAINERS, item, monster_list,
                               variant_chosen, variant, gen_mgr.VARIANT_DESCRIPTIONS, item_map,
                               coords)
        save_data.close()
    else:
        #try:
        if save_data['Email'] is None:
            print('A valid email is required. Please run Setup.')
            sys.exit('Invalid email!')
        print('>Loading last saved game...')
        player, biome, local_map, container_map, item_map, x_coord, y_coord, \
        coords, fire_lit, monster_list, monsters, monster_queue, travellers, \
        travellers_here = save_mgr.load_save(save_data)
        save_data.close()
        travellers_here = ()
        things_changed = []
        container_map_queue = []
        variant = None
        variant_chosen = False
        #except KeyError as e:
        #    print(e)
        #    sys.exit('Save data corrupted or missing! \n This error may occur during save file editing.')"""
    auto_explore = False
    container = []
    item = None
    discovered = True
    things_changed = []
    vowels = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
    vowel_word = {'C': 'a', 'V': 'an'}
    #Writes the initial variables and grabs the first location.
    while True:
        while True:
            player = level_mgr.level_check(player, dicts.LEVELS)
            try:
                container_map[coords] = container_map[coords]
                print(' \n')
            except KeyError:
                print('>You have not explored this area.\n')
            if monsters > 0:
                if player.stats['Sneaking'] is False:
                    check_epic_action = []
                    epic_monsters = []
                    monster_list_read = []
                    for x in monster_list:
                        monster_list_read.append(x['Name'])
                    monster_list_count = Counter(monster_list_read)
                    for x in monster_list:
                        player, do_epic_action, x, monsters, monster_list, player_death = combat_mgr.monster_attack(x, monsters, monster_list, monster_list_count, player)
                        #player_vals['Attacked'] += 1
                        if do_epic_action is True:
                            check_epic_action.append(do_epic_action)
                            epic_monsters.append(x)
                            if player_death is True:
                                break
                    if True in check_epic_action:
                        for x in epic_monsters:
                            player, x, monsters, monster_list = combat_mgr.do_epic_skill(player, x, monsters, monster_list, dicts.MONSTER_COMPENDIUM)
                if player.stats['Sneaking'] is True:
                    try:
                        hidden = random.randint(player.defaults['PrlngStlth'], player.stats['Stamina'])
                    except ValueError:
                        print('>You have become too tired to hide effectively--your exhaustion makes you \n trip and flounder.')
                        player.stats['Sneaking'] = False
                        hidden = 0
                        check_epic_action = []
                        epic_monsters = []
                        monster_list_read = []
                        for x in monster_list:
                            monster_list_read.append(x['Name'])
                        monster_list_count = Counter(monster_list_read)
                        for x in monster_list:
                            player, do_epic_action, x, monsters, monster_list, player_death = combat_mgr.monster_attack(x, monsters, monster_list, monster_list_count)
                            #player_vals['Attacked'] += 1
                            if do_epic_action is True:
                                check_epic_action.append(do_epic_action)
                                epic_monsters.append(x)
                            if player_death is True:
                                break
                        if True in check_epic_action:
                            for x in epic_monsters:
                                player.stats, x, monsters, monster_list, player.active_status_effects = combat_mgr.do_epic_skill(player.stats, player.defaults, x, monsters, monster_list, dicts.MONSTER_COMPENDIUM, player.active_status_effects)
                    if hidden <= 5:
                        print('You have been noticed! You stop hiding.')
                        player.stats['Sneaking'] = False
                        check_epic_action = []
                        epic_monsters = []
                        monster_list_read = []
                        for x in monster_list:
                            monster_list_read.append(x['Name'])
                        monster_list_count = Counter(monster_list_read)
                        for x in monster_list:
                            player, do_epic_action, x, monsters, monster_list, player_death = combat_mgr.monster_attack(x, monsters, monster_list, monster_list_count, player)
                            #player_vals['Attacked'] += 1
                            if do_epic_action is True:
                                check_epic_action.append(do_epic_action)
                                epic_monsters.append(x)
                            if player_death is True:
                                break
                        if True in check_epic_action:
                            for x in epic_monsters:
                                player.stats, x, monsters, monster_list, player.active_status_effects = combat_mgr.do_epic_skill(player.stats, player.defaults, x, monsters, monster_list, dicts.MONSTER_COMPENDIUM, player.active_status_effects)
                    else:
                        if monsters > 1:
                            print('>You remain hidden from the monsters.')
                        else:
                            print('>You remain hidden from the monster.')
            if player.active_status_effects and player.stats['Health'] > 0:
                effects_to_remove = []
                #print(player.active_status_effects)
                for x in list(player.active_status_effects):
                    #print(x)
                    player, effect_to_remove = player.active_status_effects[x]['Command'](player)
                    if effect_to_remove != None:
                        effects_to_remove.append(effect_to_remove)
                for x in effects_to_remove:
                    player.active_status_effects.pop(x, None)
            if player.stats['Sneaking'] is True:
                player.stats['Stamina'] -= player.defaults['SnkStm']
                print('>You are sneaking.')
            if player.stats['Health'] <= 0:
                cprint('>You have died!', 'red')
                save_data = shelve.open('save_data')
                save_data['SaveActive'] = False
                time.sleep(5)
                sys.exit('Death!')
            player.stats['Hunger'] += player.defaults['HngrInc']
            if player.stats['Stamina'] > 0:
                player.stats['Fatigue'] = 0
            if player.stats['Stamina'] <= player.defaults['TireThrshld'] and player.stats['Fatigue'] < 15:
                print('>You are tired.')
                player.stats['Fatigue'] += player.defaults['FtgueRate']
            if player.stats['Fatigue'] >= player.defaults['FtgueThrshld']:
                if player.defaults['FtgueTxt'] is True:
                    print('>You are fatigued. The effects of sleep depravation may be \n permanant...')
                player.stats['MaxStamina'] -= player.defaults['FtgueDmg']
            player = output_mgr.report_hunger(player)
            if fire_lit is True:
                print('>Your fire glows warmly, offering a peaceful beacon of respite.')
            if travellers_here:
                #print(travellers_here)
                print('>There is a %s on the path here.' % (travellers_here['Name'].lower()))
            if isinstance(player.stats['Damage'], int) is False:
                player.stats['Damage'] = int(round(player.stats['Damage']))
            complete = False
            #print(travellers)
            #print(player.active_status_effects)
            variant_chosen = False
            if auto_explore is False:
                enter = input(': ')
                if enter != ('Repeat.'):
                    action = enter
                action = action.upper()
                try:
                    if action[len(action) - 1] != '.' and action != ('DEV:'):
                        print('>>>Invalid input. Periods are required after commands.')
                        break
                except IndexError:
                    pass
                #player_vals['actions'] += 1
                if player.stats['Insanity'] >= 10:
                    crazy = random.randint(player.stats['Insanity'], 50)
                    if crazy == 50:
                        crazy = random.randint(1, 3)
                        if crazy == 1:
                            print('>You frown at the voice in your head. \n Why would you possibly \n want to do that? Instead, you decide to \n go north.')
                            action = 'GO N.'
                        if crazy == 2:
                            if type(Iventory[0]) != str:
                                print('>You cock your head to the side at the command \n in you head. Why would you want to do that? Instead, you decide \n to \n drop your %s.' % (player.inventory[0]['Name'].lower))
                                action = 'DROP %s.' % player.inventory[0]['Name'].upper()
                            else:
                                print('>You cock your head to the side at the command \n in you head. Why would you want to do that? Instead, you decide \n to \n drop your %s.' % (player.inventory[0].lower))
                                action = 'DROP %s.' % player.inventory[0].upper()
                        if crazy == 3:
                            print(">You shake your head in denial. You don't really \n was to do that. Instead, you \n check your coin pouch.")
                            action = 'CHECK COIN POUCH.'
                for x in dicts.ALT_COMMANDS_LIST:
                    y = r'\b%s\b' % x
                    alts = re.search(y, action)
                    if alts:
                        action = re.sub(y, dicts.ALT_COMMANDS[x], action, flags = re.IGNORECASE)
            else:
                action = 'EXPLORE.'
                print('>You explore the area.')
                auto_explore = False
            multi_action = []
            attack_interpret = re.search(r'\bATTACK\b (.*).', action)
            cook_interpret = re.search(r'\bCOOK\b (.*).', action)
            drop_interpret = re.search(r'\bDROP\b (.*).', action)
            eat_interpret = re.search(r'\bEAT\b (.*).', action)
            equip_interpret = re.search(r'\bEQUIP\b (.*).', action)
            go_interpret = re.search(r'\bGO\b (.*).', action)
            search_interpret = re.search(r'\bSEARCH\b (.*).', action)
            take_interpret = re.search(r'\bTAKE\b (.*).', action)
            talk_interpret = re.search(r'\bTALK TO\b (.*).', action)
            use_interpret = re.search(r'\bUSE\b (.*).', action)
            multi_commands_list = [attack_interpret, cook_interpret, drop_interpret,
                               eat_interpret, equip_interpret, go_interpret,
                               search_interpret, take_interpret, talk_interpret,
                               use_interpret]
            for x in multi_commands_list:
                try: multi_action.append(x.groups()[0])
                except AttributeError: pass
            if len(multi_action) > 1:
                print("You can't do all of that at once!")
                break
            if attack_interpret:
                complete = True
                if monsters == 0:
                    print('>You flail wildly at the air.')
                    player.stats['Insanity']+= 1
                    break
                attack_interpret = attack_interpret.groups()[0]
                found_monster = False
                for x in monster_list:
                    if attack_interpret == x['Name'].upper():
                        x, hit, player= combat_mgr.do_player_attack(x, player)
                        #player_vals['Attacks'] += 1
                        player.stats['Stamina'] -= player.defaults['AtkStam']
                        if hit is True:
                            if x['HP'] <= 0:
                                cprint('>You killed the %s.' % (x['Name'].lower()), 'green')
                                healed = random.randint(player.defaults['KillHealChance'], 3)
                                if healed == 3:
                                    player.stats['Health'] += player.defaults['KillHealth']
                                    if player.stats['Health'] >= player.stats['MaxHealth']:
                                        player.stats['Health'] = player.stats['MaxHealth']
                                    print('>You feel a surge of relief.')
                                monster_list.remove(x)
                                monsters -= 1
                                player.stats['XP'] += x['XP'] + player.defaults['XPMod']
                                player, item_map = inv_mgr.loot_monster(x, player, item_map, coords, dicts.USABLES, dicts.USABLES_LIST)
                            else:
                                output_mgr.report_monster_damage(x)
                        break
                    else:
                        try:
                            for x in monster_list:
                                if found_monster is False:
                                    if x['Name'].title() in dicts.INTERPRET_COMPREHENSIONS['Monsters'][attack_interpret.title()]:
                                        x, hit, player = combat_mgr.do_player_attack(x, player)
                                        #player_vals['Attacks'] += 1
                                        player.stats['Stamina'] -= player.defaults['AtkStam']
                                        if hit is True:
                                            if x['HP'] <= 0:
                                                cprint('>You killed the %s.' % x['Name'].lower(), 'green')
                                                healed = random.randint(player.defaults['KillHealChance'], 3)
                                                if healed == 3:
                                                    player.stats['Health'] += player.defaults['KillHealth']
                                                    if player.stats['Health'] >= player.stats['MaxHealth']:
                                                        player.stats['Health'] = player.stats['MaxHealth']
                                                    print('>You feel a surge of relief.')
                                                monster_list.remove(x)
                                                monsters -= 1
                                                player.stats['XP'] += x['XP'] + player.defaults['XPMod']
                                                player, item_map = inv_mgr.loot_monster(x, player, item_map, coords, dicts.USABLES, dicts.USABLES_LIST)
                                            else:
                                                output_mgr.report_monster_damage(x)
                                        found_monster = True
                        except KeyError:
                            if attack_interpret[0] in vowels:
                                print(">You don't see an %s nearby." % attack_interpret.lower())
                            else:
                                print(">You don't see a %s nearby." % attack_interpret.lower())
            if cook_interpret:
                complete = True
                cook_interpret = cook_interpret.groups()[0]
                cook_interpret = cook_interpret.lower()
                cook_ready = False
                if fire_lit is False:
                    print('>You need a fire to cook food!')
                    player.stats['Insanity'] += 1
                    break
                for x in player.inventory:
                    try:
                        if cook_interpret == x['Name'].lower():
                            cook_ready = True
                    except TypeError:
                        if cook_interpret == x.lower():
                            cook_ready = True
                if cook_ready is True:
                    try:
                        player.inventory.append(dicts.COOKING_CHART[cook_interpret.title()])
                        player.inventory.remove(cook_interpret.title())
                        print('>You cook your %s.' % cook_interpret)
                    except KeyError:
                        print(">You can't cook that.")
                else:
                    if cook_interpret == 'meal':
                        meal_cooked = False
                        all_ing = True
                        print('>You prepare an area in which multiple ingredients can be added.')
                        temp_meal_ingredients = input('What ingredients do you use? (Use a comma for seperation.) \n : ')
                        temp_meal_ingredients = temp_meal_ingredients.split(', ')
                        meal_ingredients = []
                        for x in temp_meal_ingredients:
                            meal_ingredients.append(x.title())
                        for x in meal_ingredients:
                            if x not in player.inventory:
                                for y in player.inventory:
                                    if type(y) != str and y['Name'] in meal_ingredients:
                                        all_ing = False
                                        if y['Name'][0] in vowels:
                                            print(">You can't cook with an %s." % y['Name'].lower())
                                            break
                                        else:
                                            print(">You can't cook with a %s." % y['Name'].lower())
                                            break
                                if x[0] in vowels:
                                    all_ing = False
                                    print(">You don't have an %s." % x.lower())
                                    break
                                else:
                                    all_ing = False
                                    print(">You don't have a %s." % x.lower())
                                    break
                        if all_ing is True:
                            for x in dicts.MEAL_CHART:
                                if dicts.MEAL_CHART[x] == meal_ingredients:
                                    meal_cooked = True
                                    player.inventory.append(x)
                                    for y in meal_ingredients:
                                        player.inventory.remove(y)
                                    if x[0] in vowels:
                                        print('>You prepare an %s.' % x.lower())
                                    else:
                                        print('>You prepare a %s.' % x.lower())
                            if meal_cooked is False:
                                print(">You cook your ingredients together... but they don't smell very \n appealing. You decide not to eat the results.")
                                for y in meal_ingredients:
                                    player.inventory.remove(y)
                        if all_ing is False:
                            break
                    else:
                        print(">You can't cook imaginary food...")
                        player.stats['Insanity'] += 3
            if drop_interpret:
                complete = True
                drop_interpret = drop_interpret.groups()[0]
                drop_interpret = drop_interpret.lower()
                dropped = False
                for x in player.inventory:
                    if type(x) == str:
                        if drop_interpret == x.lower():
                            print('>You drop your %s.' % drop_interpret)
                            player.inventory.remove(x)
                            item_map[coords].append(x)
                            dropped = True
                            break
                    else:
                        if drop_interpret == x['Name'].lower():
                            print('>You drop your %s.' % drop_interpret)
                            player.inventory.remove(x)
                            item_map[coords].append(x)
                            dropped = True
                            break
                if dropped is False:
                    print(">You don't have a %s..." % drop_interpret)
                    player.stats['Insanity'] += 1
            if eat_interpret:
                complete = True
                eat_interpret = eat_interpret.groups()[0]
                eat_interpret = eat_interpret.title()
                in_inventory = False
                if eat_interpret not in player.inventory:
                    for x in player.inventory:
                        try:
                            if eat_interpret == x['Name']:
                                print(">Try as you might, you can't physically eat that.")
                                in_inventory = True
                                break
                        except TypeError:
                            pass
                else:
                    in_inventory = True
                if in_inventory is False:
                    print(">You don't have that in your player.inventory...")
                    break
                try:
                    food = dicts.EDIBLES[eat_interpret]
                except KeyError:
                    print('>Try as you might, you are unable to bring yourself \n to eat that.')
                    break
                player.inventory.remove(eat_interpret)
                print('>You eat your %s.' % eat_interpret.lower())
                if food['Meal'] is True:
                    print('>You sit down for a delicious full meal--a luxury seldom enjoyed \n by travellers.')
                    player.stats['MaxHealth'] += 1
                    player.stats['Health'] += 1
                if food['Sickening'] is True:
                    print("It doesn't sit quite right in your stomach...")
                    player.active_status_effects['Sickened'] = {'Command': status_effects.sickened, 'Stack': 2}
                if food['Satiating'] is True:
                    print('>You feel your hunger dissipate.')
                    player.stats['Hunger'] = 0
                if food['Bonus'] > 0:
                    print('>With your full stomach comes a surge of health.')
                    player.stats['Health'] += food['Bonus'] + player.defaults['MealMod']
                    if player.stats['Health'] > player.stats['MaxHealth']:
                        player.stats['Health'] = player.stats['MaxHealth']
                if food['Bonus'] < 0 and food['Bonus'] > -5:
                    print('>You choke on the %s.' % eat_interpret.lower())
                    player.stats['Health'] += food['Bonus']
                if food['Bonus'] <= -5:
                    print('>The %s slices your tonuge and the \n back of your throat.' % eat_interpret.lower())
                    player.stats['Health'] += food['Bonus']
            if equip_interpret:
                complete = True
                equip_interpret = equip_interpret.groups()[0]
                equip_interpret = equip_interpret.title()
                something_equipped = False
                for x in player.inventory:
                    if type(x) != str:
                        if x['Name'] == equip_interpret:
                            if x['Type'] == 'Weapon' or x['Type'] == 'Armor':
                                player = inv_mgr.equip_item(player, dicts.USABLES, x)
                                player.inventory.remove(x)
                                print('>You equip your %s.' % equip_interpret.lower())
                                something_equipped = True
                                break
                try:
                    if dicts.USABLES[equip_interpret]['Type'] == 'Potion':
                        player.inventory.remove(equip_interpret)
                        print('>You pour out your potion and stick the empty bottle on your little toe. \n But... why?')
                        player.stats['Insanity'] += 1
                    elif equip_interpret in player.inventory:
                        player.inventory.remove(equip_interpret)
                        print(">You shove the %s in your ear. \n It's rather painful." % equip_interpret.lower())
                        player.stats['Insanity'] += 1
                    else:
                        if something_equipped is False:
                            print('>You attempt to wear your imaginary %s...' % equip_interpret.lower())
                            player.stats['Insanity'] += 1
                except KeyError:
                    pass
            if go_interpret:
                complete = True
                if monsters > 0:
                    if player.stats['Sneaking'] is True:
                        sneak_away = random.randint(1, 3)
                        if sneak_away == 1:
                            print('>The monsters see you and block your path!')
                            player.stats['Sneaking'] = False
                            break
                        else:
                            print('>You slip away from the monsters.')
                    else:
                        print('>The monsters block your path!')
                        break
                elif player.stats['Fatigue'] >= 10:
                    print('>You are too tired to travel. You must rest.')
                    break
                elif monster_queue:
                    Ambush = random.randint(player.defaults['AmbushChance'], 2)
                    if Ambush == 2:
                        if monster_queue[0]['Name'][0] in vowels:
                            print('>As you try to leave, you are ambushed by an %s!' % monster_queue[0]['Name'].lower())
                        else:
                            print('>As you try to leave, you are ambushed by a %s!' % monster_queue[0]['Name'].lower())
                        monsters += len(monster_queue)
                        for x in monster_queue:
                            monster_list.append(x)
                        monster_queue = []
                        #player_vals['Ambushed'] += 1
                        break
                altar_chance = random.randint(player.defaults['AltrChance'], 20)
                if altar_chance == 20:
                    print('>As you walk, you come across a sparse circle of trees with an altar \n in the center. Do you approach it?')
                    approach = input('(Y/N): ')
                    if approach.upper() == 'Y':
                        player = crafting_mgr.combo_altar(player, dicts.USABLES_LIST, dicts.USABLES, dicts.PREFIX_MODIFIERS)
                    else:
                        print('>You move on.')
                Possibilities = ['N', 'E', 'S', 'W']
                go_interpret = go_interpret.groups()[0]
                if go_interpret in Possibilities:
                    travellers_here = []
                    if fire_lit is True:
                        container_map[coords].append('ASH PILE')
                        fire_lit = False
                    x_coord, y_coord = map_mgr.get_direction(go_interpret, x_coord, y_coord)
                    coords = '%s, %s' % (str(x_coord), str(y_coord))
                    for x in travellers:
                        do_trav_move = random.randint(0, 5)
                        if do_trav_move == 0:
                            coord_change = random.choice(['XCoord', 'YCoord'])
                            travellers[x][coord_change]+= random.choice([(-1), (1)])
                            travellers[x]['Coords'] = (str(travellers[x]['XCoord']) + ', ' + str(travellers[x]['YCoord']))
                            if travellers[x]['Coords'] == coords:
                                travellers_here.append(travellers[x])
                    while len(travellers_here) > 1:
                        travellers[travellers_here[(len(travellers_here) - 1)]]['XCoord'] -= 1
                        travellers_here.remove(travellers_here[(len(travellers_here) - 1)])
                    if len(travellers_here) > 0:
                        print('As you walk, you see another figure along the barren landscape. \n He hails you as a friend and fellow traveller.')
                    else:
                        travellers_here = ()
                    traveller_choose = None
                    for x in travellers_here:
                        print(x)
                        traveller_choose = x
                    if traveller_choose != None:
                        travellers_here = travellers_here[0]
                    item_map[coords] = []
                    if coords in local_map:
                        print(coords, local_map)
                        discovered = True
                    else:
                        discovered = False
                    if discovered is True:
                        biome = local_map[coords]
                        things_changed.append(1)
                    if discovered is False:
                        try:
                            local_map[coords] = gen_mgr.MAP_SPECIALS['Coords'][coords]
                            biome = local_map[coords]
                            variant_chosen = False
                            for x in gen_mgr.MAP_SPECIALS['Monsters'][biome]:
                                monsters += 1
                                monster_list.append(x)
                            print(gen_mgr.MAP_SPECIAL['Descriptions'][biome])
                        except KeyError:
                            same_biome = random.randint(1, 4)
                            if same_biome == 2:
                                local_map[coords] = biome
                                variant_chosen = False
                            else:
                                biome_choice = random.randint(1, 100)
                                biome_choice = str(biome_choice)
                                biome = gen_mgr.get_biome(biome_choice)
                                local_map[(coords)] = biome
                                variant_chance = random.randint(player.defaults['VrntChance'], 8)
                                if variant_chance == 8:
                                    variant = random.choice(gen_mgr.VARIANTS[biome])
                                    variant_chosen = True
                                    container_map_queue, monster_queue = gen_mgr.variant_actions(container_map_queue, monster_queue, variant)
                                else:
                                    variant_chosen = False
                            things_changed.append(1)
                            monsters = random.randint(2, 5)
                            if monsters > 0:
                                new_monsters_chosen = 0
                                while new_monsters_chosen < monsters:
                                    new_monster, biome_match = gen_mgr.get_new_monster(dicts.MONSTER_COMPENDIUM, dicts.MONSTER_DICT, player, biome)
                                    if biome_match is True:
                                        monster_list.append(new_monster)
                                        new_monsters_chosen += 1
                                    if biome_match is False:
                                        monsters -= 1
                                if monster_list:
                                    things_changed.append(5)
                    if player.stats['Sneaking'] is True:
                        player.stats['Stamina'] -= 2 * player.defaults['WlkngStamLoss'] + dicts.BIOME_TRAV_DIFFICULTY[biome]
                    else:
                        player.stats['Stamina'] -= player.defaults['WlkngStamLoss'] + dicts.BIOME_TRAV_DIFFICULTY[biome]
                    if local_map[coords] == 'the Mountains':
                        see_peak = random.randint(0, 3)
                        if see_peak == 3:
                            print('>From this high peak, you can see the terrain around and below you.')
                            nter = '%s, %s' % (str(x_coord), str(y_coord+1))
                            ster = '%s, %s' % (str(x_coord), str(y_coord-1))
                            eter = '%s, %s' % (str(x_coord+1), str(y_coord))
                            wter = '%s, %s' % (str(x_coord-1), str(y_coord))
                            ters = [nter, ster, eter, wter]
                            ter_dir = {nter: 'north', ster: 'south', eter: 'east',
                                    wter: 'west'}
                            for x in ters:
                                if x in local_map:
                                    print('>To the %s you see %s.' % (ter_dir[x], local_map[x].lower()))
                                else:
                                    biome_choice = random.randint(1, 100)
                                    biome_choice = str(biome_choice)
                                    biome = gen_mgr.get_biome(biome_choice)
                                    local_map[x] = biome
                                    print('>To the %s you see %s.' % (ter_dir[x], local_map[x].lower()))
                            for x in travellers:
                                if travellers[x]['Coords'] in ters:
                                    for y in ters:
                                        if y == travellers[x]['Coords']:
                                            trav_ter_dir = y
                                    if trav_ter_dir == nter:
                                        trav_ter_dir = 'north'
                                    elif trav_ter_dir == ster:
                                        trav_ter_dir = 'south'
                                    elif trav_ter_dir == eter:
                                        trav_ter_dir = 'east'
                                    elif trav_ter_dir == wter:
                                        trav_ter_dir = 'west'
                                    print('>You see another figure walking on the path to the %s.' % trav_ter_dir)
                else:
                    print(">You don't know how to do that.")
                if monsters == 0 and variant_chosen is False:
                    auto_explore = True
                else:
                    auto_explore = False
            if search_interpret:
                complete = True
                search_interpret = (search_interpret.groups()[0])
                item_category = None
                try:
                    if container_map[coords]:
                        container_map[coords] = container_map[coords]
                except KeyError:
                    for x in player.inventory:
                        if type(x) != str and search_interpret.lower() == x['Name'].lower():
                            print(">You can't search an item.")
                            break
                        elif search_interpret.lower() == x.lower():
                            print(">You can't search an item.")
                            break
                    else:
                        print('>You must first explore this area.')
                    break
                for x in container_map[coords]:
                    if x != (None):
                        x = x.upper()
                        if search_interpret == x.upper():
                            item_types = dicts.CONTAINERS[search_interpret]['Holds']
                            item_category = random.choice(item_types)
                            if item_category == ('Misc'):
                                item = random.choice(dicts.ITEMS)
                                if len(player.inventory)<player.defaults['InvHoldLen']:
                                    player.inventory.append(item)
                                    things_changed.append(4.1)
                                else:
                                    item_map[coords].append(item)
                                    if item[0] in vowels:
                                        print('>You find an %s.' % str(item).lower())
                                    else:
                                        print('>You find a %s.' % str(item).lower())
                                    things_changed.append(4.2)
                            if item_category == ('Usables'):
                                chosen = False
                                while chosen is False:
                                    item = random.choice(dicts.USABLES_LIST)
                                    if dicts.USABLES[item]['Appearance Level'] <= player.stats['Level']:
                                        chosen = True
                                if item[0] in vowels:
                                    print('>You find an %s.' % str(item).lower())
                                else:
                                    print('>You find a %s.' % str(item).lower())
                                if dicts.USABLES[item]['Type'] == 'Weapon' or dicts.USABLES[item]['Type'] == ('Armor'):
                                    equipable = {'Name': (item),
                                                 'Type': dicts.USABLES[item]['Type'],
                                                 'Bonus': dicts.USABLES[item]['Bonus'],
                                                 'Power': dicts.USABLES[item]['Power'],
                                                 'Stamina': dicts.USABLES[item]['Power']
                                                }
                                    if equipable['Type'] == 'Armor':
                                        equipable['SentenceStructure'] = dicts.USABLES[item]['SentenceStructure']
                                        equipable['Retaliation'] = dicts.USABLES[item]['Retaliation']
                                        equipable['Damage'] = dicts.USABLES[item]['Damage']
                                    else:
                                        equipable['BonusType'] = dicts.USABLES[item]['BonusType']
                                        equipable['Defense'] = dicts.USABLES[item]['Defense']
                                else:
                                    equipable = item
                                if len(player.inventory) < player.defaults['InvHoldLen']:
                                    player.inventory.append(equipable)
                                    print('>You pick up the %s.' % str(item).lower())
                                else:
                                    item_map[coords].append(equipable)
                                    things_changed.append(4.2)
                            if item_category == 'Gold':
                                item = random.randint(1, 20)
                                print('>You find %s gold.' % str(item))
                                player.gold += item
                            container_map[coords].remove(search_interpret)
                            container_map[coords].append('Nothing')
                            break
                        else:
                            for x in container_map[coords]:
                                try:
                                    if x.title() in dicts.INTERPRET_COMPREHENSIONS['Containers'][search_interpret.title()]:
                                        search_interpret = x.upper()
                                        item_types = dicts.CONTAINERS[search_interpret]['Holds']
                                        item_category = random.choice(item_types)
                                        if item_category == 'Misc':
                                            item = random.choice(dicts.ITEMS)
                                            if len(player.inventory) < player.defaults['InvHoldLen']:
                                                player.inventory.append(item)
                                                things_changed.append(4.1)
                                            else:
                                                item_map[coords].append(item)
                                                if item[0] in vowels:
                                                    print('>You find an %s.' % str(item).lower())
                                                else:
                                                    print('>You find a %s.' % str(item).lower())
                                                things_changed.append(4.2)
                                        if item_category == 'Usables':
                                            chosen = False
                                            while chosen is False:
                                                item = random.choice(dicts.USABLES_LIST)
                                                if dicts.USABLES[item]['Appearance Level'] <= player.stats['Level']:
                                                    chosen = True
                                            if item[0] in vowels:
                                                print('>You find an %s.' % str(item).lower())
                                            else:
                                                print('>You find a %s.' % str(item).lower())
                                            if dicts.USABLES[item]['Type'] == 'Weapon' or dicts.USABLES[item]['Type'] == 'Armor':
                                                equipable = {'Name': item,
                                                             'Type': dicts.USABLES[item]['Type'],
                                                             'Bonus': dicts.USABLES[item]['Bonus'],
                                                             'Power': dicts.USABLES[item]['Power'],
                                                             'Stamina': dicts.USABLES[item]['Power']
                                                            }
                                                if equipable['Type'] == 'Armor':
                                                    equipable['SentenceStructure'] = dicts.USABLES[item]['SentenceStructure']
                                                    equipable['Retaliation'] = dicts.USABLES[item]['Retaliation']
                                                    equipable['Damage'] = dicts.USABLES[item]['Damage']
                                                else:
                                                    equipable['BonusType'] = dicts.USABLES[item]['BonusType']
                                                    equipable['Defense'] = dicts.USABLES[item]['Defense']
                                            else:
                                                equipable = item
                                            if len(player.inventory) < player.defaults['InvHoldLen']:
                                                player.inventory.append(equipable)
                                                print('>You pick up the %s.' % str(item).lower())
                                            else:
                                                item_map[coords].append(equipable)
                                                things_changed.append(4.2)
                                        if item_category == 'Gold':
                                            item = random.randint(1, 20)
                                            print('>You find %s gold.' % str(item))
                                            player.gold += item
                                        container_map[coords].remove(search_interpret)
                                        container_map[coords].append('Nothing')
                                        break
                                except (KeyError, AttributeError):
                                    pass
                if item_category == None:
                    it_was_itemic = False
                    if search_interpret.title() in item_map[coords] or search_interpret.title() in player.inventory:
                        it_was_itemic = True
                        print(">You can't search an item.")
                    else:
                        for x in player.inventory:
                            if type(x) != str:
                                if x['Name'].lower() == search_interpret.lower():
                                    it_was_itemic = True
                                    print(">You can't search an item.")
                    if it_was_itemic is False:
                        for x in item_map[coords]:
                            if type(x) != str:
                                if x['Name'].lower() == search_interpret.lower():
                                    it_was_itemic = True
                                    print(">You can't search an item.")
                    if it_was_itemic is False:
                        print(">You don't see a %s nearby." % search_interpret.lower())
            if take_interpret:
                complete = True
                taken = False
                take_interpret = take_interpret.groups()[0]
                take_interpret = take_interpret.title()
                if take_interpret in item_map[coords]:
                    print('>You take the %s and pocket it.' % take_interpret.lower())
                    player.inventory.append(take_interpret)
                    item_map[coords].remove(take_interpret)
                    taken = True
                else:
                    for x in item_map[coords]:
                        if type(x) != str:
                            if take_interpret == x['Name'].title():
                                print('>You take the %s and put it in your backpack.' % take_interpret.lower())
                                player.inventory.append(x)
                                item_map[coords].remove(x)
                                taken = True
                if taken is False:
                    print(">You don't see that anywhere.")
                    player.stats['Insanity'] += 1
            if talk_interpret:
                complete = True
                talk_interpret = talk_interpret.groups()[0]
                talk_interpret = talk_interpret.upper()
                if travellers_here and travellers_here['Name'] == talk_interpret.title():
                    try:
                        if travellers_here['Interactions'] == 0:
                            print(travellers_here['FirstPhrase'])
                            travellers_here['Interactions']+= 1
                        else:
                            print(random.choice(travellers_here['Phrases']))
                    except KeyError:
                        travellers_here['Interactions'] = 1
                        print(travellers_here['FirstPhrase'])
                    if travellers_here['EffectsList']:
                        traveller_effect = random.choice(travellers_here['EffectsList'])
                        print(travellers_here['Effects'][traveller_effect]['ASE'])
                        print(travellers_here)
                        player.active_status_effects[traveller_effect] = {'Command': None, 'Stack': None}
                        player.active_status_effects[traveller_effect]['Command'] = travellers_here['Effects'][traveller_effect]['ASE']
                        player.active_status_effects[traveller_effect]['Stack'] = 10
                        print(travellers_here['Effects'][traveller_effect]['Description'])
                    if travellers_here['SalesList']:
                        print('The %s offers you his wares and shows his \n prices.' % travellers_here['Name'])
                        for x in travellers_here['SalesList']:
                            if x[0] in vowels:
                                print('An %s for %s gold.' % (x, travellers_here['Sells'][x]['Price']))
                            else:
                                print('A %s for %s gold.' % (x, travellers_here['Sells'][x]['Price']))
                        while True:
                            buy_item = input('Would you like to make a purchase? (Y/N) \n : ')
                            if buy_item == ('Y'):
                                bought_item = input('What would you like? \n : ')
                                if bought_item.title() in travellers_here['SalesList']:
                                    if travellers_here['Sells'][bought_item.title()]['Price'] <= player.gold:
                                        player.inventory.append(travellers_here['Sells'][bought_item.title()]['InvVal'])
                                        print('The %s says: \'Thank you for your purchase!\'' % travellers_here['Name'])
                                        break
                                    else:
                                        print('You cannot afford that.')
                                else:
                                    print('The %s does not sell that.' % travellers_here['Name'])
                            else:
                                break
                    elif travellers_here['ItemsList']:
                        i = 0
                        while i < 6:
                            travellers_here['SalesList'].append(random.choice(travellers_here['ItemsList']))
                            i += 1
                        print('The %s offers you his wares and shows his \n prices.' % travellers_here['Name'].lower())
                        for x in travellers_here['SalesList']:
                            if x[0] in vowels:
                                print('An %s for %s gold.' % (x, str(travellers_here['Sells'][x]['Price'])))
                            else:
                                print('A %s for %s gold.' % (x, str(travellers_here['Sells'][x]['Price'])))
                        while True:
                            buy_item = input('Would you like to make a purchase? (Y/N) \n : ')
                            if buy_item == ('Y'):
                                bought_item = input('What would you like? \n : ')
                                if bought_item.title() in travellers_here['SalesList']:
                                    if travellers_here['Sells'][bought_item.title()]['Price'] <= player.gold:
                                        player.inventory.append(travellers_here['Sells'][bought_item.title()]['InvVal'])
                                        print('The %s says: \'Thank you for your purchase!\'' % travellers_here['Name'].lower())
                                        break
                                    else:
                                        print('You cannot afford that.')
                                else:
                                    print('The %s does not sell that.' % travellers_here['Name'])
                            else:
                                break
                else:
                    print('>You are alone here... Talking to yourself? You give yourself a shake--\
                          \n the rain must be messing with your head.')
                    player.stats['Insanity'] += 5
            if use_interpret:
                complete = True
                use_interpret = use_interpret.groups()[0]
                use_interpret = use_interpret.title()
                if use_interpret in player.inventory:
                    if use_interpret in dicts.USABLES:
                        if dicts.USABLES[use_interpret]['Type'] == 'Scroll 1':
                            monsters, monster_list, player = random.choice(spells.BASIC_SPELLS)(monsters, monster_list, player)
                            used = random.randint(player.defaults['ScrlDstrctChance'], 3)
                            if used == 3:
                                print('>Your %s burns away into ash.' % use_interpret.lower())
                                player.inventory.remove(use_interpret)
                            if player.stats['Sneaking'] is True:
                                print('>You are, pretty obviously, no longer sneaking.')
                                player.stats['Sneaking'] = False
                        elif dicts.USABLES[use_interpret]['Type'] == 'Scroll 2':
                            monsters, monster_list, player.stats = random.choice(spells.ADVANCED_SPELLS)(monsters, monster_list, player.stats, player.active_status_effects)
                            player.inventory.remove(use_interpret)
                            used = random.randint(1, 3)
                            if used == 3:
                                print('Your %s burns away into ash.' % use_interpret['Name'].lower())
                                player.inventory.remove(use_interpret)
                            if player.stats['Sneaking'] is True:
                                print('>You are, pretty obviously, no longer sneaking.')
                                player.stats['Sneaking'] = False
                        elif dicts.USABLES[use_interpret]['Type'] == 'Potion':
                            print('>You feel a wash of relief as you drink the potion.')
                            player.stats['Health'] += dicts.USABLES[use_interpret]['Bonus'] + player.defaults['PotMod']
                            player.inventory.remove(use_interpret)
                            if player.stats['Health'] > player.stats['MaxHealth']:
                                player.stats['Health'] = player.stats['MaxHealth']
                            if player.stats['Sneaking'] is True:
                                print('>You are, pretty obviously, no longer sneaking.')
                                player.stats['Sneaking'] = False
                        elif dicts.USABLES[use_interpret]['Type'] == 'Bandage':
                            print('>You attempt to mend your wounds with the %s.' % use_interpret.lower())
                            print('>You feel a little stronger.')
                            player.stats['Health'] += dicts.USABLES[use_interpret]['Bonus']
                            if ('Bleeding') in player.active_status_effects and player.defaults['BandagesStopBleed'] is True:
                                print('>You stop your bleeding.')
                                player.active_status_effects['Bleeding']['Stack'] = 0
                            player.inventory.remove(use_interpret)
                        else:
                            print('>You think it would be a better idea to equip your %s.' % use_interpret.lower())
                else:
                    print('>You attempt to use your imaginary %s.' % use_interpret.lower())
                    player.stats['Insanity']+= 1
            if action == 'EXPLORE.':
                complete = True
                discovered = map_mgr.container_coords(container_map, coords)
                if discovered != None:
                    for x in container_map[coords]:
                        container.append(x)
                    if len(item_map[coords]) > 0:
                        im_length = len(item_map[coords]) - 1
                        im_read = []
                        for x in item_map[coords]:
                            if type(x) is str:
                                im_read.append(x)
                            else:
                                im_read.append(x['Name'])
                        if im_length > 0:
                            print('>Your %s and %s lie soaking in the mud.' % \
                                  (','.join(im_read[0:im_length]).lower(), \
                                   im_read[im_length].lower()))
                        else:
                            print('>Your %s lies soaking in the mud.' % im_read[0].lower())
                    things_changed.append(3)
                if discovered is None:
                    if len(item_map[coords]) > 0:
                        im_length = len(item_map[coords]) - 1
                        im_read = []
                        for x in item_map[coords]:
                            if type(x) == str:
                                im_read.append(x)
                            else:
                                im_read.append(x['Name'])
                        if im_length > 0:
                            print('>Your %s and %s lie soaking in the mud.' % \
                                  (','.join(im_read[0:im_length]).lower(), \
                                   im_read[im_length].lower()))
                        else:
                            print('>Your %s lies soaking in the mud.' % im_read[0].lower())
                    how_many_containers = random.randint(0, 3)
                    containers_chosen = 0
                    container_map[coords] = []
                    while containers_chosen <= how_many_containers:
                        container_choice = random.randint(player.defaults['ContnrBtmRng'], 100)
                        container.append(gen_mgr.get_container(biome, container_choice, dicts.CONTAINERS))
                        containers_chosen += 1
                    for x in container_map_queue:
                        container.append(x.upper())
                    container_map_queue = []
                    container_map[coords].append(container)
                    container_map[coords] = container_map[coords][0]
                    container = list(set(container))
                    container_map[coords] = list(set(container_map[coords]))
                    things_changed.append(2)
            if action == 'FLEE.' or action == 'RUN AWAY.':
                complete = True
                if player.stats['Stamina'] != 0:
                    if monsters > 0 or monster_queue:
                        print('>You flee the battle, fearing for your life.')
                        player.stats['Sneaking'] = False
                        variant_chosen = False
                        player.stats['Stamina'] -= 5
                        monsters = 0
                        monster_list = []
                        monster_queue = []
                        x_coord += random.randint(player.defaults['FleeRng'][0], player.defaults['FleeRng'][1])
                        y_coord += random.randint(player.defaults['FleeRng'][0], player.defaults['FleeRng'][1])
                        coords = (str(x_coord) + ', ' + str(y_coord))
                        item_map[coords] = []
                        if coords in local_map:
                            discovered = True
                        else:
                            discovered = False
                        if discovered is True:
                            biome = local_map[coords]
                            things_changed.append(1)
                        if discovered is False:
                            same_biome = random.randint(1, 2)
                            if same_biome == 2:
                                local_map[(coords)] = biome
                            else:
                                biome_choice = random.randint(1, 100)
                                biome_choice = str(biome_choice)
                                biome = gen_mgr.get_biome(biome_choice)
                                local_map[coords] = biome
                            things_changed.append(1)
                        if local_map[coords] == 'the Mountains':
                            see_peak = random.randint(0, 3)
                            if see_peak == 3:
                                print('>From this high peak, you can see the terrain around and below you.')
                                nter = str(x_coord) + ', ' + str(y_coord+1)
                                ster = str(x_coord) + ', ' + str(y_coord-1)
                                eter = str(x_coord+1) + ', ' + str(y_coord)
                                wter = str(x_coord-1) + ', ' + str(y_coord)
                                ters = [nter, ster, eter, wter]
                                ter_dir = {nter: 'north', ster: 'south', eter: 'east',
                                           wter: 'west'}
                                for x in ters:
                                    if x in local_map:
                                        print('>To the %s you see %s.' % (ter_dir[x], local_map[x].lower()))
                                    else:
                                        biome_choice = random.randint(1, 100)
                                        biome_choice = str(biome_choice)
                                        biome = gen_mgr.get_biome(biome_choice)
                                        local_map[x] = biome
                                        print('>To the %s you see %s.' % (ter_dir[x], local_map[x].lower()))
                                for x in travellers:
                                    if travellers[x]['Coords'] in ters:
                                        for y in ters:
                                            if y == travellers[x]['Coords']:
                                                trav_ter_dir = y
                                        print('>You see another figure walking on the path to the %s.' % y)
                    else:
                        print('>You run around in circles, fleeing your imaginary \n enemies.')
                        player.stats['Insanity'] += 4
                else:
                    if monsters > 0:
                        print('>You are too tired to run.')
                    else:
                        print('>You run around in circles, fleeing your imaginary \n enemies.')
                        player.stats['Insanity'] += 4
            if action == 'BEGIN SNEAKING.' or action == 'START SNEAKING.' or action == 'HIDE.' or action == 'SNEAK.':
                complete = True
                if player.stats['Sneaking'] is False:
                    if monsters > 0:
                        try:
                            monster_hide = random.randint(player.defaults['PrlngStlth'], player.stats['Stamina'])
                        except ValueError:
                            monster_hide = 1
                        if monster_hide <= 5:
                            print('>You are unable to hide.')
                        else:
                            print('>You slip into the shadows, moving slowly and carefully so as not to \n attract attention.')
                            player.stats['Sneaking'] = True
                    else:
                        print('>You slip into the shadows, moving slowly and carefully so as not to \n attract attention, at the expense of energy.')
                        player.stats['Sneaking'] = True
                else:
                    print('>You are already sneaking.')
            if action == 'FORAGE.':
                complete = True
                if 'Forage' in dicts.CLASS_ABILITIES[player.pclass]:
                    if len(player.inventory) > player.defaults['InvHoldLen']:
                        print('Your inventory is already full.')
                    else:
                        print('>You spend some time looking for edible plants and berries.')
                        player.stats['Stamina'] -= 2
                        forage_num = random.randint(1, 80)
                        for x in dicts.FORAGE_TABLE:
                            if forage_num >= dicts.FORAGE_TABLE[x][0] and forage_num <= dicts.FORAGE_TABLE[x][1]:
                                print('>You find some ' + x.lower() + '.')
                                player.inventory.append(x)
                else:
                    print(">You don't know how to do that.")
            if action == 'SCHEME.':
                complete = True
                if 'Scheme' in dicts.CLASS_ABILITIES[player.pclass]:
                    if monsters == 1:
                        print('>You pause for a moment to assess your surroundings and \n take stock of your foe. You quickly identify its weaknesses \n and defenses.')
                        player.stats['TempDamage'] += random.randint(1, 14) + player.stats['Level']
                        player.stats['TempDef'] += random.randint(5, 10)
                    elif monsters > 1:
                        print('>You pause for a moment to assess your surroundings and \n take stock of your enemies. You quickly identify their weaknesses \n and defenses.')
                        player.stats['TempDamage'] += random.randint(1, 14) + player.stats['Level']
                        player.stats['TempDef'] += random.randint(5, 10)
                    else:
                        if monster_queue:
                            print('>You scan your surroundings, and notice the form of some creature \n hiding nearby. You calculate its line of sight so that \n you can avoid it.')
                            monster_queue = []
                        else:
                            print(">You don't see any reason to do that now.")
                else:
                    print(">You don't know how to do that.")
            if action == 'TREK.':
                complete = True
                if 'Trek' in dicts.CLASS_ABILITIES[player.pclass]:
                    print('>You pull out your map and decide on a location to trek to.')
                    time.sleep(0.3)
                    print(local_map)
                    destination = input(': ')
                    if destination in local_map:
                        trek_coords = coords.split(', ')
                        trek_dest = destination.split(', ')
                        trek_dist = round(math.sqrt(((int(trek_dest[0]) - int(trek_coords[0])) ** 2) + ((int(trek_dest[1]) - int(trek_coords[1])) ** 2)))
                        coords = destination
                        x_coord = int(trek_dest[0])
                        y_coord = int(trek_dest[1])
                        player.stats['Stamina'] -= trek_dist * 3
                        print('>You travel to the location that you marked on your map, using \n familiar landmarks to stay on track, and walking carefully to \n avoid monsters.')
                    else:
                        print('>You have never been there.')
                else:
                    print(">You don't know how to do that.")
            if action == 'STOP SNEAKING.':
                complete = True
                if player.stats['Sneaking'] is True:
                    print('You stand upright.')
                    player.stats['Sneaking'] = False
                else:
                    print("You aren't sneaking.")
            if action == 'CHECK MAP.':
                complete = True
                print(coords)
                print(local_map)
            #Prints out the map.
            if action == 'CHECK INVENTORY.' or action == 'OPEN INVENTORY.':
                complete = True
                player.inventory_read = []
                for x in player.inventory:
                    if type(x) != str:
                        if x['Name'] not in player.inventory_read:
                            player.inventory_read.append(x['Name'])
                    elif x not in player.inventory_read:
                        player.inventory_read.append(x)
                player.inventory_list = []
                for x in player.inventory:
                    if type(x) != str:
                        player.inventory_list.append(x['Name'])
                    else:
                        player.inventory_list.append(x)
                player.inventory_count = Counter(player.inventory_list)
                for x in player.inventory_read:
                    if player.inventory_count[x] == 1:
                        if x[0] in vowels:
                            print('>You have an %s.' % x.lower())
                        else:
                            print('>You have a %s.' % x.lower())
                    else:
                        print('>You have %s %ss.' % (str(player.inventory_count[x]), x.lower()))
                if player.equipped['Weapon']['Name'][0] in vowels:
                    print('>You are holding an %s.' % player.equipped['Weapon']['Name'].lower())
                else:
                    print('>You are holding a %s.' % player.equipped['Weapon']['Name'].lower())
                print('>You are wearing %s %s.' % (player.equipped['Armor']['SentenceStructure'], player.equipped['Armor']['Name'].lower()))
            if action == 'CHECK COIN POUCH.' or action == 'CHECK GOLD.' or action == 'COUNT GOLD.' or action == 'COUNT COINS.':
                complete = True
                print('>You have %s gold.' % str(player.gold))
            if action == 'REST.' or action == 'SLEEP.' or action == 'RELAX.' or action == 'LAY DOWN.':
                complete = True
                if monsters > 0:
                    if player.defaults['RestDeath'] is True:
                        print('>As you drop down mid-battle for a nap, the monsters eat you.')
                        player.stats['Health'] = 0
                    else:
                        print('>As you drop down mid-battle for a nap, the monsters look about in \n confusion, not quite sure what to do.')
                    break
                if fire_lit is True:
                    print('>You rest by the fireside, and the warmth helps to dry you. \n You spend several hours peacefully resting.')
                    player.stats['Stamina'] = player.stats['MaxStamina']
                    player.stats['Health'] += round(player.stats['MaxHealth'] / 3)
                    try:
                        if player.active_status_effects['Waterlogged']['Stack'] >= 1:
                            player.active_status_effects['Waterlogged']['Stack'] = 0
                    except KeyError:
                        pass
                if fire_lit is False:
                    print('>You spend several hours resting. Your fitfull sleep, however, \n leaves you an easy target for monsters.')
                    player.stats['Stamina'] = player.stats['MaxStamina']
                    player.stats['Health'] += round(player.stats['MaxHealth'] / 5)
                    sick_over_rest = random.randint(1, player.defaults['RestSick'])
                    if sick_over_rest == 5:
                        print('>As you lay in the frigid, soaking mud, a creeping \n dampness spreads through your body.')
                        player.active_status_effects['Waterlogged'] = {'Command': status_effects.waterlogged, 'Stack': 1}
                    monsters = random.randint(0, 1)
                    if monsters > 0:
                        new_monsters_chosen = 0
                        while new_monsters_chosen < monsters:
                            new_monster, biome_match = gen_mgr.get_new_monster(dicts.MONSTER_COMPENDIUM, dicts.MONSTER_DICT, player, biome)
                            if biome_match is True:
                                monster_list.append(new_monster)
                                new_monsters_chosen += 1
                            if biome_match is False:
                                monsters -= 1
                        if monster_list:
                            things_changed.append(5)
                print('>You wake up.')
            if action == 'START FIRE.' or action == 'MAKE FIRE.' or action == 'IGNITE FIRE.':
                complete = True
                if 'Strike-Stone' in player.inventory:
                    tinder_true = False
                    tinder = input('What tinder do you use? \n : ')
                    tinder = tinder.upper()
                    for x in player.inventory:
                        try:
                            if x['Name'].upper() == tinder:
                                tinder_true = x
                        except TypeError:
                            if x.upper() == tinder:
                                tinder_true = x
                    if tinder_true != False:
                        try:
                            start_chance = dicts.FIRESTARTING_PROBABILITIES['Biomes'][biome] + dicts.FIRESTARTING_PROBABILITIES['Tinder'][tinder]
                            started = random.randint(1, 100)
                            player.inventory.remove(tinder_true)
                            if started<= (start_chance):
                                print('After assembling bits of deadwood into a campfire, \n you light your tinder, and the wood, to your relief, catches.')
                                fire_lit = True
                                stone_break = random.randint(1, 10)
                                if stone_break == 1:
                                    player.inventory.remove('Strike-Stone')
                                    print('Your strike-stone is ruined.')
                            else:
                                if dicts.FIRESTARTING_PROBABILITIES['Biomes'][biome] < 30:
                                    print('>You are unable to get a fire going. Perhaps in an area with more cover \n you might fare better...')
                                else:
                                    print('>You are unable to get a fire going.')
                        except KeyError:
                            print("You can't use that as tinder.")
                    else:
                        print("That isn't in your player.inventory.")
                else:
                    print('You need a strike-stone.')
            if action == 'DODGE':
                complete = True
                if 'DODGE.' in player.learned_commands:
                    if monsters == 0:
                        print('There are no enemies to dodge.')
                    else:
                        if monsters == 1:
                            print_word = ("enemy's")
                        if monsters > 1:
                            print_word = ("enemies'")
                        print('You ready yourself for your %s attacks, spinning and jumping out of their path.' % print_word)
                        player.stats['TempDef'] += 5
                else:
                    print("You don't know how to dodge.")
            if action == 'CHARGE.':
                complete = True
                if 'CHARGE' in player.learned_commands:
                    if monsters == 0:
                        print('>You charge wildly towards nothing.')
                        player.stats['Insanity'] += 2
                        break
                    x = random.choice(monster_list)
                    print('>You muster up your strength and charge at the %s.' % x['Name'].lower())
                    player.stats['Damage'] += 5
                    x, hit, player = combat_mgr.do_player_attack(x, player)
                    player.stats['Damage'] -= 5
                    #player_vals['Attacks'] += 1
                    player.stats['Stamina'] -= 2 * player.defaults['AtkStam']
                    if hit is True:
                        if x['HP'] <= 0:
                            cprint('>You killed the %s.' % x['Name'].lower(), 'green')
                            healed = random.randint(player.defaults['KillHealChance'], 3)
                            if healed == 3:
                                player.stats['Health'] += player.defaults['KillHealth']
                                if player.stats['Health'] >= player.stats['MaxHealth']:
                                    player.stats['Health'] = player.stats['MaxHealth']
                                print('>You feel a surge of relief.')
                            monster_list.remove(x)
                            monsters -= 1
                            player.stats['XP'] += x['XP'] + player.defaults['XPMod']
                            player.inventory, item_map, player.gold = inv_mgr.loot_monster(x, player.inventory, player.defaults, player.stats, item_map, coords, dicts.USABLES, dicts.USABLES_LIST, player.gold)
                        elif x['HP'] / x['MaxHP'] < 0.1:
                            print('>The %s is mortally injured.' % x['Name'].lower())
                        elif x['HP'] / x['MaxHP'] < 0.25:
                            print('>The %s is critically wounded.' % x['Name'].lower())
                        elif x['HP'] / x['MaxHP'] < 0.5:
                            print('>The %s is injured.' % x['Name'].lower())
                        else:
                            print('>The %s grunts at your attack.' % x['Name'].lower())
                else:
                    print("You don't know how to charge.")
            if action == 'CLEAVE.':
                complete = True
                if 'CLEAVE' in player.learned_commands:
                    if monsters == 0:
                        print('>You swing back and forth at nothing.')
                        player.stats['Insanity'] += 2
                        break
                    player.stats['Damage'] -= 10
                    if monsters == 1:
                        print_word = 'foe'
                    else:
                        print_word = 'foes'
                    print('>You slash towards your %s.' % print_word)
                    for x in monster_list:
                        x, hit, player = combat_mgr.do_player_attack(x, player)
                        #player_vals['Attacks'] += 1
                        player.stats['Stamina'] -= 2*player.defaults['AtkStam']
                        if hit is True:
                            if x['HP'] <= 0:
                                cprint('>You killed the %s.' % x['Name'].lower(), 'green')
                                healed = random.randint(player.defaults['KillHealChance'], 3)
                                if healed == 3:
                                    player.stats['Health'] += player.defaults['KillHealth']
                                    if player.stats['Health'] >= player.stats['MaxHealth']:
                                        player.stats['Health'] = player.stats['MaxHealth']
                                    print('>You feel a surge of relief.')
                                monster_list.remove(x)
                                monsters -= 1
                                player.stats['XP'] += x['XP'] + player.defaults['XPMod']
                                player.inventory, item_map, player.gold = inv_mgr.loot_monster(x, player.inventory, player.defaults, player.stats, item_map, coords, dicts.USABLES, dicts.USABLES_LIST, player.gold)
                            elif x['HP'] / x['MaxHP'] < 0.1:
                                print('>The %s is mortally injured.' % x['Name'].lower())
                            elif x['HP'] / x['MaxHP'] < 0.25:
                                print('>The %s is critically wounded.' % x['Name'].lower())
                            elif x['HP'] / x['MaxHP'] < 0.5:
                                print('>The %s is injured.' % x['Name'].lower())
                            else:
                                print('>The %s grunts at your attack.' % x['Name'].lower())
                    player.stats['Damage'] += 10
            if action == 'HELP.':
                complete = True
                output_mgr.show_help()
            if action == 'DEV:':
                while True:
                    devaction = input('Dev: ')
                    if devaction == ('Stats'):
                        print(player.stats)
                    if devaction == ('ASE'):
                        print(player.active_status_effects)
                    if devaction == ('Travellers'):
                        print(travellers)
                    if devaction == ('travellers_here'):
                        print(travellers_here)
                    if devaction == ('PlayerDefaults'):
                        print(player.defaults)
                    if devaction == ('Monsters'):
                        print(monsters, monster_list)
                    if devaction == (''):
                        break
            if action == 'EXIT.':
                print('>Saving...')
                save_data = shelve.open('save_data')
                save_data = save_mgr.write_save(save_data, player, local_map, \
                                                container_map, item_map, x_coord, y_coord, biome, \
                                                fire_lit, travellers, travellers_here, \
                                                monster_list, monsters, monster_queue)
                save_data['SaveActive'] = True
                save_data.close()
                sys.exit('Game quit!')
            if complete == False:
                print(">You don't know how to do that.")
            output_mgr.area_status(things_changed, biome, container, item, monster_list, variant_chosen, variant, gen_mgr.VARIANT_DESCRIPTIONS, item_map, coords)
            #Prints out the area status.
            player, item_map = inv_mgr.check(player, item_map, coords)
            things_changed = []
            container = []
            #Resets some variables.
if __name__ == '__main__':
    main()
    """try:
        main()
    except Exception as Ex:
        pass"""
    """except Exception as Ex:
        try:
            print('An error occurred!')
            print('Creating error report...')
            ExType, ExObj, ExTb = sys.exc_info()
            ExName = os.path.split(ExTb.tb_frame.f_code.co_filename)[1]
            ErrorInfo = (ExType, ExName, ExTb.tb_lineno)
            CurrentDir = os.path.dirname(os.path.realpath(__file__))
            CrashLogPath = (CurrentDir + '/CrashLogs')
            if not os.path.exists(CrashLogPath):
                os.makedirs(CrashLogPath)
            CrashLog = shelve.open(os.path.join(CrashLogPath, 'CrashLog'))
            CrashLog['PlayerStats'] = player.stats
            CrashLog['PlayerClass'] = player.pclass
            CrashLog['PlayerDefaults'] = player.defaults
            CrashLog['LearnedCommands'] = player.learned_commands
            for x in player.active_status_effects:
                player.active_status_effects[x]['Command'] = player.active_status_effects[x]['Command'].__name__
            CrashLog['ActiveStatusEffects'] = player.active_status_effects
            CrashLog['local_map'] = local_map
            CrashLog['ContainerMap'] = container_map
            CrashLog['itemMap'] = item_map
            CrashLog['XCoord'] = x_coord
            CrashLog['YCoord'] = y_coord
            CrashLog['biome'] = biome
            CrashLog['FireLit'] = fire_lit
            for x in travellers:
                for y in travellers[x]['Effects']:
                    travellers[x]['Effects'][y]['ASE'] = travellers[x]['Effects'][y]['ASE'].__name__
            CrashLog['Travellers'] = travellers
            CrashLog['travellers_here'] = travellers_here
            CrashLog['MonsterList'] = monster_list
            CrashLog['Monsters'] = monsters
            CrashLog['MonsterQueue'] = monster_queue
            CrashLog['player.inventory'] = player.inventory
            CrashLog['player.equipped'] = player.equipped
            CrashLog['GoldPouch'] = player.gold
            CrashLog['action'] = action
            try: CrashLog['ID'] = ID
            except NameError:
                CrashLog['ID'] = None
            CrashLog.close()
            FilestoZip = os.listdir(CrashLogPath)
            ZipFile = zipfile.ZipFile('CrashLogs.zip', mode = 'w')
            for x in FilestoZip:
                ZipFile.write(('CrashLogs/' + x), compress_type = zipfile.ZIP_DEFLATED)
            ZipFile.close()
            Body = ('Crash at ' + (formatdate(localtime = True)) + ': ' + str(Ex) + str(ErrorInfo))
            Server = smtplib.SMTP('smtp.gmail.com:587')
            Server.starttls()
            save_data = shelve.open('save_data')
            Username = save_data['Email']
            Password = save_data['Password']
            save_data.close()
            try: Server.login(Username, Password)
            except SMTPAuthenticationError:
                save_data = shelve.open('save_data')
                save_data['Email'] = None
                save_data.close()
                sys.exit('A valid email address is required.')
            Msg = MIMEMultipart()
            Msg['From'] = Username
            Msg['To'] = ('rainwashcrashreport@gmail.com')
            Msg['Date'] = formatdate(localtime = True)
            Msg['Subject'] = ('Crash Report: ' + str(Ex))
            Msg.attach(MIMEText(Body))
            CurrentDir = os.path.dirname(os.path.realpath(__file__))
            Logs = [(CurrentDir + '/CrashLogs.zip')]
            for x in Logs:
                Attachment = MIMEBase('application', 'octet-stream')
                Attachment.set_payload(open(x, 'rb').read())
                encoders.encode_base64(Attachment)
                Attachment.add_header('Content-Disposition', "attachment; filename = '{0}'".format(os.path.basename(x)))
                Msg.attach(Attachment)
            Server.sendmail(Username, 'rainwashcrashreport@gmail.com', Msg.as_string())
            Server.quit()
            time.sleep(5)
            sys.exit('Error!')
        except Exception as FEx:
            print('Fatal error!')
            print('Please copy the following error and send it to \n rainwashcrashreports@gmail.com: ')
            print(Ex)
            print(ErrorInfo)
            ExType, ExObj, ExTb = sys.exc_info()
            FErrorInfo = (ExType, ExObj, ExTb.tb_lineno)
            print(FEx)
            print(FErrorInfo)
            time.sleep(30)
            sys.exit('Fatal error!')"""
