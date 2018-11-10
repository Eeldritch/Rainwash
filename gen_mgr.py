"""Generatres, biomes, monsters, containers, special events, etc."""

import random

def get_biome(biome_choice):
    """Returns biome from chosen percentile"""
    for x in BIOMES:
        if int(biome_choice) in BIOMES[x]:
            return x

def get_container(biome, container_choice, containers):
    """Returns container in reference to biome"""
    for x in containers:
        if container_choice in containers[x]['Numbers']:
            if biome in containers[x]['Biome']:
                return x
            return "Nothing"

def get_new_monster(monster_compendium, monster_dict, player, biome):
    """Generates new monsters"""
    new_monster = random.choice(monster_dict)
    new_monster_champion = False
    if biome in monster_compendium[new_monster]['Biomes'] and monster_compendium[new_monster]['MaxLevel'] - player.stats['Level'] <= 5:
        new_monster_stats = {}
        if monster_compendium[new_monster]['MaxLevel'] <= player.stats['Level']:
            new_monster_stats['HP'] = random.randint(monster_compendium[new_monster]['HPModifier'][0], monster_compendium[new_monster]['HPModifier'][1] + player.stats['Level'])
            new_monster_stats['Damage'] = random.randint(monster_compendium[new_monster]['DamageModifier'][0], monster_compendium[new_monster]['DamageModifier'][1] + player.stats['Level'])
            if new_monster_stats['HP'] == monster_compendium[new_monster]['HPModifier'][1] + player.stats['Level'] and new_monster_stats['Damage'] == monster_compendium[new_monster]['DamageModifier'][1] + player.stats['Level']:
                new_monster_champion = True
        else:
            new_monster_stats['HP'] = random.randint(monster_compendium[new_monster]['HPModifier'][0],
                                                     monster_compendium[new_monster]['HPModifier'][1]) + monster_compendium[new_monster]['MaxLevel']
            new_monster_stats['Damage'] = random.randint(monster_compendium[new_monster]['DamageModifier'][0], monster_compendium[new_monster]['DamageModifier'][1]) + monster_compendium[new_monster]['MaxLevel']
            if new_monster_stats['HP'] == monster_compendium[new_monster]['HPModifier'][1] + monster_compendium[new_monster]['MaxLevel'] and new_monster_stats['Damage'] == monster_compendium[new_monster]['DamageModifier'][1] + monster_compendium[new_monster]['MaxLevel']:
                new_monster_champion = True
        if new_monster_champion is True:
            new_monster_name = monster_compendium[new_monster]['ChampionName']
        else:
            new_monster_name = new_monster
        add_monster = {'Name': new_monster_name, 'HP': new_monster_stats['HP'],
                       'MaxHP': new_monster_stats['HP'],
                       'Damage': new_monster_stats['Damage'],
                       'Carries': monster_compendium[new_monster]['Carries'],
                       'XP': monster_compendium[new_monster]['XP'],
                       'Epic': monster_compendium[new_monster]['Epic']
                      }
        if add_monster['Epic'] is True:
            add_monster['EpicType'] = monster_compendium[new_monster]['EpicType']
        if 'Item' in add_monster['Carries']:
            add_monster['Items'] = monster_compendium[new_monster]['Items']
        return add_monster, True
    return None, False

def variant_actions(container_map_queue, monster_queue, variant):
    """Queueing system for biome variants"""
    if VARIANT_ACTION[variant]["Type"] == 1:
        container_map_queue.append(VARIANT_ACTION[variant]["Add"])
    if VARIANT_ACTION[variant]["Type"] == 2:
        monster_queue.append(VARIANT_ACTION[variant]["Add"])
    return container_map_queue, monster_queue

BIOMES = {"a Forest": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                       22, 23, 24, 25],
          "the Plains": [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
                         45, 46, 47, 48, 49, 50],
          "the Mountains": [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                            69, 70, 71, 72, 73, 74, 75],
          "some Ruins": [76, 77, 78, 79, 80, 81, 82, 83, 84, 85],
          "a Castle": [86, 87, 88, 89, 90],
          "a Dungeon": [91, 92, 93, 94, 95],
          "a Graveyard": [96, 97, 98, 99, 100],}

