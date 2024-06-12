import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 글꼴 경로 설정
font_path = 'fonts/NanumGothic.ttf'  # 경로 확인 필요
font_prop = fm.FontProperties(fname=font_path)

# 전체 글꼴 설정
plt.rc('font', family=font_prop.get_name())

# 데이터 불러오기
voting_data = pd.read_csv('vote.csv')
age_data = pd.read_csv('age.csv', encoding='utf-8')

# 데이터 병합 및 처리
merged_data = pd.merge(voting_data, age_data, left_on=['구', '읍면동명'], right_on=['시군구명', '읍면동명'], how='left')
grouped_by_district = merged_data.groupby('구').agg({'투표수': 'sum', '선거인수': 'sum'})
grouped_by_district['투표율'] = grouped_by_district['투표수'] / grouped_by_district['선거인수'] * 100

merged_data['weighted_age'] = merged_data['투표수'] * merged_data['전체 평균연령']
age_by_district = merged_data.groupby('구').agg({'weighted_age': 'sum', '투표수': 'sum'})
age_by_district['average_voting_age'] = age_by_district['weighted_age'] / age_by_district['투표수']

candidate_columns = ['박영선','오세훈','허경영','이수봉','배영규','김진아','송명숙','정동희','이도엽','신지예']
votes_per_candidate = merged_data.groupby('구')[candidate_columns].sum()
total_votes_per_district = votes_per_candidate.sum(axis=1)
for candidate in candidate_columns:
    votes_per_candidate[candidate + '_share'] = votes_per_candidate[candidate] / total_votes_per_district * 100
vote_shares = votes_per_candidate[[col + '_share' for col in candidate_columns]]

# 시각화 코드
fig, axes = plt.subplots(3, 1, figsize=(10, 18))

# 첫 번째 그래프: 투표율
grouped_by_district['투표율'].sort_values().plot(kind='barh', ax=axes[0], color='skyblue')
axes[0].set_title('Voter Turnout by District (%)', fontproperties=font_prop)
axes[0].set_xlabel('Turnout (%)', fontproperties=font_prop)
# Y축 틱 레이블에 글꼴 적용
axes[0].set_yticklabels(axes[0].get_yticklabels(), fontproperties=font_prop)

# 두 번째 그래프: 평균 투표 연령
age_by_district['average_voting_age'].sort_values().plot(kind='barh', ax=axes[1], color='lightgreen')
axes[1].set_title('Average Voting Age by District', fontproperties=font_prop)
axes[1].set_xlabel('Average Age', fontproperties=font_prop)
axes[1].set_yticklabels(axes[1].get_yticklabels(), fontproperties=font_prop)

# 세 번째 그래프: 후보별 득표율
sns.heatmap(vote_shares.T, annot=True, fmt=".1f", linewidths=.5, ax=axes[2], cmap='viridis')
axes[2].set_title('Candidate Vote Share by District (%)', fontproperties=font_prop)
axes[2].set_xlabel('District', fontproperties=font_prop)
axes[2].set_ylabel('Candidate', fontproperties=font_prop)
# Seaborn heatmap의 경우, 내부적으로 틱 레이블을 조정할 필요가 있습니다
axes[2].set_yticklabels(axes[2].get_yticklabels(), fontproperties=font_prop)
axes[2].set_xticklabels(axes[2].get_xticklabels(), fontproperties=font_prop, rotation=45)

plt.tight_layout()
plt.show()

st.title('4.7')
st.title('서울특별시장 보궐 선거 결과 분석')
st.write('분석 결과')
st.pyplot(fig, axes)  # Streamlit을 통해 플롯 출력
