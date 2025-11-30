import requests
import json

# Task 3 – Extract and Display Specific Weather Data

def get_weather_with_error_handling(city_name):
    api_key = "43515020b975430fef86ec954065d6bc"  # your API key
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(base_url, timeout=5)

        if response.status_code != 200:
            print("Error: Could not connect to API. Check your API key, city name, or network connection.")
            print(f"Status code: {response.status_code}")
            try:
                print("Response:", response.json())
            except Exception:
                print("No JSON body available.")
            return None

        data = response.json()
        return data

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please check your internet connection and try again.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Network problem occurred. Please check your internet connection.")
        return None

    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return None


def show_weather_details(city_name):
    data = get_weather_with_error_handling(city_name)

    if data is None:
        print("No data received from API.")
        return

    # Some APIs return cod as int or string, handle both safely
    if str(data.get("cod", "")) != "200":
        print("Error from API:", data.get("message", "Unknown error"))
        return

    # Extract required fields
    city = data.get("name", "Unknown")
    main = data.get("main", {})
    weather_list = data.get("weather", [])

    temp = main.get("temp", "N/A")
    humidity = main.get("humidity", "N/A")
    description = weather_list[0].get("description", "N/A") if weather_list else "N/A"

    # Print in user-friendly format
    print("\n--- Weather Details ---")
    print(f"City       : {city}")
    print(f"Temperature: {temp} °C")
    print(f"Humidity   : {humidity} %")
    print(f"Weather    : {description}")
    print("------------------------\n")


if __name__ == "__main__":
    city = input("Enter city name: ")
    show_weather_details(city)
