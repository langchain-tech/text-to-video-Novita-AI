import os
import json
import requests
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI

import pdb

st.sidebar.title("Configure keys:")
OPENAI_API_KEY = st.sidebar.text_input("Enter your OpenAI key:")
NOIVITA_KEY = st.sidebar.text_input("Enter your NovitaAI key:")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
output_format = "{summary: "", script: [{}, {}, {}]}"


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a story narrator on the provided topic. You need to provide a summary of the story on the provided topic and a script with time frames for each utterance in the story.",
        ),
        (   
            "human",
            "Topic is --> {topic} and the final response by you is should be python dict(datatype) with two key-value pairs for summary and scrip, make sure the script will hold array of utterances eg --> {output_format}, Don't use this ```python or \n, only code is required ",
        )
    ]
)

def convert_to_required_format(input_list):
    output_list = []
    for item in input_list:
        new_item = {
            "frames": 32,
            "prompt": item['utterance']
        }
        output_list.append(new_item)
    return output_list


def novita_api(script):
    print(script, "scripsdfsdfsdfsdfsf")
    script = convert_to_required_format(script)
    print(script, "scripsdfsdfsdfsdfsf")
    url = 'https://api.novita.ai/v3/async/txt2video'
    headers = {
        'Authorization': f"Bearer {NOIVITA_KEY}",
        'Content-Type': 'application/json'
    }
    data = {
        "model_name": "darkSushiMixMix_225D_64380.safetensors",
        "height": 512,
        "width": 512,
        "steps": 20,
        "seed": -1,
        "prompts": script[:4],
        "negative_prompt": "nsfw,ng_deepnegative_v1_75t, badhandv4, (worst quality:2),(low quality:2), (normal quality:2), lowres,((monochrome)), ((grayscale)),watermark"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['task_id']
    else:
        st.write(f"Request failed with status code: {response.status_code} --> {response.text}")

def novita_get_task_url(task_id):
    url = 'https://api.novita.ai/v3/async/task-result'
    headers = {
        'Authorization': f"Bearer {NOIVITA_KEY}"
    }
    params = {
        'task_id': task_id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response = response.json()
        if response['task']['status'] == "TASK_STATUS_SUCCEED":
            return response['videos'][0]['video_url']
        else:
            st.write(f"TASK STATUS:--> {response['task']['status']}")
            return False
    else:
        st.write(f"Request failed with status code: {response.status_code} --> {response.text}")

def generate_story_script(topic):
    chat = ChatOpenAI(model="gpt-4o", temperature=0.2)
    chain = prompt | chat
    response = chain.invoke({"topic": topic, "output_format": output_format})
    return response.content

st.title("Video Generator App")
st.write("Enter a topic and get a story summary with a script!")

topic = st.text_input("Enter the story topic:")

if st.button("Generate Story"):
    if topic and OPENAI_API_KEY and NOIVITA_KEY :
        response = generate_story_script(topic)
        st.write("## Story Summary and Script")
        response = json.loads(response)
        st.write("## Story Summary")
        st.write(response['summary'])
        st.write("## Story Script")
        frames = response['script']
        for frame in frames:
            st.write(f"Time: {frame['time']}")
            st.write(f"Frame: {frame['utterance']}")

        task_id = novita_api(frames)
        st.write(f"## Task ID (Copy it from here!)--> {task_id}")
    else:
      st.write(f"## Make Sure OpenAI and NovitaAi api key are configured.")


task_id = st.text_input("Enter task id of video")
if st.button("Click to download Video"):
    if task_id:
        url = novita_get_task_url(task_id)
        if url:
            st.video(url)
        else:
            "Not Found"