VARIANTS = {"a Forest": ["Sparse Clearing", "Dying Oak", "Fairy Circle",
                         "Cobwebs", "Birches", "Tusk Marks",
                         "Awful Stench", "Fire Pit", "Flowers"],
            "the Plains": ["Tall Grass", "Odd Birdcall", "Flowers",
                           "Chittering", "Charred Fields"],
            "the Mountains": ["Howling Peaks", "Wind-Torn Tree", "Rocky Pass",
                              "Biting Sleet", "Odd Birdcall", "Bone Pit",
                              "Collapsed Cave"],
            "some Ruins": ["Row of Statues", "Stone Basin", "Bone Pit",
                           "Awful Stench", "Ivy-Covered Wall",
                           "Collapsed Cave"],
            "a Castle": ["Rows of Arrow-Slits", "Odd Birdcall", "Cobwebs",
                         "Chittering", "Fire Pit", "Winding Tower",
                         "Ancient Tapestry"],
            "a Dungeon": ["Cobwebs", "Chittering", "Awful Stench", "Bone Pit"],
            "a Graveyard": ["Cobwebs", "Dying Oak", "Decrepit Gravestones",
                            "Upturned Earth", "Distant Screaming"]}

VARIANT_DESCRIPTIONS = {"Sparse Clearing": "The trees here thin out to a sparse \n clearing, with light ground covering.",
                        "Dying Oak": "A massive leafless oak tree clings desperately \n to the last shreds of its life.",
                        "Fairy Circle": "A ring of toadstools arises on the ground \n in front of you--a fairy circle.",
                        "Cobwebs": "Huge white cobwebs stretch around you, remnants of their \n prey leaving a miasma of death.",
                        "Birches": "Tall white birch trees surround you, shedding bits of white \n bark on the forest floor.",
                        "Tusk Marks": "The trees around you are covered with scrapes and gouges, \n as if by some tusked beast...",
                        "Awful Stench": "An awful stench overcomes you--you feel like vomiting. \n Something very, very close is very, very decayed.",
                        "Fire Pit": "A circle of stones surrounds a pile of charred sticks and ash. \n A few glowing embers remain--this fire is recent.",
                        "Flowers": "Hundreds of vibrant wildflowers envelop you with \n their sweet aromas.",
                        "Tall Grass": "The grass here is unusually tall, some having grown \n up to your neck.",
                        "Odd Birdcall": "A strange birdcall in the distance sets you on edge...",
                        "Chittering": "You hear unusual chittering and clicking \n nearby, like that of a large spider...",
                        "Charred Fields": "The grass here is charred and burnt, as if a recent wildfire \n was quenched by the rain.",
                        "Howling Peaks": "The wind howls and screams through the \n peaks above you. The haunting sound sets your nerves on edge.",
                        "Wind-Torn Tree": "A lone tree clings to the side of a cliff above you. \n The wind has long since stripped away its bark.",
                        "Rocky Pass": "Here, the peaks split to make a rocky pass across the mountains.",
                        "Biting Sleet": "The rain freezes and clings to your \n clothing and body, biting your bare skin and face.",
                        "Bone Pit": "You peer downwards into a pit of bones. \n Some shake and move suspiciousy.",
                        "Collapsed Cave": "The collapsed entrance to some cave or tunnel \n looms in front of you.",
                        "Row of Statues": "You come face-to-face with a row of grotesque statues.",
                        "Stone Basin": "A massive stone basin dominates the center of \n the room. Rain water spills out over its edges like a fountain.",
                        "Ivy-Covered Wall": "One wall is covered with ivy, which has slowly \n cracked the wall to the point of disrepair.",
                        "Rows of Arrow-Slits": "One wall has dozens of arrow slits, which start \n wide on the inside and narrow towards the outside, \n giving archers safety during seige.",
                        "Winding Tower": "You peer out of an ancinet stone window, and \n gaze over the flooding land from the peak of what appears \n to be a winding tower.",
                        "Ancient Tapestry": "An rotting, tattered tapestry hangs from one wall. \n It depicts some ancient battle with a strange beast, \n whose body is made of roiling black clouds and whose weapons \n seem forged of the lightning itself.",
                        "Decrepit Gravestone": "The gravestones here are crumbling and decayed-- \n they are older than most.",
                        "Upturned Earth": "The earth at your feet has been recently upturned...",
                        "Distant Screaming": "In the distance, you hear a wailing scream of \n dispair, which echoes through the land.",}

