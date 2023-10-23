# Final Part of the Passenger Boarding Kiosk project
# Check Passengers Boarding Passes and Update Flight Info Table Based on Validation
from azure_table_service import get_passenger_from_azure_table, update_passenger_validation
from azure_form_recognizer_service import process_boarding_pass, process_license
from kiosk_validation import validate_boarding_pass_passenger_name, validate_license_passenger_name, validate_license_dob, validate_boarding_pass_flight
from azure_face_identity import validate_passenger_face
from azure_custom_vision_service import validate_passenger_luggage

# Passenger Input for Kiosk
passenger_name = "{passenger_name}"
boarding_pass_image_url = "{boarding_pass_image_url}"
license_image_url = "{license_image_url}"

# Get Passengers Flight Info
passenger_data = get_passenger_from_azure_table(passenger_name)

# Get Passengers Boarding Pass
boarding_pass_data = process_boarding_pass(boarding_pass_image_url)

# Get Passengers License 
license_data = process_license(license_image_url)

kiosk_validation_result = {}

# Check 3 Way Person Name Validation
person_validation_boarding_pass = validate_boarding_pass_passenger_name(passenger_data, boarding_pass_data)
person_validation_license = validate_license_passenger_name(passenger_data, license_data)
kiosk_validation_result["PersonNameValidation"] = person_validation_boarding_pass & person_validation_license 

# Data Of Birth Validation
kiosk_validation_result["DateOfBirthValidation"] = validate_license_dob(passenger_data, license_data)

# Boarding Pass Validation
BoardingPassValidition = validate_boarding_pass_flight(passenger_data, boarding_pass_data)

kiosk_validation_result["BoardingPassValid"] = BoardingPassValidition["isvalid"]

# Person Identity Validation
person_group_id = "{person_group_id}"
person_identity_check = validate_passenger_face(license_image_url, person_group_id)
kiosk_validation_result["PersonIdentityValid"] = person_identity_check["passenger_face_valid"]

# Luggage Validation
passenger_luggage_image = "lighter_test_set_1of5.jpg"
project_id = "{project_id}"

# Only Check Validation if the passenger checked in luggage
if passenger_data["Baggage"] == "YES":
    passenger_luggage_check = validate_passenger_luggage(passenger_luggage_image, project_id)
    kiosk_validation_result["LuggageValidation"] = not passenger_luggage_check["lighter_found"]
else: 
    kiosk_validation_result["LuggageValidation"] = True
    
# Update Azure Table Based on Validation
update_passenger_validation(passenger_data, kiosk_validation_result)

# Show Formated Kiosk Screen Based on Validation Rules
passenger_info_isvalid = True

print("**********************************************************************")
print(f"kiosk output for passenger {passenger_name}")
print("**********************************************************************")
# Check if Passenger Information is valid
if kiosk_validation_result["PersonNameValidation"] == False or kiosk_validation_result["DateOfBirthValidation"] == False:
    passenger_info_isvalid = False
    print("Dear Sir/Madam,")
    print("Some of the information on your ID card does not match the flight manifest data, so you cannot board the plane.")
    print("Please see a customer service representative.")
elif kiosk_validation_result["BoardingPassValid"] == False:
    passenger_info_isvalid = False
    print("Dear Sir/Madam,")
    print("Some of the information in your boarding pass does not match the flight manifest data, so you cannot board the plane.")
    print("Please see a customer service representative.")

if passenger_data["Sex"] == "M":
    passenger_title = "Mr."
else: 
   passenger_title = "Ms."
 
# Show Boarding Information if the passenger passed all validation
# Note: The user must talk to customer service if they failed the Luggage Check
if passenger_info_isvalid == True:
    print(f"Dear {passenger_title} {boarding_pass_data['PassengerName']}")
    print(f"You are welcome to flight # {boarding_pass_data['FlightNumber']} leaving at {boarding_pass_data['BoardingTime']} from {boarding_pass_data['From']} to {boarding_pass_data['To']}")
    print(f"Your seat number is {boarding_pass_data['Seat']}, and it is confirmed.")

    if kiosk_validation_result["LuggageValidation"]:
        print("We did not find a prohibited item (lighter) in your carry-on baggage,")
        print("thanks for following the procedure.")
  
        if kiosk_validation_result["PersonIdentityValid"]:
            print("Your identity is verified so please board the plane.")
        else:
            print("Your identity could not be verified. Please see a customer service representative.")      
    else:
        print("We have found a prohibited item in your carry-on baggage, and it is flagged for removal.") 

        if kiosk_validation_result["PersonIdentityValid"]:
            print("Your identity is verified. However, your baggage verification failed, so please see a customer service representative.")
        else:
            print("Your identity could not be verified. Please see a customer service representative.")      
        

