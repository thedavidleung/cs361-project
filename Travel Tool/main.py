import inquirer
import requests
from geopy import distance, geocoders
import pyfiglet
from simple_chalk import chalk

# API KEY for Openweathermap App
open_weather_api_key = "ebfefd1a1a9ec827d5d67b85849a9b5d"

# URL for Openweathermap App
api_url = "https://api.openweathermap.org/data/2.5/weather"

# Function to get weather information
def get_weather(city, country):
    url = f"{api_url}?q={city},{country}&appid={open_weather_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        city_ascii = pyfiglet.figlet_format(city)
        country_ascii = pyfiglet.figlet_format(country)
        if unit_system_choice['unit_system'] == 'Imperial':
            output = f"{city_ascii.strip()}, {country_ascii.strip()}\n\n" + f"Currently: {description}\n" + f"Temperature: {temperature}°F\n" + f"Feels like: {feels_like}°F\n"
        else:
            output = f"{city_ascii.strip()}, {country_ascii.strip()}\n\n" + f"Currently: {description}\n" + f"Temperature: {temperature}°C\n" + f"Feels like: {feels_like}°C\n"
        return chalk.green(output)
    else:
        return chalk.red("Error: Unable to retrieve weather information")

print(chalk.cyanBright("Welcome to the travel tool! \nThis tool allows you to calculate the distance between cities and \nthe current weather conditions to make sure you're prepared for anything! \n(requires the command line interface and makes calls to weathermap API)\n" ))
print(chalk.cyanBright("If you ever want to exit the program, press ctrl + c and the program will end abruptly\n"))

while True:
    print('(Use the arrow keys to change your selection.\nPress enter when you have decided)')
    unit_system_choice = inquirer.prompt([
        inquirer.List('unit_system',
                      message=chalk.cyanBright('Choose preferred unit system:'),
                      choices=['Metric', 'Imperial'],
                      default='Metric')
    ])

    if unit_system_choice['unit_system'] == 'Imperial':
        distance_unit = 'mi'
    else:
        distance_unit = 'km'

    while True:
        print(chalk.cyanBright('Press 1 to continue, 0 to restart unit system selection, or any other key to exit\n'))
        choice = input("Enter your choice: ")

        if choice == '0':
            break  # Go back to unit system selection

        if choice != '1':
            print(chalk.red("Exiting the application. Goodbye!"))
            exit()

        # Ask user for the current city
        current_city = inquirer.prompt([
            inquirer.Text('name', message=chalk.cyanBright('Which city are you currently at?(Enter your current city): ')),
            inquirer.Text('country', message=chalk.cyanBright('Which country is that city in?(Enter your current country)'))
        ])

        # Ask user for the destination city
        destination_city = inquirer.prompt([
            inquirer.Text('name', message=chalk.cyanBright('Which city are you going to? (Enter your destination city)')),
            inquirer.Text('country', message=chalk.cyanBright('Which country is that city in? (Enter your destination country)'))
        ])

        # Calculate the distance between the two locations
        current_location = f"{current_city['name']}, {current_city['country']}"
        current_coordinates = geocoders.Nominatim(user_agent="distance_calculator").geocode(current_location).point

        destination_location = f"{destination_city['name']}, {destination_city['country']}"
        destination_coordinates = geocoders.Nominatim(user_agent="distance_calculator").geocode(destination_location).point

        walk_distance = distance.distance(current_coordinates, destination_coordinates).kilometers
        bus_distance = walk_distance
        plane_distance = walk_distance

        if unit_system_choice['unit_system'] == 'Imperial':
            walk_distance *= 0.621371
            bus_distance *= 0.621371
            plane_distance *= 0.621371

        walk_time = walk_distance / 5
        bus_time = bus_distance / 50
        plane_time = plane_distance / 500

        # Get weather information for the current city
        print("\n Weather information for " + current_location )
        print(get_weather(current_city['name'], current_city['country']))

        print(chalk.blue(f"Distance between {current_location} and {destination_location} by :"))
        print(chalk.yellow(f" By walking: {walk_distance:.2f} {distance_unit}, time {walk_time:.2f} hours"))
        print(chalk.yellow(f" By bus: {bus_distance:.2f} {distance_unit}, time {bus_time:.2f} hours"))
        print(chalk.yellow(f" By plane: {plane_distance:.2f} {distance_unit}, time {plane_time:.2f} hours"))

        # Get weather information for the destination city
        print("\n Weather information for " + destination_location)
        
        print(get_weather(destination_city['name'], destination_city['country']))

        restart_choice = input(chalk.cyanBright('Do you want to travel to try another destination? (yes/no): '))

        if restart_choice.lower() != 'yes':
            exit()
