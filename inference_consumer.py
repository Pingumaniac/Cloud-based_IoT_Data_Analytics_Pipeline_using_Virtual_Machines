from kafka import KafkaConsumer, KafkaProducer
import json
import base64
from PIL import Image
import io
import torch
import torchvision.transforms as transforms
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

consumer = KafkaConsumer(
    "image_data",
    bootstrap_servers="192.168.5.43:9092",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers="192.168.5.250:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

model = torch.hub.load('chenyaofo/pytorch-cifar-models', 'cifar10_resnet20', pretrained=False)

model.load_state_dict(torch.load("cifar10_resnet20.pt"))
model.eval()
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.247, 0.243, 0.261]),
])


classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def decode_image(img_data):
    img_bytes = base64.b64decode(img_data)
    return Image.open(io.BytesIO(img_bytes))

def infer_image(image):
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)

    predicted_idx = torch.max(output, 1)[1]
    return classes[predicted_idx.item()]
def consume_images():
    for message in consumer:
        image_data = message.value
        image = decode_image(image_data['Data'])

        inferred_value = infer_image(image)
        result = {
            "ID": image_data['ID'],
            "GroundTruth": image_data['GroundTruth'],
            "InferredValue": inferred_value
        }

        producer.send("inference_results", value=result)
        producer.flush()

        print(f"Sent inference result for image {image_data['ID']}: {inferred_value}")

@app.route('/infer', methods=['POST'])
def manual_infer():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = Image.open(request.files['image'])
    inferred_value = infer_image(image)

    return jsonify({"InferredValue": inferred_value})

if __name__ == "__main__":
    consumer_thread = Thread(target=consume_images)
    consumer_thread.start()

    app.run(host='0.0.0.0', port=5000)
