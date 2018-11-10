"""Manages various crafting processes"""
def combo_altar(player, prefix_modifiers):
    """Standard, single-encounter combination altar"""
    import random
    VOWELS = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
    print('>On this altar, there are two large rectangles of slate. \n It appears that some sort of reaction will be triggered if \n both have an item on them.')
    while True:
        s1_check = False
        s1_equipped = False
        s2_check = False
        s2_equipped = False
        slate1 = input("Type 'Leave.' to leave. \n Slate 1: ")
        if slate1.upper() == 'LEAVE.':
            return player
        slate1 = slate1.title()
        for x in player.inventory:
            if x is str:
                if x['Name'] == slate1:
                    s1_check = True
                    print('>The slate begins to glow with a strange light.')
            else:
                if x == slate1:
                    s1_check = True
                    print('>The slate shakes and rattles ominously.')
        if s1_check is False:
            for x in player.equipped:
                if player.equipped[x]['Name'] == slate1:
                    s1_check = True
                    s1_equipped = True
                    print('>The slate begins to glow with a strange light.')
            if s1_check is False:
                print(">You don't have that in your player.inventory.")
        slate2 = input('Slate 2: ')
        slate2 = slate2.title()
        for x in player.inventory:
            if x is str:
                if x['Name'] == slate2:
                    s2_check = True
                    print('>The slate shakes and rattles ominously.')
            else:
                if x == slate2:
                    s2_check = True
                    print('>The slate begins to glow with a strange light.')
        if s2_check is False:
            for x in player.equipped:
                if player.equipped[x]['Name'] == slate2:
                    s2_check = True
                    s2_equipped = True
                    print('>The slate shakes and rattles ominously.')
            if s2_check is False:
                print(">You don't have that in your inventory.")
            print(">You don't have that in your inventory.")
        if s1_check is True and s2_check is True:
            activator_options = []
            for x in prefix_groups_list:
                if slate2 in prefix_groups[x]:
                    activator_options.append(x)
            if activator_options:
                if s1_equipped is True:
                    for x in player.equipped:
                        bright_print = False
                        if player.equipped[x]['Name'] == slate1:
                            try:
                                if player.equipped[x]['Enchanted'] and bright_print != True:
                                    print('>The slate gets brighter and brighter, then abruptly goes out- \n nothing else happens.')
                                    bright_print = True
                                    break
                            except KeyError:
                                pass
                            prefix_activator = random.choice(activator_options)
                            if player.equipped[x]['Type'] == 'Weapon':
                                player.equipped[x]['Name'] = '%s %s' % (prefix_activator, player.equipped[x]['Name'])
                                player.equipped[x]['Enchanted'] = True
                                player.equipped[x][prefix_modifiers[prefix_activator]['WeaponEffect']] += int(prefix_modifiers[prefix_activator]['Bonus'])
                                if player.equipped[x]['Name'][0] in VOWELS:
                                    print('>The %s crumbles to dust, and your %s becomes an %s.' % (slate2.lower(), slate1.lower(), player.equipped[x]['Name'].lower()))
                                else:
                                    print('>The %s crumbles to dust, and your %s becomes a %s.' % (slate1.lower(), slate2.lower(), player.equipped[x]['Name'].lower()))
                                player.inventory.remove(slate2)
                            if player.equipped[x]['Type'] == 'Armor':
                                player.equipped[x]['Name'] = '%s %s' % (prefix_activator, player.equipped[x]['Name'])
                                player.equipped[x]['Enchanted'] = True
                                player.equipped[x][prefix_modifiers[prefix_activator]['ArmorEffect']] += int(prefix_modifiers[prefix_activator]['Bonus'])
                                if player.equipped[x]['Name'][0] in VOWELS:
                                    print('>The %s crumbles to dust, and your %s becomes an %s.' % (slate2.lower(), slate1.lower(), player.equipped[x]['Name'].lower()))
                                else:
                                    print('>The %s crumbles to dust, and your %s becomes a %s.' % (slate2.lower(), slate1.lower(), player.equipped[x]['Name'].lower()))
                                player.inventory.remove(slate2)
                    if x == 'Armor':
                        remove_item = player.equipped['Armor']
                        player.stats['Power'] -= remove_item['Power']
                        player.stats['Damage'] -= remove_item['Damage']
                        player.stats['Stamina'] -= remove_item['Stamina']
                        player.stats['Defense'] -= remove_item['Bonus']
                        player.stats['Power'] += player.equipped[x]['Power']
                        player.stats['Damage'] += player.equipped[x]['Damage']
                        player.stats['Stamina'] += player.equipped[x]['Stamina']
                        player.stats['Defense'] += player.equipped[x]['Bonus']
                        player.equipped['Armor'] = player.equipped[x]
                    else:
                        remove_item = player.equipped['Weapon']
                        player.stats['Power'] -= remove_item['Power']
                        player.stats['Defense'] -= remove_item['Defense']
                        player.stats['Stamina'] -= remove_item['Stamina']
                        if remove_item['BonusType'] == 'Add':
                            player.stats['Damage'] -= remove_item['Bonus']
                            player.stats['Damage'] += player.equipped[x]['Bonus']
                        else:
                            player.stats['Damage'] -= remove_item['Bonus']*player.stats['Level']
                            player.stats['Damage'] += player.equipped[x]['Bonus']*player.stats['Level']
                        player.stats['Power'] += player.equipped[x]['Power']
                        player.stats['Defense'] += player.equipped[x]['Defense']
                        player.stats['Stamina'] += player.equipped[x]['Stamina']
                        player.equipped['Weapon'] = player.equipped[x]
                else:
                    for x in player.inventory:
                        if x is not str and x['Name'] == slate1:
                            try:
                                if x['Enchanted']:
                                    print('>The slate gets brighter and brighter, then abruptly goes out- \n nothing else happens.')
                                    break
                            except KeyError:
                                pass
                            prefix_activator = random.choice(activator_options)
                            if x['Type'] == 'Weapon':
                                x['Name'] = '%s %s' % (prefix_activator, x['Name'])
                                x['Enchanted'] = True
                                x[prefix_modifiers[prefix_activator]['WeaponEffect']] += int(prefix_modifiers[prefix_activator]['Bonus'])
                                if x['Name'][0] in VOWELS:
                                    print('>The %s crumbles to dust, and your %s becomes an %s.' % (slate2.lower(), slate1.lower(), x['Name'].lower()))
                                else:
                                    print('>The %s crumbles to dust, and your %s becomes a %s.' % (slate2.lower(), slate1.lower(), x['Name'].lower()))
                                player.inventory.remove(slate2)
                            if x['Type'] == 'Armor':
                                x['Name'] = '%s %s' % (prefix_activator, x['Name'])
                                x['Enchanted'] = True
                                x[prefix_modifiers[prefix_activator]['ArmorEffect']] += int(prefix_modifiers[prefix_activator]['Bonus'])
                                if x['Name'][0] in VOWELS:
                                    print('>The %s crumbles to dust, and your %s becomes an %s.' % (slate2.lower(), slate1.lower(), x['Name'].lower()))
                                else:
                                    print('>The %s crumbles to dust, and your %s becomes a %s.' % (slate2.lower(), slate1.lower(), x['Name'].lower()))
                                player.inventory.remove(slate2)
            else:
                print('>Nothing happens.')
    return player

