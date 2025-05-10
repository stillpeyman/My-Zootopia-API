import json
from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.getenv('API_KEY')
HOST = "api.api-ninjas.com"


def get_animal_name():
    """
    Prompt user for an animal name and return it.
    """
    while True:
        animal_name = input('\nEnter the name of the animal: ').strip()
        if animal_name:
            return animal_name
        else:
            print('Invalid input. Please enter a valid animal name.')


def fetch_data(animal_name):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary.
    """
    api_url = f"https://{HOST}/v1/animals?name={animal_name}"
    headers = {
        'X-Api-Key': API_KEY
    }

    # simple connection test
    try:
        response = requests.get(api_url, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            animal_data = response.json()
            with open("response.json", "w") as fileobj:
                json.dump(animal_data, fileobj)
            return animal_data
        
        else:
            print(f"Error occurred: {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: ", e)

    except requests.exceptions.Timeout as e:
        print("Timeout: ", e)

    except requests.exceptions.RequestException as e:
        print("RequestException: ", e)

