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
import streamlit as st
import openai

import streamlit as st

# 여행지 추천 데이터
def get_recommendations(preferences):
    # 추천 여행지 데이터
    recommendations = {
        '해변': "🏖️ **하와이** - 푸른 바다와 백사장이 매력적인 하와이에서 여유로운 해변 휴가를 즐기세요! 🌺",
        '산': "🏔️ **스위스** - 장엄한 알프스 산맥을 배경으로 하이킹과 스키를 즐길 수 있는 스위스! 🏂",
        '도시': "🏙️ **뉴욕** - 브로드웨이 공연과 세계적인 박물관이 가득한 뉴욕에서 활기찬 도시 생활을 만끽하세요! 🗽",
        '역사': "🏛️ **로마** - 고대 로마의 유적지와 아름다운 건축물들이 있는 로마에서 역사 여행을 즐기세요! 🍝",
        '자연': "🌳 **캐나다** - 광활한 자연과 국립공원에서 트레킹과 야생동물 관찰을 즐길 수 있는 캐나다! 🍁",
        '문화': "🎨 **도쿄** - 전통과 현대가 어우러진 도쿄에서 일본의 독특한 문화를 체험하세요! 🍣",
        '모험': "🧗 **뉴질랜드** - 다양한 모험 활동이 가득한 뉴질랜드에서 액티브한 여행을 즐기세요! 🚁",
        '휴양': "🌴 **발리** - 평화롭고 아름다운 발리에서 스파와 요가를 통해 완벽한 휴양을 즐기세요! 🌞"
    }
    
    # 사용자가 선택한 여행지 유형에 맞는 추천 여행지 필터링
    matched_recommendations = [rec for pref in preferences for rec in recommendations.values() if pref in rec]
    
    # 추천 여행지가 없을 경우 기본 메시지
    if not matched_recommendations:
        matched_recommendations = ["추천할 수 있는 여행지가 없습니다. 다른 여행지 유형을 선택해 보세요!"]
    
    return matched_recommendations

# 웹 앱 제목
st.title('🌟 맞춤형 여행지 추천기 🌍')

# 여행지 유형 선택
st.write("🗺️ **선호하는 여행지 유형을 선택하세요!**")
preferences = st.multiselect(
    '여행지 유형을 선택해 주세요:',
    ['해변', '산', '도시', '역사', '자연', '문화', '모험', '휴양']
)

# 여행지 추천 출력
if preferences:
    st.write("🔍 **당신에게 맞는 여행지 추천:**")
    recommendations = get_recommendations(preferences)
    for rec in recommendations:
        st.write(rec)


st.write("🗺️ **자세히 알고 싶으면 아래 똑똑이에게 질문해봐! **")



