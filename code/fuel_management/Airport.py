class Airport:
	'airport class'
	
	def __init__(self,AirportID,AirportName,CityName,
	Country,code,ICAOcode,Latitude,Longitude,
	Altitude,TimeOffset,DST,Tz):
	
		self.airportID = AirportID
		self.airportName = AirportName
		self.cityName = CityName
		self.country = Country
		self.code = code
		self.icaoCode = ICAOcode
		self.latitude = Latitude
		self.longitude = Longitude
		self.altitude = Altitude
		self.timeOffset = TimeOffset
		self.dst = DST
		self.tz = Tz
		
	def __str__(self):
		'string representation of airport object'
		a = ("Airport :"+ 
		self.airportID +","+
		self.airportName +","+
		self.cityName +","+
		self.country +","+
		self.code +","+
		self.icaoCode +","+
		self.latitude +","+
		self.longitude +","+
		self.altitude +","+
		self.timeOffset +","+
		self.dst +","+
		self.tz)
		
		return a

		
	def get_position(self):
		'return the latitude and longitude as a tuple'
		return(self.latitude,self.longitude)
		
		
		
		
		
	
