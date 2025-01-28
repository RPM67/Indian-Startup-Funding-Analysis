import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.sidebar.title('Startup Funding Details')
option = st.sidebar.selectbox('Select One',['Select','Overall Analysis','Start Up', 'Investor'])

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    req_df = df[df['amount(in cr)'] != 'undisclosed'].copy()
    req_df['amount(in cr)'] = pd.to_numeric(req_df['amount(in cr)'])
    total = round(req_df['amount(in cr)'].sum())

    # max amount infused in a startup
    max_funding = req_df.groupby('startup')['amount(in cr)'].max().sort_values(ascending=False).head(1)

    # avg ticket size
    avg_funding = req_df.groupby('startup')['amount(in cr)'].sum().mean()

    # total funded startups
    total_funded_startups = df['startup'].nunique()

    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.subheader('Total')
        st.write( str(total) + ' Cr')
    with col2:
        st.subheader('Max')
        st.write(str(max_funding.values[0]) + ' Cr ('+str(max_funding.index[0])+')')
    with col3:
        st.subheader('Avg')
        st.write(str(round(avg_funding,2))+ ' Cr')
    with col4:
        st.subheader('Total Funded Startups')
        st.write(str(total_funded_startups))

    # MoM graph
    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type',['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = req_df.groupby(['year', 'month'])['amount(in cr)'].sum().reset_index()
    else:
        temp_df = req_df.groupby(['year', 'month'])['amount(in cr)'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

    fig, ax = plt.subplots()
    ax.plot(temp_df['x_axis'], temp_df['amount(in cr)'], color='blue')
    st.pyplot(fig)



def load_recent_investments(investor):
    # recent investments
    st.title(option + ' ' + investor + ' details')
    st.subheader('Recent investments')
    top_5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'rounds', 'amount(in cr)']]
    st.dataframe(top_5_df)

    col1, col2 = st.columns(2)

    # biggest investments
    with col1:
        req_df = df[df['amount(in cr)'] != 'undisclosed'].copy()
        req_df['amount(in cr)'] = pd.to_numeric(req_df['amount(in cr)'])
        big_series = req_df[req_df['investors'].str.contains(investor)].groupby('startup')[
            'amount(in cr)'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    # vertical investments
    with col2:
        vertical_series = req_df[req_df['investors'].str.contains(investor)].groupby('vertical')[
            'amount(in cr)'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    # round investments
    with col3:
        round_series = req_df[req_df['investors'].str.contains(investor)].groupby('rounds')['amount(in cr)'].sum()
        st.subheader("round funding's")
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    # city investments
    with col4:
        city_series = req_df[req_df['investors'].str.contains(investor)].groupby('city')['amount(in cr)'].sum()
        st.subheader("cities invested in")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%1.1f%%')
        st.pyplot(fig3)

    # yoy growth
    yoy_series = req_df[req_df['investors'].str.contains(investor)].groupby('year')['amount(in cr)'].sum()
    st.subheader("YOY investments")
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_series.index, yoy_series.values)
    st.pyplot(fig4)

if option == 'Select':
    st.write("select one option the dropdown")

elif option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Start Up':
    startup = st.sidebar.selectbox('Select StartUp', df['startup'].unique().tolist())
    btn = st.sidebar.button('Find '+startup+' details')
    if btn:
        st.title(option+' '+startup+' details')
else:
    investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn = st.sidebar.button('Find '+investor+' details')
    if btn:
        load_recent_investments(investor)