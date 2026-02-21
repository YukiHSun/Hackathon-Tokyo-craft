import pandas as pd
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def sample_multiple_iris(n=10, csv_path='iris.csv'):
    df = pd.read_csv(csv_path)
    samples = df.sample(n).to_dict('records')
    return samples

def generate_round_prompts(data, round_num):
    model = genai.GenerativeModel('gemini-pro-latest')
    
    prompt = f"""
    You are a botanical expert for a game called "Iris Phenotype Vision Generator".
    Based on the following Iris measurements (in cm):
    - Sepal Length: {data['sepal_length']}
    - Sepal Width: {data['sepal_width']}
    - Petal Length: {data['petal_length']}
    - Petal Width: {data['petal_width']}
    - True Species: {data['species']}

    Create 3 detailed visual descriptions (prompts) for an image generator (DALL-E style).
    
    1. **correct**: A scientifically accurate description of this specific {data['species']} individual.
    2. **deceptive_a**: Describe the same physical measurements but state the species as a DIFFERENT but similar-looking species.
    3. **deceptive_b**: Describe the same physical measurements but state the species as another DIFFERENT species.

    Focus on lighting, macro-photography style, petal texture, and botanical accuracy.
    
    IMPORTANT CONSTRAINTS:
    - DO NOT include any text, labels, captions, or branding in the descriptions.
    - DO NOT include measurement numbers or scales (like "5 cm") inside the image description as something to be rendered.
    - The image should be a pure, natural photograph or illustration without any overlayed characters or diagrammatic symbols.
    - IMPORTANT: The name of the species (e.g., "setosa") must NOT appear as text within the generated image.
    
    Return the result as a JSON object with keys: "correct", "deceptive_a", "deceptive_b", "true_species".
    """
    
    response = model.generate_content(prompt)
    try:
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        prompts = json.loads(content)
        prompts['metrics'] = data
        prompts['round'] = round_num
        return prompts
    except Exception as e:
        print(f"Error parsing Gemini response for round {round_num}: {e}")
        return None

if __name__ == "__main__":
    rounds_to_generate = 10
    samples = sample_multiple_iris(rounds_to_generate)
    game_data = []

    for i, sample in enumerate(samples, 1):
        print(f"Generating prompts for Round {i}...")
        round_prompts = generate_round_prompts(sample, i)
        if round_prompts:
            game_data.append(round_prompts)
    
    with open('rounds_data.json', 'w') as f:
        json.dump(game_data, f, indent=2)
    print(f"Generated data for {len(game_data)} rounds in rounds_data.json")
