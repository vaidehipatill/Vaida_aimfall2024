import json
import os
import time
from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Contract details
contract_address = ""  # Replace with your contract's address on Ganache
contract_abi = [
    # Custom ABI
]

# Load the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Output file path in CNN Model directory
output_file_path = "../CNN Model/product_data.json"

# Function to handle event data and save it to a file
def handle_event(event):
    # Extract data from the ProductPurchased event
    product_id = event['args']['productId']
    buyer = event['args']['buyer']
    seller = event['args']['seller']
    price = event['args']['price']

    # Prepare data to be saved
    product_data = {
        "productId": product_id,
        "buyer": buyer,
        "seller": seller,
        "price": price
    }

    # Write data to a JSON file in the CNN Model directory
    with open(output_file_path, "w") as file:
        json.dump(product_data, file, indent=4)

    print(f"Data for product {product_id} saved to {output_file_path}")


# Set up an event filter to listen for the "ProductPurchased" event
event_filter = contract.events.ProductPurchased.create_filter(from_block='latest')

# Main loop to poll for new events
print("Listening for ProductPurchased events...")
while True:
    for event in event_filter.get_new_entries():
        handle_event(event)
    # Poll every 2 seconds
    time.sleep(2)
