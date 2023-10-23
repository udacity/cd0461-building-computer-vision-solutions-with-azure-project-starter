import os
import pathlib
 
## Package - pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

# Use This URL to Get Azure Vision Settings - https://www.customvision.ai/projects#/settings
PREDICTION_ENDPOINT = "https://tfscustomvision-prediction.cognitiveservices.azure.com/"
prediction_key = "{prediction_key}"
prediction_resource_id = "/subscriptions/51791864-7a0f-4d43-9114-3ad5d091491a/resourceGroups/TFS/providers/Microsoft.CognitiveServices/accounts/tfscustomvision-Prediction"

## Custom Vision Published Model Configuration
publish_iteration_name = "tfs_lighter_model"
localImagePath = pathlib.Path().resolve()

def validate_passenger_luggage(luggage_image_file, project_id):
    
    luggage_check = {}
    luggage_check["luggage_image_file"] = luggage_image_file
    luggage_check["lighter_found"] = False

    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)
    
    with open(os.path.join (localImagePath,  luggage_image_file), "rb") as image_contents:
        results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
  
        for prediction in results.predictions:
            luggage_check[prediction.tag_name] = { "tagname": prediction.tag_name, "probability": prediction.probability * 100}
           
    # Check to See if lighter was found in Luggage     
    lighter_probability = luggage_check["lighter"]["probability"]
    if lighter_probability > 65:
        luggage_check["lighter_found"] = True

    return luggage_check