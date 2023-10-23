from datetime import datetime

def validate_boarding_pass_passenger_name(passenger_data, boarding_pass_data):
    
    isvalid = False
    passenger_name = f"{passenger_data['FirstName']} {passenger_data['LastName']}"
    boarding_pass_fullname = boarding_pass_data["PassengerName"]
    
    if passenger_name == boarding_pass_fullname:
        isvalid = True
    
    return isvalid

def validate_license_passenger_name(passenger_data, license_data):
   
    isvalid = False
    passenger_name = f"{passenger_data['FirstName']} {passenger_data['LastName']}"
    license_fullname = f"{license_data['FirstName']} {license_data['LastName']}"
    
    if passenger_name == license_fullname:
        isvalid = True
    
    return isvalid

def validate_license_dob(passenger_data, license_data):
   
    isvalid = False
    
    # Must Convert (Format) Dates from Azure Table and License before comparing
    passenger_dob = passenger_data['DateOfBirth']
    license_dob = license_data['DateOfBirth']
    
    passenger_dob_date = datetime.strptime(passenger_dob, "%d-%b-%y")
    license_dob_date = datetime.strptime(license_dob, "%m/%d/%Y")

    if passenger_dob_date == license_dob_date:
        isvalid = True
    
    return isvalid

def validate_boarding_pass_flight(passenger_data, boarding_pass_data):
    check_boarding_pass = {}
    check_boarding_pass["isvalid"] = True
    
    # Check if Class Should be Missing from Azure Table
    check_boarding_pass['HasBaggage'] = boarding_pass_data['Baggage']
    
    if passenger_data['FlightNo'] != boarding_pass_data['FlightNumber']:
        check_boarding_pass["isvalid"] = False
    
    if passenger_data['Seat'] != boarding_pass_data['Seat']:
         check_boarding_pass["isvalid"] = False
         
    if passenger_data['From'] != boarding_pass_data['From']:
         check_boarding_pass["isvalid"] = False
         
    if passenger_data['To'] != boarding_pass_data['To']:
         check_boarding_pass["isvalid"] = False
         
    if  passenger_data['Gate'] != boarding_pass_data['Gate']:
         check_boarding_pass["isvalid"] = False

    # Check Flight Date and Time
    passenger_data_flight_date = datetime.strptime(passenger_data["Date"], "%d-%b-%y")
    boarding_pass_flight_date = datetime.strptime(boarding_pass_data["Date"], "%B %d, %Y")

    if passenger_data_flight_date != boarding_pass_flight_date:
          check_boarding_pass["isvalid"] = False

    if  passenger_data['BoardingTime'] != boarding_pass_data['BoardingTime']:
         check_boarding_pass["isvalid"] = False

    return check_boarding_pass
