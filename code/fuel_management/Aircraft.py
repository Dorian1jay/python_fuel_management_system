class Aircraft:
	'Aircraft Class'

	def  __init__(self,code,plane_type,units,
    manufacturer,flight_range,max_fuel,fuel_unit):
    
		self.code = code
		self.plane_type = plane_type
		self.units = units 
		self.manufacturer = manufacturer
		self.flight_range = flight_range
		self.max_fuel = max_fuel
		# strip the newline from the fuel unit
		self.fuel_unit = fuel_unit
		# assume an aircraft starts with a full tank
		self.current_fuel = self.max_fuel
    	
    	
	def __str__(self):
		'string representation of aircraft object'
			
		s = ("Aircraft: "+ self.code + ","+
		self.plane_type + ","+
		self.units+","+
		self.manufacturer+","+
		str(self.flight_range)+","+
		str(self.max_fuel)+","+
		self.fuel_unit)

		return s
    	
	def convert_imperial_to_metric(self):
		'converts imperial units to metric'

		if self.units == "imperial":
			self.flight_range = float(self.flight_range) * 1.6093
			self.units = "metric"	    
    	
		if self.fuel_unit == "gallons":
			self.max_fuel = float(self.max_fuel) * 3.785
			self.current_fuel = self.max_fuel
			self.fuel_unit = "litres"
	
    	
	def get_litres_per_km(self):	
		'calculates fuel used in litres per kilometer'
		return self.max_fuel / self.flight_range
    	
    	
    	
