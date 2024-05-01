import google.generativeai as palm
import requests
# aai.settings.api_key = "bb7da29b06c343939583e1f59f6ffb3d"
API_KEY = "AIzaSyDG5rub57fdJ47Dog7b6zsrSfdoiX8yl9c"
palm.configure(api_key=API_KEY)
model = palm.GenerativeModel('gemini-pro')

response = model.generate_content("Please provide a list of the most influential people in the world.")

print(response.text)