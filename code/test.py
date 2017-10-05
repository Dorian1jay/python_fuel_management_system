#!/usr/bin/python3

import unittest
import fuel_management as fm



class TestUtils(unittest.TestCase):

	def test_get_aircraft_list(self):
	
		result = fm.utils.AC.Aircraft('A319','jet','metric','Airbus','3750','30190','litres')
		aircraft_list = fm.utils.get_aircraft_list('testfiles/aircraft.csv')
					
		self.assertEqual(aircraft_list[0].code,result.code)
		self.assertEqual(aircraft_list[0].plane_type,result.plane_type)
		self.assertEqual(aircraft_list[0].units,result.units)
		self.assertEqual(aircraft_list[0].manufacturer,result.manufacturer)
		self.assertEqual(aircraft_list[0].flight_range,result.flight_range)
		self.assertEqual(aircraft_list[0].max_fuel,result.max_fuel)
		self.assertEqual(aircraft_list[0].fuel_unit,result.fuel_unit)


	
	def test_get_country_list(self):
	
		result = fm.utils.AP.Airport('2048','Herat','Herat','Afghanistan','HEA',
		'OAHR','34.210017','62.2283','3206','4.5','U','Asia/Kabul')
		country_list = fm.utils.get_country_list('testfiles/airport.csv')
		
		self.assertEqual(country_list[0],result.country)

	
	
	def test_get_country_airport_list(self):
	
		result = fm.utils.AP.Airport('2048','Herat','Herat','Afghanistan','HEA',
		'OAHR','34.210017','62.2283','3206','4.5','U','Asia/Kabul')
		airport_list = fm.utils.get_country_airport_list('testfiles/airport.csv','Afghanistan')
		
		self.assertEqual(airport_list[0],result.code)
		
	
	
	def test_get_airport_record(self):

		result = fm.utils.AP.Airport('2048','Herat','Herat','Afghanistan','HEA',
		'OAHR','34.210017','62.2283','3206','4.5','U','Asia/Kabul')
		airport = fm.utils.get_airport_record('testfiles/airport.csv','HEA')

		self.assertEqual(airport.airportID,result.airportID)
		self.assertEqual(airport.airportName,result.airportName)
		self.assertEqual(airport.country,result.country)
		self.assertEqual(airport.code,result.code)
		self.assertEqual(airport.icaoCode,result.icaoCode)
		self.assertEqual(airport.latitude,result.latitude)
		self.assertEqual(airport.longitude,result.longitude)
		self.assertEqual(airport.timeOffset,result.timeOffset)
		self.assertEqual(airport.dst,result.dst)
		self.assertEqual(airport.tz,result.tz)
		
	
	
	def test_sub_divide_list(self):
	
	
		list_data = ['aaa','bbb','ccc','ddd','eee','fff','ggg','hhh','iii','jjj']
		lists = fm.utils.sub_divide_list(list_data,3)
		
		self.assertEqual(lists[0],list_data[0:3])
		self.assertEqual(lists[1],list_data[3:6])
		self.assertEqual(lists[2],list_data[6:9])
		self.assertEqual(lists[3],[list_data[9]])
		
	
	
	def test_format_list_as_string(self):
		list_data = ['aaa','bbb','ccc']
		
		s = fm.utils.format_list_as_string(list_data)
		
		self.assertEqual(s,'aaa bbb ccc')
	
	
	def test_validate_airports(self):
	
		airport_list =[]
		
		a = fm.utils.AP.Airport('2048','Herat','Herat','Afghanistan','HEA',
		'OAHR','34.210017','62.2283','3206','4.5','U','Asia/Kabul')
		airport_list.append(a)
		
		a = fm.utils.AP.Airport('2049','Jalalabad','Jalalabad','Afghanistan','JAA','OAJL',
		'34.399842','70.498625','1814','4.5','U','Asia/Kabul')
		airport_list.append(a)
		
		a = fm.utils.AP.Airport('2050','Kabul Intl','Kabul','Afghanistan','KBL','OAKB',
		'34.565853','69.212328','5877','4.5','U','Asia/Kabul')
		airport_list.append(a)
		
		a = fm.utils.AP.Airport('2051','Kandahar','Kandahar','Afghanistan','KDH','OAKN',
		'31.505756','65.847822','3337','4.5','U','Asia/Kabul')
		airport_list.append(a)
		
		a = fm.utils.AP.Airport('2048','Herat','Herat','Afghanistan','HEA',
		'OAHR','34.210017','62.2283','3206','4.5','U','Asia/Kabul')
		airport_list.append(a)
		
		self.assertTrue(airport_list)

	
	
if __name__ == '__main__':
    unittest.main()
 
