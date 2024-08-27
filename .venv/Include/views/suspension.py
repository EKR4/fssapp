import streamlit as st
import numpy as np
import plotly.graph_objs as go
import pandas as pd

st.title("Suspension App")
# Constants and Variables (initial values)
Track_Width = 1.168
Wheel_Base = 1.72
Jounce = 0.05
Roll_Height = 0.127
Cog_Height = 0.325
Roll_Distance = 0.198
Weight_Rear_Ratio = 0.55
Weight_Front_Ratio = 0.45
Weight = 380
Cornering_Speed = 13.88
Turn_Radius = 6.0
g = 9.8
Kt = 38.608
Cg_Rear = 0.72

# Calculate centripetal acceleration
def calculate_centripetal_acceleration(cornering_speed, turn_radius):
    A = pow(cornering_speed, 2) / (turn_radius * g)
    return A

# Create interactive widgets
cornering_speed_slider = st.sidebar.slider('Cornering Speed', 10.0, 20.0, Cornering_Speed, step=0.1)
turn_radius_slider = st.sidebar.slider('Turn Radius', 1.0, 10.0, Turn_Radius, step=0.1)

# Calculate and display centripetal acceleration
A = calculate_centripetal_acceleration(cornering_speed_slider, turn_radius_slider)
st.write(f"Centripetal Acceleration: {A:.2f}")

# Calculate weight shift during turning
def calculate_weight_shift(track_width, roll_distance, weight, weight_front_ratio, weight_rear_ratio):
    Kr = weight_rear_ratio * Kt
    Kf = weight_front_ratio * Kt
    A = calculate_centripetal_acceleration(cornering_speed_slider, turn_radius_slider)
    Wf = A * (weight / track_width) * (roll_distance * Kf) / (Kt + Cg_Rear * Roll_Height)
    Wr = A * (weight / track_width) * (roll_distance * Kr) / (Kt + Cg_Rear * Roll_Height)
    return Wf, Wr

# Create interactive widgets
track_width_slider = st.sidebar.slider('Track Width', 0.5, 2.0, Track_Width, step=0.1)
roll_distance_slider = st.sidebar.slider('Roll Distance', 0.05, 0.5, Roll_Distance, step=0.01)
weight_slider = st.sidebar.slider('Weight', 100, 1000, Weight, step=10)
weight_front_ratio_slider = st.sidebar.slider('Front Weight Ratio', 0.1, 1.0, Weight_Front_Ratio, step=0.1)
weight_rear_ratio_slider = st.sidebar.slider('Rear Weight Ratio', 0.1, 1.0, Weight_Rear_Ratio, step=0.1)

# Calculate and display weight shift
Wf, Wr = calculate_weight_shift(track_width_slider, roll_distance_slider, weight_slider, weight_front_ratio_slider, weight_rear_ratio_slider)
st.write(f"Front Weight Shift: {Wf:.2f}")
st.write(f"Rear Weight Shift: {Wr:.2f}")

# Create a function to generate the simulation data
def simulate_weight_shift(track_width, roll_distance, weight, weight_front_ratio, weight_rear_ratio, steps=100):
    speeds = np.linspace(10, 20, steps)
    radii = np.linspace(1, 10, steps)
    Wf_values = []
    Wr_values = []
    for speed, radius in zip(speeds, radii):
        Wf, Wr = calculate_weight_shift(track_width, roll_distance, weight, weight_front_ratio, weight_rear_ratio)
        Wf_values.append(Wf)
        Wr_values.append(Wr)
    return speeds, Wf_values, Wr_values

# Create a function to generate the plot
def plot_weight_shift(track_width, roll_distance, weight, weight_front_ratio, weight_rear_ratio):
    speeds, Wf_values, Wr_values = simulate_weight_shift(track_width, roll_distance, weight, weight_front_ratio, weight_rear_ratio)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=speeds, y=Wf_values, mode='lines', name='Front Weight Shift'))
    fig.add_trace(go.Scatter(x=speeds, y=Wr_values, mode='lines', name='Rear Weight Shift'))
    fig.update_layout(title='Weight Shift During Turning',
                      xaxis_title='Cornering Speed (m/s)',
                      yaxis_title='Weight Shift (N)')
    return fig

# Display the plot
weight_shift_plot = plot_weight_shift(track_width_slider, roll_distance_slider, weight_slider, weight_front_ratio_slider, weight_rear_ratio_slider)
st.plotly_chart(weight_shift_plot)

# Create a function to generate the plot
def plot_centripetal_acceleration(cornering_speed, turn_radius):
    A = calculate_centripetal_acceleration(cornering_speed, turn_radius)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[cornering_speed], y=[A], mode='markers', name='Centripetal Acceleration'))
    fig.update_layout(title='Centripetal Acceleration vs Cornering Speed',
                      xaxis_title='Cornering Speed (m/s)',
                      yaxis_title='Centripetal Acceleration (m/s^2)')
    return fig

