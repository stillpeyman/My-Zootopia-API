import data_fetcher as df


def generate_animal_info(animals, name):
    """
    Generate HTML list items for animals matching the selected skin type.
    """
    # Define empty string
    output = ''

    if not animals:
        output = f'''
        <div class="message-card">
            <p>🐢 <strong>Dude, {name} is a no-show! Try another animal 🐒</strong></p>\n
        </div>
        '''.strip()

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
    animal_name = df.get_animal_name()
    animal_data = df.fetch_data(animal_name)
    animal_info = generate_animal_info(animal_data, animal_name)
    template = read_template('animals_template.html')
    animals_html = merge_template_with_data(template, animal_info)
    write_to_file('animals.html', animals_html)
    print("\nWebsite was successfully generated to the file animals.html 🐾\n")
    

if __name__ == "__main__":
    main()
