import json
import qrcode
import io
from os.path import exists
from datetime import date

pathToJSON = "./data.json"

dateString = date.today().strftime("%m-%d-%Y")

if not exists(pathToJSON):
    f = open(pathToJSON, "a")
    f.write("{\"members\":[],\"member-count\": 0}")
    f.close()


def read_json(filename=pathToJSON):
    with open(filename,) as file:
        return json.load(file)


def write_json(new_data, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["members"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def increment_member_count(filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["member-count"] = file_data["member-count"]+1
        file.seek(0)
        json.dump(file_data, file, indent=4)


def print_QR_code(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


while True:
    task = input(
        "What would you like to do? Type 'add' to add a member, 'get qr' to get a member's QR code, or 'quit' to quit!")
    if task == "add":
        name = input("What's the name of the user you'd like to add?")
        idnum = read_json()["member-count"]
        write_json({"id": idnum,
                    "name": name,
                    "days-attended": {

                    }}
                   )
        increment_member_count()
        print("Successfully added " + name +
              " as ID #" + str(idnum) + ". \nQR code:")
        print_QR_code(idnum)

    elif task == "get qr":
        name = input("Please type the member's full name")
        memberJSON = read_json()
        for member in memberJSON["members"]:
            if member["name"] == name:
                print_QR_code(member["id"])
    elif task == "quit":
        break
    else:
        print("Invalid Input")
