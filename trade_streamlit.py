from ast import If
from turtle import width
from matplotlib.axis import YAxis
import streamlit as st #streamlit
import datetime         #날짜 추출
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from tkinter import *

#original_df = pd.read_csv('Trade_History.csv', encoding='cp949')
#original_df['매매일시'] = pd.to_datetime(original_df['매매일시'], format="%Y-%m-%d %H:%M") #날짜 문자열을 datatime으로 형변환
#THR_df = pd.read_csv('Trade_History_real.csv', encoding = 'cp949')
#BHR_df = pd.read_csv('Balance_History_real.csv', encoding ='cp949')
#THt_df = pd.read_csv('Trade_History_temp.csv', encoding = 'UTF8')
#balance_df = pd.read_csv('Balance_History.csv', encoding='UTF8')

original_df = pd.read_csv('C:/Users/PC/Desktop/산학/venv/Trade_History.csv', encoding='cp949')
original_df['매매일시'] = pd.to_datetime(original_df['매매일시'], format="%Y-%m-%d %H:%M") #날짜 문자열을 datatime으로 형변환
#수익률 비교 코스닥 코스비 내수익률
cmp_bnf_df = pd.read_csv('C:/Users/PC/Desktop/산학/venv/kospi_kosdaq_data.csv', encoding='cp949')
account_df = pd.read_csv('C:/Users/PC/Desktop/산학/venv/Account.csv', encoding='cp949')
st.set_page_config(page_icon="📊", page_title="강화학습 기반 자동매매 시스템", layout='wide')

today = datetime.datetime.now()
dateDict = {0:'월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
str_today = today.strftime("%Y-%m-%d")
sidebar_col1, sidebar_col2 = st.sidebar.columns([1,1])
rate = original_df.iloc[-1][7]-1000000 #현재 - 시작
rate = rate / 1000000 #손익/시작
rate = rate * 100 #백분율
rate_text = str(rate) + "%"
if rate>=0:
    rate_text = '<p style="font-family:돋움; color:Red; font-weight:bolder; font-size: 20px;">%s</p>' % rate_text
if rate < 0:
    rate_text = '<p style="font-family:돋움; color:Blue; font-weight:bolder; font-size: 20px;">%s</p>' % rate_text


with sidebar_col1:
    st.title(str_today) #날짜 요일 출력
    st.subheader("\n")
    st.subheader("사용자 : ")
    st.subheader("시작 금액 : ")
    st.subheader("거래 시작일 : ")
    st.subheader("마지막 거래일 : ")
    st.subheader("현재 보유 자산 : ")
    st.subheader("수익률 : ")
with sidebar_col2:
    st.title(dateDict[today.weekday()])
    st.subheader("\n")
    st.subheader("퀸트고")
    st.subheader("1,000,000 원")
    text = original_df.iloc[0][0].strftime("%Y-%m-%d")
    st.subheader(text)
    text = original_df.iloc[-1][0].strftime("%Y-%m-%d")
    st.subheader(text)
    st.subheader(format(original_df.iloc[-1][7],','))
    st.markdown(rate_text, unsafe_allow_html=True)

st.sidebar.subheader(" ")

#st.sidebar.subheader("사용자 : 정일영")
#st.sidebar.subheader("시작 금액 : %d" % original_df.iloc[0][7])
#st.sidebar.subheader("현재 보유 자산 : %d" % original_df.iloc[-1][7]) #현재 보유자산 = tempset 마지막행 총평가금액
st.sidebar.subheader(" ")
st.sidebar.subheader(" ")


col = ["매매 날짜", "매매 시간", "종목명", "주문 내용", "체결 단가", "체결 수량", "체결 금액", "총 평가금액", "잔고 수량", "종가"] #매매로그 컬럼
df_mmlog = pd.DataFrame(data=None, columns=col) #매매 로그를 위한 데이터프레임
df_mmlog_c = pd.DataFrame(data=None, columns=col)
df_log = pd.DataFrame(data=None, columns=col)#mmlog 거꾸로
df_log_c = pd.DataFrame(data=None, columns=col)



now_date = original_df.loc[0][0].date() #첫 매매 날짜
for i in range(len(original_df)): #원본 프레임 탐색
    x = original_df.loc[i]
    now_date = x[0].date()
    if x[3] == "정규장현금매수":
        x[3] = "매수"
    if x[3] == "정규장현금매도":
        x[3] = "매도"
    oneline_mmlog = [now_date, x[0].strftime("%H:%M:%S"), x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]]
    oneline_mmlog_c = [now_date, x[0].strftime("%H:%M:%S"), x[2], x[3], format(x[4],','), format(x[5], ',')
        , format(x[6], ','), format(x[7],','), format(x[8],','), format(x[9], ',')]
    df_mmlog.loc[i] = oneline_mmlog #데이터프레임에 원본파일 1행씩 추가
    df_mmlog_c.loc[i] = oneline_mmlog_c

for i in range(len(df_mmlog)):
    df_log.loc[i] = df_mmlog.loc[len(df_mmlog)-1-i]
    df_log_c.loc[i] = df_mmlog_c.loc[len(df_mmlog) - 1 - i]



### 보유 종목 리스트를 위한 정보 불러오기 csv 필요

df_inter = pd.DataFrame(data=None, columns=['총자산'])
for i in range(len(df_mmlog)):
    df_inter.loc[df_mmlog.iloc[i][0]] = df_mmlog.iloc[i][7] #당일 마지막 거래 평가금액을 차트용 DF에 저장

account_df = account_df.sort_values(by=account_df.columns[3], ascending=False)

st.sidebar.subheader("메뉴 선택")
add_selectbox = st.sidebar.selectbox("", ("메인 화면", "매매 로그", "총 자산 현황", "보유 종목 리스트"))

st.sidebar.subheader("\n")
st.sidebar.subheader("\n")

st.sidebar.subheader("기간 별 수익률")

