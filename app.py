from message_log import message_log
import openai
import streamlit as st
import os
import time
os.environ["http_proxy"] = "http://127.0.0.1:xxxx"
os.environ["https_proxy"] = "http://127.0.0.1:xxxx"

api_key = "your api key"
openai.api_key = api_key


def generate_response(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        # The conversation history up to this point, as a list of dictionaries
        messages=message_log,
        # max_tokens=4096,        # The maximum number of tokens (words or subwords) in the generated response
        # stop=None,              # The stopping sequence for the generated response, if any (not used here)
        # The "creativity" of the generated response (higher temperature = more creative)
        temperature=0.7,
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


st.markdown("# 究极无敌CHATGPT3.5")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input = st.text_area("You:", key='input')


if user_input:
    # print(message_log)
    message_log.append({"role": "user", "content": user_input})
    output = generate_response(message_log)
    message_log.append({"role": "assistant", "content": output})
    # store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # message(st.session_state["generated"][i], key=str(i))
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')
        # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        # you can choose the color of the text and change it in the span style
        st.markdown(
            f'''<span style="color: RED;">您提问的内容: {st.session_state['past'][i]}</span>''', unsafe_allow_html=True)

    timestick = time.strftime("%Y-%m-%d-%H", time.localtime())
    # save the conversation
    with open(f'./conversation/conversation_{timestick}.txt', 'w') as f:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            f.write(f'AI: {st.session_state["generated"][i]}\n')
            f.write(f'您提问的内容: {st.session_state["past"][i]}\n')


#A popup prompting that the user's conversation history will be automatically saved
st.markdown(
    #you can set the font size and color of the text in the span style
    f'''<span style="font-size: 12px; color: RED;">您的对话历史将自动保存到./conversation/conversation_xx.txt</span>''', unsafe_allow_html=True)

