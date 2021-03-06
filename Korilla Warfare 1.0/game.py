#!/usr/bin/python3
import time
from map import rooms
from player import *
from items import *
from gameparser import *
from enemy import *
import random
import sys

global type_attack

type_attack = ["Slash", "Fire", "Stab", "Bludgeon", "Gun"]
#declares a list of attack types, to calculate "super effective" "not very effective" etc. 
def class_decide(question):
    #is used to pick your class at the start of the game
    global inventory
    global hp
    global temp_hp
    global class_name
    #declares these as global variables so you don't have to use dictionary variable names throughout the code
    print("choose a class from:" + """ 
        
        Warrior - Warriors have increased health starting at 200HP and come equipped with a sword.

        Mage - Mages start with basic health at 150HP and a powerful mage staff

        Rogue - Rogues start with basic health at 130HP and a dagger. Rogues are sneaky and lightfooted giving you the opportunity to skip some obstacles.

        Cleric - Clerics have less health than the other classes but have a special ability to heal themselves one time. Starts with a sturdy mace!\n""")

    reply = str(input(question + '(w/m/r/c)' + " to decide:")).lower().strip()
    #asks user what class they want to choose by asking them to input single characters 
    if len(reply) < 1:
        class_decide("please enter ")
    elif reply[0] == 'w':
        inventory = warrior["inventory"] 
        hp = warrior["hp"]
        temp_hp = warrior["temp_hp"]
        class_name = "warrior"
    elif reply[0] == 'm':
        inventory = mage["inventory"]
        hp = mage["hp"]
        temp_hp = mage["temp_hp"]
        class_name = "mage"
    elif reply[0] == 'r':
        inventory = rogue["inventory"]
        hp = rogue["hp"]
        temp_hp = rogue["temp_hp"]
        class_name = "rogue"
    elif reply[0] == 'c':
        inventory = cleric["inventory"]
        hp = cleric["hp"]
        temp_hp = cleric["temp_hp"]
        class_name = "cleric"
    else: 
        class_decide("please enter ")
        #sets the global variables to equal those defined in the player module
        
def list_of_items(items):
    return ", ".join(i["name"] for i in items) 
     #returns items as a string for viewing in the game     

def print_room_items(room):
    #tells the user what items there are in the room
       if len(room["items"]) != 0: 
        print("There is " + str(list_of_items(room["items"]) + " here."))  
        print("") 
def print_inventory_items(items):
    global gold
    #tells the user what items they have in their inventory 
    if len(list_of_items(items)) > 0:
        print("You have " + str(list_of_items(items)) + ".") 
        print("")
    if current_room["name"] == "General Store": #added gold amount player has
        print("You have ", str(gold), " gold coins.")
        print("")

def yes_or_no(question):
    #declares function for asking the user a closed question 
    reply = str(input(question+' (y/n): ')).lower().strip()
    if len(reply) < 1:
        return yes_or_no("please enter y/n")
    elif reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    #loops through until they answer with either y/n 

def print_enemies(enemies):
    global current_room
    global prev_room
    global inventory
    global temp_hp
    #declares variables globally to allow us to manipulate them 
    print("Your health is",temp_hp,"\n")
    x = []
    for enemy_ in enemies:
        #enemy_ used so we dont colide with enemy module 
        x.append(enemy_["name"])
        #adds the enemies that are in the list so we print it off as a nice string. 
    if len(inventory)==0:
        #MAKE SURE ATTACK ITEM NOT JUST ANY ITEM. 
        current_room = prev_room
        print("There are enemies ahead, arm yourself!")
        print_room(current_room)
    else:
        print("There is " + str(x) + " here.")
        question = "Do you want to fight?"
        #asks the user whether they want to fight the current enemies or flee for the time being
        if yes_or_no(question) == False:
            current_room = prev_room
            print("You run back where you came from... Like a pussy.")
            print_room(current_room)
        else:
            return True       
def print_room(room):
    # Display room name
    print("")
    print(room["name"].upper())
    print("")
    # Display room description
    print(room["description"])
    print("")


    
    if len(room["items"]) != 0: 
        print_room_items(room) 



def print_arena(enemies):
    for current in enemies:
        print(current["name"] + ":" + str(current["temp_hp"]))
        #prints the enemies along with their current hp

