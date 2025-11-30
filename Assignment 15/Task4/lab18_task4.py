import requests
import json

# Task 4 – Build a Function with Parameters (City Name)

def get_city_weather(city_name: str):
    """
    Fetches weather data for a given city.
    Returns a dictionary like:
    {
        "city": ...,
        "temp": ...,
        "humidity": ...,
        "weather": ...
    }
    or None if any error occurs.
    """
    api_key = "43515020b975430fef86ec954065d6bc"  # your API key
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(base_url, timeout=5)

        # If HTTP status is not 200, handle it
        if response.status_code != 200:
            print("Error: Could not connect to API. Check your API key, city name, or network connection.")
            print(f"Status code: {response.status_code}")
            try:
                print("Response:", response.json())
            except Exception:
                print("No JSON body available.")
            return None

        data = response.json()

        # Handle invalid city (like xyz123)
        if str(data.get("cod", "")) == "404":
            print("Error: City not found. Please enter a valid city.")
            print("Message from API:", data.get("message", "No message"))
            return None

        # Extract useful data
        city = data.get("name", city_name)
        main = data.get("main", {})
        weather_list = data.get("weather", [])

        temp = main.get("temp", None)
        humidity = main.get("humidity", None)
        description = weather_list[0].get("description", "") if weather_list else ""

        # Build and return dictionary
        result = {
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "weather": description
        }

        return result

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please check your internet connection and try again.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Network problem occurred. Please check your internet connection.")
        return None

    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None


if __name__ == "__main__":
    city_input = input("Enter city name: ")
    result = get_city_weather(city_input)

    if result is None:
        print("Could not retrieve weather data.")
    else:
        print("\n--- Weather Details ---")
        print(f"City       : {result['city']}")
        print(f"Temperature: {result['temp']} °C")
        print(f"Humidity   : {result['humidity']} %")
        print(f"Weather    : {result['weather']}")
        print("------------------------\n")
