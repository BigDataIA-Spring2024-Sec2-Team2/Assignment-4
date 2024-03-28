import os 

def print_keys(**kwargs):
    print("-----------------------------")
    print(f"Your Secret key is: {os.getenv('SAMPLE_ENV')}") # Donot print this anywhere, this is just for demo
    print("-----------------------------")