def exit_leads_to(exits, direction):
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    print("GO " + direction.upper() + " to " + leads_to + ".")

def print_menu(exits, room_items, inv_items, room_market):
    print("_" * 50)

    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))
    print("")

    for i in room_market:
        print("BUY " + str(i["id"]).upper() + " to buy " + str(i["name"]) + " for", str(i["cost"]), "gold coins.")
        #Added price to items in store!!!!!!!!!
    for i in room_items: 
        print("TAKE " + str(i["id"]).upper() + " to take " + str(i["name"]) + ".")
    
    for i in inv_items:
        if i["type"] == "Armour":
            print("WEAR "+ str(i["id"].upper()+ " to wear "+str(i["name"]+".")))

    print("SEE MAP to see map")


    if len(current_room["market"]) > 0:
        for i in inv_items:
            if i["type"] != "buff":
                print("SELL " + str(i["id"]).upper() + " to sell " + str(i["name"]) + " for", int(i["cost"] * 0.5) ," gold coins.") 
    for i in inv_items: 
        if i["type"] != "buff":
            print("DROP " + str(i["id"]).upper() + " to drop " + str(i["name"]) + ".")    
    print("What do you want to do?")
    print("_" * 50)

def print_combat_menu(inventory, enemies):
    print("You can: ")
    item = []  
    for i in inventory:
        if str(i["type"]) in type_attack:
            item.append(i["id"])
        
    for enemy_ in enemies:
        print("ATTACK " + str(enemy_["id"]).upper() + " with " + str(', '.join(item)).upper() + ".")
    for i in inventory:
        if i["type"] == "Heal":
            print("USE " + str(i["id"]).upper() + " to heal for " + str(i["hp"]) + ".")
            #creates a list of the users items depending on type and then for each item in list shows whether they can "use" or "attack" with the item
    print("What do you want to do?")
    
def is_valid_exit(exits, chosen_exit):
    return chosen_exit in exits.keys()

def execute_buy(item_id):
    global gold
    for item in current_room["market"]:
            #searches through the items that are in the market part of the rooms dictionary 
        if item_id == item["id"]:
            if gold >= item["cost"]:
                    #if you have more gold than the item costs then proceed with buying 
                inventory.append(item)
                current_room["market"].remove(item)
                gold = gold - item["cost"]
                    #adds the item to ure inventory and removes it from the shop, gold minus the cost is your remaining gold now 
                print("you have bought " + str(item["name"]))
                print("you have " + str(gold) + " gold")  
                break
            else:
                print("You don't have enough gold mate. You only have",str(gold))

                
def execute_sell(item_id):
    global gold 
    for item in inventory:
        if item_id == item["id"]: 
            if item["type"] != "buff": 
                inventory.remove(item)
                gold = gold + int((0.5*int(item["cost"]))) 
                current_room["market"].append(item)
                print("you have sold " + str(item["name"]) + " you have gained, " + str(int(0.5*item["cost"]))) 
                print("you have " + str(gold) + " gold")
                #same process as buy but adds half the items cost to your gold value and adds to shop instead of taking away
                break
    else: 
        print("You cannot sell that")       
                     
def execute_go(direction):
    global current_room
    global prev_room
    prev_room = current_room 
    if is_valid_exit(current_room["exits"], direction) == True: 
        current_room = move(current_room["exits"], direction)
        if len(current_room["check_item"])> 0:
            if item_helping_hand in inventory:
                question = "do you want to use helping hand to get through?"
                x = yes_or_no(question)
                if x == True:
                    print("moving into " + str(current_room["name"]))
                    inventory.remove(item_helping_hand)
            #checks to see if the user has the helping hand item that may be used to pass through areas without
            #a specific item and then asks them whether they want to use helping hand to get through or not
            #important that this comes before the other item check or it wont check for helping hand 
                else:
                    current_room = prev_room
                    print("you moved back as you did not want to sacrifice helping hand")
            elif current_room["check_item"] not in inventory:
                current_room = prev_room
                print("You cannot enter here yet, there must be something you need")
            else:
                print("moving into " + str(current_room["name"]))
    else:
        print("You cannot go there") 

