import math
import csv 
from . import Aircraft as AC
from . import Airport as AP
from . import CountryCurrency as CC
from . import CurrencyRates as CR


def get_aircraft_list(filename):
	'reads an aircraft csv file and returns a list of Aircraft objects'
	aircraft_list = []
	try:	
		with open (filename,'r') as csvfile:
		
			# skip first line
			csvfile.readline()
			
			for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
                    quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
										
				aircraft = AC.Aircraft(r[0],r[1],r[2],r[3],r[4],r[5],r[6])
			
				aircraft_list.append(aircraft)
		
			return aircraft_list
	
	except FileNotFoundError:
		quit("The file"+ filename + " was not found",1)	
	
	except IndexError:
		quit("Index Error occured in file "+ filename ,1)
	
	except StopIteration :
		quit("Invalid data in file "+ filename ,1)
	
	except :
		# general error
		quit("An error occured processing file "+ filename ,1)
			

def get_country_list(filename):
	''
	country_list = []
	
	try:
		with open (filename,'r') as csvfile:
						
			for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
                     quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
			
				
				airport = AP.Airport(r[0],r[1],r[2],r[3],
					r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11])
				
				if airport.country not in country_list:
					country_list.append(airport.country)
		
		return country_list
	
	except FileNotFoundError:
		quit("The file"+ filename + " was not found",1)
	
	except IndexError:
		quit("Index Error occured in file "+ filename ,1)
	
	except StopIteration :
		quit("Invalid data in file "+ filename ,1)
	
	except :
		# general error
		quit("An error occured processing file "+ filename ,1)
	
		
def get_country_airport_list(filename,country):
	'gets a list of the selected airports from the user'
	
	country_airport_list = []
	
		
	with open (filename,'r') as csvfile:
		
		for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
                     quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
									
				
			airport = AP.Airport(r[0],r[1],r[2],r[3],
			r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11])
		
		
					
			if country == airport.country:
				country_airport_list.append(airport.code)
		
		return country_airport_list
		
def get_airport_record(filename,airport_code):
	'returns an airport record for user given airport code'
	
	with open (filename,'r') as csvfile:
		
		for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
                     quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
									
			
			airport = AP.Airport(r[0],r[1],r[2],r[3],
			r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11])
		
					
			if airport_code == airport.code:
				return airport
			
		return None

def sub_divide_list(list_data,no_of_cols):
	'returns a list of lists of length no_of_cols'
	
	list_of_lists = []
	inc = no_of_cols
	i = 0
		
	while i < len(list_data):
	
		if i + inc <= len(list_data):
			list_of_lists.append(list_data[0+i:i+inc])
			i += inc
		else:
			remainder = len(list_data) - i
			list_of_lists.append(list_data[i:i+remainder])
			i += remainder

	return list_of_lists

def format_list_as_string(list_data):
	'returns a list as a string with space inbetween'
	
	string = ""
	
	for i in list_data:
		string += (i + ' ')
	
	return string.strip()

def format_nested_list_as_string(list_data):
	'returns a list as a string with space inbetween'
	
	string = ""
	
	for i in list_data:
		string += (format_list_as_string(i) + '\n')
	
	return string		
	
	
def quit(msg,exitcode):
	'display a message and quit'
	print(msg)
	exit(exitcode)	
	
	
	
def calc_flightpath_cost(airport_list,aircraft):
	'calculate flightpath cost'
	
	# store information for each destination in a dict
	flight_info = [dict() for x in range(0,len(airport_list)-1)]
	
	#loop through airports and calculate distances between each
	for i in range(0,len(airport_list)-1) :
	
		lat1,long1 = airport_list[i].get_position()
		lat2,long2 = airport_list[i+1].get_position()
		
		# create dictionary items
		flight_info[i]['distance']	= distance(lat1,long1,lat2,long2)
		flight_info[i]['code'] = airport_list[i+1].code 
		flight_info[i]['rate'] = get_exchange_rate_for_country(airport_list[i+1].country)
		flight_info[i]['id'] = i


	# check the aircraft can make all the journeys
	check_flight_range(aircraft,flight_info,airport_list)
	
	# keep track of refuel information
	fuel_cost_info = []
	
	# at each destination
	for f in flight_info:
		
		# subtract the fuel
		fpkm = f['distance'] * aircraft.get_litres_per_km()
		aircraft.current_fuel = aircraft.current_fuel - fpkm
		
		# check if the plane at the final destination
		if f['id'] == flight_info[len(flight_info) -1]['id']:
			
			# refill the remaining amount
			d = gen_refuel_record(f,aircraft)
			fuel_cost_info.append(d)
		
			
		# contine on journey
		else:

			# is there enough fuel to fly to the next airport
			fpkm = flight_info[ f['id'] +1 ]['distance'] * aircraft.get_litres_per_km()
			if aircraft.current_fuel - fpkm >= 0:

				# refuel if current rate is cheaper
				if f['rate'] < flight_info[ f['id'] +1 ]['rate']:

					# refuel
					d = gen_refuel_record(f,aircraft)
					fuel_cost_info.append(d)
					
			else:

				# refuelling is necessary
				d = gen_refuel_record(f,aircraft)
				fuel_cost_info.append(d)
				

	return (flight_info,fuel_cost_info)
		




