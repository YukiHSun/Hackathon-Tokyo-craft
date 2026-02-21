import pandas as pd
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def sample_iris_data(csv_path='iris.csv'):
    df = pd.read_csv(csv_path)
    # Randomly sample one individual
    sample = df.sample(1).iloc[0]
    return sample.to_dict()

def generate_phenotype_prompts(data):
    model = genai.GenerativeModel('gemini-pro-latest')
    
    prompt = f"""
    You are a botanical expert. Based on the following Iris measurements (in cm):
    - Sepal Length: {data['sepal_length']}
    - Sepal Width: {data['sepal_width']}
    - Petal Length: {data['petal_length']}
    - Petal Width: {data['petal_width']}
    - True Species: {data['species']}

    Your goal is to create 3 detailed visual descriptions (prompts) for an image generator.
    
    1. **Correct Prompt**: A scientifically accurate description of this specific {data['species']} individual.
    2. **Deceptive Prompt A**: Describe the same physical measurements but state the species as a DIFFERENT but similar-looking species.
    3. **Deceptive Prompt B**: Describe the same physical measurements but state the species as another DIFFERENT species.

    Focus on lighting, macro-photography style, petal texture, and botanical accuracy in the descriptions.
    Return the result as a JSON object with keys: "correct", "deceptive_a", "deceptive_b", "true_species".
    """
    
    response = model.generate_content(prompt)
    try:
        # Extract JSON from potential markdown wrapping
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return None

if __name__ == "__main__":
    data = sample_iris_data()
    print(f"Sampled Data: {data}")
    prompts = generate_phenotype_prompts(data)
    if prompts:
        print("Generated Prompts:")
        print(json.dumps(prompts, indent=2))
        with open('current_round.json', 'w') as f:
            json.dump(prompts, f)