MAP_SPECIALS = {"Coords": {"15, 15": "Pylon I", "15, -15": "Pylon II",
                           "-15, -15": "Pylon III", "-15, 15": "Pylon IV",
                          },
              "Descriptions": {"Pylon I": (">You approach a clearing with a long stone obelisk in the center. \n This blue granite pylon faintly oozes moisture. As you approach it, \n the condensation collects into a small, thin form, who glares menacingly."),
                               "Pylon II": (">You enter a dark, dank alcove--almost cavelike, but smaller, with a long \n stone obelisk in the center. \n This misty grey pylon sems to swirl and steam inside. As you approach it, \n the sky around you darkens, and a shadowy figure emerges from inside \n the stone."),
                               "Pylon III": (">You approach a circle of black, charred earth with a long stone \n obelisk in the center. This pylon is blindingly white, a crackles with energy. \n As you approach it, a man flashes into existence, his body pure energy."),
                               "Pylon IV": (">You approach a wind-blown hilltop, thunder roaring in your ears. \n A long stone obelisk resonates with a screaming, crashing sound. \n A figure emerges from the pylon, his face harrowed and crazed, \n and lunges at you."),
                              },
              "Monsters": {"Pylon I": [{"Name": ("Sodden Soul"), "HP": (60), "MaxHP": (70), "Damage": (20), "Carries": [], "Epic": True, "EpicType": ("Water"), "XP": (40)}],
                           "Pylon II": [{"Name": ("Shadowed Soul"), "HP": (60), "MaxHP": (60), "Damage": (20), "Carries": [], "Epic": True, "EpicType": ("Shadow"), "XP": (40)}],
                           "Pylon III": [{"Name": ("Searing Soul"), "HP": (60), "MaxHP": (60), "Damage": (27), "Carries": [], "Epic": True, "EpicType": ("Lightning"), "XP": (40)}],
                           "Pylon IV": [{"Name": ("Thundering Soul"), "HP": (60), "MaxHP": (60), "Damage": (23), "Carries": [], "Epic": True, "EpicType": ("Thunder"), "XP": (40)}],
                          },
}