start_date = st.sidebar.date_input("시작 날짜", df_mmlog.iloc[0][0]) #시작날짜 : 거래 첫번째 날짜
start_date_error = 0
while 1:
    if start_date < df_mmlog.iloc[0][0]:
        start_date_error = 1
        break
    df_start_value = df_mmlog[df_mmlog['매매 날짜'] == start_date]
    if len(df_start_value) == 0:
        start_date = start_date - datetime.timedelta(days=1)
        continue
    else:
        start_value = df_start_value.iloc[-1][7]
        break

if start_date_error == 0:
    st.sidebar.write("평가 금액 : %s" % format(start_value, ','))
else:
    st.sidebar.write("시작날짜 지정 오류")

end_date = st.sidebar.date_input("마지막 날짜", today.date())  #마지막날짜 : 오늘
df_end_value = df_mmlog[df_mmlog['매매 날짜'] == end_date]
end_date_error = 0
while 1:
    #st.sidebar.write(end_date)
    if end_date < start_date:
        end_date_error = 1
        break
    df_end_value = df_mmlog[df_mmlog['매매 날짜'] == end_date]
    if len(df_end_value) == 0:
        end_date = end_date - datetime.timedelta(days=1)
        continue
    else:
        end_value = df_end_value.iloc[-1][7]
        break
if end_date_error == 0:
    st.sidebar.write("평가 금액 : %s" % format(end_value, ','))
else:
    st.sidebar.write("마지막날짜 지정 오류")

if (end_date_error == 0 )& (start_date_error == 0):
    rate = end_value - start_value
    rate = rate / start_value
    rate = rate * 100
    if rate > 0:
        text = "수익률 :       +%.5f %%" % float(rate)
    else:
        text = "수익률 :       %.5f %%" % float(rate)
else:
    text = "날짜 지정 오류"
st.sidebar.subheader(text)
st.sidebar.write(" ")
st.sidebar.write(" ")

#사이드바 메뉴

