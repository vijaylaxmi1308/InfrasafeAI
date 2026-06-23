import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

device = torch.device("cpu")

# LOAD MODEL
model = models.mobilenet_v2(weights=None)

model.classifier[1] = nn.Linear(
    model.last_channel,
    2
)

model.load_state_dict(
    torch.load(
        "emergency_model.pth",
        map_location=device
    )
)

model.eval()

# TRANSFORM
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

# CLASS MAPPING
classes = {
    0: "Accident",
    1: "Invalid Emergency"
}

# DETECTION FUNCTION
def detect_emergency(image_path):

    try:

        img = Image.open(image_path)
        img.load()
        img = img.convert("RGB")

        img = transform(img).unsqueeze(0)

        with torch.no_grad():

            output = model(img)

            prediction = torch.argmax(output, 1).item()

        return classes[prediction]

    except Exception as e:

        print("EMERGENCY AI ERROR:", e)

        return "Detection Failed"