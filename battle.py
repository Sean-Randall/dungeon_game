#battle.py
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Lists
player_spells = [fire, thunder, blizzard, meteor, cure, curaga]
enemy_spells = [fire, meteor, curaga]
player_items = [
    {"item": potion, "quantity": 15},
    {"item": hipotion, "quantity": 5},
    {"item": superpotion, "quantity": 5},
    {"item": elixer, "quantity": 5},
    {"item": hielixer, "quantity": 2},
    {"item": grenade, "quantity": 5}
]

# Instantiate People
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
def start_battle(players, enemies):
    running = True

    print(bcolors.FAIL + bcolors.BOLD + "Your party has entered the monsters' room!" + bcolors.ENDC)

    while running:
        print("======================")

        print("\nNAME                 HP                                     MP")
        for player in players:
            player.get_stats()

        print("")
        for enemy in enemies:
            enemy.get_enemy_stats()

        for player in players:
            if player.get_hp() == 0:
                print(f"{player.name.replace(' ', '')} is dead and cannot take actions.")
                continue

            player.choose_action()
            choice = input("    Choose action: ")
            index = int(choice) - 1

            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)
                if enemy is None:
                    continue
                enemies[enemy].take_damage(dmg)
                print(f"You attacked {enemies[enemy].name.strip()} for {dmg} points of damage.")
                if enemies[enemy].get_hp() == 0:
                    print(f"{enemies[enemy].name.strip()} has died.")
                    del enemies[enemy]

            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("    Choose magic: ")) - 1
                if magic_choice == -1:
                    continue
                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()
                if spell.cost > player.get_mp():
                    print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue
                player.reduce_mp(spell.cost)
                if spell.type == "white":
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + f"\n{spell.name} heals for {magic_dmg} HP." + bcolors.ENDC)
                elif spell.type == "black":
                    enemy = player.choose_target(enemies)
                    if enemy is None:
                        continue
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + f"\n{spell.name} deals {magic_dmg} damage to {enemies[enemy].name.strip()}" + bcolors.ENDC)
                    if enemies[enemy].get_hp() == 0:
                        print(f"{enemies[enemy].name.strip()} has died.")
                        del enemies[enemy]

            elif index == 2:
                player.choose_item()
                item_choice = int(input("    Choose item: ")) - 1
                if item_choice == -1:
                    continue
                item = player.items[item_choice]["item"]
                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
                    continue
                player.items[item_choice]["quantity"] -= 1
                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + f"\n{item.name} heals for {item.prop} HP" + bcolors.ENDC)
                elif item.type == "elixer":
                    if item.name == "MegaElixer":
                        for p in players:
                            p.hp = p.maxhp
                            p.mp = p.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKGREEN + f"\n{item.name} fully restores HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy = player.choose_target(enemies)
                    if enemy is None:
                        continue
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + f"\n{item.name} deals {item.prop} damage to {enemies[enemy].name.strip()}" + bcolors.ENDC)
                    if enemies[enemy].get_hp() == 0:
                        print(f"{enemies[enemy].name.strip()} has died.")
                        del enemies[enemy]

        # Check victory/defeat
        if len(enemies) == 0:
            print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
            running = False
            break
        elif all(p.get_hp() == 0 for p in players):
            print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
            running = False
            break

        # Enemy attack phase
        for enemy in enemies:
            if enemy.get_hp() == 0:
                continue
            enemy_choice = random.randint(0, 1)

            target = random.choice([p for p in players if p.get_hp() > 0])

            if enemy_choice == 0:
                enemy_dmg = enemy.generate_damage()
                target.take_damage(enemy_dmg)
                print(f"{enemy.name.strip()} attacks {target.name.strip()} for {enemy_dmg}")
            elif enemy_choice == 1:
                spell = random.choice(enemy.magic)
                magic_dmg = spell.generate_damage()
                if spell.cost > enemy.get_mp():
                    continue
                enemy.reduce_mp(spell.cost)
                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(f"{enemy.name.strip()} casts {spell.name} and heals for {magic_dmg}")
                elif spell.type == "black":
                    target.take_damage(magic_dmg)
                    print(f"{enemy.name.strip()} casts {spell.name} and deals {magic_dmg} to {target.name.strip()}")
    if len(enemies) == 0:
        return "win"
    elif all(p.get_hp() == 0 for p in players):
        return "lose"