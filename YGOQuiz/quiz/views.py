import os
import random
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PIL import Image
from django.conf import settings

def home(request):
    return HttpResponse("Hello, Django!")



def fetch_image(request):
    # Path to your images folder
    images_path = 'C:/Users/PC/Documents/Projects/yugioh-quiz-backend/images'  # Change this to your images directory
    image_name = request.GET.get('name')

    image_path = os.path.join(images_path, f"{image_name}.jpg")

    image = Image.open(image_path)
    resized_image = image.resize((624, 624), Image.Resampling.LANCZOS)
    response = HttpResponse(content_type="image/jpeg")
    resized_image.save(response, "JPEG")
    return response

def random_image_info(request):
    # Path to your images folder
    images_path = 'C:/Users/PC/Documents/Projects/yugioh-quiz-backend/images'

    # List all .json files in the directory
    images = [file for file in os.listdir(images_path) if file.lower().endswith('.json')]
    if not images:
        return HttpResponse("No images found", status=404)

    # Choose a random image
    random_image_filename = random.choice(images)
    # Construct the full path to the JSON file
    json_path = os.path.join(images_path, random_image_filename)
    data = {"name": random_image_filename, "race": None, "correct_choice": None, "choices": ["Spell", "Trap", "Monster"], "question": None}


    # Check if the JSON file exists and load data
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            json_data = json.load(file)

            card_type = json_data['type']
            linkval = json_data['linkval']
            race_value = json_data.get('race')

            if card_type == 'Spell Card':
                random_number = random.randint(0, 1)

                if random_number == 0: #name mode
                    three_random_names = []
                    while len(three_random_names) < 3:
                        random_name = random.choice(images)
                        if random_name != random_image_filename:
                            with open(os.path.join(images_path, random_name), 'r') as random_file:
                                random_json_data = json.load(random_file)
                                three_random_names.append(random_json_data['name'])
                    correct_choice = json_data['name']
                    choices = three_random_names
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the name of this card?'
                
                if random_number == 1: #type mode
                    all_spell_races = ['Normal Spell', 'Normal Trap', 'Continuous Spell', 'Continuous Trap', 'Counter Trap', 'Equip', 'Field', 'Quick-Play', 'Ritual']
                    random.shuffle(all_spell_races)
                    correct_choice = race_value
                    if correct_choice == 'Normal':
                        correct_choice = 'Normal Spell'
                    if correct_choice == 'Continuous':
                        correct_choice = 'Continuous Spell'
                    choices = []
                    for choice in all_spell_races:
                        if choice != correct_choice:
                            choices.append(choice)
                        if choices.__len__() == 3:
                            break
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the type of this card?'
            elif card_type == 'Trap Card':
                random_number = random.randint(0, 1)

                if random_number == 0: #name mode
                    three_random_names = []
                    while len(three_random_names) < 3:
                        random_name = random.choice(images)
                        if random_name != random_image_filename:
                            with open(os.path.join(images_path, random_name), 'r') as random_file:
                                random_json_data = json.load(random_file)
                                three_random_names.append(random_json_data['name'])
                    correct_choice = json_data['name']
                    choices = three_random_names
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the name of this card?'
                
                if random_number == 1: #type mode
                    all_trap_races = ['Normal Spell', 'Normal Trap', 'Continuous Spell', 'Continuous Trap', 'Counter Trap', 'Equip', 'Field', 'Quick-Play', 'Ritual']
                    random.shuffle(all_trap_races)
                    correct_choice = race_value
                    if correct_choice == 'Normal':
                        correct_choice = 'Normal Trap'
                    if correct_choice == 'Continuous':
                        correct_choice = 'Continuous Trap'
                    choices = []
                    for choice in all_trap_races:
                        if choice != correct_choice:
                            choices.append(choice)
                        if choices.__len__() == 3:
                            break
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the type of this card?'


                
            else:
                if card_type == 'Link Monster':
                    random_number = random.randint(0, 4)
                else:
                    random_number = random.randint(0, 5)
                if random_number == 0: #type mode

                    all_monster_types = ['Zombie', 'Warrior', 'Spellcaster', 'Fiend', 'Fairy', 'Beast-Warrior', 'Beast',
                                        'Winged Beast', 'Aqua', 'Pyro', 'Thunder', 'Dragon', 'Machine', 'Rock', 'Insect',
                                        'Cyberse', 'Plant', 'Dinosaur', 'Reptile', 'Fish', 'Sea Serpent', 'Psychic',
                                        'Wyrm', 'Divine-Beast', 'Illusion']
                    random.shuffle(all_monster_types)
                    correct_choice = race_value
                    choices = []
                    for choice in all_monster_types:
                        if choice != correct_choice:
                            choices.append(choice)
                        if choices.__len__() == 3:
                            break
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the type of this monster?'
                if random_number == 1: #attribute mode
                    all_monster_attributes = ['DARK', 'EARTH', 'FIRE', 'LIGHT', 'WATER', 'WIND', 'DIVINE']
                    random.shuffle(all_monster_attributes)
                    correct_choice = json_data['attribute']
                    choices = []
                    for choice in all_monster_attributes:
                        if choice != correct_choice:
                            choices.append(choice)
                        if choices.__len__() == 3:
                            break
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the attribute of this monster?'
                if random_number == 2: #level mode
                    if card_type == 'Link Monster':
                        all_monster_levels = ['1', '2', '3', '4', '5', '6']
                        correct_choice = str(json_data['linkval'])
                    else:
                        all_monster_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                        correct_choice = str(json_data['level'])
                    random.shuffle(all_monster_levels)
                    
                    choices = []
                    for choice in all_monster_levels:
                        if choice != correct_choice:
                            choices.append(choice)
                        if choices.__len__() == 3:
                            break
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the level of this monster?'
                    if card_type == 'Link Monster':
                        question = 'What is the link rating of this monster?'
                    if card_type == 'XYZ Monster':
                        question = 'What is the rank of this monster?'
                if random_number == 3: #atk mode
                    #random number from 0 to 5000 in multiples of 50
                    all_monster_atk = [str(i) for i in range(0, 5000, 50)]
                    # Defining weights
                    weights = [5 if int(atk) <= 3000 else 1 for atk in all_monster_atk]

                    # Picking 3 unique elements
                    selected_atks = set()
                    while len(selected_atks) < 3:
                        c = random.choices(all_monster_atk, weights=weights, k=1)[0]
                        if c != str(json_data['atk']):
                            selected_atks.add(str(c))

                    selected_atks = list(selected_atks)
                    random.shuffle(all_monster_atk)
                    correct_choice = str(json_data['atk'])
                    choices = selected_atks
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the ATK of this monster?'
                
                if random_number == 4: #name mode:
                    three_random_names = []
                    while len(three_random_names) < 3:
                        random_name = random.choice(images)
                        if random_name != random_image_filename:
                            with open(os.path.join(images_path, random_name), 'r') as random_file:
                                random_json_data = json.load(random_file)
                                three_random_names.append(random_json_data['name'])
                    correct_choice = json_data['name']
                    choices = three_random_names
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the name of this card?'
                if random_number == 5: #def mode
                    #random number from 0 to 5000 in multiples of 50
                    all_monster_def = [str(i) for i in range(0, 5000, 50)]
                    # Defining weights
                    weights = [5 if int(defense) <= 3000 else 1 for defense in all_monster_def]

                    # Picking 3 unique elements
                    selected_defs = set()
                    while len(selected_defs) < 3:
                        c = random.choices(all_monster_def, weights=weights, k=1)[0]
                        if c != str(json_data['defense']):
                            selected_defs.add(str(c))

                    selected_defs = list(selected_defs)
                    random.shuffle(all_monster_def)
                    correct_choice = str(json_data['defense'])
                    choices = selected_defs
                    choices.append(correct_choice)
                    random.shuffle(choices)
                    question = 'What is the DEF of this monster?'

            
            data['race'] = race_value
            data['correct_choice'] = correct_choice
            data['choices'] = choices
            data['question'] = question
            random.shuffle(data['choices'])

    return JsonResponse(data)
