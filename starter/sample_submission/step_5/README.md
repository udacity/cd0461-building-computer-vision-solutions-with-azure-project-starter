Please add your submission content here.
# Overview
This is the code for the kiosk passenger boarding application. This project includes all the logic for kiosk application to validate a passenger using their boarding pass, license and face to determine if they can successfully board their flight.

The application preforms the following validation checks:
You will perform the following recognition and validation process:

- Digital ID recognition
- Boarding pass recognition
- Identity validation
- Lighter detection in carry-on items
- Automated kiosk experience

The application uses the following Azure Services
- Azure Form Recognize
- Azure Computer Vision
- Azure Computer Video Analyzer
- Face services
- Azure Storage (Table)

**Note:**
For the project work, I used my own Azure Subscription. Unfortunately Microsoft is now limiting access to the Face API Service without requesting permission. To work around this I used
the generated Udacity Lab to create the Face Model for the project. All Other Azure Resources were kept in my personal Azure Resource Group (Subscription).

https://learn.microsoft.com/en-us/legal/cognitive-services/computer-vision/limited-access-identity

# Code Overview
The main module for this project's application is **kiosk_app.py** file located under Step_5. The application makes references to the other service classes which perform validation or provide access to different Azure Resources.

For the project, I created my own license, boarding pass and video which are include in the repo. For testing the project, I used three different uses including myself.
- Todd Snyder - Passed Validation Except Luggage Check
- James Webb - Passed All Validation Except Face (Person) Validation. This is because I only used my own video for the facial check 
- Libby Herold - Failed Date of Birth Validation. As a test, I set Libby Birthdate in the table to be different than what is on their license 

# List of Python Libraries used in the project 
The following Azure and Utility Python libraries were used to build the kiosk passenger boarding application.

- from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
- from msrest.authentication import ApiKeyCredentials
- from azure.cognitiveservices.vision.face import FaceClient
- from msrest.authentication import CognitiveServicesCredentials
- from azure.ai.formrecognizer import FormRecognizerClient
- from azure.core.credentials import AzureKeyCredential
- from azure.data.tables import TableClient, UpdateMode

# Folder  Resources
 - kiosk_app.py - Main Entry Point for the Application
 - kiosk_validation.py - Validation Functions
 - azure_table_service.py - Service for Accessing Azure Table Storage
 - azure_form_recognizer_service.py - Service for Accessing Azure Form Recognizer
 - azure_face_identity.py - Service for Accessing Azure Face Identity Service
 - azure_custom_vision_service - Service for Accessing Azure Custom Vision Service
 - lighter_test_set_1of5 - lighter_test_set_5of5 - Images for Checking Baggage
 - Microsoft Azure_Resource_Group.png - Screen Shot of Azure Resource Group
 - table - Screen Shot of Updated Flight Manifest Table After running validations
 - Kiosk_results - Results displayed from Kiosk
 - Report - Azure Monitoring Report for Azure AI Resources 

