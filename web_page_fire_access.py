import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("private_web_page.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://mywebpage-29697-default-rtdb.firebaseio.com/"
})

# Reference to the commands node
ref = db.reference("/commands")

# Fetch all command entries
commands_dict = ref.get()

# Initialize an empty list to store commands in order
commands_list = []

if commands_dict:
    # Iterate over the dictionary in the order of insertion
    for key, value in commands_dict.items():
        for sub_key, sub_value in value.items():
            # Append the command to the list
            commands_list.append(sub_value['command'])

    # Print the commands in order
    for i, command in enumerate(commands_list, start=1):
        print(f"Command {i}: {command}")
else:
    print("No commands found.")
