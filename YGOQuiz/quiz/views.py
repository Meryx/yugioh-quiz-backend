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
    resized_image = image.resize((421, 614), Image.Resampling.LANCZOS)
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
    data = {"name": random_image_filename, "race": None, "correct_choice": None, "choices": ["spell", "trap", "monster"]}

    # Check if the JSON file exists and load data
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            json_data = json.load(file)
            race_value = json_data.get('race')
            data['race'] = race_value
            data['correct_choice'] = race_value
            data['choices'].append(race_value)
            random.shuffle(data['choices'])

    return JsonResponse(data)