prefix_groups = {'Flaming 1': ['Shredded Hood', 'Torn Parchment', 'Hardened Twig',
                               'Wheel Axle', 'Strike-Stone', 'Candlewick',
                               'Moldy Tome', 'Red Beetle', 'Orange Beetle',
                               'Yellow Beetle'],
                 'Flaming 2': ['Shredded Hood', 'Torn Parchment', 'Hardened Twig',
                               'Wheel Axle', 'Strike-Stone', 'Candlewick',
                               'Moldy Tome', 'Red Beetle', 'Orange Beetle',
                               'Yellow Beetle'],
                 'Flaming 3': ['Shredded Hood', 'Torn Parchment', 'Hardened Twig',
                               'Wheel Axle', 'Strike-Stone', 'Candlewick',
                               'Moldy Tome', 'Red Beetle', 'Orange Beetle',
                               'Yellow Beetle'],
                 'Earthen 1': ['Hardened Twig', 'Worn Shoe', 'Dirt Clod',
                               'Worm Larvae', 'Moth Larvae', 'Green Beetle',
                               'Blue Beetle', 'Yellow Beetle'],
                 'Earthen 2': ['Hardened Twig', 'Worn Shoe', 'Dirt Clod',
                               'Worm Larvae', 'Moth Larvae', 'Green Beetle',
                               'Blue Beetle', 'Yellow Beetle'],
                 'Earthen 3': ['Hardened Twig', 'Worn Shoe', 'Dirt Clod',
                               'Worm Larvae', 'Moth Larvae', 'Green Beetle',
                               'Blue Beetle', 'Yellow Beetle', 'Boar Tusk'],
                 'Dampened 1': ['Damp String', 'Indigo Beetle',
                                'Violet Beetle', 'Blue Beetle'],
                 'Dampened 2': ['Damp String', 'Indigo Beetle',
                                'Violet Beetle', 'Blue Beetle'],
                 'Dampened 3': ['Damp String', 'Indigo Beetle',
                                'Violet Beetle', 'Blue Beetle'],
                 'Aerial 1': ['Owl Pellet', 'Torn Parchment', 'Moth Larvae',
                              'Hawk Egg', 'Sparrow Egg', 'Yellow Beetle'],
                 'Aerial 2': ['Owl Pellet', 'Torn Parchment', 'Moth Larvae',
                              'Hawk Egg', 'Sparrow Egg', 'Yellow Beetle'],
                 'Aerial 3': ['Owl Pellet', 'Torn Parchment', 'Moth Larvae',
                              'Hawk Egg', 'Sparrow Egg', 'Yellow Beetle'],
                 'Lucky': ['Card Deck', 'Wooden Dice', 'Rabbit Foot'],
                 'Good': ['Love Letter', 'Cloth Doll'],
                 'Evil': ['Old Bone', 'Dead Mouse', 'Rusty Nail', 'Skull'],
                 'Empowered': ['Shiny Stone', 'Modly Tome', 'Pixie Dust'],
                 'Deadened': ['Old Bone', 'Dirt Clod', 'Damp String'],
                 'Well-Used': ['Old Bone', 'Owl Pellet', 'Dead Mouse', 'Worn Shoe', 'Moldy Tome'],
                 'Rusted': ['Old Bone', 'Rusty Nail', 'Broken Amulet'],
                 'Deplorable': ['Dead Mouse', 'Wheel Axle'],
                 'Ancient': ['Broken Amulet', 'Moldy Tome'],
                 'Silent': ['Glass Shard', 'Moth Larvae'],
                 'Damascan': ['Odd Leaf'],
                 }
prefix_groups_list = ['Flaming 1', 'Flaming 2', 'Flaming 3', 'Earthen 1',
                      'Earthen 2', 'Earthen 3', 'Dampened 1', 'Dampened 2',
                      'Dampened 3', 'Aerial 1', 'Aerial 2', 'Aerial 3',
                      'Lucky', 'Good', 'Evil', 'Empowered', 'Deadened',
                      'Well-Used', 'Rusted', 'Deplorable', 'Ancient',
                      'Silent', 'Damascan']