# imports
import sending
import receiving
 
# example park 
park_address = "Central Park"


# To request data / send data
sending.get_park(park_address)

# "sending {'address': 'Erindale'}" should appear in the terminal


#To receive data 
trails_data = receiving.get_trails_data(park_address)
if trails_data:
    print(f'Trails within 50 miles of {park_address}:')
    for trail_name, trail_description in trails_data.items():
        print(f"Trail: {trail_name}\n")
        print(f"Description: {trail_description}\n")
else:
    print("No trail data found")
# should receive the coordinates of the location, the trail name and trail description