def execute_take(item_id):
    global gold 
    for item in current_room["items"]: 
        if item_id == item["id"]:
            if item in inventory:
                if item["type"] in type_attack:
                    gold = gold + (0.5 * item["cost"])
                    print("you have gained " + str(0.5*item["cost"]) + " gold from " + str(item["name"]))
                    print("you have " + str(gold) + " gold.")
            else: 
                inventory.append(item)
                print("you have taken " + str(item["name"]))
            current_room["items"].remove(item) 
        
            break   
        else: 
            print("You cannot take that.") 
        
    

def execute_drop(item_id):
    for item in inventory:
        if item_id == item["id"]:
            if item["type"] != "buff": 
                inventory.remove(item)
                current_room["items"].append(item)
                print("you have dropped " + str(item["name"])) 
                break
    if item_id != item["id"]: 
        print("You cannot drop that")           

def execute_attack(enemy_, item_id, enemies):
    #global enemies 
    global temp_hp
    enemy_attack = int()
    for i in enemies:
        if enemy_ == i["id"]:
            enemy_attack = int(i["attack"])
    for item in inventory:
        if item_id == item["id"]:
            if str(item["type"]) in type_attack:
                attack = item["attack"]
                for enemyx in enemies:
                    if enemy_ == enemyx["id"]: 
                        if item_buff_potion in inventory: 
                            if random.randint(0, item["crit"]) > 1: 
                                attack = item["attack"]*2 
                                print("You Crit!")
                        elif random.randint(0, item["crit"]) > 2:
                            attack = item["attack"]*2
                            print("You Crit!")
                        else: 
                            attack = item["attack"]
                        if item["type"] in enemyx["weak"]:
                            enemyx["temp_hp"] = enemyx["temp_hp"] - int((2 * attack))
                            print("that was super effective!")
                            print(enemyx["name"] + " has " + str(enemyx["temp_hp"]) + " hp")
                            temp_hp= (temp_hp - enemy_attack)
                            print("You've received a hit your health is now",temp_hp)
                            break
                        elif item["type"] in enemyx["resist"]: 
                            enemyx["temp_hp"] = enemyx["temp_hp"] - int((0.5 * attack))
                            print("that wasn't very effective...")
                            print(enemyx["name"] + " has " + str(enemyx["temp_hp"]) + " hp")
                            temp_hp= (temp_hp - enemy_attack)
                            print("You've received a hit your health is now",temp_hp)
                            break
                        else: 
                            enemyx["temp_hp"] = enemyx["temp_hp"] -  int(attack)
                            print(enemyx["name"] + " has " + str(enemyx["temp_hp"]) + " hp")
                            temp_hp= (temp_hp - enemy_attack)
                            print("You've received a hit your health is now",temp_hp)
                            break
                #these if statements above check the damage type and compare to whether the enemy is weak to it and
            else:
                print("you cannot attack with that!") 
                   #does damage accordingly, 2x 0.5x or normal damage 

def execute_use(item_id):
    global hp 
    global temp_hp
    for item in inventory:
        if item_id == item["id"]:
            if item["type"] == "Heal":
                temp_hp = temp_hp + item["hp"]
                if temp_hp > hp:
                    temp_hp = hp
                print("hp: " + str(temp_hp))
                inventory.remove(item)
                break
            else:
                print("You cannot use that item") 

def execute_wear(item_id):
    global hp
    global temp_hp
    for item in inventory: 
        if item_id == item["id"]:
            if item["type"] == "Armour": 
                hp = hp+30 
                temp_hp = temp_hp + 30
                inventory.remove(item)
                print("Your Max Hp is now: " + str(hp) +"\n" + "Your current Hp is: " + str(temp_hp)) 
                break
            else:
                print("You cannot wear that.")  

def execute_see(maporcompass):
    if maporcompass == "map":
        print("""\
        ╔═════════════════════════════════════════╗
        ║                                         ║
        ║ HARAMBE                                 ║
        ║     ║                                   ║
        ║     ║                                   ║
        ║    ZOO════════════════FESTIVAL GROUNDS  ║
        ║     ║                               ║   ║
        ║     ║                               ║   ║
        ║   CASTLE                            ║   ║
        ║     ║                               ║   ║
        ║     ║                               ║   ║
        ║   BRDGE═══FOREST═════CLEARING═════CAMP  ║
        ║     ║        ║                      ║   ║
        ║     ║        ║                      ║   ║
        ║    SHOP════VILAGE══════════════════BAR  ║
        ║                                         ║
        ╚═════════════════════════════════════════╝
        """)
    else:
        print("You cannot see that.")
