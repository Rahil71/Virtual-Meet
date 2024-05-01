import moviepy.editor as mp
from time import time
import assemblyai as aai
# import openai
import json
import os
import re
import google.generativeai as palm
import requests
aai.settings.api_key = ""
API_KEY = ""
palm.configure(api_key=API_KEY)

# model_list=[_ for _ in palm.list_models()]
# for model in model_list:
#     print(model.name)


def give_open_ai_response(text):

    # model_id='models/text-bison-001'

    prompt=f'''{text}
    provide me brief summary of  the above text in 200 words and dont include words like good morning , hello etc and provide a suitable title .give me a sutiable title and good summary.
    '''
    model = palm.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt)
    text=response.text.replace("*","")
    title=text.split("\n")[0]
    summary=text.split("\n")[1:]
    data={
        'title':title,"summary":" ".join(summary)
        }
    # print(response.json)
        # try:
        # response = requests.post(
        #     "https://api.openai.com/v1/engines/text-bison-001/completions",
        #     headers={"Content-Type": "application/json", "Authorization": "Bearer {API_KEY}"},
        #     json={"prompt": prompt, "max_tokens": 200}
        #     )

        # # Process the API response to extract the title and summary
        # api_response = response.json()
        # print(api_response)
        # summary_text = api_response['choices'][0]['text'].strip()

        # # Extracting the title from the summary
        # title = summary_text.split('\n')[0]

        # # Format the summary and title into a JSON object
        # output = {"title": title, "summary": summary_text}

        # # Print or use the JSON-formatted summary
        # print(output)

        # return output
    # except requests.exceptions.RequestException as e:
    #     print(f"Error: {e}")
    #     return None
  
    # prompt=f"""
    # {text}
    # Summarize the above text in 200 words and dont include words like good morning , hello etc and provide a suitable title .give me a sutiable title and good summary in json format with keys as title and summary for example  
    # """+"{'title:data,summary:data}"
    
    # output = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo", 
    #   messages=[{"role": "user", "content":prompt}]
    # )
    # print(output)


    # data=json.loads(output['choices'][0]['message']['content'])  #convert the output to json and store in data variable
    return data



def transcribe_and_analyze(source):
    transcriber = aai.Transcriber()
    print("transcriber loaded")

    config = aai.TranscriptionConfig(
        speaker_labels=True
        ) #audio diarization 
    print("config done")

    transcript = transcriber.transcribe(f'{source}.mp3', config)


    users=[
        'john',
        'dave',
        'mary',
        'jojo',
        'joe',
        'walter',
        'jessie',
        'james',
        'skyler',
        'jack',
        'jill',
        'hank',
        'guss',
        'micheal',
        'finn',
        'ethan'
    ]
    print(len(users))

    speaker_map={}
    for index,utterance in enumerate(transcript.utterances):
        print(index)
        speaker_map[f'Speaker {utterance.speaker}']=users[index]
    
    print(speaker_map)

    speaker_and_text={}
    for utterance in transcript.utterances:
        # print(f"Speaker {utterance.speaker}: {utterance.text}")
        if f"Speaker {utterance.speaker}" in speaker_and_text: # if speaker not in text previously
            speaker_and_text[f"Speaker {utterance.speaker}"]=speaker_and_text[f"Speaker {utterance.speaker}"]+"..."+utterance.text
        else:
            speaker_and_text[f"Speaker {utterance.speaker}"]=utterance.text

    user_and_text={}
    for u,text in speaker_and_text.items():
        user_and_text[  speaker_map[u] ]=text


    speaker_text=""
    for speaker,sentences in user_and_text.items():
        speaker_text=speaker_text+f"{speaker}\n{sentences}\n\n"
    
   
    # prompt=f"""
    # Summarize the following text in 200 words and dont include words like good morning , hello etc and provide a suitable title .give me a sutiable title and good summary in json format with keys as title and summary which i can parse for my business needs. the text is  {transcript.text}
    # """
    # output = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo", 
    #   messages=[{"role": "user", "content":prompt}]
    # )
    # print(output)
    print("came here")

    # data=json.loads(output['choices'][0]['message']['content'])  #convert the output to json and store in data variable
    # while True:
    #     try:
    data=give_open_ai_response(transcript.text)
        #     break
        # except:
        #     continue

    return {
        'summary':data['summary'],
        'title':data['title'],
        'diarization':speaker_text
        }



