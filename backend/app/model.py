import os
import torch
import torch.nn as nn
from torchvision import models

CLASSES = [
    'Amphiprion_clarkii',
    'Chaetodon_lunulatus',
    'Chromis_chrysura',
    'Dascyllus_reticulatus',
    'Plectroglyphidodon_dickii'
]

def load_trained_model(weights_path: str = None, device: str = "cpu"):
    if weights_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        weights_path = os.path.join(base_dir, "models", "aquaclass_mobilenetv2_best")

    # Flexible check: Agar bina .pth ke na miley, toh .pth laga kar check kar lo
    if not os.path.exists(weights_path):
        if os.path.exists(weights_path + ".pth"):
            weights_path = weights_path + ".pth"
        elif os.path.exists(weights_path.replace(".pth", "")):
            weights_path = weights_path.replace(".pth", "")
        else:
            raise FileNotFoundError(f"Model weights file nahi mili! Yahan check kiya: {weights_path}")

    # Recreate MobileNetV2 architecture
    model = models.mobilenet_v2(weights=None)
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, len(CLASSES))
    
    # Load state dict
    state_dict = torch.load(weights_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model