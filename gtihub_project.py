#Install Dependencies


!pip install openai

import openai

from email.message import EmailMessage

import ssl

import smtplib

import requests




# FIXED VARIABLES 

COUNT = 10   # Number of issues to be considered

openai.api_key = 'pk-aBGRJvkkPEqwjVhOPAxMsShDXWRhMIsFQYRsVlNGsMXogigy'  # Set your OpenAI GPT-3 API key

url = "https://api.github.com/repos/twitter/communitynotes/issues"   # Github api url 





headers = {"Authorization": "token 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"}

response = requests.get(url, headers=headers)

issue_titles = []

if response.status_code == 200:
    issues = response.json()
    for issue_num in range(COUNT):
        issue_titles.append(issues[issue_num]['body'])
        # print(issues[issue_num]["body"])
else:
    print(f"Failed to retrieve issues. Status code: {response.status_code}")
    print(response.text)



# List of issue titles
issue_titles = [
    "Issue 1: Fix bug in login functionality",
    "Issue 2: Update documentation for new features",
    "Issue 3: Critical security vulnerability in authentication",
    # ... add more issue titles as needed
]

# Concatenate the issue titles into a single string
prompt = f"Rank the following issues according to severity:\n\n"
prompt += "\n".join(issue_titles)


# Request summary from GPT-3
headers = {
    'Authorization': f'Bearer {openai.api_key}',
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'pai-001-light-beta',
    'prompt': prompt,
    'temperature': 0.7,
    'max_tokens': 256,
    'stop': [
        'Human:',
        'AI:',
    ],
}

response = requests.post('https://api.pawan.krd/v1/completions', headers=headers, json=json_data)

# Extract and print the summary
summary = response.json()['choices'][0]['text']
# print("Summary of Repository Issues:")
# print(summary)


email_sender = 'tarush.s10@gmail.com'
email_receiver = 'tsharma_be20@thapar.edu'
email_password = 'gabn knog cvrl fgme'

subject = "Python Script"

body = summary


mail = EmailMessage()

mail['From'] = email_sender
mail['To'] = email_receiver
mail['subject'] = subject
mail.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
  smtp.login(email_sender, email_password)
  smtp.sendmail(email_sender,email_receiver,mail.as_string())
