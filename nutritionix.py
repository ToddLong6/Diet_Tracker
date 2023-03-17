import requests
# from dotenv import load_dotenv
import os

# load_dotenv()

API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")


def get_food(eat):
	url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

	headers = {
		"x-app-id": APP_ID,
		"x-app-key": API_KEY,
		"x-remote-user-id": "0",
		"Content-Type": "application/json"
	}
	body = {
		"query": eat,
		"timezone": "US/Eastern"
	}

	response = requests.post(url=url, json=body, headers=headers)
	result = response.json()

	intake_item = []

	for key, value in result.items():
		for name in value:
			# print(f'{name["food_name"].title()} has Sugar: {name["nf_sugars"]} and Calories: {name["nf_calories"]}')
			item = name["food_name"].title()
			sugar = name["nf_sugars"]
			calories = name["nf_calories"]
			intake_item.append([item, sugar, calories])
	# print(f"\n{result}\n")
	return intake_item


def get_exercise(exercise, gender, kg, cm, age):
	exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

	headers = {
		"x-app-id": APP_ID,
		"x-app-key": API_KEY,
		"Content-Type": "application/json"
	}

	parameters = {
		"query": exercise,
		"gender": gender,
		"weight_kg": kg,
		"height_cm": cm,
		"age": age
	}

	response = requests.post(exercise_endpoint, json=parameters, headers=headers)
	result = response.json()

	workout_item = []

	for key, value in result.items():
		for name in value:
			# print(f'You {name["user_input"].title()} and the Duration: {name["duration_min"]} and you Burned {name["nf_calories"]} Calories')
			item = name["name"].title()
			duration = name["duration_min"]
			burned = name["nf_calories"]
			workout_item.append([item, duration, burned])
	# print(f"\n{result}")
	return workout_item

# test run tryouts
# if __name__ == '__main__':
# 	eat = "I eat 2 hotdog and a bag of chips"
# 	get_food(eat)
# 	exercise = "I walked 5 mile in 2 hour and did 50 push up in 3 minute"
# 	get_exercise(exercise, gender="male", kg=(213 / 2.2), cm=66, age=40)