# Display the plot
centripetal_acceleration_plot = plot_centripetal_acceleration(cornering_speed_slider, turn_radius_slider)
st.plotly_chart(centripetal_acceleration_plot)

# Calculate lateral force
def calculate_lateral_force(weight, centripetal_acceleration):
    return weight * centripetal_acceleration

# Calculate longitudinal force
def calculate_longitudinal_force(weight, acceleration):
    return weight * acceleration

# Calculate tire slip angle
def calculate_tire_slip_angle(cornering_speed, turn_radius, wheel_base):
    return np.arctan(wheel_base / turn_radius) * (180 / np.pi)

# Display additional results
lateral_force = calculate_lateral_force(weight_slider, A)
st.write(f"Lateral Force: {lateral_force:.2f}")

longitudinal_force = calculate_longitudinal_force(weight_slider, A)
st.write(f"Longitudinal Force: {longitudinal_force:.2f}")

tire_slip_angle = calculate_tire_slip_angle(cornering_speed_slider, turn_radius_slider, Wheel_Base)
st.write(f"Tire Slip Angle: {tire_slip_angle:.2f}")

# Define the results DataFrame
results_df = pd.DataFrame(columns=['Cornering Speed', 'Turn Radius', 'Centripetal Acceleration', 'Lateral Force', 'Longitudinal Force', 'Tire Slip Angle'])

# Update additional values
def update_additional_values():
    A = calculate_centripetal_acceleration(cornering_speed_slider, turn_radius_slider)
    lateral_force = calculate_lateral_force(weight_slider, A)
    longitudinal_force = calculate_longitudinal_force(weight_slider, A)
    tire_slip_angle = calculate_tire_slip_angle(cornering_speed_slider, turn_radius_slider, Wheel_Base)
    
    st.write(f"Lateral Force: {lateral_force:.2f}")
    st.write(f"Longitudinal Force: {longitudinal_force:.2f}")
    st.write(f"Tire Slip Angle: {tire_slip_angle:.2f}")

# Create a function to generate the plot for lateral force
def plot_lateral_force(cornering_speed, turn_radius, weight):
    A = calculate_centripetal_acceleration(cornering_speed, turn_radius)
    lateral_force = calculate_lateral_force(weight, A)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[cornering_speed], y=[lateral_force], mode='markers', name='Lateral Force'))
    fig.update_layout(title='Lateral Force vs Cornering Speed',
                      xaxis_title='Cornering Speed (m/s)',
                      yaxis_title='Lateral Force (N)')
    return fig

# Display the plot for lateral force
lateral_force_plot = plot_lateral_force(cornering_speed_slider, turn_radius_slider, weight_slider)
st.plotly_chart(lateral_force_plot)

# Update the DataFrame with new values
def update_results_df():
    A = calculate_centripetal_acceleration(cornering_speed_slider, turn_radius_slider)
    lateral_force = calculate_lateral_force(weight_slider, A)
    longitudinal_force = calculate_longitudinal_force(weight_slider, A)
    tire_slip_angle = calculate_tire_slip_angle(cornering_speed_slider, turn_radius_slider, Wheel_Base)
    
    new_row = {
        'Cornering Speed': cornering_speed_slider,
        'Turn Radius': turn_radius_slider,
        'Centripetal Acceleration': A,
        'Lateral Force': lateral_force,
        'Longitudinal Force': longitudinal_force,
        'Tire Slip Angle': tire_slip_angle
    }
    results_df.loc[len(results_df)] = new_row
    st.write(results_df)

# Display the DataFrame
st.write(results_df)

# Display widgets
st.sidebar.title('FSS Suspension App')
cornering_speed_slider = st.sidebar.slider('Cornering Speed', 10.0, 20.0, Cornering_Speed, step=0.1, key='cornering_speed_slider', on_change=update_additional_values)
turn_radius_slider = st.sidebar.slider('Turn Radius', 1.0, 10.0, Turn_Radius, step=0.1, key='turn_radius_slider', on_change=update_additional_values)
track_width_slider = st.sidebar.slider('Track Width', 0.5, 2.0, Track_Width, step=0.1, key='track_width_slider', on_change=update_additional_values)
roll_distance_slider = st.sidebar.slider('Roll Distance', 0.05, 0.5, Roll_Distance, step=0.01, key='roll_distance_slider', on_change=update_additional_values)
weight_slider = st.sidebar.slider('Weight', 100, 1000, Weight, step=10, key='weight_slider', on_change=update_additional_values)
weight_front_ratio_slider = st.sidebar.slider('Front Weight Ratio', 0.1, 1.0, Weight_Front_Ratio, step=0.1, key='weight_front_ratio_slider', on_change=update_additional_values)
weight_rear_ratio_slider = st.sidebar.slider('Rear Weight Ratio', 0.1, 1.0, Weight_Rear_Ratio, step=0.1, key='weight_rear_ratio_slider', on_change=update_additional_values)

# Update the plots and DataFrame when sliders change
update_additional_values()
update_results_df()
