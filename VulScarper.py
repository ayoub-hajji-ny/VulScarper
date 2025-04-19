import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

with open('html.txt', 'r') as html_file:
    html = html_file.read()# Read the entire file


start_index = html.find('<article')

if start_index != -1:
    result_html = html[start_index: start_index + 30000]
else:
    print('No <article class="notice"> found in the file.')
    exit

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(""),
        UserMessage("Given the HTML content of a security notice page, which is: " + result_html + ", extract the name of each vulnerability, the Ubuntu versions affected, and the CVE identifiers. Each notice in the HTML contains a title (vulnerability name), one or more affected Ubuntu versions, and one or more CVE identifiers. Return the result as a JSON object with the following structure: { \"vulnerabilities\": [ { \"name\": \"Vulnerability Name\", \"affected_versions\": [\"Ubuntu Version 1\", \"Ubuntu Version 2\"], \"cve\": [\"CVE-Identifier 1\", \"CVE-Identifier 2\", \"...\", \"X others\"] } ] }. If the notice lists specific CVEs and also mentions additional ones (e.g., \"and 4 others\"), include \"4 others\" (as a string) in the \"cve\" list. If no vulnerabilities are found, return this JSON object: { \"oops no\": [] }. Return only the JSON object. Do not include any additional output."
),
    ],
    temperature=1,
    top_p=1,
    model=model_name
)


json_response = response.choices[0].message.content

try:
    json_data = json.loads(json_response)

    with open('vulnerabilities.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print("JSON response saved to 'vulnerabilities.json'")
except json.JSONDecodeError:
    print("Failed to parse the response as JSON.")
    print("Response:", json_response)
