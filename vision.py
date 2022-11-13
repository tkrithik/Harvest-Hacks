#-----------Import Commands-----------
import io
import os.path
import requests
import json
import wikipedia
from pprint import pprint
# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
class Vision:

    def __init__(self):
        print("Initializing Vision Class")

    def process_image(self, file_name):

        client = vision.ImageAnnotatorClient()

        # The name of the image file to annotate
        file_name = os.path.abspath(file_name)

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        fruit_name = self.filter_fruit_label(labels)
        return self.get_fruit_detail(fruit_name)

    def filter_fruit_label(self, labels):
        for label in labels:
            fruit = str(label.description).lower()
            fruit_name = self.is_valid_fruit(fruit)
            try:
                print(f"Fruit Name: {fruit_name['name']}")
                return fruit_name['name']
            except:
                print(f"Not a valid fruit: {fruit}")

        return None

    def is_valid_fruit(self, fruit):
        url = f'https://www.fruityvice.com/api/fruit/{fruit}'
        response = requests.get(url)
        data = response.json()
        return data

    def get_fruit_detail(self, fruit_name):
        wiki_page = wikipedia.page(f"{fruit_name} (fruit)")
        pprint(wiki_page.title)
        pprint(wiki_page.url)
        pprint(wiki_page.summary)

        return wiki_page.title, wiki_page.url, wiki_page.summary, wiki_page.images[0]



