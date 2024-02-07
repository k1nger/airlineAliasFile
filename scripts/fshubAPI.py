import requests

url = "https://fshub.io/api/v3/airline"
result_array = []

headers = {
    "Content-Type": "application/json",
    # "x-pilot-token": INSERT API TOKEN HERE
}

def get_airline_data(cursor):
    params = {
        "limit": 100,
        "cursor": cursor
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        airlines = data.get("data", [])

        for airline in airlines:
            name = airline.get("name")
            abbr = airline.get("abbr")

            result_array.append({"abbr": abbr, "name": name})

        return data.get("meta", {}).get("cursor", {}).get("next")

    else:
        print(f"Error: {response.status_code}")
        return None

# Initial call with cursor set to 0
cursor = 0

while cursor is not None:
    cursor = get_airline_data(cursor)

# Save results to a text file
output_file = "./airline_results.txt"

with open(output_file, "w") as file:
    for result in result_array:
        try:
            file.write(f"{result.get('abbr')} {result.get('name')}\n")
        except UnicodeEncodeError as e:
            print(f"Name: {result.get('name')}, Abbr: {result.get('abbr')}")
            continue
   

print(f"Results saved to {output_file}")