CONTAINERS = {"BARREL": {"Numbers": [1, 2, 3, 4, 5], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Castle", "a Dungeon", "a Graveyard"],
                         "Holds": ["Usables", "Misc", "Misc"],
                        },
                "SACK": {"Numbers": [6, 7], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Castle", "a Dungeon", "a Graveyard"],
                           "Holds": ["Gold", "Misc"],
                         },
                "CRATE": {"Numbers": [11, 12, 13, 14, 15], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Castle", "a Dungeon", "a Graveyard"],
                            "Holds": ["Usables", "Misc", "Misc"],
                          },
                "EAGLE'S NEST": {"Numbers": [16], "Biome": ["a Forest", "the Mountains"],
                                 "Holds": ["Misc"],
                                 },
                "CHEST": {"Numbers": [21, 22, 23, 24, 25], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Castle", "a Dungeon", "a Graveyard"],
                            "Holds": ["Gold", "Usables"],
                          },
                "HOLLOW TREE": {"Numbers": [26, 27, 28, 29, 30], "Biome": ["a Forest", "a Graveyard"],
                                 "Holds": ["Usables", "Misc"],
                                },
                "CORPSE": {"Numbers": [31, 32, 33], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Dungeon", "a Graveyard"],
                             "Holds": ["Gold", "Usables", "Misc"],
                           },
                "WINESKIN": {"Numbers": [34, 35], "Biome": ["a Dungeon", "a Castle"],
                               "Holds": ["Misc"],
                             },
                "HOLE": {"Numbers": [36, 37, 38], "Biome": ["a Forest", "the Plains", "the Mountains"],
                                          "Holds": ["Misc"],
                                       },
                "ANCIENT SHIPWRECK": {"Numbers": [39, 40], "Biome": ["the Plains"],
                                        "Holds": ["Gold", "Usables"],
                                      },
                "OVERTURNED BOWL": {"Numbers": [41, 42], "Biome": ["some Ruins", "a Dungeon"],
                                     "Holds": ["Gold", "Misc"],
                                    },
                "BACKPACK": {"Numbers": [43, 44, 45], "Biome": ["a Forest", "the Mountains"],
                                "Holds": ["Gold", "Usables", "Misc"],
                             },
                "WRECKED SHRINE": {"Numbers": [46, 47, 48], "Biome": ["some Ruins", "a Graveyard"],
                                    "Holds": ["Gold", "Usables"],
                                   },
                "COFFIN": {"Numbers": [49, 50], "Biome": ["a Graveyard"],
                             "Holds":["Weapns", "Misc"],
                           },
                "VASE": {"Numbers": [51, 52, 53, 54, 55], "Biome": ["some Ruins", "a Castle", "a Dungeon"],
                           "Holds": ["Gold", "Misc"],
                         },
                "CHAMBER POT": {"Numbers": [56, 57, 58, 59, 60], "Biome": ["some Ruins", "a Dungeon"],
                                 "Holds": ["Misc"],
                                },
                "ABANDONED COINPURSE": {"Numbers": [61, 62, 63, 64, 65], "Biome": ["a Forest", "the Plains", "the Mountains", "some Ruins", "a Castle", "a Dungeon", "a Graveyard"],
                                         "Holds": ["Gold"],
                                        },
                "RABBIT HOLE": {"Numbers": [66, 67, 68, 69, 70], "Biome": ["a Forest", "the Plains"],
                                 "Holds": ["Misc"],
                                },
                "TALL GRASS": {"Numbers": [71, 72, 73, 74, 75], "Biome": ["a Forest", "the Plains"],
                                "Holds": ["Misc"],
                               },
                "ABANDONED CART": {"Numbers": [76, 77, 78, 79, 80], "Biome": ["a Forest", "the Plains", "the Mountains"],
                                    "Holds": ["Gold", "Usables", "Misc"],
                                   },
                "AVALANCHE-BURIED CARAVAN": {"Numbers": [81, 82, 83], "Biome": ["the Mountains"],
                                              "Holds": ["Gold", "Usables", "Misc"],
                                             },
                "TENT": {"Numbers": [84, 85], "Biome": ["the Plains"],
                           "Holds": ["Usables", "Misc"],
                         },
                "DITCH": {"Numbers": [86, 87, 88, 89, 90], "Biome": ["the Plains"],
                            "Holds": ["Misc"],
                          },
                "HOLLOW-MOUTHED STATUE": {"Numbers": [91, 92, 93], "Biome": ["some Ruins"],
                                          "Holds": ["Usables"],
                                          },
                "RANSACKED FARMHOUSE": {"Numbers": [94, 95, 96], "Biome": ["a Forest", "the Plains"],
                                         "Holds": ["Gold", "Usables", "Misc"],
                                        },
                "ANCIENT TOWER": {"Numbers": [97, 98], "Biome": ["the Mountains"],
                                   "Holds": ["Gold", "Usables"],
                                  },
                "SHELVES": {"Numbers": [99], "Biome": ["a Dungeon"],
                              "Holds": ["Usables"],
                            },
                "SEALED BOX": {"Numbers": [100], "Biome": ["a Dungeon"],
                                "Holds": ["Usables"],
                               },
                "DYING OAK": {"Numbers": [], "Biome": [],
                              "Holds": ["Usables", "Usables", "Misc"],
                              },
                "BARK PILE": {"Numbers": [], "Biome": [],
                              "Holds": ["Misc", "Misc", "Usables"],
                              },
                "ASH PILE": {"Numbers": [], "Biome": [],
                             "Holds": ["Misc", "Misc", "Gold", "Gold", "Usables"],
                             },
                }
