import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from dotenv import load_dotenv
import glob
import settings

# API KEY 정보로드
#load_dotenv()

# python -m streamlit run main.py
st.title("🍎이번 여름 휴가 코스, 내가 짜주마!🦈")

import streamlit as st
import openai
import os

# OpenAI API 키 설정
def set_openai_api_key(api_key):
    openai.api_key = api_key

# 여행 코스 생성 함수
def generate_travel_itinerary(destination):
    prompt = f"Create an efficient and enjoyable travel itinerary for {destination}. Include key attractions, activities, and dining options. Make sure to suggest a daily plan for a 5-day trip."
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # 또는 원하는 모델
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# 웹 앱 제목
st.title('🌟 여행 코스 추천기 🌍')

# 사용자 입력: OpenAI API 키 설정
api_key = st.text_input("🔑 OpenAI API Key", type="password")
if api_key:
    set_openai_api_key(api_key)
    st.write("API 키가 설정되었습니다. 여행지를 입력해 주세요!")

# 사용자 입력: 여행지
destination = st.text_input('가고 싶은 여행지를 입력하세요!')

# 여행 코스 생성 및 출력
if destination:
    with st.spinner('여행 코스를 생성 중입니다...'):
        itinerary = generate_travel_itinerary(destination)
        st.write(f"✈️ **{destination}**에 대한 추천 여행 코스:")
        st.write(itinerary)


config = settings.load_config()
if "api_key" in config:
    st.session_state.api_key = config["api_key"]
    st.write(f'사용자 입력 API키 : {st.session_state.api_key[-5:]}')
else : 
    st.session_state.api_key = st.secrets["openai_api_key"]
    st.write(f'API키 : {st.secrets["openai_api_key"][-5:]}')
main_text = st.empty()

api_key = st.text_input("🔑 새로운 OPENAI API Key", type="password")
save_btn = st.button("설정 저장", key="save_btn")

if save_btn:
    settings.save_config({"api_key": api_key})
    st.session_state.api_key = api_key
    st.write("설정이 저장되었습니다.")


# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

    prompt_files = glob.glob("prompts/*.yaml")
    selected_prompt = st.selectbox("프롬프트를 선택해 주세요", prompt_files, index=0)
    task_input = st.text_input("TASK 입력", "")


# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


# 체인 생성
def create_chain(prompt_filepath, task=""):
    # prompt 적용
    prompt = load_prompt(prompt_filepath, encoding="utf-8")

    # 추가 파라미터가 있으면 추가
    if task:
        prompt = prompt.partial(task=task)

    # GPT
    #llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=st.session_state.api_key)

    # 출력 파서
    output_parser = StrOutputParser()

    # 체인 생성
    chain = prompt | llm | output_parser
    return chain


# 초기화 버튼이 눌리면...
if clear_btn:
    st.session_state["messages"] = []

# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 만약에 사용자 입력이 들어오면...
if user_input:
    # 사용자의 입력
    st.chat_message("user").write(user_input)
    # chain 을 생성
    chain = create_chain(selected_prompt, task=task_input)

    # 스트리밍 호출
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
        container = st.empty()

        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # 대화기록을 저장한다.
    add_message("user", user_input)
    add_message("assistant", ai_answer)
