"""Manage and edit player player.inventory"""

import random

import dicts

def check(player, item_map, coords):
    """Verifies held items do not exceed carry limit, and drops some if they do."""
    if len(player.inventory) > player.defaults['InvHoldLen']:
        dropped = random.choice(player.inventory)
        player.inventory.remove(dropped)
        item_map[coords].append(dropped)
        try:
            print('>You dropped your %s.' % (dropped.lower()))
        except AttributeError:
            print('>You dropped your %s.' % (dropped.lower()))
    return player, item_map
def equip_item(player, usables, item):
    """Manages equipping/unequipping and changing stats."""
    if item['Type'] == 'Armor':
        remove_item = player.equipped['Armor']
        for stat in ['Power', 'Damage', 'Stamina']:
            player.stats[stat] -= remove_item[stat]
            player.stats[stat] += item[stat]
        player.stats['Defense'] -= remove_item['Bonus']
        player.stats['Defense'] += item['Bonus']
        player.equipped['Armor'] = item
    else:
        remove_item = player.equipped['Weapon']
        for stat in ['Power', 'Stamina', 'Defense']:
            player.stats[stat] -= remove_item[stat]
            player.stats[stat] += item[stat]
        if remove_item['BonusType'] == 'Add':
            player.stats['Damage'] -= remove_item['Bonus']
            player.stats['Damage'] += item['Bonus']
        else:
            player.stats['Damage'] -= (remove_item['Bonus']*player.stats['Level'])
            player.stats['Damage'] += (remove_item['Bonus']*player.stats['Level'])
        player.equipped['Weapon'] = item
    player.inventory.append(remove_item)
    return player
def loot_monster(monster, player, item_map, coords, usables, usables_list):
    """Manages loot appendation to player.inventory"""
    vowels = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]
    try:
        item_dropped = random.choice(monster["Carries"])
    except IndexError:
        print(">The %s wasn't carrying anything." % monster["Name"].lower())
        item_dropped = None
    if item_dropped == "Item":
        item = random.choice(monster["Items"])
        if len(player.inventory) < player.defaults["InvHoldLen"]:
            player.inventory.append(item)
            if item[0] in vowels:
                print(">The %s was carrying an %s." % (monster["Name"].lower(), item.lower()))
            else:
                print(">The %s was carrying a %s." % (monster["Name"].lower(), item.lower()))
            print(">You pick up the %s." % item.lower())
        else:
            item_map[coords].append(item)
            print(">Unable to carry the %s's %s, \n you drop it on the ground." % \
                  (monster["Name"].lower(), item.lower()))
    if item_dropped == "Misc":
        item = random.choice(dicts.ITEMS)
        if len(player.inventory) < player.defaults["InvHoldLen"]:
            player.inventory.append(item)
            if item[0] in vowels:
                print(">The %s was carrying an %s." % (monster["Name"].lower(), item.lower()))
            else:
                print(">The %s was carrying a %s." % (monster["Name"].lower(), item.lower()))
            print(">You pick up the %s." % item.lower())
        else:
            item_map[coords].append(item)
            print(">Unable to carry the %s's %s, \n you drop it on the ground." % \
                  (monster["Name"].lower(), item.lower()))
    if item_dropped == "Usables":
        chosen = False
        while chosen is False:
            item = random.choice(usables_list)
            if usables[item]["Appearance Level"] <= player.stats["Level"]:
                chosen = True
        if item[0] in vowels:
            print(">The %s was carrying an %s." % (monster["Name"].lower(), item.lower()))
        else:
            print (">The %s was carrying a %s." % (monster["Name"].lower(), item.lower()))
        if usables[item]["Type"] == "Weapon" or usables[item]["Type"] == "Armor":
            equipable = {"Name": item,
                         "Type": usables[item]["Type"],
                         "Bonus": usables[item]["Bonus"],
                         "Power": usables[item]["Power"],
                         "Stamina": usables[item]["Stamina"],
                        }
            if equipable["Type"] == "Armor":
                equipable["SentenceStructure"] = usables[item]["SentenceStructure"]
                equipable["Retaliation"] = usables[item]["Retaliation"]
                equipable["Damage"] = usables[item]["Damage"]
            else:
                equipable["BonusType"] = usables[item]["BonusType"]
                equipable["Defense"] = usables[item]["Defense"]
        else:
            equipable = item
        if len(player.inventory) < player.defaults["InvHoldLen"]:
            player.inventory.append(equipable)
            print (">You pick up the %s." % item.lower())
        else:
            item_map[coords].append(equipable)
            print(">Unable to carry the %s's %s, \n \
                  you drop it on the ground." % (monster["Name"].lower(), item.lower()))
    if item_dropped == "Gold":
        item = random.randint(1, player.defaults["MaxGold"])
        print(">The %s was carrying %s gold." % (monster["Name"].lower(), item.lower()))
        player.gold += item
    return player, item_map
