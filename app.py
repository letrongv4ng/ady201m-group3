import streamlit as st
import requests
import pandas as pd
from matplotlib import pyplot as plt

# Page config
st.set_page_config(
    page_title="Lab 2 - Open-Meteo Weather GUI",
    layout="wide"
)

# CSS 
st.markdown("""
<style>
    .main {
        background-color: white;
        color: black;
        text-align: center;
    }
    .stSelectbox > div > div {
        background-color: white;
        color: black;
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: black;
        border: 1px solid black;
    }
    .stButton > button {
        background-color: white;
        color: black;
        border: 1px solid black;
        margin: 0 auto;
        display: block;
    }
    .stButton > button:hover {
        background-color: #f0f0f0;
        color: black;
    }
    .stDownloadButton > button {
        background-color: white;
        color: black;
        border: 1px solid black;
        margin: 0 auto;
        display: block;
    }
    .stDownloadButton > button:hover {
        background-color: #f0f0f0;
        color: black;
    }
    h1, h2, h3 {
        text-align: center;
    }
    .stDataFrame {
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

def get_coordinates_from_city(city_name):
    """Using geocoding to get city location"""
    try:
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        response = requests.get(geocoding_url)
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            return result['latitude'], result['longitude'], result['name']
        else:
            return None, None, None
    except Exception as e:
        st.error(f"Error while getting coordinates: {str(e)}")
        return None, None, None

def fetch_weather_data(latitude, longitude, metrics):
    """Open-Meteo API calling"""
    try:
        # Regex URL
        base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Map metrics to API
        daily_params = []
        if "Temperature" in metrics:
            daily_params.extend(["temperature_2m_max", "temperature_2m_min"])
        if "Precipitation" in metrics:
            daily_params.append("precipitation_sum")
        if "Wind" in metrics:
            daily_params.append("wind_speed_10m_max")
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ",".join(daily_params),
            "timezone": "auto",
            "forecast_days": 7
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        st.error(f"Error while getting weather info: {str(e)}")
        return None

def process_weather_data(data, metrics):
    """Resolve raw data to dataframe"""
    if not data or 'daily' not in data:
        return None
    
    daily_data = data['daily']
    df_data = {'Date': daily_data['time']}
    
    # Add metrics
    if "Temperature" in metrics:
        if 'temperature_2m_max' in daily_data:
            df_data['Max Temp (°C)'] = daily_data['temperature_2m_max']
        if 'temperature_2m_min' in daily_data:
            df_data['Min Temp (°C)'] = daily_data['temperature_2m_min']
    
    if "Precipitation" in metrics:
        if 'precipitation_sum' in daily_data:
            df_data['Precipitation (mm)'] = daily_data['precipitation_sum']
    
    if "Wind" in metrics:
        if 'wind_speed_10m_max' in daily_data:
            df_data['Max Wind Speed (km/h)'] = daily_data['wind_speed_10m_max']
    
    df = pd.DataFrame(df_data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def create_line_chart(df, metrics):
    if df is None or df.empty:
        return None

    fig, ax = plt.subplots(figsize=(16, 8))

    # Set style
    plt.style.use('default')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Different line styles and markers
    line_styles = [
        {'linestyle': '-', 'marker': 'o', 'markersize': 5},
        {'linestyle': '--', 'marker': 's', 'markersize': 4},
        {'linestyle': '-.', 'marker': '^', 'markersize': 5},
        {'linestyle': ':', 'marker': 'D', 'markersize': 4},
        {'linestyle': '-', 'marker': 'v', 'markersize': 5},
    ]

    # Plot data
    style_idx = 0
    for col in df.columns:
        if col != 'Date':
            style = line_styles[style_idx % len(line_styles)]
            ax.plot(df['Date'], df[col],
                   color='black',
                   linewidth=2,
                   label=col,
                   linestyle=style['linestyle'],
                   marker=style['marker'],
                   markersize=style['markersize'],
                   markerfacecolor='white',
                   markeredgecolor='black',
                   markeredgewidth=1.5)
            style_idx += 1

    # Styling
    ax.set_xlabel('Date', fontsize=20, color='black', fontweight='bold')
    ax.set_ylabel('Values', fontsize=20, color='black', fontweight='bold')
    ax.set_title('Weather Forecast', fontsize=16, color='black', fontweight='bold', pad=20)

    # Remove grid and spines
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)

    # Styling legend borders
    if len(df.columns) > 2:
        legend = ax.legend(
            frameon=True,
            loc='center left',
            bbox_to_anchor=(1.02, 0.5),
            fancybox=False,
            shadow=False,
            framealpha=1,
            edgecolor='black'
        )
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_linewidth(1)

    # Rotate x-axis labels
    plt.xticks(rotation=0, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    return fig

# Main app
def main():
    st.title("Lab 2&3 ")
    st.markdown("**Present by group []: Le Hung, Quang Minh and Manh Chung**")
    # Input section
    st.header("Input Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        input_type = st.radio("Choose input method:", ["City Name", "Coordinates"])
        
        if input_type == "City Name":
            city_input = st.text_input("Enter city name:", value="Hanoi", placeholder="e.g., Hanoi, Vietnam")
            latitude, longitude = None, None
        else:
            latitude = st.number_input("Latitude:", value=21.0285, format="%.4f")
            longitude = st.number_input("Longitude:", value=105.8542, format="%.4f")
            city_input = None
    
    with col2:
        metrics = st.multiselect(
            "Select metrics to display:",
            ["Temperature", "Precipitation", "Wind"],
            default=["Temperature", "Precipitation", "Wind"]
        )
    
    # Fetch data button
    if st.button("Fetch Weather Data", type="primary"):
        if not metrics:
            st.error("Please select at least one metric to display.")
            return
        
        # Get coordinates
        if input_type == "City Name" and city_input:
            with st.spinner("Getting coordinates..."):
                lat, lon, found_city_name = get_coordinates_from_city(city_input)
                if lat is None:
                    st.error(f"Could not find coordinates for '{city_input}'. Please try another city.")
                    return
                latitude, longitude = lat, lon
                # Use original input instead of API result to avoid wrong names
                city_name = city_input  # Keep user input as city name
                st.success(f"Found: {found_city_name} ({lat:.4f}, {lon:.4f})")
                st.info(f"Using city name: {city_name}")
        
        if latitude is None or longitude is None:
            st.error("Please provide valid coordinates or city name.")
            return
        
        # Fetch weather data
        with st.spinner("Fetching weather data..."):
            weather_data = fetch_weather_data(latitude, longitude, metrics)
            
            if weather_data:
                # Process data
                df = process_weather_data(weather_data, metrics)
                
                if df is not None and not df.empty:
                    st.success("Weather data fetched successfully!")
                    # Display data table
                    st.header("Weather Forecast Data")
                    st.dataframe(df, use_container_width=True)

                    # Display chart
                    st.header("Weather Forecast Chart")
                    fig = create_line_chart(df, metrics)
                    if fig:
                        st.pyplot(fig)

                    # Display location info
                    st.info(f"Location: {latitude:.4f}, {longitude:.4f}")
                    st.info(f"Timezone: {weather_data.get('timezone', 'Unknown')}")

if __name__ == "__main__":
    main()
