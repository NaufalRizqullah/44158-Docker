import torchvision
import torch
import functools
import os

from torch import nn
from pathlib import Path

@functools.cache
def create_effnetb2_model(num_class: int):
    """Create a pytorch model for EfficientNetB2.

    Making a EfficientNetB2 as Feature Extractor and also
    can custom output class as need it.

    Args:
        num_class: A number of class, that will be output (head) of model.

    Returns:
        a tuple of (model, transforms) of EfficientNetB2.

    """
    
    # Get weights of ResNet50
    weights_effnetb2 = torchvision.models.EfficientNet_B2_Weights.IMAGENET1K_V1

    # Get transforms used in resnet
    transforms = weights_effnetb2.transforms()

    # making model
    model = torchvision.models.efficientnet_b2(weights=weights_effnetb2)

    # Freeze All layer
    for param in model.parameters():
        param.requires_grad = False

    # Custom Output class
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408,
                  out_features=num_class)
    )

    # Load trained weights
    path_model_weights = Path("./src/data") / "44158_3_efficientnet_b2.pth"
    model.load_state_dict(
        torch.load(path_model_weights, map_location=torch.device("cpu"))
    )

    return model, transforms