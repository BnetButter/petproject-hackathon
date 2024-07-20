import pandas as pd
import sys
import os
import requests
import json


infile, outfile = sys.argv[1:]
df = pd.read_csv(infile)
# Set your OpenAI API key

api_key = os.environ["OPENAI_KEY"]

# Define the API endpoint
url = "https://api.openai.com/v1/chat/completions"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

result = []

for i, row in df.iterrows():
    text = row['text'].replace('\n', '')

    # Define the payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [

            {"role": "user", "content": "summarize all violations based on the text extracted from a pdf file --" + row['text'].replace('\n', '') }
        ],
        "temperature": 0.7
    }

    # Make the API call
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content']
        result.append({ "id": row['id'], "text": text, "summary": summary })
    else:
        result.append({ 'id': row["id"], "text": text, "summary": None })
    


new_df = pd.DataFrame(result)
print(new_df)

new_df.to_csv(outfile)