def execute_command(command):

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")
    elif command[0] == "buy":
        if len(command) > 1:
            execute_buy(command[1])
        else:
            print("Buy what?") 
    elif command[0] == "sell":
        if len(command) > 1:
            execute_sell(command[1])
        else:
            print("Sell what?") 
    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")
    elif command[0] == "wear":
        if len(command) > 1:
            execute_wear(command[1])
        else:
            print("Wear what?")
    elif command[0] == "see":
        if len(command) >1:
            execute_see(command[1])
        else:
            print("See what?")
    else:
        print("This makes no sense.")
def execute_combat_command(command):
    if 0 == len(command):
        return
    if command[0] == "attack":
        if len(command)> 2:
            execute_attack(command[1], command[2], current_room["enemy_present"])
        else:
            print("Attack what?")
    elif command[0] == "use":
        if len(command)> 1:
            execute_use(command[1])
        else:
            print("Use what?")
    else:
        print("This makes no sense.") 

def menu(exits, room_items, inv_items, room_market):

    # Display menu
    print_menu(exits, room_items, inv_items, room_market)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    
    # Next room to go to 
    return rooms[exits[direction]]
def combat_menu(inventory, enemies):
    print_combat_menu(inventory, enemies)

    user_input = input("> ")

    normalised_user_input = normalise_input(user_input)

    return normalised_user_input 
    
def combat():
	global current_room 
	global gold
	if current_room["combat"] == True:
		global enemies
		# enemies = []
		if len(current_room["enemy_present"]) < 1:
			enemies = []
			#enemies = current_room["enemy_present"]
			for x in range(current_room["min enemy"], current_room["max enemy"]):
				temp_enemy = random.choice(current_room["enemy"])
				if temp_enemy not in current_room["enemy_present"]:
						current_room["enemy_present"].append(temp_enemy)
		# enemies = current_room["enemy_present"]

		if print_enemies(current_room["enemy_present"]) == True:
			while True:
				print_arena(current_room["enemy_present"])
					
				command = combat_menu(inventory, current_room["enemy_present"])
				#print(command) 
				execute_combat_command(command)

				if temp_hp <1:
					print("You have lost!")
					raise SystemExit

				for enemy_ in current_room["enemy_present"]:
					if enemy_["temp_hp"] < 1:
						print("You killed 1 " + enemy_["name"])
						enemy_["temp_hp"] = enemy_["hp"]
						for item in enemy_["drop"]: 
							if random.randint(0, item["chance"]) > 2: 
								if item["type"] in type_attack: 
									if item in inventory:  
										gold = (item["cost"]*0.5) + gold
										print("you gained " + str((item["cost"]*0.5)) + " Gold")  
								else: 
									inventory.append(item)
								print("The enemy dropped a " + item["name"])
						current_room["enemy_present"].remove(enemy_)
				if len(current_room["enemy_present"]) == 0:
					current_room["combat"] = False
					break
	else:
		return None

def activity():
    global current_room
    if len(current_room["activity"]) > 0:
        bar_drink()

