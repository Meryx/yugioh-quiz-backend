import os
import random
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PIL import Image
from django.conf import settings

def home(request):
    return HttpResponse("Hello, Django!")

IMG_DIR = 'C:/Users/PC/Documents/Projects/yugioh-quiz-backend/images'
IMG_SIZE = (624, 624)
IMG_RESAMPLE_MODE = Image.Resampling.LANCZOS
IMG_EXT = 'jpg'
IMG_CONTENT_TYPE = "image/jpeg"
IMG_TYPE = "JPEG"

MONSTER_TYPES = [
    'Zombie', 'Warrior', 'Spellcaster', 'Fiend', 'Fairy', 'Beast-Warrior', 'Beast',
    'Winged Beast', 'Aqua', 'Pyro', 'Thunder', 'Dragon', 'Machine', 'Rock', 'Insect',
    'Cyberse', 'Plant', 'Dinosaur', 'Reptile', 'Fish', 'Sea Serpent', 'Psychic',
    'Wyrm', 'Divine-Beast', 'Illusion'
]

MONSTER_ATTRIBUTES = ['DARK', 'EARTH', 'FIRE', 'LIGHT', 'WATER', 'WIND', 'DIVINE']

ALL_MONSTER_DEF = [str(i) for i in range(0, 5000, 50)]
ALL_MONSTER_ATK = [str(i) for i in range(0, 5000, 50)]
WEIGHTS = [5 if int(defense) <= 3000 else 1 for defense in ALL_MONSTER_DEF]

def resize_image(image):
    return image.resize(IMG_SIZE, IMG_RESAMPLE_MODE)

def fetch_image(request):
    image_name = request.GET.get('name')
    image_path = os.path.join(IMG_DIR, f"{image_name}.{IMG_EXT}")
    image = Image.open(image_path)

    resized_image = resize_image(image)

    response = HttpResponse(content_type=IMG_CONTENT_TYPE)
    resized_image.save(response, IMG_TYPE)
    return response

def get_three_random_names(images_json, random_image_filename):
    three_random_names = []
    while len(three_random_names) < 3:
        random_name = random.choice(images_json)
        if random_name != random_image_filename:
            with open(os.path.join(IMG_DIR, random_name), 'r') as random_file:
                random_json_data = json.load(random_file)
                three_random_names.append(random_json_data['name'])
    return three_random_names

def generate_name_question(json_data, images_json, random_image_filename):
    three_random_names = get_three_random_names(images_json, random_image_filename)
    correct_choice = json_data['name']
    choices = three_random_names
    choices.append(correct_choice)
    random.shuffle(choices)
    question = 'What is the name of this card?'
    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_choice
    }

def generate_type_question(json_data, images_json, random_image_filename):
    all_types = ['Normal Spell', 'Normal Trap', 'Continuous Spell', 'Continuous Trap', 
                 'Counter', 'Equip', 'Field', 'Quick-Play', 'Ritual']
    random.shuffle(all_types)
    correct_choice = json_data['race']
    frame_name = json_data['frame_type']
    if frame_name == 'spell':
        if correct_choice == 'Normal':
            correct_choice = 'Normal Spell'
        if correct_choice == 'Continuous':
            correct_choice = 'Continuous Spell'
    if frame_name == 'trap':
        if correct_choice == 'Normal':
            correct_choice = 'Normal Trap'
        if correct_choice == 'Continuous':
            correct_choice = 'Continuous Trap'
    choices = []
    for choice in all_types:
        if choice != correct_choice:
            choices.append(choice)
        if choices.__len__() == 3:
            break
    choices.append(correct_choice)
    random.shuffle(choices)
    question = 'What is the type of this card?'
    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_choice
    }

def generate_spell_or_trap_question(json_data, images_json, random_image_filename):
    generators = [generate_type_question, generate_name_question]
    generator = random.choice(generators)
    return generator(json_data, images_json, random_image_filename)

def generate_monster_name_question(json_data, images_json, random_image_filename):
    return generate_name_question(json_data, images_json, random_image_filename)

def generate_monster_atk_question(json_data, *args, **kwargs):
    correct_attack = str(json_data['atk'])
    possible_choices = set(ALL_MONSTER_ATK) - {correct_attack}
    
    selected_atks = set()
    while len(selected_atks) < 3:
        selected_atk = random.choices(list(possible_choices), weights=[WEIGHTS[ALL_MONSTER_ATK.index(atk)] for atk in possible_choices], k=1)[0]
        selected_atks.add(selected_atk)
        possible_choices.remove(selected_atk)

    choices = list(selected_atks) + [correct_attack]
    random.shuffle(choices)
    question = 'What is the ATK of this monster?'

    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_attack
    }

