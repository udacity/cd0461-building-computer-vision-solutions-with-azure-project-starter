from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

## Setup URL and Key for Azure Form Recognizer Servic3e
AZURE_FORM_RECOGNIZER_ENDPOINT = "https://tfslabproject.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "{AZURE_FORM_RECOGNIZER_KEY}"
endpoint = AZURE_FORM_RECOGNIZER_ENDPOINT
key = AZURE_FORM_RECOGNIZER_KEY

## Custom Model ID for Boarding Pass Model 
custom_model_id = "{custom_model_id}"

def process_boarding_pass(boarding_pass_url):
    boarding_pass = {}
    
    ## Process Image File Using Trained Model
    form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    source_image_url = boarding_pass_url
    custom_test_action = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=custom_model_id, form_url=source_image_url)

    ## Get Data For Requested Boarding Pass
    custom_test_action_result = custom_test_action.result()
    for recognized_content in custom_test_action_result:
        print("Form type: {}".format(recognized_content.form_type))
        for name, field in recognized_content.fields.items():
            boarding_pass[name] = field.value

    return boarding_pass

def process_license(license_url):
    license = {}
    
    form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    id_content_from_url = form_recognizer_client.begin_recognize_identity_documents_from_url(license_url)

    ## Get Rsults from Processing license photo
    id_data = id_content_from_url.result()
    content = id_data[0] 
    
    license["FirstName"] = content.fields.get("FirstName").value
    license["LastName"] = content.fields.get("LastName").value
    license["DateOfBirth"] = content.fields.get("DateOfBirth").value_data.text

    return license