import os
import torch
import torch.nn as nn
from torchvision import models

# Aapke project ki 5 classes
CLASSES = [
    'Amphiprion_clarkii',
    'Chaetodon_lunulatus',
    'Chromis_chrysura',
    'Dascyllus_reticulatus',
    'Plectroglyphidodon_dickii'
]

def export_model_to_onnx():
    # Weights ka path set karein (aapke folder structure ke mutabiq)
    weights_path = "backend/models/aquaclass_mobilenetv2_best.pth"
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weights file nahi mili: {weights_path}")

    print("Loading PyTorch model architecture and weights...")
    
    # 1. Architecture recreate karein (wahi jo aapki file mein hai)
    model = models.mobilenet_v2(weights=None)
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, len(CLASSES))
    
    # 2. Weights load karein
    state_dict = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    # 3. Frontend public folder ensure karein ke exist karta ho
    os.makedirs("frontend/public/model", exist_ok=True)
    
    output_onnx_path = "frontend/public/model/aquaclass_model.onnx"
    
    # 4. Dummy input tensor (Batch=1, Channels=3, Height=224, Width=224)
    dummy_input = torch.randn(1, 3, 224, 224)

    print(f"Exporting model to ONNX format at: {output_onnx_path} ...")
    
    # 5. Export to ONNX
    torch.onnx.export(
        model, 
        dummy_input, 
        output_onnx_path,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    
    print("SUCCESS: Model successfully converted to ONNX and saved in frontend/public/model/!")

if __name__ == "__main__":
    export_model_to_onnx()