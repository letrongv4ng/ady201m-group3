import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def create_interactive_chart(df, metrics):
    """Create interactive plotly chart"""
    if df is None or df.empty:
        return None

    fig = go.Figure()
    
    # Color palette - simple and clean
    colors = ['#000000', '#666666', '#333333', '#999999', '#555555']
    
    # Line styles
    line_styles = ['solid', 'dash', 'dashdot', 'dot']
    
    color_idx = 0
    for col in df.columns:
        if col != 'Date':
            line_style = line_styles[color_idx % len(line_styles)]
            color = colors[color_idx % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[col],
                mode='lines+markers',
                name=col,
                line=dict(
                    color=color,
                    width=2,
                    dash=line_style
                ),
                marker=dict(
                    color='white',
                    size=6,
                    line=dict(
                        color=color,
                        width=2
                    )
                ),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                              'Date: %{x}<br>' +
                              'Value: %{y}<br>' +
                              '<extra></extra>'
            ))
            color_idx += 1
    
    # Update layout - keep it simple and clean
    fig.update_layout(
        title={
            'text': 'Weather Forecast',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'black'}
        },
        xaxis_title='Date',
        yaxis_title='Values',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        showlegend=True,
        legend=dict(
            bgcolor='white',
            bordercolor='black',
            borderwidth=1,
            font=dict(color='black')
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='black',
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='black',
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        height=500
    )
    
    return fig

# Main app
def main():
    st.title("EasyWeather")
    st.subheader("**Present by group [3]: Le Hung, Quang Minh and Manh Chung**")
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
            default=[]
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

                    # Display interactive chart
                    st.header("Weather Forecast Chart")
                    fig = create_interactive_chart(df, metrics)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                    # Display location info
                    st.info(f"Location: {latitude:.4f}, {longitude:.4f}")
                    st.info(f"Timezone: {weather_data.get('timezone', 'Unknown')}")

if __name__ == "__main__":
    main()