def bar_drink():
    global temp_hp
    global gold
    global class_name
    global inventory
    challenge = ""
    correct_input = 0
    print("Sitting along the bar three strangers reside. They notice your arrival and hail you over. The men are quite clearly drunk and challenge you to drink a pint faster then them game hoping your pockets might fund their next pint \n")
    print("You have: " + str(gold) + " Gold.") 
    while correct_input != 1:
        challenge = input("Would you like to accept their challenge? (Costs 10 coins), (Type y/n) \n").lower()
        if challenge == "y":
            if gold < 10:
                print("You need more gold to challenge")
                correct_input = 1
            else: 
                correct_input = 1
                print("You sit down at the end of the bar, the men slide you over a drink,")
                ####CHANGE THIS FOR OTHERS####
                gold-=10
                print("You hand over 10 gold and begin to drink.")
                random_number = random.randint(1,10)
                if class_name == "warrior":
                    random_number+1
                if random_number >8:
                    print("The race begins, you put the pint upto your mouth and drink like you've never drunk before, beating all the other men at the bar.")
                    print("You take back your gold plus 10 from the other competitors.\n")
                    print("A hand grabs you on the back, a stranger sits down and explains his amazement of your drinking skills, you talk some more about your quest and he agrees to give you his trust Rifle.")
                    gold+=20
                    if item_hunting_rifle not in inventory: 
                        inventory.append(item_hunting_rifle)
                        print("You have: " + str(gold) + " Gold.")
                        current_room["activity"] = []
                else:
                    random_fail = random.randint(1,5)
                    if random_fail ==1 or random_fail ==2:
                        print("The race begins, you pickup the pint of beer and bring it to your mouth, but not before,\n your hand slips and the glass shatters cutting your leg, you feel damaged. You lose 5 hp\n")
                        temp_hp = temp_hp - 5
                        bar_drink()
                    elif random_fail ==3 or random_fail ==4:
                        temp_hp = temp_hp - 5
                        print("The race begins, you pickup the pint of beer from the bar and begin to drink. half way through you start to choke,\n Your life flashes briefly before your eyes. You lose 5 hp")
                        bar_drink()
                    elif random_fail ==5:
                        temp_hp = temp_hp - 10
                        gold-=10
                        print("The race begins, you pickup the pint of beer and start to drink, you feel a little wobly and fall from your stool.\n You wake up after the bartender splashes a pale of water on your face.\n You lose 10 hp and 10 gold.")
                        bar_drink()
        elif challenge == "n":
            correct_input = 1
            print("You politely decline the offer and move away from the drunk men. \n")
        else:
            print("You need to enter y/n \n")


                 
def end_game():
    for i in range(1,51):
            print("\n")
            time.sleep(0.1)
    ascii()
    time.sleep(2)
    print("\nDeeon Roy -- Executive Programmer\n")
    time.sleep(1.5)
    print("Ben Rant -- Programmer\n")
    time.sleep(1.5)
    print("Oliver Storey-Soung -- Programmer\n")
    time.sleep(1.5)
    print("Artem Protasavytsky -- Programmer\n")
    time.sleep(1.5)
    print("Luke Jones -- Programmer\n")
    time.sleep(1.5)
    print("Austen Wells -- Beta Tester/Programmer\n")
    time.sleep(1.5)
    print("Nojus Lenciauskas -- Visual Artist/Programmer\n")
    time.sleep(1.5)
    print("Ben van Rooyen -- 404 Page Not Found\n")
    time.sleep(1.5)
    print("Rest In Peace Harambe 1999-2016\n")
    raise SystemExit


    
def ascii():
    print(" _  __          _ _ _                             __                ")
    print("| |/ /         (_) | |                           / _|               ")
    print("| ' / ___  _ __ _| | | __ _  __      ____ _ _ __| |_ __ _ _ __ ___  ")
    print("|  < / _ \| '__| | | |/ _` | \ \ /\ / / _` | '__|  _/ _` | '__/ _ \ ")
    print("| . \ (_) | |  | | | | (_| |  \ V  V / (_| | |  | || (_| | | |  __/ ")
    print("|_|\_\___/|_|  |_|_|_|\__,_|   \_/\_/ \__,_|_|  |_| \__,_|_|  \___| ")       
        
# This is the entry point of our program
def main():
    global prev_room

    class_decide("Use ")

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print("\n" * 4)
        print(current_room["ascii"])

        print_room(current_room)
        print_inventory_items(inventory)

        combat()
        if len(current_room["activity"]) > 1:
            activity()
        if current_room["name"] == "Harambe's Pen":
            end_game() 
        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory, current_room["market"])

        # Execute the player's command
        execute_command(command)

if __name__ == "__main__":
    ascii()
    input("""

        Welcome to Korilla Warfare! You play the hero Amanda O'Donohuge a heroin from the land of cincinnati in the year of 500AD.
            Times are hard and the land is ruled by a ruthless being who resids in the Zoo!

                                                Hit enter to start!""")
    main()
    

