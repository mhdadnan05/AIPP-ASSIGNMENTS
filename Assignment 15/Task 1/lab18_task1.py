import requests
import json

# Task 1 – Weather API (No Error Handling)

def get_weather_no_error_handling(city_name):
    api_key = "43515020b975430fef86ec954065d6bc"  # your API key
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(base_url)
    data = response.json()

    print(json.dumps(data, indent=4))
    return data


if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather_no_error_handling(city)
