import json
import os

if __name__ == "__main__":
    with open(os.path.join("dao", "properties.json"), "r") as file:
        data = json.load(file)

    print(data)
