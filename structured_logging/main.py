from Customer import *
from CustAddress import CustAddress
from faker import Faker
import json
from struct_logging import logger

customer = Customer()
fake = Faker()


# Create a customer object with basic details
customer.cust_basic.first_name = fake.first_name()
customer.cust_basic.last_name = fake.last_name()
customer.cust_basic.email = fake.email()
customer.cust_basic.phone_number = fake.phone_number()
customer.cust_basic.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")

# Create a customer object with address details
address = CustAddress()
address.address_counter = 1
address.address_line_1 = fake.street_address()
address.address_line_2 = fake.secondary_address()
address.address_line_3 = fake.building_number()
address.city = fake.city()
address.state = fake.state()
address.zip_code = fake.zipcode()
address.country = fake.country()
customer.cust_address.append(address)

# Create a customer object with card details
card = CustCard()
card.card_counter = 1
card.card_type = fake.credit_card_provider()
card.card_number = fake.credit_card_number()
card.expiration_date = fake.credit_card_expire()
card.cardholder_name = fake.name()
customer.cust_card.append(card)

logger.info("printing customer object", customer=json.loads(str(customer)))
# print (customer)

