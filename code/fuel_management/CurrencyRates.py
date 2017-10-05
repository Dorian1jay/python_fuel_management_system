class CurrencyRates:

	def __init__(self,currency_name,currency_alphabetic_code,
	currency_to_euro,euro_to_currency):
	
		self.currency_name = currency_name
		self.currency_alphabetic_code = currency_alphabetic_code
		self.currency_to_euro =float(currency_to_euro)
		self.euro_to_currency =float(euro_to_currency)
		
	
