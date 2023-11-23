import socket
import json
import pandas as pd
import time

def send_data_over_socket(file_path, host='127.0.0.1', port=9999, chunk_size=2):
    # Create a new socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a specific address and port
    s.bind((host, port))
    # Enable the server to accept connections
    s.listen(1)
    print(f"Listening for connections on {host}:{port}")
    
    # Wait for an incoming connection
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    
    last_sent_index = 0
    try:
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            # skip the lines that were already sent
            for _ in range(last_sent_index):
                next(file)
            
            records = []
            for line in file:
                # Load JSON data from each line
                records.append(json.loads(line))
                # If the number of records reaches the chunk size
                if len(records) == chunk_size:
                    # Convert the list of records to a DataFrame
                    chunk = pd.DataFrame(records)
                    print(chunk)
                    # Convert each record to JSON and send it over the socket
                    for record in chunk.to_dict(orient='records'):
                        serialize_data = json.dumps(record).encode('utf-8')
                        conn.send(serialize_data + b'\n')
                        # Wait for 5 seconds before sending the next record
                        time.sleep(5)
                        last_sent_index += 1
                    
                    records = []
    # Handle the case where the client disconnects prematurely
    except (BrokenPipeError, ConnectionResetError):
        print('Client disconnected.')
    finally:
        # Close the connection
        conn.close()
        print('Connection closed')

if __name__ == '__main__':
    # Call the function with the path to the JSON file
    send_data_over_socket("datasets/yelp_academic_dataset_review.json")