VARIANT_ACTION = {"Sparse Clearing": {"Type": 1, "Add":("Ditch")},
                  "Dying Oak": {"Type": 1, "Add":("Dying Oak")},
                  "Fairy Circle": {"Type": 2, "Add":({"Name": ("Fairy"), "HP": (20), "MaxHP": (20), "Damage": (7), "Carries": ["Item"], "Items": ("Pixie Dust"), "Epic": False, "XP": (0)})},
                  "Cobwebs": {"Type": 2, "Add":({"Name": ("Master Spinner Spider"), "HP": (15), "MaxHP": (20), "Damage": (10), "Carries": [], "Epic": True, "EpicType": ("Spider"), "XP": (10)})},
                  "Birches": {"Type": 1, "Add":("Bark Pile")},
                  "Tusk Marks": {"Type": 2, "Add":({"Name": ("Furious Boar"), "HP": (40), "MaxHP": (40), "Damage": (12), "Carries": ["Item"], "Items": ("Boar Tusk"), "Epic": False, "XP": (20)})},
                  "Awful Stench": {"Type": 2, "Add":({"Name": ("Decrepit Zombie"), "HP": (40), "MaxHP": (60), "Damage": (4), "Carries": [], "Epic": False, "XP": (20)})},
                  "Fire Pit": {"Type": 1, "Add":("Ash Pile")},
                  "Flowers": {"Type": 0},
                  "Tall Grass": {"Type": 0},
                  "Odd Birdcall": {"Type": 2, "Add":({"Name": ("Orc Scout"), "HP": (14), "MaxHP": (14), "Damage": (8), "Carries": ["Item"], "Items": ("Raw Venison Steak", "Boar Tusk"), "Epic": False, "XP": (10)})},
                  "Chittering": {"Type": 2, "Add":({"Name": ("Giant Brown Recluse"), "HP": (13), "MaxHP": (13), "Damage": (13), "Carries": [], "Epic": False, "XP": (10)})},
                  "Charred Fields": {"Type": 1, "Add":("Ash Pile")},
                  "Howling Peaks": {"Type": 0},
                  "Wind-Torn Tree": {"Type": 0},
                  "Rocky Pass": {"Type": 0},
                  "Biting Sleet": {"Type": 0},
                  "Bone Pit": {"Type": 2, "Add":({"Name": ("Carrion Rat"), "HP": (18), "MaxHP": (18), "Damage": (14), "Carries": [], "Epic": False, "XP": (20)})},
                  "Collapsed Cave": {"Type": 0},
                  "Row of Statues": {"Type": 1, "Add":("Hollow-Mouthed Statue")},
                  "Stone Basin": {"Type": 0},
                  "Ivy-Covered Wall": {"Type": 0},
                  "Rows of Arrow-Slits": {"Type": 0},
                  "Winding Tower": {"Type": 1, "Add":("Sealed Box")},
                  "Ancient Tapestry": {"Type": 0},
                  "Decrepit Gravestone": {"Type": 0},
                  "Upturned Earth": {"Type": 2, "Add":({"Name": ("Necromancer"), "HP": (10), "MaxHP": (10), "Damage": (9), "Carries": ["Item"], "Items": ("Old Bone"), "Epic": True, "EpicType": ("Undead"), "XP": (10)})},
                  "Distant Screaming": {"Type": 0},
                  }
