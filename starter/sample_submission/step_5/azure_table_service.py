from azure.data.tables import TableClient, UpdateMode

## Connection String for Azure Table Storage
connection_string = "{table_storage_connection_string}"

# Get Passenger Data from Azure Table
# Table Field Include
# 'Baggage':
# 'Seat':
# 'Gate':
# 'BoardingTime':
# 'TicketNo':
# 'FirstName':
# 'LastName':
# 'DateOfBirth':
# 'Sex':
# 'DoBValidation':
# 'PersonValidation':
# 'LuggageValidation':
# 'NameValidation':
# 'BoardingPassValidation':
# 'Class':
def get_passenger_from_azure_table(passenger_name):
    passenger = {}
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name="FlightManifest")

    query_filter = f"PartitionKey eq '{passenger_name}'"
    queried_passengers = table_client.query_entities(query_filter)
    
    for entity_chosen in queried_passengers:
        passenger = entity_chosen

    return passenger

def update_passenger_validation(passenger, kiosk_validation_result):
    
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name="FlightManifest")
    passenger_entity = table_client.get_entity(partition_key=passenger["PartitionKey"], row_key=passenger["RowKey"])
        
    passenger_entity["NameValidation"] = kiosk_validation_result["PersonNameValidation"]
    passenger_entity["PersonValidation"] = kiosk_validation_result["PersonIdentityValid"]
    passenger_entity["BoardingPassValidation"] = kiosk_validation_result["BoardingPassValid"]
    passenger_entity["DoBValidation"] = kiosk_validation_result["DateOfBirthValidation"]
    passenger_entity["LuggageValidation"] = kiosk_validation_result["LuggageValidation"]    
    
    result = table_client.update_entity(mode=UpdateMode.MERGE, entity=passenger_entity)
    
    return True