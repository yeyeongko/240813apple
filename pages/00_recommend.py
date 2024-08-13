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
st.title('🌟 sweet apple의 맞춤형 여행지 추천기 🌍')

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