def gen_refuel_record(flight_dict,aircraft):
	'generate a dictionary with refuel info'
	
	fuel_purchased = aircraft.max_fuel - aircraft.current_fuel 
	price = calculate_fuel_price( flight_dict['rate'], aircraft )
	
	d = {'fuel_purchased':fuel_purchased,
	'rate':flight_dict['rate'],
	'price':price,
	'code':flight_dict['code']}
	
	return d		
	
def calculate_fuel_price(rate,aircraft):
	fuel = aircraft.max_fuel - aircraft.current_fuel
	return fuel * rate
	

def check_flight_range(aircraft,flight_info,airport_list):
	'check if any flight distance is greater than plane range'
	
	for i in range (0,len(flight_info)):	
		#Check if aircraft can make the journey
		if aircraft.flight_range < flight_info[i]['distance']:
			msg =( "The aircraft "+aircraft.code + 
			" is not capable of flying the distance between "+
			airport_list[i].country+" : "+ airport_list[i].code + " and "+
			airport_list[i+1].country+" : "+airport_list[i+1].code)

			quit(msg,1)




def distance(lat1,long1, lat2,long2):
    # convert degrees to radians
    degree_to_radians = math.pi/180.0

    #phi = 90 - lat 
    phi1 = (90 - float(lat1) ) * degree_to_radians
    phi2 = (90 - float(lat2) ) * degree_to_radians

    #theta = longitude
    theta1 = float(long1) * degree_to_radians
    theta2 = float(long2) * degree_to_radians

    #get spherical distance from coordinates
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1) *math.cos(phi2))
    arc = math.acos(cos)

    #multiply arc by earth radius
    return arc * 6371	
    

def get_country_currency(filename,country):
	'returns country currency for user given country'
	
	with open (filename,'r') as csvfile:
		
		for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
                     quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
		
	
			countryCurrency = CC.CountryCurrency(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],
			r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19])
		
					
			if country == countryCurrency.name:
				return countryCurrency.currency_alphabetic_code
			
		return None
		

def get_currency_rates(filename,currency_alphabetic_code):
	'returns an airport record for user given airport code'
	
	with open (filename,'r') as csvfile:
		
				
		for r in csv.reader(csvfile.readlines(), quotechar='"', delimiter=',',
			quoting= csv.QUOTE_MINIMAL, skipinitialspace=True):
									
			currency = CR.CurrencyRates(r[0],r[1],r[2],r[3])
		
					
			if currency_alphabetic_code == currency.currency_alphabetic_code:
				return currency.currency_to_euro
			
		return None	
		
def validate_airports(airport_list):
	'validate airport business logic'	
	
	# Check if first and last airport are the same 
	if airport_list[0].code != airport_list[4].code:
		return False
	
	# check departure airport is not arrival	
	for i in range(0,len(airport_list)-1):
		if airport_list[i].code == airport_list[i+1].code:
			return False
	
	# check no airport is visited more than twice 
	codes = [a.code for a in airport_list]
	
	for i in airport_list:
	
		if codes.count(i.code) > 2 :
			return False
			
	return True
	
	
def get_exchange_rate_for_country(country):
	'returns exhanges rates for a country'
	
		
	#take in a country and return a currency code
	cc = get_country_currency('data/countrycurrency.csv',country)
	#take in currency code and return an exchange rate
	cr = get_currency_rates('data/currencyrates.csv',cc)
		
	return cr	
		
def write_invoice(filename,fuel_cost_info):
	'write fuel cost to a csv file'
	

	with open(filename, 'w') as csvfile:
		
		fieldnames = fuel_cost_info[0].keys()
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	
		writer.writeheader()

		for i in fuel_cost_info:
			writer.writerow(i)
	
	
