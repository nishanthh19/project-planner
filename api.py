import os
import requests
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv
from flask import Flask, request, jsonify
load_dotenv()

app = Flask(__name__)

def generate_solar_plan(energy_required, space_available, budget):
    try:
        # Logic to generate solar power plant plan based on energy, space, and budget
        # Example prompt to generate plan details
        prompt_template = f"""
        You are a solar power plant planner in India. 
        You have the following requirements:
        - Energy to be generated: {energy_required} kWh
        - Space available: {space_available} square meters
        - Budget: {budget} INR
        
        Generate a comprehensive plan including:
        - Solar panels required and their specifications
        - Inverters and other equipment recommendations
        - Total area required for installation
        - Estimated cost breakdown (including installation)
        - Recommended suppliers with links and any ongoing offers or discounts
        - Necessary permits or approvals required in India
        
        Provide a clear, detailed plan.
        """
        return prompt_template
    
    except Exception as e:
        return f"Error generating solar plan: {str(e)}"

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    energy_required = data['energy_required']
    space_available = data['space_available']
    budget = data['budget']
    num_outputs = data['num_outputs']

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    groq_api_key = os.getenv('GROQ_API_TOKEN')

    prompt_data = generate_solar_plan(energy_required, space_available, budget)

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt_data}],
        "n": num_outputs
    }

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(groq_url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return jsonify([choice['message']['content'] for choice in result['choices']])
    return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
