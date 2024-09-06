import streamlit as st
import requests
import time
import random
import os
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env file

api_url = os.getenv("API_URL")
chatflow_id = os.getenv("CHATFLOW_ID")
authorization = os.getenv("AUTHORIZATION")

st.set_page_config(
    page_title="Weather Chatbot",
    page_icon="🔥"
)

st.title("Weather Chatbot")
st.caption("A Chatbot Powered by Bryan Machin Garcia.")

def query(payload):
    try:
        response = requests.post(api_url + '/prediction/' + chatflow_id, json=payload)
        return response.json()
    except Exception as e:
        print(e)



def viewChatMessage(sessionId):
    _messages = []
    try:
        _response = requests.get(api_url + '/chatmessage/' + chatflow_id, params={"sessionId":sessionId}, headers={"Authorization": authorization})
        for item in _response.json():
            _messages.append({"role": "user" if item['role'] == 'userMessage' else 'ai', "content": item['content']})
    except Exception as e:
        print(e)
    return _messages



def deleteChatMessage(sessionId):
    try:
        return requests.delete(api_url + '/chatmessage/' + chatflow_id, params={"sessionId":sessionId}, headers={"Authorization": authorization})
    except Exception as e:
        print(e)



def main():
    with st.sidebar:
        st.title('Hello, you must log-in to start your session in WeatherBot.')
        st.session_state['EMAIL'] = st.text_input('Enter E-mail:',  key='email')
        st.session_state['PASS'] = st.text_input('Enter password:', type='password', key='password')
        if not (st.session_state and st.session_state['EMAIL'] and st.session_state['PASS']):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
            st.session_state['history'] = viewChatMessage(st.session_state['EMAIL'] + st.session_state['PASS'])

        if st.button("Clear Chat", use_container_width=True, type="primary"):
            st.session_state['history'] = []
            deleteChatMessage(st.session_state['EMAIL'] + st.session_state['PASS'])
            st.rerun()

    # All messages
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    else:
        # Show messages.
        for message in st.session_state['history']:
            if message != None:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])

    if prompt := st.chat_input(disabled=not (st.session_state and st.session_state['EMAIL'] and st.session_state['PASS'])):
        st.session_state['history'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("ai"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    full_response = ""
                    output = query({"question": prompt, "overrideConfig": {"sessionId": st.session_state['EMAIL'] + st.session_state['PASS'], "returnSourceDocuments": True} , "history": st.session_state['history']})
                    for chunk in [output['text']]:
                        word_count = 0
                        random_int = random.randint(5,10)
                        for word in chunk:
                            full_response+=word
                            word_count+=1
                            if word_count == random_int:
                                time.sleep(0.05)
                                message_placeholder.markdown(full_response + "_")
                                word_count = 0
                                random_int = random.randint(5,10)
                    message_placeholder.markdown(output['text'])
                    # build history with the new messages.
                    st.session_state['history'].append({"role": "user", "content": prompt})
                    st.session_state['history'].append({"role": "ai", "content": output['text']})
                except Exception as e:
                    if not output['success']:
                        message_placeholder.markdown(output['message'])
            

main()