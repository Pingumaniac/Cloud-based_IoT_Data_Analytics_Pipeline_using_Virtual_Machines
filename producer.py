import os
import time
import json
from kafka import KafkaProducer
from PIL import Image
import io
import base64
import uuid
import random
from torchvision import datasets, transforms
import numpy as np

cifar10 = datasets.CIFAR10(root='./data', train=True, download=True)
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def add_noise(image):
    img_array = np.array(image)

    mean = 0
    stddev = 1
    noise = np.random.normal(mean, stddev, img_array.shape).astype(np.uint8)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)

    return Image.fromarray(noisy_img)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks=1
)

for i in range(100):
    index = random.randint(0, len(cifar10) - 1)
    image, label = cifar10[index]
    
    noisy_image = add_noise(image)
    
    message = {
        "ID": str(uuid.uuid4()),
        "GroundTruth": classes[label],
        "Data": encode_image(noisy_image)
    }

    producer.send("image_data", value=message)
    producer.flush()
    
    print(f"Sent image {i+1}: {classes[label]}")
    time.sleep(1)

producer.close()
