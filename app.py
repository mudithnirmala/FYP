import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
from script import run_optimization

# Set page configuration
st.set_page_config(page_title="Optimal Schedule", layout="wide")

# Define the CSV file paths
csv_file_shift = "shiftable_dataframe.csv"
csv_file_shed = "shedable_dataframe.csv"

# Check if the CSV file exists for shiftable loads
if os.path.isfile(csv_file_shift):
    df_shift = pd.read_csv(csv_file_shift)
else:
    df_shift = pd.DataFrame(columns=["load_name", "start", "end", "duration", "consumption"])

# Check if the CSV file exists for sheddable loads
if os.path.isfile(csv_file_shed):
    df_shed = pd.read_csv(csv_file_shed)
else:
    df_shed = pd.DataFrame(columns=["load_name", "start", "end", "penalty", "consumption"])


def app_layout():
    global df_shift, df_shed
    st.sidebar.title("Settings")

    # Inputs on the sidebar
    st.sidebar.subheader("Input Data Files")
    forecast_file = st.sidebar.file_uploader("Upload Forecast Data (CSV)", type="csv")
    tariff_file = st.sidebar.file_uploader("Upload Tariff Data (CSV)", type="csv")

    st.sidebar.subheader("Battery Parameters")
    battery_capacity = st.sidebar.number_input("Battery Capacity (kWh)", value=400)
    battery_state_0 = st.sidebar.number_input("Initial State of Charge (%)", value=50)

    st.sidebar.subheader("Time Settings")
    T = st.sidebar.number_input("Resolution/Time Period", value=24)

    st.sidebar.subheader('Load Input Interface')
    with st.sidebar.form("Shiftable Load Form"):
        st.sidebar.header('Shiftable Load')
        load_name_shift = st.sidebar.text_input('Enter the load name', key="shift_load_name")
        start_time_shift = st.sidebar.number_input('Enter the Starting Time', format="%i", key="shift_start_time")
        end_time_shift = st.sidebar.number_input('Enter the Ending Time', format="%i", key="shift_end_time")
        duration_shift = st.sidebar.number_input('Enter the Time duration', format="%i", key="shift_duration")
        power_consumption_shift = st.sidebar.number_input('Enter the Power Consumption', format="%i", key="shift_power_consumption")

        add_shift = st.form_submit_button('Add to Shiftable')
        delete_shift = st.form_submit_button('Delete Data from Shiftable')

    with st.sidebar.form("Sheddable Load Form"):
        st.sidebar.header('Sheddable Load')
        load_name_shed = st.sidebar.text_input('Enter the load name', key="shed_load_name")
        start_time_shed = st.sidebar.number_input('Enter the Starting Time', format="%i", key="shed_start_time")
        end_time_shed = st.sidebar.number_input('Enter the Ending Time', format="%i", key="shed_end_time")
        penalty_shed = st.sidebar.number_input('Enter the Penalty', format="%i", key="shed_penalty")
        power_consumption_shed = st.sidebar.number_input('Enter the Power Consumption', format="%i", key="shed_power_consumption")

        add_shed = st.form_submit_button('Add to Sheddable')
        delete_shed = st.form_submit_button('Delete Data from Sheddable')

    if add_shift:
        df_shift.loc[len(df_shift)] = [load_name_shift, int(start_time_shift), int(end_time_shift), int(duration_shift), int(power_consumption_shift)]
        df_shift.to_csv(csv_file_shift, index=False)

    if delete_shift:
        df_shift = pd.DataFrame(columns=["load_name", "start", "end", "duration", "consumption"])
        df_shift.to_csv(csv_file_shift, index=False)

    if add_shed:
        df_shed.loc[len(df_shed)] = [load_name_shed, int(start_time_shed), int(end_time_shed), int(penalty_shed), int(power_consumption_shed)]
        df_shed.to_csv(csv_file_shed, index=False)

    if delete_shed:
        df_shed = pd.DataFrame(columns=["load_name", "start", "end", "penalty", "consumption"])
        df_shed.to_csv(csv_file_shed, index=False)

    st.header('Shiftable Loads')
    st.table(df_shift)

    st.header('Sheddable Loads')
    st.table(df_shed)

    if forecast_file is not None:
        st.header("Forecast Data")
        forecast_df = pd.read_csv(forecast_file, parse_dates=['Timestamp'])
        st.dataframe(forecast_df.head())

        if "Timestamp" in forecast_df.columns and "Solar Forecasting" in forecast_df.columns and "Actual Solar" in forecast_df.columns:
            date_to_show = st.date_input("Select a date to display data", value=datetime.now().date() - timedelta(days=1))
            df_last_day = forecast_df[forecast_df['Timestamp'].dt.date == date_to_show]

            plot_solar(df_last_day)
            plot_building(df_last_day)
        else:
            st.error("The CSV file must have 'Timestamp', 'Solar Forecasting', and 'Actual Solar' columns.")

    if tariff_file is not None:
        st.header("Tariff Data")
        tariff_df = pd.read_csv(tariff_file, parse_dates=['Time'])
        st.dataframe(tariff_df.head())

        if "Time" in tariff_df.columns and "Rates" in tariff_df.columns:
            plot_tariff(tariff_df)
        else:
            st.error("The Tariff CSV file must have 'Time' and 'Rates' columns.")

    if st.button("Run Optimization"):
        st.header("Optimization Results")
        solar_forecasting, actual_solar, building_forecasting, actual_building, electricity_tariff = [], [], [], [], []
        shiftable_loads, sheddable_loads = [], []

        battery_schedule_opt = run_optimization()
        #print("print",battery_schedule_opt)
        show_output(battery_schedule_opt["battery_schedule"])


def plot_solar(df):
    fig = px.line(df, x='Timestamp', y=['Solar Forecasting', 'Actual Solar'], title='Solar Forecasting and Actual Solar Power')
    st.plotly_chart(fig)


def plot_building(df):
    fig = px.line(df, x='Timestamp', y=['Building Forecasting', 'Actual Building'], title='Building Load Forecasting and Actual Building Load')
    st.plotly_chart(fig)


def plot_tariff(df):
    fig = px.line(df, x='Time', y='Rates', title='Tariff Rates over Time')
    st.plotly_chart(fig)



def plot_dispatch(schedule):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(schedule))), y=schedule, mode='lines', name='Battery Dispatch Schedule'))
    fig.update_layout(title='Battery Dispatch Schedule', xaxis_title='Hour of the Day', yaxis_title='Battery Power (kW)')
    st.plotly_chart(fig)


#battery_soc = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

def show_output(schedule):
    c_rates = [rate*5 for rate in schedule]  # Convert power from kW to kWh
    soc_0 = st.sidebar.number_input("Initial State of Charge (%)", value=50, min_value=0, max_value=100)   # Initial SOC as a fraction
    battery_soc = [sum(c_rates[:i+1]) + soc_0 for i in range(len(c_rates))]
    soc_df = pd.DataFrame({'Hour of Day': range(len(schedule)), 'Battery SOC': battery_soc})
    print("babbajdsf",battery_soc)

    # Plot SOC level vs. hour of the day
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=soc_df['Hour of Day'], y=soc_df['Battery SOC'], mode='lines', name='Battery SOC'))
    fig.update_layout(title='Battery State of Charge (SOC) vs. Hour of the Day', xaxis_title='Hour of the Day', yaxis_title='SOC')
    st.plotly_chart(fig)

    # Plot battery dispatch schedule
    plot_dispatch(schedule)


def main():
    st.title("Optimal Schedule")
    app_layout()


if __name__ == "__main__":
    main()