if add_selectbox == "메인 화면":
    #balance = pd.read_csv('balancetemp.csv', encoding = 'cp949')

    title_col1, title_col2 = st.columns([4,1])
    title_col1.title('📊계좌 정보 요약')
    title_col2.selectbox("계좌 선택", ("1번 계좌", "2번 계좌"))

    st.subheader("\n")
    st.subheader("\n")
    st.subheader("\n")
    asset_col1, asset_col2, asset_col2_1, asset_col2_2, asset_col2_3, asset_col3, asset_col4, asset_col5 = st.columns([1.2, 0.3,0.3, 0.2, 0.3, 0.1, 0.5, 0.5])
    aFontstyle = '<p style="font-family:돋움; color:Black; font-weight: bolder; font-size: 20px;">%s</p>'
    bFontstyle = '<p style="font-family:굴림; color:Black; font-weight: normal; font-size: 15px;">%s</p>'
    cash = original_df.iloc[-1][7]

    with asset_col2:
        st.subheader("\n")
        st.subheader("\n")
        text = aFontstyle % "종목명"
        st.markdown(text, unsafe_allow_html=True)
    with asset_col2_1:
        st.subheader("\n")
        st.subheader("\n")
        text = aFontstyle % "평가 금액"
        st.markdown(text, unsafe_allow_html=True)
    with asset_col2_2:
        st.subheader("\n")
        st.subheader("\n")
        text = aFontstyle % "수량"
        st.markdown(text, unsafe_allow_html=True)
    with asset_col2_3:
        st.subheader("\n")
        st.subheader("\n")
        text = aFontstyle % "평균 단가"
        st.markdown(text, unsafe_allow_html=True)
    for i in range(len(account_df)):
        with asset_col2:
            text = bFontstyle % account_df.iloc[i][0]
            st.markdown(text, unsafe_allow_html=True)
        with asset_col2_1:
            cash = cash - account_df.iloc[i][2]
            text = bFontstyle % format(account_df.iloc[i][2],',')
            st.markdown(text, unsafe_allow_html=True)
        with asset_col2_2:
            text = bFontstyle % account_df.iloc[i][1]
            st.markdown(text, unsafe_allow_html=True)
        with asset_col2_3:
            text = bFontstyle % format(account_df.iloc[i][3],',')
            st.markdown(text, unsafe_allow_html=True)

    with asset_col3:
        st.write('\n')

    with asset_col4:
        st.subheader("시작원금")
        st.subheader("당일 평가금액 " )
        st.subheader("보유 현금  ")
        st.subheader("수익률  ")
    with asset_col5:
        start_asset_col4 = 1000000
        now_asset_col4 = original_df.iloc[-1][7]
        rate_col4 = (now_asset_col4 - start_asset_col4)
        rate_col4 = rate_col4 / start_asset_col4
        rate_col4 = rate_col4 * 100
        text_col4 = "%.2f%% " % float(rate_col4)
        st.subheader(": " + format(start_asset_col4, ","))
        st.subheader(": " + format(now_asset_col4, ","))
        st.subheader(": " + format(cash, ","))
        if rate_col4 > 0:
            rate_text = '<p style="font-family:돋움; color:Red; font-size: 30px;">: %s</p>' % text_col4
        else:
            rate_text = '<p style="font-family:돋움; color:Blue; font-size: 30px;">: %s</p>' % text_col4
        st.markdown(rate_text, unsafe_allow_html=True)

    account_df.loc[len(account_df)] = None
    account_df.loc[len(account_df)-1, "평가금액"] = cash
    account_df.loc[len(account_df) - 1, "종목명"] = "보유 현금"

    with asset_col1:
        tips_df = px.data.tips()
        fig = px.pie(account_df, values='평가금액', names='종목명')
        fig.update_layout(template="presentation", width=500, height=400
                          , title=dict(text="자산 포트폴리오", font=dict(size=30, family='Impact')))
        st.write(fig)

    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    #timestamp -> date
    cmpflag = 0
    a = 0
    cmp_bnf_df['Date'] = pd.to_datetime(cmp_bnf_df['Date'], format="%Y-%m-%d")
    # cmp_bnf_df 의 timestamp를 date로 바꾸기 위한 새로운 df
    d_cmp_bnf_df = pd.DataFrame(data=None, columns=['Date', 'Kospi', 'Kosdaq', '내수익률'])
    for i in range(len(cmp_bnf_df)):
        if cmp_bnf_df.iloc[i][0] == df_mmlog.iloc[a][0]:
            cur_date = df_mmlog.iloc[a][0]
            oneline = [cmp_bnf_df.iloc[i][0].date(), cmp_bnf_df.iloc[i][1], cmp_bnf_df.iloc[i][2], np.float64(df_mmlog.iloc[a][7])]
            d_cmp_bnf_df.loc[i] = oneline
            cmpflag = 1
            escape = 1
            while escape:
                a = a + 1
                if a == len(df_mmlog)-1:
                    escape = 0
                else:
                    if cur_date == df_mmlog.iloc[a][0]:
                        escape = 1
                    else:
                        escape = 0

        else:
            if cmpflag == 1:
                oneline = [cmp_bnf_df.iloc[i][0].date(), cmp_bnf_df.iloc[i][1], cmp_bnf_df.iloc[i][2],
                           d_cmp_bnf_df.iloc[i - 1][3]]
            else:
                oneline = [cmp_bnf_df.iloc[i][0].date(), cmp_bnf_df.iloc[i][1], cmp_bnf_df.iloc[i][2], 0]
            d_cmp_bnf_df.loc[i] = oneline
    chart_col1, chart_col2, chart_col3 = st.columns([3,0.5, 0.5])

    with chart_col2:
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')

    #기간 입력
        start_date_cmp = st.date_input("시작", df_mmlog.iloc[0][0], key='start_date_compare')
        end_date_cmp = st.date_input("마지막", today.date(), key='end_date_compare')
        start_date_ori = original_df.iloc[0][0]
        if start_date_ori>start_date_cmp:
            start_date_cmp = start_date_ori
    #기간에 맞는 df 추출
    df_std = d_cmp_bnf_df[(d_cmp_bnf_df['Date']>=start_date_cmp)&(d_cmp_bnf_df['Date']<=end_date_cmp)]
    kospi_std = df_std.iloc[0][1]
    kosdaq_std = df_std.iloc[0][2]
    my_std = df_std.iloc[0][3]
    #수익률 구하고 반올림
    df_std['kospi_bnf'] = (df_std['Kospi']-kospi_std)/kospi_std * 100
    df_std['kospi_bnf'] = round(df_std['kospi_bnf'], 4)
    df_std['kosdaq_bnf'] = (df_std['Kosdaq'] - kosdaq_std) / kosdaq_std * 100
    df_std['kosdaq_bnf'] = round(df_std['kosdaq_bnf'], 4)
    df_std['my_bnf'] = (df_std['내수익률'] - float(my_std)) / float(my_std) * 100
    df_std['my_bnf'] = np.float64(df_std['my_bnf'])
    df_std['my_bnf'] = round(df_std['my_bnf'], 4)
    with chart_col2:
        text =  '<p style="font-family:돋움; color:Green; font-weight: Bolder; font-size: 20px;">내 수익률 </p>'
        st.markdown(text, unsafe_allow_html=True)
        text = '<p style="font-family:돋움; color:Red; font-weight: Bolder; font-size: 20px;">KOSPI </p>'
        st.markdown(text, unsafe_allow_html=True)
        text = '<p style="font-family:돋움; color:Blue; font-weight: Bolder; font-size: 20px;">KOSDAQ </p>'
        st.markdown(text, unsafe_allow_html=True)
    with chart_col3:
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')
        st.subheader('\n')

        text = format(df_std.iloc[-1][6])
        if df_std.iloc[-1][6]==0:
            col2_text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        elif df_std.iloc[-1][6]>0:
            col2_text = '<p style="font-family:돋움; color:Red; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        else:
            col2_text = '<p style="font-family:돋움; color:Blue; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        st.markdown(col2_text, unsafe_allow_html=True)
        text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text

        text = format(df_std.iloc[-1][4])
        if df_std.iloc[-1][6] == 0:
            col2_text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        elif df_std.iloc[-1][6] > 0:
            col2_text = '<p style="font-family:돋움; color:Red; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        else:
            col2_text = '<p style="font-family:돋움; color:Blue; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        st.markdown(col2_text, unsafe_allow_html=True)
        text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text

        text = format(df_std.iloc[-1][5])
        if df_std.iloc[-1][6] == 0:
            col2_text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        elif df_std.iloc[-1][6] > 0:
            col2_text = '<p style="font-family:돋움; color:Red; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        else:
            col2_text = '<p style="font-family:돋움; color:Blue; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text
        st.markdown(col2_text, unsafe_allow_html=True)
        text = '<p style="font-family:돋움; color:Black; font-weight: Bolder; font-size: 20px;"> : %s %%</p>' % text

    with chart_col1:
        FIG = go.Figure()
        FIG.add_trace(go.Scatter(x=df_std['Date'].to_list(), y=df_std['kospi_bnf'].to_list(), name="KOSPI",mode = 'lines'
                    , line = dict(dash='solid', color = 'red')))
        FIG.add_trace(go.Scatter(x=df_std['Date'].to_list(), y=df_std['kosdaq_bnf'].to_list(), name="KOSDAQ",mode = 'lines'
                    , line = dict(dash='solid', color = 'blue')))
        FIG.add_trace(go.Scatter(x=df_std['Date'].to_list(), y=df_std['my_bnf'].to_list(), name="내 수익률",mode = 'lines'
                    , line = dict(dash='solid', color = 'green')))
        FIG.update_layout(template = "presentation",autosize = True
                    , title = dict(text = "시장대비 수익률", font=dict(size=30, family='Impact'))
                    )
        FIG.update_xaxes(showgrid = True, gridwidth=2, gridcolor = 'LightGrey')
        FIG.update_yaxes(showgrid = True, gridwidth=2, gridcolor='LightGrey',tickformat=',', tickfont_size=15)

    #FIG.update_yaxes(showgrid = True, gridwidth = 1, gridcolor = 'LightPink', zeroline=True, zerolinewidth=2, )
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly',
    #     'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
    #     'ygridoff', 'gridon', 'none'] #템플렛 옵션
    #st.write(FIG)#차트그리기
        st.plotly_chart(FIG, use_container_width=True)

