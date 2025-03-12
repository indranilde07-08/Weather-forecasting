import requests

API_KEY = "35eed2c976138f3a4d414906aa78577d"


def get_data(place, days=None, label=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    filtered_data = filtered_data[:8*days]
    if label == "Temperature":
        filtered_data =  [dict["main"]["temp"]for dict in filtered_data]
    elif label == "Sky":
        filtered_data = [dict["weather"][0]["main"]for dict in filtered_data]
    return filtered_data





if __name__ == "__main__":
    print(get_data(place="mundra",days=3,label="Temperature"))
