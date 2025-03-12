import base64

import streamlit as st
import plotly.express as px
from backend import get_data


# Add background image
def set_background(image_url):
    with open(image_url, "rb") as file:  # read data into binnary from
        encode_string = base64.b64encode(file.read()).decode()  # binnary to convert base64 then bas64 decode as string
    st.markdown(
        f"""
        <style>
        .stApp {{
        background-image: url("data:png;base64,{encode_string}");
        background-size:cover;
        background-position: center;
        background-attachment: fixed;
    }}
        </style>

""",
        unsafe_allow_html=True
    )


set_background("7280763.png")


# Convert wind direction from degrees to compass directions
def get_wind_direction(deg):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(deg / 45) % 8
    return directions[idx]

try:
    # Add title,text input,slider,selectbox and subhead er
    st.title("Weather Forcast for the Next Days")
    place = st.text_input("Place:")
    days = st.slider("Forcast Days", min_value=1, max_value=5
                     , help="Select the number of forecasted days")
    option = st.selectbox("Select data to view", ("Temperature", "Sky", "Humidity", "Wind-speed"))

    st.subheader(f"{option} for the next {days} days in {place}")

    if place:
        # Get the temperature/sky data
        filtered_data = get_data(place, days)

        # Create a temperature plot
        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperature = [temperature - 273 for temperature in temperatures]
            Dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=Dates, y=temperature, labels={"x": "Dates", "y": "Temperatures (C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            # define day and night images
            images = {
                "Clear": {"day": "images/clear.png", "night": "images/night.png"},
                "Clouds": {"day": "images/cloud.png", "night": "images/cloudy-night.png"},
                "Rain": {"day": "images/rain.png", "night": "images/rainy.png"},
                "Snow": {"day": "images/snow.png", "night": "images/snow_night.png"},
            }
            # Extract weather condition and timestamps
            sky_conditons = [dict["weather"][0]["main"] for dict in filtered_data]
            timesstamps = [dict["dt_txt"] for dict in filtered_data]

            # Determine if it's day or night
            images_path = []
            for i, condition in enumerate(sky_conditons):
                hour = int(timesstamps[i].split(" ")[1].split(":")[0])  # Extract hour
                time_of_day = "day" if 6 <= hour < 18 else "night"
                images_path.append(images[condition][time_of_day])

            st.image(images_path, width=115)



        elif option == "Humidity":
            humidity = [dict["main"]["humidity"] for dict in filtered_data]
            Dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.bar(x=Dates, y=humidity, labels={"x": "Dates", "y": "Humidity"},
                            color_discrete_sequence=["#FF5733"])
            st.plotly_chart(figure)
        elif option == "Wind-speed":
            wind_speed = [dict['wind']['speed'] for dict in filtered_data]
            wind_Speed = [i * 3.6 for i in wind_speed] # convert m/s to km/h
            wind_deg = [get_wind_direction(dict['wind']['deg']) for dict in filtered_data]
            ploat = px.bar_polar(r=wind_Speed, theta=wind_deg, title="wind speed & Direction ")
            st.plotly_chart(ploat)
        if option == "Wind-speed":
            wind_speed = [dict['wind']['speed'] for dict in filtered_data]
            wind_Speed = [i * 3.6 for i in wind_speed]  # convert m/s to km/h
            Dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.scatter(x=Dates, y=wind_Speed, labels={"x": "Dates", "y": "wind-speed"},
                                color_discrete_sequence=["#FF5733"])
            st.plotly_chart(figure)
except KeyError:
    st.write("Please check spelling your city name or  that city  not found try another city")
