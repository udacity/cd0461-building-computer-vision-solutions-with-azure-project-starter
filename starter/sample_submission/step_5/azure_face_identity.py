## Installed Latest Azure package - pip install azure-cognitiveservices-vision-face
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials

# Azure is now limiting access to Face API
# https://learn.microsoft.com/en-us/legal/cognitive-services/computer-vision/limited-access-identity
# My WorkAround for this was to use the Generated Udacity Lab to create the Face Model and use it for project
# All Other Azure Resources were kept in my personal Azure Resource Group
# AZURE_FACE_KEY = "{AZURE_FACE_KEY}"
# AZURE_FACE_ENDPOINT = "https://tfsface.cognitiveservices.azure.com/"

AZURE_FACE_KEY = "{AZURE_FACE_KEY}"
AZURE_FACE_ENDPOINT = "https://tfsfacelab1021.cognitiveservices.azure.com/"

def validate_passenger_face(passenger_face_url, person_group_id):
    face_result = {}
    
    # Detect Face from License 
    face_client = FaceClient(AZURE_FACE_ENDPOINT, CognitiveServicesCredentials(AZURE_FACE_KEY))
    detected_faces_result = face_client.face.detect_with_url(url=passenger_face_url, detection_model='detection_03')
    if not detected_faces_result:
        raise Exception('No face detected from image {}'.format(passenger_face_url)) 
    
    face_result["detected_faces"] = str(len(detected_faces_result))
    
    face_id = -1
    for face in detected_faces_result: 
        face_id = face.face_id
        
    face_result["face_id"] = face_id
    
    # Display Confidence of Matching License Image Agaist Model   
    person_gp_results = face_client.face.identify([face_id], person_group_id)
    
    # For Initial Code We are assuming a single candidate image is returned 
    for result in person_gp_results:
        if result.candidates:
            for candidate in result.candidates:
                face_result["detected_confidence"] = candidate.confidence
                face_result["passenger_face_valid"] = candidate.confidence > .65
        else:
            face_result["detected_confidence"] = 0
            face_result["passenger_face_valid"] = False
    
    print(face_result)
    return face_result
