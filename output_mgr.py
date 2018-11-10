"""Manages large-scale text output"""

import random

from collections import Counter

def cprint(string, color):
    '''Prints output in the specified color'''
    colors = {'black': '\u001b[30m',
              'red': '\u001b[31m',
              'green': '\u001b[32m',
              'yellow': '\u001b[33m',
              'blue': '\u001b[34m',
              'magenta': '\u001b[35m',
              'cyan': '\u001b[36m',
              'white': '\u001b[37m'}
    print('%s%s%s' % (colors[color], string, '\u001b[0m'))

def area_status(things_changed, biome, container, item, monster_list, variant_chosen, variant,
                variant_descriptions, item_map, coords):
    """Writes area_status based on code of things_changed"""
    vowels = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]
    vowel_word = {"V": "an", "C": "a"}
    for x in things_changed:
        if x == 1:
            if variant_chosen is True:
                cprint(">You find yourself in %s. %s" % (biome.lower(), variant_descriptions[variant]), 'green')
            else:
                cprint(">You find yourself in %s." % (biome.lower()), 'green')
        if x == 2:
            container_read = []
            all_nothing = True
            for y in container:
                if y != "Nothing":
                    if y is None:
                        pass
                    else:
                        all_nothing = False
                        container_read.append(y)
            if all_nothing is False:
                for y in container_read:
                    z = "C"
                    if y[0] in vowels:
                        z = "V"
                    print(">You find %s %s." % (vowel_word[z], y.lower()))
            if all_nothing is True:
                print(">You find nothing.")
        if x == 3:
            container_read = []
            all_nothing = True
            for y in container:
                if y != "Nothing":
                    if y == None:
                        pass
                    else:
                        all_nothing = False
                        container_read.append(y)
            if all_nothing is False:
                for y in container_read:
                    z = "C"
                    if y[0] in vowels:
                        z = "V"
                    print(">There is %s %s here." % (vowel_word[z], y.lower()))
            if all_nothing is True:
                if len(item_map[coords]):
                    print(">There is nothing else of note here.")
                else:
                    print(">There is nothing of note here.")
        if x == 4.1:
            z = "C"
            if item[0] in vowels:
                z = "V"
            print(">You find %s %s." % (vowel_word[z], item.lower()))
            print(">You pick up the %s." % (item.lower()))
        if x == 4.2:
            print(">Unable to carry any more, you set the %s on the ground." % (item.lower()))
        if x == 5:
            monster_list_read = []
            monster_list_prep = []
            for y in monster_list:
                monster_list_prep.append(y["Name"])
                if y["Name"] not in monster_list_read:
                    monster_list_read.append(y["Name"])
            monster_list_count = Counter(monster_list_prep)
            for y in monster_list_read:
                sentence_modifiers = random.randint(1, 7)
                if monster_list_count[y] == 1:
                    z = ("C")
                    if y[0] in vowels:
                        z = ("V")
                    if sentence_modifiers == 1:
                        cprint(">%s %s moves to attack." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 2:
                        cprint(">%s %s prepares to strike." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 3:
                        cprint(">%s %s glares menacingly." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 4:
                        cprint(">%s %s charges you." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 5:
                        cprint(">%s %s rears its ugly head." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 6:
                        cprint(">%s %s advances." % (vowel_word[z].title(), y.lower()), 'red')
                    if sentence_modifiers == 7:
                        cprint(">%s %s rushes your way." % (vowel_word[z].title(), y.lower()), 'red')
                else:
                    if sentence_modifiers == 1 or sentence_modifiers == 5:
                        cprint(">%d %ss move to attack." % (monster_list_count[y], y.lower()), 'red')
                    if sentence_modifiers == 2:
                        cprint(">%d %ss prepare to strike." % (monster_list_count[y], y.lower()), 'red')
                    if sentence_modifiers == 3:
                        cprint(">%d %ss glare menacingly." % (monster_list_count[y], y.lower()), 'red')
                    if sentence_modifiers == 4:
                        cprint(">%d %ss charge you." % (monster_list_count[y], y.lower()), 'red')
                    if sentence_modifiers == 6:
                        cprint(">%d %ss rears its ugly head." % (monster_list_count[y], y.lower()), 'red')
                    if sentence_modifiers == 7:
                        cprint(">%d %ss rush your way." % (monster_list_count[y], y.lower()), 'red')

def do_dmg_text(player):
    """Output damage response based on current health"""
    if player.stats['Health'] <= 0:
        cprint('>You have been struck your final blow.', 'red')
        player.death = True
    elif player.stats['Health'] == 1:
        cprint('>You are barely conscious, clinging to life by a thread.', 'red')
    elif player.stats['Health']/player.stats['MaxHealth'] < 0.1:
        cprint('>You are fatally wounded.', 'yellow')
    elif player.stats['Health']/player.stats['MaxHealth'] < 0.25:
        cprint('>You are critically injured.', 'yellow')
    elif player.stats['Health']/player.stats['MaxHealth'] < 0.5:
        cprint('>You are in considerable pain.', 'yellow')
    else:
        cprint('>You wince as you are hit.', 'yellow')
    return player

def report_hunger(player):
    """Returns levels of hunger"""
    if player.stats['Hunger'] >= 35 and player.stats['Health'] < 10:
        cprint('>You are starving to death!', 'red')
        player.stats['Health'] -= 1
    elif player.stats['Hunger'] >= 35 and player.stats['Health'] >= 10:
        cprint('>You are starving.', 'yellow')
        player.stats['Health'] -= 2
    elif player.stats['Hunger'] >= 20 and player.stats['Hunger'] <= 35:
        player.stats['Hunger'] += player.defaults['TireHngr']
        cprint('>You are hungry.', 'yellow')
    elif player.stats['Hunger'] >= 35:
        player.stats['Hunger']+= 1
        cprint('>You are very hungry.', 'yellow')
    return player

def report_monster_damage(monster):
    """Returns damage level of monster"""
    if monster['HP'] / monster['MaxHP'] < 0.1:
        print('>The %s is mortally injured.' % monster['Name'].lower())
    elif monster['HP'] / monster['MaxHP'] < 0.25:
        print('>The %s is critically wounded.' % monster['Name'].lower())
    elif monster['HP'] / monster['MaxHP'] < 0.5:
        print('>The %s is injured.' % monster['Name'].lower())
    else:
        print('>The %s grunts at your attack.' % monster['Name'].lower())

def show_help():
    """Prints out a command sheet"""
    print(">Show help? (Y/N)")
    check = input(": ")
    if check == "Y":
        print("User commands require a period at the end. Prompted commands \n \
              should not have a period. Commands: \n \
              Attack/Fight/Battle/Kill/Hit- Attack [Monster].- Uses your \n \
              equipped weapon to attack [Monster]. \n \
              Cook- Cook [Food].- Can only be used if a fire has been lit. \n \
              Drop/Discard- Discard [Item].- Drops your item on the ground. \n \
              Eat- Eat [Food].- You consume [Food]. \n \
              Equip/Hold/Wear- Equip [Item].- Equips [Item], if it can be equipped. \n \
              Go/Walk/Move/Travel/Head- Go [Forward/N/S/East/etc.].- You travel in \n \
              the appropriate direction. \n \
              Search/Open/Investigate- Search [Container].- Searches [Container]. \n \
              Take/Pick up- Take [Item].- Takes an item off of the ground. \n \
              Items are automatically placed on the ground when you find an item but \n \
              are unable to carry it, or when they are dropped. \n \
              You can see what items are on the ground with \"Explore.\" \n \
              Use- Use [Item]- Uses [Item], if it can be used. \n \
              Explore.- Explores the area. Containers and items are revealed. \n \
              Flee/Run Away.- Attempt to flee from any threats. \n \
              Check Map.- Lists your current location, then the places you have been, \n \
              coordinate-style. \n \
              Check Inventory/Open Inventory.- Lists your current items. \n \
              Check Coin Pouch/Check Gold/etc.- Shows your gold counter. \n \
              Rest/Sleep/etc.- You rest. A lit fire provides extra benefits. \n \
              Start Fire/Make Fire/etc.- You strt a fire. Requires a strike-stone \n \
              and tinder. \n \
              Exit.- Saves the game and exits.")
