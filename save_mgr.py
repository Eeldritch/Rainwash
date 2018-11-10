"""Handles saves"""

def save_primer():
    """Primes base stats"""
    return {}, {}, {}, 0, 0, "0, 0", [], 0, [], [], [], False, \
           [], [], \
           None, False

def load_save(save_data):
    """Loads save data"""
    travellers = save_data["Travellers"]
    travellers_here = save_data["TravellersHere"]
    try:
        for x in travellers_here["Effects"]:
            travellers_here["Effects"][x]["ASE"] = locals()[travellers_here["Effects"][x]["ASE"]]
    except TypeError:
        pass
    class PlayerStruct:
        def __init__(self):
            self.stats = save_data['Stats']
            self.pclass = save_data['PClass']
            self.learned_commands = save_data['LearnedCommands']
            self.inventory = save_data['Inventory']
            self.equipped = save_data['Equipped']
            self.gold = save_data['Gold']
            self.active_status_effects = save_data['ASE']
            self.defaults = save_data['Defaults']
            self.actions = save_data['Actions']
    player = PlayerStruct()
    return player, save_data['Biome'], save_data['LocalMap'], save_data['ContainerMap'], \
           save_data['ItemMap'], save_data['XCoord'], save_data['YCoord'], \
           '%s, %s' % (str(save_data['XCoord']), str(save_data['YCoord'])), \
           save_data['FireLit'], save_data['MonsterList'], save_data['Monsters'], \
           save_data['MonsterQueue'], travellers, travellers_here

def write_save(save_data, player, local_map, container_map, item_map, x_coord, y_coord, biome, \
               fire_lit, travellers, travellers_here, monster_list, monsters, monster_queue):
    """Writes save data"""
    save_data['Stats'] = player.stats
    save_data['PClass'] = player.pclass
    save_data['LearnedCommands'] = player.learned_commands
    save_data['Inventory'] = player.inventory
    save_data['Equipped'] = player.equipped
    save_data['Gold'] = player.gold
    save_data['ASE'] = player.active_status_effects
    save_data['Defaults'] = player.defaults
    save_data['Actions'] = player.actions
    save_data['LocalMap'] = local_map
    save_data['ContainerMap'] = container_map
    save_data['ItemMap'] = item_map
    save_data['XCoord'] = x_coord
    save_data['YCoord'] = y_coord
    save_data['Biome'] = biome
    save_data['FireLit'] = fire_lit
    save_data['Travellers'] = travellers
    save_data['TravellersHere'] = travellers_here
    save_data['MonsterList'] = monster_list
    save_data['Monsters'] = monsters
    save_data['MonsterQueue'] = monster_queue
    return save_data
