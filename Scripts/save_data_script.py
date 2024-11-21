import json
import os
import time
from web3 import Web3
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load your trained model
model = load_model('C:/Users/phama/Downloads/Vaida_aimfall2024/CNN Model/real_vs_fake_vgg16_model.keras')

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Contract details
contract_address = "0x2763F5c622B6d44D646E7D58dEF3bC9309c29f95"  # Replace with your contract's address on Ganache
compiled_contract_path = "../Smart Contract/build/contracts/ProductAuth.json"

# Load contract ABI and bytecode
with open(compiled_contract_path, "r") as file:
    contract_json = json.load(file)
    contract_abi = contract_json["abi"]

# Load the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Output file path in CNN Model directory
output_file_path = "../CNN Model/product_data.json"

# Function to load and preprocess the input image
def load_and_preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict whether the image is Real or Fake
def predict_image(img_path):
    preprocessed_image = load_and_preprocess_image(img_path)
    prediction = model.predict(preprocessed_image)
    return prediction[0][0] > 0.5  # Returns True if "Real", False if "Fake"

# Function to handle event data and save it to a file
def handle_event(event):
    product_id = event['args']['productId']
    buyer = event['args']['buyer']
    seller = event['args']['seller']
    price = event['args']['price']
    image_hash = event['args']['imageHash']  # Capture image hash
    
    # Fetch image file based on hash (assuming you have a mapping of imageHash to path)
    img_path = f"../images/{image_hash}.jpg"  # Adjust to your actual image storage

    # Pass the image to the model
    is_real = predict_image(img_path)
    print(f"The product is {'Real' if is_real else 'Fake'} based on model prediction.")
    
    # Write data to JSON
    product_data = {
        "productId": product_id,
        "buyer": buyer,
        "seller": seller,
        "price": price,
        "is_real": is_real
    }
    with open(output_file_path, "w") as file:
        json.dump(product_data, file, indent=4)

    print(f"Data for product {product_id} saved to {output_file_path}")

# Set up event filter for ProductPurchased
event_filter = contract.events.ProductPurchased.create_filter(from_block='latest')

print("Listening for ProductPurchased events...")
while True:
    for event in event_filter.get_new_entries():
        handle_event(event)
    time.sleep(2)
