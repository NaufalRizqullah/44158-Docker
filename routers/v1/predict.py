import torch

from fastapi import APIRouter, UploadFile
from PIL import Image
from timeit import default_timer as timer 

from src.utils.model import create_effnetb2_model
from src.utils.helper import load_class_names
from src.schemas.output_44158 import OutputBase



router = APIRouter()

@router.post("/predict", response_model=OutputBase)
def inference(greetings: str, im: UploadFile):

    # Load class names
    class_names = load_class_names()
    
    # get image to PIL format
    image = Image.open(im.file).convert('RGB')
       
    # Get model, transformation and calculate time to load it.
    start_time = timer()
    model, transforms = create_effnetb2_model(len(class_names))
    end_time = timer()
    print(f"[INFO] Total Loading model time: {end_time - start_time:.3f} seconds")

    # Inference Time Start
    inference_start_time = timer()

    # turn image to same transformation
    img = torch.unsqueeze(transforms(image), dim=0)

    # Put model into evaluation mode and turn on inference mode
    model.eval()
    with torch.inference_mode():
        # no need to send data to GPU, cause default is cpu.
        pred_logits = model(img)
        pred_probs = torch.softmax(pred_logits, dim=1)


    # Create prediction labels 
    predicted_label_index = torch.argmax(pred_probs).item() # get single index if not add dim.
    predicted_label = class_names[predicted_label_index]

    # Inference Time End
    inference_start_end = timer()

    # Get probability predictions
    probability_pred = pred_probs[0][predicted_label_index].item()

    return OutputBase(
        message=greetings,
        class_predicted=predicted_label,
        prob=probability_pred,
        inference_time=f"{inference_start_end - inference_start_time:.3f} Seconds"
    )