if add_selectbox == "매매 로그":
    st.title("📊매매 로그 출력")

    #st.markdown(Fontstyle, unsafe_allow_html=True)
    mmlog_col1, mmlog_col2 = st.columns([5,1])
    with mmlog_col2:
        selected_item = st.selectbox("기간 선택", ("전체", "한달", "일주일", "어제", "금일", "기간 지정"))
    now = datetime.datetime.now()
    #st.write(df_log_c)
    Fontstyle = '<p style="font-family:돋움; color:Blue; font-weight: bold; font-size: 20px;">당일 평가 금액 : </p>'
    f_text = '<p style="font-family:돋움; color:Black; font-weight: bolder; font-size: 25px;">%s</p>'
    d_text = '<p style="font-family:돋움; color:Black; font-weight: bold; font-size: 20px;">%s</p>'
    c1_text = '<p style="font-family:돋움; color:Red; font-weight: bold; font-size: 20px;">%s</p>'
    c2_text = '<p style="font-family:돋움; color:Blue; font-weight: bold; font-size: 20px;">%s</p>'
    c3_text = '<p style="font-family:돋움; color:Green; font-weight: bold; font-size: 20px;">%s</p>'
    if selected_item == "전체":
        with mmlog_col1:
            st.subheader("전체 로그 출력")
        dateflag = 1
        cur_date = df_log.iloc[0][0]
        st.subheader(cur_date)  # 첫 거래 날짜
        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns([1, 1, 1.5, 1.5, 1, 1.5, 1])
        st.markdown("""---""")
        with log_col1:
            text = f_text % "종목 명"
            st.markdown(text, unsafe_allow_html=True)
        with log_col2:
            text = f_text % "주문 내용"
            st.markdown(text, unsafe_allow_html=True)
        with log_col3:
            text = f_text % "체결 단가"
            st.markdown(text, unsafe_allow_html=True)
        with log_col4:
            text = f_text % "종가"
            st.markdown(text, unsafe_allow_html=True)
        with log_col5:
            text = f_text % "체결 수량"
            st.markdown(text, unsafe_allow_html=True)
        with log_col6:
            text = f_text % "체결 금액"
            st.markdown(text, unsafe_allow_html=True)
        with log_col7:
            text = f_text % "잔고 수량"
            st.markdown(text, unsafe_allow_html=True)
        lenlog = len(df_log)
        for i in range(lenlog):
            if df_log.iloc[i][0] == cur_date:
                if dateflag == 1:
                    for j in range(len(df_log_c[df_log['매매 날짜']==cur_date])):
                        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                            [1, 1, 1.5, 1.5, 1, 1.5, 1])
                        with log_col1:#종목명
                            text = d_text % df_log_c[df_log['매매 날짜']==cur_date].iloc[j][2]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col2:#주문내용
                            if df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][3] == "보유":
                                text = c3_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][3]
                                st.markdown(text, unsafe_allow_html=True)
                            elif df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][3] == "매도":
                                text = c2_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][3]
                                st.markdown(text, unsafe_allow_html=True)
                            else:
                                text = c1_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][3]
                                st.markdown(text, unsafe_allow_html=True)
                        with log_col3:#체결단가
                            text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][4]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col4:#종가
                            text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][9]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col5:
                            text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][5]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col6:
                            text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][6]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col7:
                            text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[j][8]
                            st.markdown(text, unsafe_allow_html=True)
                    dateflag =0
                else:
                    continue
            else:
                mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
                with mm_col2:
                    st.markdown(Fontstyle, unsafe_allow_html=True)
                with mm_col3:
                    text = d_text % df_log_c.iloc[i-1][7]
                    st.markdown(text, unsafe_allow_html=True)
                st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                cur_date = df_log.iloc[i][0]
                st.subheader(cur_date)
                log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                    [1, 1, 1.5, 1.5, 1, 1.5, 1])
                st.markdown("""---""")
                with log_col1:
                    text = f_text % "종목 명"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col2:
                    text = f_text % "주문 내용"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col3:
                    text = f_text % "체결 단가"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col4:
                    text = f_text % "종가"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col5:
                    text = f_text % "체결 수량"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col6:
                    text = f_text % "체결 금액"
                    st.markdown(text, unsafe_allow_html=True)
                with log_col7:
                    text = f_text % "잔고 수량"
                    st.markdown(text, unsafe_allow_html=True)
                if len(df_log[df_log['매매 날짜']==cur_date])==1:
                    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                        [1, 1, 1.5, 1.5, 1, 1.5, 1])
                    with log_col1:  # 종목명
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][2]
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col2:  # 주문내용
                        if df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][3] == "보유":
                            text = c3_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][3]
                            st.markdown(text, unsafe_allow_html=True)
                        elif df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][3] == "매도":
                            text = c2_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][3]
                            st.markdown(text, unsafe_allow_html=True)
                        else:
                            text = c1_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][3]
                            st.markdown(text, unsafe_allow_html=True)
                    with log_col3:  # 체결단가
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][4]
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col4:  # 종가
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][9]
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col5:
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][5]
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col6:
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][6]
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col7:
                        text = d_text % df_log_c[df_log['매매 날짜'] == cur_date].iloc[0][8]
                        st.markdown(text, unsafe_allow_html=True)
                dateflag = 1
        mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
        with mm_col2:
            st.markdown(Fontstyle, unsafe_allow_html=True)
        with mm_col3:
            text = d_text % df_log_c.iloc[-1][7]
            st.markdown(text, unsafe_allow_html=True)
        st.markdown("""---""")
        #st.write("당일 평가금액 : %s" % df_log_c.iloc[-1][7])

    if selected_item == "한달":
        dateflag = 1
        thirtybeforedate = now - datetime.timedelta(days=30)  # 오늘부터 한달 전 날짜
        df_thirty = df_log[df_log['매매 날짜'] >= thirtybeforedate.date()]
        df_thirty_c = df_log_c[df_log['매매 날짜'] >= thirtybeforedate.date()]
        if len(df_thirty)==0:
            st.subheader("한달동안 매매 기록 없음")
        else:
            with mmlog_col1:
                st.subheader("한달 로그 출력")
            cur_date = df_thirty.iloc[0][0]
            st.subheader(cur_date)  # 첫 거래 날짜
            dateflag = 1
            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns([1, 1, 1.5, 1.5, 1, 1.5, 1])
            st.markdown("""---""")
            with log_col1:
                text = f_text % "종목 명"
                st.markdown(text, unsafe_allow_html=True)
            with log_col2:
                text = f_text % "주문 내용"
                st.markdown(text, unsafe_allow_html=True)
            with log_col3:
                text = f_text % "체결 단가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col4:
                text = f_text % "종가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col5:
                text = f_text % "체결 수량"
                st.markdown(text, unsafe_allow_html=True)
            with log_col6:
                text = f_text % "체결 금액"
                st.markdown(text, unsafe_allow_html=True)
            with log_col7:
                text = f_text % "잔고 수량"
                st.markdown(text, unsafe_allow_html=True)
            lenlog = len(df_thirty)
            for i in range(lenlog):
                if df_thirty.iloc[i][0] == cur_date:
                    if dateflag == 1:
                        for j in range(len(df_thirty_c[df_thirty['매매 날짜']==cur_date])):
                            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                                [1, 1, 1.5, 1.5, 1, 1.5, 1])
                            with log_col1:#종목명
                                text = d_text % df_thirty_c[df_thirty['매매 날짜']==cur_date].iloc[j][2]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col2:#주문내용
                                if df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][3] == "보유":
                                    text = c3_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                elif df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][3] == "매도":
                                    text = c2_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                else:
                                    text = c1_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                            with log_col3:#체결단가
                                text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][4]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col4:#종가
                                text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][9]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col5:
                                text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][5]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col6:
                                text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][6]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col7:
                                text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[j][8]
                                st.markdown(text, unsafe_allow_html=True)
                        dateflag =0
                    else:
                        continue
                else:
                    mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
                    with mm_col2:
                        st.markdown(Fontstyle, unsafe_allow_html=True)
                    with mm_col3:
                        text = d_text % df_thirty_c.iloc[i-1][7]
                        st.markdown(text, unsafe_allow_html=True)
                    st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    cur_date = df_thirty.iloc[i][0]
                    st.subheader(cur_date)
                    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                        [1, 1, 1.5, 1.5, 1, 1.5, 1])
                    st.markdown("""---""")
                    with log_col1:
                        text = f_text % "종목 명"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col2:
                        text = f_text % "주문 내용"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col3:
                        text = f_text % "체결 단가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col4:
                        text = f_text % "종가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col5:
                        text = f_text % "체결 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col6:
                        text = f_text % "체결 금액"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col7:
                        text = f_text % "잔고 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    if len(df_thirty[df_thirty['매매 날짜']==cur_date])==1:
                        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                            [1, 1, 1.5, 1.5, 1, 1.5, 1])
                        with log_col1:  # 종목명
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][2]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col2:  # 주문내용
                            if df_thirty_c[df_lthirty['매매 날짜'] == cur_date].iloc[0][3] == "보유":
                                text = c3_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            elif df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][3] == "매도":
                                text = c2_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            else:
                                text = c1_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                        with log_col3:  # 체결단가
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][4]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col4:  # 종가
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][9]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col5:
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][5]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col6:
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][6]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col7:
                            text = d_text % df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][8]
                            st.markdown(text, unsafe_allow_html=True)
                    dateflag = 1
            mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
            with mm_col2:
                st.markdown(Fontstyle, unsafe_allow_html=True)
            with mm_col3:
                text = d_text % df_thirty_c.iloc[-1][7]
                st.markdown(text, unsafe_allow_html=True)
            st.markdown("""---""")

    if selected_item == "일주일":
        dateflag = 1
        sevenbeforedate = now - datetime.timedelta(days=7)  # 오늘부터 7일전 날짜
        df_seven = df_log[df_log['매매 날짜'] >= sevenbeforedate.date()]
        df_seven_c = df_log_c[df_log['매매 날짜'] >= sevenbeforedate.date()]
        if len(df_seven)==0:
            st.subheader("일주일동안 매매 기록 없음")
        else:
            with mmlog_col1:
                st.subheader("일주일 로그 출력")
            cur_date = df_seven.iloc[0][0]
            st.subheader(cur_date)  # 첫 거래 날짜
            dateflag = 1
            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns([1, 1, 1.5, 1.5, 1, 1.5, 1])
            st.markdown("""---""")
            with log_col1:
                text = f_text % "종목 명"
                st.markdown(text, unsafe_allow_html=True)
            with log_col2:
                text = f_text % "주문 내용"
                st.markdown(text, unsafe_allow_html=True)
            with log_col3:
                text = f_text % "체결 단가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col4:
                text = f_text % "종가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col5:
                text = f_text % "체결 수량"
                st.markdown(text, unsafe_allow_html=True)
            with log_col6:
                text = f_text % "체결 금액"
                st.markdown(text, unsafe_allow_html=True)
            with log_col7:
                text = f_text % "잔고 수량"
                st.markdown(text, unsafe_allow_html=True)
            lenlog = len(df_seven)
            for i in range(lenlog):
                if df_seven.iloc[i][0] == cur_date:
                    if dateflag == 1:
                        for j in range(len(df_seven_c[df_seven['매매 날짜']==cur_date])):
                            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                                [1, 1, 1.5, 1.5, 1, 1.5, 1])
                            with log_col1:#종목명
                                text = d_text % df_seven_c[df_seven['매매 날짜']==cur_date].iloc[j][2]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col2:#주문내용
                                if df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][3] == "보유":
                                    text = c3_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                elif df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][3] == "매도":
                                    text = c2_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                else:
                                    text = c1_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                            with log_col3:#체결단가
                                text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][4]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col4:#종가
                                text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][9]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col5:
                                text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][5]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col6:
                                text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][6]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col7:
                                text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[j][8]
                                st.markdown(text, unsafe_allow_html=True)
                        dateflag =0
                    else:
                        continue
                else:
                    mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
                    with mm_col2:
                        st.markdown(Fontstyle, unsafe_allow_html=True)
                    with mm_col3:
                        text = d_text % df_seven_c.iloc[i-1][7]
                        st.markdown(text, unsafe_allow_html=True)
                    st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    cur_date = df_seven.iloc[i][0]
                    st.subheader(cur_date)
                    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                        [1, 1, 1.5, 1.5, 1, 1.5, 1])
                    st.markdown("""---""")
                    with log_col1:
                        text = f_text % "종목 명"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col2:
                        text = f_text % "주문 내용"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col3:
                        text = f_text % "체결 단가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col4:
                        text = f_text % "종가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col5:
                        text = f_text % "체결 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col6:
                        text = f_text % "체결 금액"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col7:
                        text = f_text % "잔고 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    if len(df_seven[df_seven['매매 날짜']==cur_date])==1:
                        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                            [1, 1, 1.5, 1.5, 1, 1.5, 1])
                        with log_col1:  # 종목명
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][2]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col2:  # 주문내용
                            if df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][3] == "보유":
                                text = c3_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            elif df_thirty_c[df_thirty['매매 날짜'] == cur_date].iloc[0][3] == "매도":
                                text = c2_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            else:
                                text = c1_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                        with log_col3:  # 체결단가
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][4]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col4:  # 종가
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][9]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col5:
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][5]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col6:
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][6]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col7:
                            text = d_text % df_seven_c[df_seven['매매 날짜'] == cur_date].iloc[0][8]
                            st.markdown(text, unsafe_allow_html=True)
                    dateflag = 1
            mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
            with mm_col2:
                st.markdown(Fontstyle, unsafe_allow_html=True)
            with mm_col3:
                text = d_text % df_seven_c.iloc[-1][7]
                st.markdown(text, unsafe_allow_html=True)
            st.markdown("""---""")

    if selected_item == "어제":
        dateflag = 1
        onebeforedate = now - datetime.timedelta(days=1)  # 오늘부터 하루전 날짜
        df_yesterday = df_log[df_log['매매 날짜'] >= onebeforedate.date()]
        df_yesterday_c = df_log_c[df_log['매매 날짜'] >= onebeforedate.date()]
        if len(df_yesterday) == 0:
            st.subheader("어제 이후 매매 기록 없음")
        else:
            with mmlog_col1:
                st.subheader("어제이후 로그 출력")
            cur_date = df_yesterday.iloc[0][0]
            st.subheader(cur_date)  # 첫 거래 날짜
            dateflag = 1
            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns([1, 1, 1.5, 1.5, 1, 1.5, 1])
            st.markdown("""---""")
            with log_col1:
                text = f_text % "종목 명"
                st.markdown(text, unsafe_allow_html=True)
            with log_col2:
                text = f_text % "주문 내용"
                st.markdown(text, unsafe_allow_html=True)
            with log_col3:
                text = f_text % "체결 단가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col4:
                text = f_text % "종가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col5:
                text = f_text % "체결 수량"
                st.markdown(text, unsafe_allow_html=True)
            with log_col6:
                text = f_text % "체결 금액"
                st.markdown(text, unsafe_allow_html=True)
            with log_col7:
                text = f_text % "잔고 수량"
                st.markdown(text, unsafe_allow_html=True)
            lenlog = len(df_yesterday)
            for i in range(lenlog):
                if df_yesterday.iloc[i][0] == cur_date:
                    if dateflag == 1:
                        for j in range(len(df_yesterday_c[df_yesterday['매매 날짜']==cur_date])):
                            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                                [1, 1, 1.5, 1.5, 1, 1.5, 1])
                            with log_col1:#종목명
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜']==cur_date].iloc[j][2]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col2:#주문내용
                                if df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][3] == "보유":
                                    text = c3_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                elif df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][3] == "매도":
                                    text = c2_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                else:
                                    text = c1_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                            with log_col3:#체결단가
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][4]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col4:#종가
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][9]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col5:
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][5]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col6:
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][6]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col7:
                                text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[j][8]
                                st.markdown(text, unsafe_allow_html=True)
                        dateflag =0
                    else:
                        continue
                else:
                    mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
                    with mm_col2:
                        st.markdown(Fontstyle, unsafe_allow_html=True)
                    with mm_col3:
                        text = d_text % df_yesterday_c.iloc[i-1][7]
                        st.markdown(text, unsafe_allow_html=True)
                    st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    cur_date = df_yesterday.iloc[i][0]
                    st.subheader(cur_date)
                    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                        [1, 1, 1.5, 1.5, 1, 1.5, 1])
                    st.markdown("""---""")
                    with log_col1:
                        text = f_text % "종목 명"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col2:
                        text = f_text % "주문 내용"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col3:
                        text = f_text % "체결 단가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col4:
                        text = f_text % "종가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col5:
                        text = f_text % "체결 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col6:
                        text = f_text % "체결 금액"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col7:
                        text = f_text % "잔고 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    if len(df_yesterday[df_yesterday['매매 날짜']==cur_date])==1:
                        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                            [1, 1, 1.5, 1.5, 1, 1.5, 1])
                        with log_col1:  # 종목명
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][2]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col2:  # 주문내용
                            if df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][3] == "보유":
                                text = c3_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            elif df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][3] == "매도":
                                text = c2_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            else:
                                text = c1_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                        with log_col3:  # 체결단가
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][4]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col4:  # 종가
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][9]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col5:
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][5]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col6:
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][6]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col7:
                            text = d_text % df_yesterday_c[df_yesterday['매매 날짜'] == cur_date].iloc[0][8]
                            st.markdown(text, unsafe_allow_html=True)
                    dateflag = 1
            mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
            with mm_col2:
                st.markdown(Fontstyle, unsafe_allow_html=True)
            with mm_col3:
                text = d_text % df_yesterday_c.iloc[-1][7]
                st.markdown(text, unsafe_allow_html=True)
            st.markdown("""---""")


    if selected_item == "금일":
        df_today = df_log_c[df_log['매매 날짜']==now.date()]
        if len(df_today) == 0:
            st.subheader("금일 매매 기록 없음")
        else:
            with mmlog_col1:
                st.subheader("금일 매매 로그 출력")
            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                [1, 1, 1.5, 1.5, 1, 1.5, 1])
            st.markdown("""---""")
            with log_col1:
                text = f_text % "종목 명"
                st.markdown(text, unsafe_allow_html=True)
            with log_col2:
                text = f_text % "주문 내용"
                st.markdown(text, unsafe_allow_html=True)
            with log_col3:
                text = f_text % "체결 단가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col4:
                text = f_text % "종가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col5:
                text = f_text % "체결 수량"
                st.markdown(text, unsafe_allow_html=True)
            with log_col6:
                text = f_text % "체결 금액"
                st.markdown(text, unsafe_allow_html=True)
            with log_col7:
                text = f_text % "잔고 수량"
                st.markdown(text, unsafe_allow_html=True)
            lenlog = len(df_today)
            for j in range(lenlog):
                log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                    [1, 1, 1.5, 1.5, 1, 1.5, 1])
                with log_col1:  # 종목명
                    text = d_text % df_today.iloc[j][2]
                    st.markdown(text, unsafe_allow_html=True)
                with log_col2:  # 주문내용
                    if df_today.iloc[j][3] == "보유":
                        text = c3_text % df_today.iloc[j][3]
                        st.markdown(text, unsafe_allow_html=True)
                    elif df_today.iloc[j][3] == "매도":
                        text = c2_text % df_today.iloc[j][3]
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        text = c1_text % df_today.iloc[j][3]
                        st.markdown(text, unsafe_allow_html=True)
                with log_col3:  # 체결단가
                    text = d_text % df_today.iloc[j][4]
                    st.markdown(text, unsafe_allow_html=True)
                with log_col4:  # 종가
                    text = d_text % df_today.iloc[j][9]
                    st.markdown(text, unsafe_allow_html=True)
                with log_col5:
                    text = d_text % df_today.iloc[j][5]
                    st.markdown(text, unsafe_allow_html=True)
                with log_col6:
                    text = d_text % df_today.iloc[j][6]
                    st.markdown(text, unsafe_allow_html=True)
                with log_col7:
                    text = d_text % df_today.iloc[j][8]
                    st.markdown(text, unsafe_allow_html=True)
            mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
            with mm_col2:
                st.markdown(Fontstyle, unsafe_allow_html=True)
            with mm_col3:
                text = d_text % df_today.iloc[-1][7]
                st.markdown(text, unsafe_allow_html=True)
            st.markdown("""---""")


    if selected_item == "기간 지정":
        st.write(" ")
        st.subheader("기간 입력")
        inter_col1, inter_col2, inter_col3 = st.columns([1, 1, 2])
        with inter_col1:
            start_date = st.date_input("시작 날짜", value=df_mmlog.iloc[0][0], key='start_date')  # 시작날짜 : 거래 첫번째 날짜
        with inter_col2:
            end_date = st.date_input("마지막 날짜", value=now.date(), key='end_date')  # 마지막날짜 : 오늘
        st.subheader("\n")
        dateflag = 1
        dateflag = 1
        df_period = df_log[(df_log['매매 날짜'] >= start_date) & (df_log['매매 날짜'] <= end_date)]
        df_period_c = df_log_c[(df_log['매매 날짜'] >= start_date) & (df_log['매매 날짜'] <= end_date)]

        if len(df_period) == 0:
            st.subheader("지정 기간 매매 기록 없음")
        else:
            with mmlog_col1:
                st.subheader("지정 기간 로그 출력")
            cur_date = df_period.iloc[0][0]
            st.subheader(cur_date)  # 첫 거래 날짜
            dateflag = 1
            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns([1, 1, 1.5, 1.5, 1, 1.5, 1])
            st.markdown("""---""")
            with log_col1:
                text = f_text % "종목 명"
                st.markdown(text, unsafe_allow_html=True)
            with log_col2:
                text = f_text % "주문 내용"
                st.markdown(text, unsafe_allow_html=True)
            with log_col3:
                text = f_text % "체결 단가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col4:
                text = f_text % "종가"
                st.markdown(text, unsafe_allow_html=True)
            with log_col5:
                text = f_text % "체결 수량"
                st.markdown(text, unsafe_allow_html=True)
            with log_col6:
                text = f_text % "체결 금액"
                st.markdown(text, unsafe_allow_html=True)
            with log_col7:
                text = f_text % "잔고 수량"
                st.markdown(text, unsafe_allow_html=True)
            lenlog = len(df_period)
            for i in range(lenlog):
                if df_period.iloc[i][0] == cur_date:
                    if dateflag == 1:
                        for j in range(len(df_period_c[df_period['매매 날짜']==cur_date])):
                            log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                                [1, 1, 1.5, 1.5, 1, 1.5, 1])
                            with log_col1:#종목명
                                text = d_text % df_period_c[df_period['매매 날짜']==cur_date].iloc[j][2]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col2:#주문내용
                                if df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][3] == "보유":
                                    text = c3_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                elif df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][3] == "매도":
                                    text = c2_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                                else:
                                    text = c1_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][3]
                                    st.markdown(text, unsafe_allow_html=True)
                            with log_col3:#체결단가
                                text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][4]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col4:#종가
                                text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][9]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col5:
                                text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][5]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col6:
                                text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][6]
                                st.markdown(text, unsafe_allow_html=True)
                            with log_col7:
                                text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[j][8]
                                st.markdown(text, unsafe_allow_html=True)
                        dateflag =0
                    else:
                        continue
                else:
                    mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
                    with mm_col2:
                        st.markdown(Fontstyle, unsafe_allow_html=True)
                    with mm_col3:
                        text = d_text % df_period_c.iloc[i-1][7]
                        st.markdown(text, unsafe_allow_html=True)
                    st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    cur_date = df_period.iloc[i][0]
                    st.subheader(cur_date)
                    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                        [1, 1, 1.5, 1.5, 1, 1.5, 1])
                    st.markdown("""---""")
                    with log_col1:
                        text = f_text % "종목 명"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col2:
                        text = f_text % "주문 내용"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col3:
                        text = f_text % "체결 단가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col4:
                        text = f_text % "종가"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col5:
                        text = f_text % "체결 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col6:
                        text = f_text % "체결 금액"
                        st.markdown(text, unsafe_allow_html=True)
                    with log_col7:
                        text = f_text % "잔고 수량"
                        st.markdown(text, unsafe_allow_html=True)
                    if len(df_period[df_period['매매 날짜']==cur_date])==1:
                        log_col1, log_col2, log_col3, log_col4, log_col5, log_col6, log_col7 = st.columns(
                            [1, 1, 1.5, 1.5, 1, 1.5, 1])
                        with log_col1:  # 종목명
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][2]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col2:  # 주문내용
                            if df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][3] == "보유":
                                text = c3_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            elif df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][3] == "매도":
                                text = c2_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                            else:
                                text = c1_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][3]
                                st.markdown(text, unsafe_allow_html=True)
                        with log_col3:  # 체결단가
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][4]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col4:  # 종가
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][9]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col5:
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][5]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col6:
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][6]
                            st.markdown(text, unsafe_allow_html=True)
                        with log_col7:
                            text = d_text % df_period_c[df_period['매매 날짜'] == cur_date].iloc[0][8]
                            st.markdown(text, unsafe_allow_html=True)
                    dateflag = 1
            mm_col1, mm_col2, mm_col3 = st.columns([8, 1.5, 1])
            with mm_col2:
                st.markdown(Fontstyle, unsafe_allow_html=True)
            with mm_col3:
                text = d_text % df_period_c.iloc[-1][7]
                st.markdown(text, unsafe_allow_html=True)
            st.markdown("""---""")
