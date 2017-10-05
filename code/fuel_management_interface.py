#!/usr/bin/python3 

import fuel_management as fm



def generate_report():

	aircraft = select_plane_menu()
	aircraft.convert_imperial_to_metric()
	
	airports = get_airport_list()
	
	
	while fm.utils.validate_airports(airports) is  False:
		codes = [a.code for a in airports]
		
		print("\n\nSelected Airports :"+str(codes) +"\n"
		"Invalid airport List Please choose again \n"
		"Two airports in a row must not be the same \n"
		"No airport can occur more than twice \n"
		"The final Airport is automatically assigned "
		"as the starting airport by the System \n")
		airports = get_airport_list()

		
	flight_info, fuel_cost_info = fm.utils.calc_flightpath_cost(airports,aircraft)
	
	display_fuel_Invoice(flight_info,fuel_cost_info)
	
	
	
	
def get_airport_list():
	
	country_list = fm.utils.get_country_list('data/airport.csv')
	airport_list = []
	
	
	while len(airport_list) < 4:
		#used to display number of times a user has selected 
		counter = len(airport_list) + 1
		
		country = select_country_menu(country_list,counter)

		airport_code = select_airport_menu(country,counter)
	
		airport_list.append(fm.utils.get_airport_record('data/airport.csv',airport_code))
		
			
	alist = airport_list[0]
	airport_list.append(alist)
	return airport_list

def menu():

	menu =("gen : Generate fuel report\n"+
		"exit : Exit Program\n")

	user_input = None
	
	while user_input != "exit":
			
			print("\n")
			
			print(menu)

	
			user_input = input("Please Select an option from the menu: ")
			
			if user_input == "gen":
				generate_report()
			
			elif user_input == "exit":
				break
				
			else:
				print("Invalid input entered, please select valid option")
				
				
	fm.utils.quit("Exiting Program",0)
	
def select_plane_menu():
	'displays a list of planes and prompts the user to select one'
		
	aircraft_list = fm.utils.get_aircraft_list('data/aircraft.csv')
	# initialize user input 
	user_input = None
	
	menu = ("\ncode : enter a valid aircraft code, eg F50 or 747\n")
		
	codes = [a.code for a in aircraft_list]
	
	while user_input not in codes:	
		
		print("\n")
		
		for aircraft in aircraft_list:
			print ("Aircraft : "+ aircraft.manufacturer +" "+ aircraft.code +" "+"range : " + aircraft.flight_range )
		
		print (menu)
		
		user_input = input("Please select an option from above : ")
			
		
		for aircraft in aircraft_list:
			
			if user_input == aircraft.code:
				return aircraft
			
			
		if user_input not in codes:
			print("Invalid option entered\n")


def select_country_menu(country_list,counter):
	'returns the selected country'
		
								
	# nested lists of countries with up to 50 counties per sub list	
	country_list_pages = fm.utils.sub_divide_list(country_list,50)
	
	max_pages = len(country_list_pages)
	
	page_no = 0
	
	user_input = None
	
	while user_input not in country_list:
	
		# nested list lines in a page with up to 5 items per line.
		page_lines = fm.utils.sub_divide_list(country_list_pages[page_no],4)
		page = fm.utils.format_nested_list_as_string(page_lines)
		
		
		print (page)
		print ("page %d/%d" % (page_no +1,max_pages))
		print ("country : select a country for choice number %d" % counter)
		if max_pages > 1:
			print("prev : view previous country page\n"+
			"next : view next country page\n")
				
		user_input = input('please select an option from the menu :')
		
				
		if user_input == 'prev' and page_no > 0 :
			page_no -= 1
		
		elif user_input == 'next' and page_no < max_pages -1:
			page_no += 1
		
		
	return user_input 
		
		
		


def select_airport_menu(country,counter):
	'displays a list of airports for a country and returns the selected airport'
	
	country_airport_list = fm.utils.get_country_airport_list('data/airport.csv',country)
	
	#nested list of airport codes with up to 50 airports per list
	country_airport_pages = fm.utils.sub_divide_list(country_airport_list,50)
	
		
	max_pages = len(country_airport_pages)
	
	page_no = 0
	
	user_input = None
	
	while user_input not in country_airport_list:
	
		# nested list lines in a page with up to 5 items per line.
		page_lines = fm.utils.sub_divide_list(country_airport_pages[page_no],10)
		page = fm.utils.format_nested_list_as_string(page_lines)
		
		
		print (page)
		print ("Airport : select Airport Code for choice number %d" % counter)
		print ("page %d/%d" % (page_no +1,max_pages))
		if max_pages > 1:
			print("prev : view previous Airport page\n"+
			"next : view next Airport page\n")
				
		user_input = input('please select an option from the menu :')
		
				
		if user_input == 'prev' and page_no > 0 :
			page_no -= 1
		
		elif user_input == 'next' and page_no < max_pages -1:
			page_no += 1
		
	return user_input 		
		
def display_fuel_Invoice(flight_info,fuel_cost_info):
	'print the invoice for the fuel refilled'

	# get airport codes
	codes = [f['code'] for f in flight_info]
	# prepend last code as first as they are the same.
	path = codes[-1] +" "+ fm.utils.format_list_as_string(codes)
	
		
	print("\nThe fuel invoice for the selected filghtpath:")
	print("\nFlight path: %s\n" % path)
	
	
	for i in fuel_cost_info:
		print("Airport Code: %s, Currency Rate: %f, Fuel Purchased: %f, Price: %f" % 
		(i['code'],i['rate'],i['fuel_purchased'],i['price']))
	
	
	filename = "output/"+path+".csv"
	print("\ninvoice saved as %s" % filename)	
	# writes invoice to csv file
	fm.utils.write_invoice(filename,fuel_cost_info)

	
		
		
		


	
def main():
	menu()
	


if __name__ == '__main__':
	main()
