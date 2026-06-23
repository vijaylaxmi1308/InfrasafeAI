import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

# ---------------- DEVICE ----------------
device = torch.device("cpu")

# ---------------- LOAD MODEL ----------------
model = models.mobilenet_v2(weights=None)

# 🔥 SAME NUMBER OF CLASSES
model.classifier[1] = nn.Linear(
    model.last_channel,
    3
)

# ---------------- LOAD TRAINED WEIGHTS ----------------
model.load_state_dict(
    torch.load(
        "infra_model.pth",
        map_location=device
    )
)

model.eval()

# ---------------- IMAGE TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

# ---------------- CLASS LABELS ----------------
# MUST MATCH dataset.class_to_idx

classes = {
    0: "Broken pole",
    1: "Invalid Report",
    2: "Pothole"
}

# ---------------- MAIN FUNCTION ----------------
def detect_issue(image_path):

    try:

        img = Image.open(image_path).convert("RGB")

        img = transform(img).unsqueeze(0)

        with torch.no_grad():

            output = model(img)

            prediction = torch.argmax(output, 1).item()

        return classes[prediction]

    except Exception as e:

        print("AI ERROR:", e)

        return "Detection Failed"