#if add_selectbox == "보유 종목 리스트":



if add_selectbox == "총 자산 현황":

    st.title('📊총 자산 현황')

    df_chart = pd.DataFrame(data=None, columns=['총자산'])
    for i in range(len(df_mmlog)):
        df_chart.loc[df_mmlog.iloc[i][0]] = df_mmlog.iloc[i][7] #당일 마지막 거래 평가금액을 차트용 DF에 저장
    #st.write(df_chart) #차트 내용
    st.subheader("기간 선택")
    date_col1, date_col2, date_col3 = st.columns([1, 1, 2])
    with date_col1:
        start_date_c = st.date_input("시작", df_mmlog.iloc[0][0])  # 시작날짜 : 거래 첫번째 날짜
    with date_col2:
        end_date_c = st.date_input("마지막", today.date())  # 마지막날짜 : 오늘
    chart_date = df_chart.index.to_list()
    chart_asset = df_chart['총자산'].to_list()
    df_chart_date = pd.DataFrame(data=chart_date, columns=['매매 날짜'])
    df_chart_asset = pd.DataFrame(data=chart_asset, columns=['총자산'])
    df_chart_int = pd.concat([df_chart_date, df_chart_asset], axis=1)

    df_chart_make = df_chart_int[(df_chart_int['매매 날짜']>=start_date_c) & (df_chart_int['매매 날짜']<=end_date_c)]
    #st.write(df_chart_make)
    #차트 옵션
    FIG = go.Figure()
    FIG.add_trace(go.Scatter(x=df_chart_make['매매 날짜'], y=df_chart_make['총자산'], name="내 수익률",mode = 'lines+markers'
                    , line = dict(dash='solid', color = 'red')))
    FIG.update_layout(template = "presentation",autosize = True
                      , title = dict(text = "일자별 총 평가금액", font=dict(size=30)),
                      xaxis_title = dict(text = '매매 날짜', font = dict(size= 20)),)

    FIG.update_xaxes(showgrid = True, gridwidth=2, gridcolor = 'LightGrey')
    FIG.update_yaxes(showgrid = True, gridwidth=2, gridcolor='LightGrey',tickformat=',', tickfont_size=15)


    #FIG.update_yaxes(showgrid = True, gridwidth = 1, gridcolor = 'LightPink', zeroline=True, zerolinewidth=2, )
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly',
    #     'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
    #     'ygridoff', 'gridon', 'none'] #템플렛 옵션
    #st.write(FIG)#차트그리기

    c1,c2 = st.columns([3, 1])

    c1.plotly_chart(FIG, use_container_width=True)
    c2.subheader("\n")
    c2.subheader("\n")
    c2.subheader("\n")
    c2.subheader("\n")
    c2.subheader("\n")



