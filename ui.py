import streamlit as st
import requests

st.set_page_config(page_title="Solar Power Plant Planner", layout='centered')
st.header("Solar Power Plant Planner")

# Input form for solar power plant details
energy_required = st.number_input('Energy to be generated (kWh):', min_value=1, step=1)
space_available = st.number_input('Available space (square meters):', min_value=1, step=1)
budget = st.number_input('Total budget (INR):', min_value=10000, step=1000)
num_outputs = st.slider('Number of output versions:', 1, 5, 1)

# Displaying the generated content
if st.button("Generate Solar Power Plan"):
    with st.spinner('Generating your solar power plant plan...'):
        # Send data to API
        response = requests.post('http://localhost:5000/generate', json={
            'energy_required': energy_required,
            'space_available': space_available,
            'budget': budget,
            'num_outputs': num_outputs
        })

        if response.status_code == 200:
            responses = response.json()
            st.success("Solar Power Plant Plan:")
            for i, response in enumerate(responses):
                st.subheader(f"Version {i+1}:")
                st.write(response)
        else:
            st.error(f"API Error: {response.status_code}")

# Section for changes to be made to the generated plan
st.subheader("Make Changes to the Plan")

updated_energy = st.number_input('Updated energy to be generated (kWh):', min_value=1, step=1)
updated_space = st.number_input('Updated space (square meters):', min_value=1, step=1)
updated_budget = st.number_input('Updated budget (INR):', min_value=10000, step=1000)

if st.button("Generate Updated Plan"):
    with st.spinner('Generating updated plan...'):
        response = requests.post('http://localhost:5000/generate', json={
            'energy_required': updated_energy,
            'space_available': updated_space,
            'budget': updated_budget,
            'num_outputs': num_outputs
        })

        if response.status_code == 200:
            updated_responses = response.json()
            st.success("Updated Solar Power Plant Plan:")
            for i, response in enumerate(updated_responses):
                st.subheader(f"Updated Version {i+1}:")
                st.write(response)
        else:
            st.error(f"API Error: {response.status_code}")
