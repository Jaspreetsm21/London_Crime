import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import altair as alt
import plotly.express as px
# Add a title
st.title('Liverpool Premier League: Journey to Winning the First Title in 30 Years')

st.write("The purpose of this dashboard is to look at Liverpool's journey in the last decade toward winning their first Premier league title in 30 Years. Using the data, I wanted to explore what things has contributed toward this success.")
@st.cache
def load_data(nrows):
    data = pd.read_csv('liverpool.csv',index_col=0,nrows=nrows)
    return data

data = load_data(10000)
st.text('Structure of the Dataset')

# cols = ["FY", "Manager", "Diff_Score", "FT_Winner", "FT_Draw","FT_Loss"]
# st_ms = st.multiselect("Columns", data.columns.tolist(), default=cols)

if st.checkbox('view data'):
    st.write(data)

# 
st.title("Liverpool's Performance in Last Decade")


#last decade
chart = round((data.groupby('FY')[['FT_Winner','FT_Draw','FT_Loss']].sum()/38).mul(100),0)


#error at heroku deployed for index 
chart1 = pd.DataFrame(chart).reset_index()
chart1 = chart1.rename(columns={'FY':'index'}).set_index('index')

#st.write(chart1)
st.subheader('               Outcome of matches in each season (%)')
st.bar_chart(chart1)

st.write('The first half of the decade Liverpool had more loss compared to draw and second half of the decade it converted loss into draws, which has resulted in more winners last season.')


#Manager
Manager = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss']]
total = Manager.groupby('Manager').sum()
total = total.reset_index()
total = total.set_index('Manager')
st.subheader('                Outcome of matches by Manager (%)')
Mang = round((total.div(total.sum(axis=1), axis=0)).mul(100),1)

#error at heroku deployed for index 
Mang = pd.DataFrame(Mang).reset_index()
Mang = Mang.rename(columns={'Manager':'index'}).set_index('index')

st.bar_chart(Mang)
#st.pyplot()



#Home vs Away
st.subheader("Liverpool's Performance Home vs Away")

More = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss','Home_Win','Away_Win','Home_Draw','Away_Draw','Home_Loss','Away_Loss']]
HA = More.groupby('Manager').sum()
#HA['Total_Matches'] = HA['FT_Winner']+ HA['FT_Draw']+ HA['FT_Loss']
HH = HA[['Home_Win', 'Away_Win', 'Home_Draw',
       'Away_Draw', 'Home_Loss', 'Away_Loss']]

plt.style.use('ggplot')
sns.set_style('darkgrid')
HH.plot(kind='bar',figsize=(12,10))#
plt.xticks(rotation=360)
plt.tick_params(axis='both', which='major', labelsize=15,labelcolor='black') 
plt.title('Performance at Home vs Away by Manager',fontsize=18)
plt.ylabel('Outcome Matches')
st.pyplot()

st.write('Under Kloop the average target shot for both Home and away matches are lowest among his peers however he still has more wins compare to other managers. This is interesting, it would be good to look into the margin of victories?')


#Difference Score 
st.subheader("Liverpool's Score Difference")

score = pd.pivot_table(data,index='Diff_Score',columns='Manager',values='Date',aggfunc='count')
sns.set_style('darkgrid')
ax =plt.figure(figsize=(15,12))
ax = score.plot(kind='bar',figsize=(14,10))
ax = plt.xlabel('Difference of Score')
ax = plt.title('Difference of Score by Manager',fontsize=18)
ax = plt.tick_params(axis='both', which='major', labelsize=15,labelcolor='black') 
st.pyplot()

st.write('Jürgen Klopp has a distribution toward right hand side, he has the most draws and majority of this winners are difference of 1 or 2 goals.')
#Number of Shot 
st.subheader("Average Number of Shots taken under Manager per Match")
#shot = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss','HS', 'AS', 'HST', 'AST']]
shots = data[['FY','Manager','HS', 'AS', 'HST', 'AST']]#pd.pivot_table(shot,index='Manager',columns=['HS', 'AS', 'HST', 'AST'],values='FY',aggfunc='mean')
dd = shots.groupby('Manager').mean()

#error at heroku deployed for index 
dd1 = pd.DataFrame(dd).reset_index()
dd1 = dd1.rename(columns={'Manager':'index'}).set_index('index')

st.line_chart(dd1)
st.write('Liverpool has more shots taken at Home(HS) and which correlates with shots on target at home matches (HST).So, we can say that liverpool win more matches at home because they take more shots and hit the target.')



@st.cache
def load_data(nrows):
    data = pd.read_csv('transfer.csv',nrows=nrows)
    return data

transfer = load_data(1000)
new_data = transfer.merge(data,left_on=transfer['Year'],right_on='FY')

spend = new_data[['Year', 'Spending', 'FT_Draw', 'FT_Loss', 'FT_Winner']]

tra =spend.groupby('Spending').sum().reset_index()
fin = transfer.merge(tra,left_on='Spending',right_on='Spending')
#fin = fin.set_index('Year')

#error at heroku deployed for index 

fin = fin.rename(columns={'Year':'index'}).set_index('index')

st.subheader('Liverpool Spending on transfers')



st.bar_chart(fin)
st.write('From the graph above, Liverpool has spend on average £43.5M in transfer each season between 2011-2016 and last season liverpool spend £143M - Buying a new goalkeeper for £56M. The Correlation between transfers and winning can be seen through each season - more spending has resulted in more wins.')


fin['Spending'] =-(fin['Spending'])
corr = fin.corr()
st.subheader('Correlation between spending and the outcome of the match')
st.table(corr)



#if __name__ == "__main__":
#    main()