if add_selectbox == '보유 종목 리스트':
    st.title('📊보유 종목')
    st.subheader("현재가 (평균 체결 단가)")
    st.subheader("\n")
    list_col1, list_col2, list_col3, list_col4 = st.columns([1,1,1,1])
    #st.write("자료 확인용")
    #st.write(df_asset_temp)
    #st.write(df_asset_temp)
    for i in range(len(account_df)):
        assetLABEL = account_df.iloc[i][0] + "  (%s개)" % str(account_df.iloc[i][1])
        assetVALUE = format(account_df.iloc[i][2]/account_df.iloc[i][1],",") + "  (%s)" % format(account_df.iloc[i][3], ',')
        DELTA = account_df.iloc[i][4]
        assetDELTA = account_df.iloc[i][5] + "  (%s)" % format(DELTA, ",")
        if i%4==0:
            with list_col1:
                st.metric(label=assetLABEL, value = assetVALUE, delta=assetDELTA)
        if i%4==1:
            with list_col2:
                st.metric(label=assetLABEL, value = assetVALUE, delta=assetDELTA)
        if i%4==2:
            with list_col3:
                st.metric(label=assetLABEL, value = assetVALUE, delta=assetDELTA)
        if i%4==3:
            with list_col4:
                st.metric(label=assetLABEL, value = assetVALUE, delta=assetDELTA)
