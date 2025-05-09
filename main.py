# %%
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
        animal_name = input('Enter the name of the animal: ').strip()
        if animal_name:
            return animal_name
        else:
            print('Invalid input. Please enter a valid animal name.')


def get_json(animal_name):
    """
    Fetches animal data based on animal name, and saves it to 'response.json'.
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


def generate_animal_info(animals, name):
    """
    Generate HTML list items for animals matching the selected skin type.
    """
    # Define empty string
    output = ''

    if not animals:
        output = f'''
        <div class="message-card">
            <p>Dude, "{name}" is a no-show! Try another animal.</p>\n'
        </div>
        '''
        
    for animal in animals:
        output += serialize_animal(animal)

    return output


def serialize_animal(animal):
    """
    Convert a single animal's data into an HTML list item string.
    """
    output = ''
    output += ' <li class="cards__item">\n'
    output += '     <div class="card__title">{}</div>\n'.format(animal.get('name', 'Unknown'))
    output += '     <div class="card__text">\n'
    output += '         <ul>\n'
    output += '             <li><strong>Scientific Name:</strong> {}</li>\n'.format(animal.get('taxonomy', {}).get('scientific_name', 'Unknown'))
    output += '             <li><strong>Type:</strong> {}</li>\n'.format(animal.get('characteristics', {}).get('type', 'Unknown'))
    output += '             <li><strong>Skin Type:</strong> {}</li>\n'.format(animal.get('characteristics', {}).get('skin_type', 'Unknown'))
    output += '             <li><strong>Diet:</strong> {}</li>\n'.format(animal.get('characteristics', {}).get('diet', 'Unknown'))
    output += '             <li><strong>Location:</strong> {}</li>\n'.format(animal.get('locations', [None])[0] or 'Unknown')
    output += '             <li><strong>Slogan:</strong> {}</li>\n'.format(animal.get('characteristics', {}).get('slogan', 'Unknown'))
    output += '         </ul>\n'
    output += '     </div>\n'
    output += ' </li>\n'

    return output


def read_template(file_path):
    """
    Read and return HTML template content from a file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def merge_template_with_data(template_str, animal_info_str):
    """
    Insert animal info into the HTML template placeholder.
    """
    return template_str.replace("__REPLACE_ANIMALS_INFO__", animal_info_str)


def write_to_file(file_path, content):
    """
    Write the final HTM content as a file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    """
    Main program flow: 
    load data, generate,
    and save HTML.
    """
    animal_name = get_animal_name()
    animal_data = get_json(animal_name)
    animal_info = generate_animal_info(animal_data, animal_name)
    template = read_template('animals_template.html')
    animals_html = merge_template_with_data(template, animal_info)
    write_to_file('animals.html', animals_html)
    

if __name__ == "__main__":
    main()