def generate_monster_def_question(json_data, *args, **kwargs):
    correct_defense = str(json_data['defense'])
    possible_choices = set(ALL_MONSTER_DEF) - {correct_defense}
    
    selected_defs = set()
    while len(selected_defs) < 3:
        selected_def = random.choices(list(possible_choices), weights=[WEIGHTS[ALL_MONSTER_DEF.index(defense)] for defense in possible_choices], k=1)[0]
        selected_defs.add(selected_def)
        possible_choices.remove(selected_def)

    choices = list(selected_defs) + [correct_defense]
    random.shuffle(choices)
    question = 'What is the DEF of this monster?'

    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_defense
    }

def generate_monster_level_question(json_data, images_json, random_image_filename):
    if json_data['type'] == 'Link Monster':
        all_monster_levels = ['1', '2', '3', '4', '5', '6']
        correct_choice = str(json_data['linkval'])
        question = 'What is the link rating of this monster?'
    elif json_data['type'] == 'XYZ Monster':
        all_monster_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        correct_choice = str(json_data['level'])
        question = 'What is the rank of this monster?'
    else:
        all_monster_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        correct_choice = str(json_data['level'])
        question = 'What is the level of this monster?'

    shuffled_levels = random.sample(all_monster_levels, len(all_monster_levels))
    incorrect_choices = [lvl for lvl in shuffled_levels if lvl != correct_choice][:3]
    choices = incorrect_choices + [correct_choice]
    random.shuffle(choices)

    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_choice
    }

def generate_monster_attribute_question(json_data, *args, **kwargs):

    shuffled_attributes = random.sample(MONSTER_ATTRIBUTES, len(MONSTER_ATTRIBUTES))
    correct_attribute = json_data['attribute']
    incorrect_choices = [attr for attr in shuffled_attributes if attr != correct_attribute][:3]
    choices = incorrect_choices + [correct_attribute]
    random.shuffle(choices)
    question = 'What is the attribute of this monster?'

    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_attribute
    }

def generate_monster_type_question(json_data, *args, **kwargs):

    shuffled_types = random.sample(MONSTER_TYPES, len(MONSTER_TYPES))
    correct_type = json_data['race']
    incorrect_choices = [t for t in shuffled_types if t != correct_type][:3]
    choices = incorrect_choices + [correct_type]
    random.shuffle(choices)
    question = 'What is the type of this monster?'

    return {
        "question": question,
        "choices": choices,
        "correct_choice": correct_type
    }

def generate_monster_question(json_data, images_json, random_image_filename):
    generators = [generate_monster_type_question, generate_monster_attribute_question, generate_monster_level_question, 
                  generate_monster_atk_question, generate_monster_name_question]
    
    if json_data['type'] != 'Link Monster':
        generators.append(generate_monster_def_question)
    generator = random.choice(generators)
    return generator(json_data, images_json, random_image_filename)



def generate_quiz_data(json_data, images_json, random_image_filename):
    card_type = json_data['type']

    if card_type.lower().endswith('monster'):
        card_type = 'Monster'
    
    if card_type.lower().endswith('token'):
        card_type = 'Monster'

    question_generators = {
        'Spell Card': generate_spell_or_trap_question,
        'Trap Card': generate_spell_or_trap_question,
        'Monster': generate_monster_question
    }

    generator = question_generators.get(card_type, lambda *args: {})
    return generator(json_data, images_json, random_image_filename)

def random_image_info(request):

    images_json = [file for file in os.listdir(IMG_DIR) if file.lower().endswith('.json')]
    random_image_json = random.choice(images_json)
    random_image_path = os.path.join(IMG_DIR, random_image_json)

    response_data = {
        "name": random_image_json,
        "race": None,
        "correct_choice": None,
        "choices": None,
        "question": None
    }

    with open(random_image_path, 'r') as file:
        json_data = json.load(file)
        quiz_data = generate_quiz_data(json_data, images_json, random_image_json)

        response_data['race'] = json_data['race']
        response_data.update(quiz_data)
        return JsonResponse(response_data)
