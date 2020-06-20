import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import altair as alt
import plotly.express as px
# Add a title
st.title('London Crime Dataset')

st.write("The purpose of this dashboard is to look at crimes in London areas in the last two years. Using the data, I wanted to explore the type of crimes been committed and the areas they tend to take place. ")
@st.cache
def load_data(nrows):
    df = pd.read_csv('Borough_crime.csv',nrows=nrows)
    return df

df = load_data(10000)
st.write('Structure of the Dataset - June 2018 to May 2020 (24 Months)')

# cols = ["FY", "Manager", "Diff_Score", "FT_Winner", "FT_Draw","FT_Loss"]
# st_ms = st.multiselect("Columns", data.columns.tolist(), default=cols)

if st.checkbox('view data'):
    st.write(df)

# # 
st.write('** Please Zoom in to see the graph values clearly')

st.title("What type of crimes are the most common?")
data = df.melt(id_vars=['MajorText', 'MinorText', 'LookUp_BoroughName'],var_name='YYYYMM',value_name='Value')
data['Year'] = np.where((data['YYYYMM'] >= '201806') & (data['YYYYMM']<='201905'),'Year1819','Year1920')
common =  pd.pivot_table(data,index='MinorText',columns='YYYYMM',values='Value',aggfunc='sum')
common_plot = common.sort_values(['201806', '201807', '201808', '201809', '201810', '201811', '201812',
       '201901', '201902', '201903', '201904', '201905', '201906', '201907',
       '201908', '201909', '201910', '201911', '201912', '202001', '202002',
       '202003', '202004', '202005'],ascending=False).head(20)
f, ax = plt.subplots(figsize=(20, 15))
sns.heatmap(common_plot, cmap="coolwarm", linewidths=.5,cbar_kws={"orientation": "horizontal"})
plt.title('Most Common Crime in London Borough ',fontsize=22)
plt.ylabel('Crime in London Borough',fontsize=20)
plt.xlabel('Month',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.tight_layout()
plt.xticks(rotation=90)
st.pyplot()


st.write('''From the heat map we can see Minor crimes are the most common crimes that have been committed across London such as theft, burglary and violence. There is pattern in Theft from a Motor Vehicle in Winter from Aug 2019 to Dec 2019.
          We can see the crime numbers has decrease across all the category since covid-19 (march 2020).
''')

#
st.title('Are crime Increasing or Decreasing?')
MoM = data.groupby(['YYYYMM','Year']).sum().reset_index()
MoM['Month'] =  MoM['YYYYMM'].str[4:] # pull months 
MM = pd.pivot_table(MoM,index='Year',columns='Month',values='Value')
Jun_Dec = MM.T.tail(7) #.plot()
Jan_May = MM.T.head(5)
sns.set_style('darkgrid')
Jun_Dec.append(Jan_May).plot(figsize=(12, 8))
plt.tick_params(axis='both', which='major', labelsize=12)
plt.title('MoM crime comparison across London',fontsize=18)
plt.ylabel('Crime in London Borough',fontsize=15)
plt.xlabel('Month - June to May',fontsize=15)
st.pyplot()

st.write('''
One of the reason for decrease in crime is because of Covid-19 and lockdown in London.

- Crime was 27% down from March to April 2020.

- Crime was 35% down when comparing with April 2019 vs April 2020

- Crime was 27% down when comparing with May 2019 vs May 2020


''')





#
st.title('What type of crimes has increased or decreased?')
crime_in_london = pd.pivot_table(data,index='MinorText',columns='Year',values='Value',aggfunc='sum')
crime_in_london.sort_values(['Year1819', 'Year1920'],ascending=False).nlargest(10,['Year1819', 'Year1920'])
Increase_in_crime =crime_in_london.pct_change(axis=1).mul(100).sort_values('Year1920',ascending=False).nlargest(5,'Year1920')

more_than_1000 = crime_in_london[crime_in_london['Year1920']>1000]
descrease_in_crime = more_than_1000.pct_change(axis=1).mul(100).sort_values('Year1920',ascending=True).head(5)

sns.set_style('darkgrid')
fig,ax=plt.subplots(2,1,figsize=(10,8),squeeze=False)
ax1= Increase_in_crime.plot(kind='barh',ax=ax[0][0])
ax2 =descrease_in_crime.plot(kind='barh',ax=ax[1][0])
ax[0][0].set_ylabel('% Crime Increased',fontsize=14)
ax[1][0].set_ylabel('% Crime decreased',fontsize=14)
#ax[0][0].set_xlabel('Crimes Committed',fontsize=14)
ax[1][0].set_xlabel('Crimes Committed',fontsize=14)
ax[0][0].set_title('Top 5 most increase type of crime in London Y-o-Y',fontsize=16)
ax[1][0].set_title('Top 5 most decrease type of crime in London Y-o-Y',fontsize=16)
ax[0][0].tick_params(axis='both', which='major', labelsize=12)
ax[1][0].tick_params(axis='both', which='major', labelsize=12)
st.pyplot()

st.write('''
- Firearm Offences has increase by 300% and which could be correlated with Possession of Drugs or Homicide.

- Possession of Blade has decrease by 15% from last year, this could be due to stop and search policy relaunched in London.



''')

# 
borough_year = pd.pivot_table(data,index='LookUp_BoroughName',columns='YYYYMM',values='Value',aggfunc='sum')
bor_mon = borough_year.sort_values(['201806', '201807', '201808', '201809', '201810', '201811', '201812',
       '201901', '201902', '201903', '201904', '201905', '201906', '201907',
       '201908', '201909', '201910', '201911', '201912', '202001', '202002',
       '202003', '202004', '202005'],ascending=False).head(5)


st.title('What London Borough has the most crimes?')
st.table(bor_mon)

area = pd.pivot_table(data,index='LookUp_BoroughName',columns='YYYYMM',values='Value',aggfunc='sum')
mmm= ['201806', '201807', '201808', '201809', '201810', '201811', '201812',
       '201901', '201902', '201903', '201904', '201905', '201906', '201907',
       '201908', '201909', '201910', '201911', '201912', '202001', '202002',
       '202003', '202004', '202005']


top__5 = area.sort_values(mmm,ascending=False).head(5)
top__5 = top__5.reset_index()
Wst =  area.sort_values(mmm,ascending=False).head(1)
Wst = Wst.reset_index()

topp_5 =top__5.melt(id_vars=['LookUp_BoroughName'], var_name='YYYYMM',value_name='Value')
Wst =Wst.melt(id_vars=['LookUp_BoroughName'], var_name='YYYYMM',value_name='Value')
Wst['Borough'] = Wst['LookUp_BoroughName']
Wst['Pct']=Wst['Value'].pct_change()
Wst = Wst.drop('LookUp_BoroughName',axis=1)
st.write(Wst)

plt.figure(figsize=(15,10))
sns.set_style('darkgrid')
sns.lineplot(x='YYYYMM',y='Value',hue='LookUp_BoroughName',data=topp_5)
plt.tick_params(axis='y', which='major', labelsize=16)
plt.tick_params(axis='x', which='major', labelsize=11)
plt.title('Areas with most crimes - Top 5 Borough',fontsize=18)
plt.ylabel('Avg Number of Crimes Committed',fontsize=15)
plt.xlabel('Month',fontsize=15)
plt.legend(fontsize=14)
plt.tight_layout()
st.pyplot()

st.write('''On Average 5000+ crime cases are register in Westminster each Month and the closes borough to that is Newham with 3000+ cases registered on average.

- We can see the crime has been down since the covid 19 pandemic hit the UK specially in London with 20k deaths.

- crime is 63% down from March 2020 to April 2020

- There is a cycle every 3 month the crime goes down, this could be due to Police policy in terms of arrest been made.''' )

#
st.title('Westminister - What type of crime is been committed?')
westminster = data[data['LookUp_BoroughName']=='Westminster']
westminster_year = pd.pivot_table(westminster,index='MinorText',columns='Year',values='Value',aggfunc='sum')
st.write(westminster_year.sort_values(['Year1819','Year1920'],ascending=False).reset_index())
st.write('Only serious crime has increased in Westminister such as Drug Trafficking by 148%. Shoplifting and Motor Vehicle crime has decreased by 15% to 20%.')



#
st.title('Serious Crime in London Borough - Homicide,Rape, Carrying Knife and Drug Tracking')

hard_crime = data[(data['MinorText']=='Drug Trafficking') | (data['MinorText']=='Homicide') | (data['MinorText']=='Rape') | (data['MinorText']=='Possession of Article with Blade or Point')]
hard_crime_london = pd.pivot_table(hard_crime,index='MinorText',columns='Year',values='Value',aggfunc='sum')
st.table(hard_crime_london.sort_values(['Year1819','Year1920'],ascending=False))

hard_crime_borough_MM = pd.pivot_table(hard_crime,index='LookUp_BoroughName',columns='YYYYMM',values='Value',aggfunc='sum')
hard_crime_borough_MM =hard_crime_borough_MM.sort_values(['201806', '201807', '201808', '201809', '201810', '201811', '201812',
       '201901', '201902', '201903', '201904', '201905', '201906', '201907',
       '201908', '201909', '201910', '201911', '201912', '202001', '202002',
       '202003', '202004', '202005'],ascending=False)#.head(10)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(hard_crime_borough_MM, annot=True, cmap="coolwarm", linewidths=.5, vmin=0, vmax=100,cbar_kws={"shrink": .5},square=True)
plt.title('Serious Crime in London Borough - Homicide,Rape, Carrying Knife and Drug Tracking',fontsize=22)
plt.ylabel('Crime in London Borough',fontsize=18)
plt.xlabel('Month',fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=14)

plt.xticks(rotation=90)
st.pyplot()
st.write('Zoom in to see the values clearly',fontsize=10)
st.write('Majority of the London Borough averages about 10 serious crimes cases each month.However from the heat map we can see some of the borough are averaging about 50 serious crime cases each month.Tower Hamlets has the most serious crime cases committed each month.')

#tower
tower = pd.pivot_table(hard_crime,index=['LookUp_BoroughName','MinorText'],columns='YYYYMM',values='Value',aggfunc='sum').reset_index()
serious_crimes = tower[tower['LookUp_BoroughName']=='Tower Hamlets']
serious_crimes_1 =serious_crimes.melt(id_vars=['MinorText'], var_name='Months',value_name='Value')
serious_crimes_1 = serious_crimes_1[4:100]
serious_crimes_1['Value'] = serious_crimes_1['Value'].astype(int)

plt.figure(figsize=(15,10))
sns.set_style('darkgrid')
sns.lineplot(x='Months',y='Value',hue='MinorText',data=serious_crimes_1)
plt.tick_params(axis='y', which='major', labelsize=16)
plt.tick_params(axis='x', which='major', labelsize=11)
plt.title('Serious Crime Committed in Tower Hamlets - Homicide,Rape, Carrying Knife and Drug Tracking',fontsize=18)
plt.ylabel('Avg Number of Crimes Committed',fontsize=15)
plt.xlabel('Month',fontsize=15)
plt.legend(fontsize=14)
plt.tight_layout()

st.pyplot()

st.write('Tower Hamlets has 25 rape cases on average each month however since covid 19 it has decreased. But Knife crime has increased since covid 19.')













# #last decade
# chart = round((data.groupby('FY')[['FT_Winner','FT_Draw','FT_Loss']].sum()/38).mul(100),0)


# #error at heroku deployed for index 
# chart1 = pd.DataFrame(chart).reset_index()
# chart1 = chart1.rename(columns={'FY':'index'}).set_index('index')

# #st.write(chart1)
# st.subheader('               Outcome of matches in each season (%)')
# st.bar_chart(chart1)

# st.write('The first half of the decade Liverpool had more loss compared to draw and second half of the decade it converted loss into draws, which has resulted in more winners last season.')


# #Manager
# Manager = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss']]
# total = Manager.groupby('Manager').sum()
# total = total.reset_index()
# total = total.set_index('Manager')
# st.subheader('                Outcome of matches by Manager (%)')
# Mang = round((total.div(total.sum(axis=1), axis=0)).mul(100),1)

# #error at heroku deployed for index 
# Mang = pd.DataFrame(Mang).reset_index()
# Mang = Mang.rename(columns={'Manager':'index'}).set_index('index')

# st.bar_chart(Mang)
# #st.pyplot()



# #Home vs Away
# st.subheader("Liverpool's Performance Home vs Away")

# More = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss','Home_Win','Away_Win','Home_Draw','Away_Draw','Home_Loss','Away_Loss']]
# HA = More.groupby('Manager').sum()
# #HA['Total_Matches'] = HA['FT_Winner']+ HA['FT_Draw']+ HA['FT_Loss']
# HH = HA[['Home_Win', 'Away_Win', 'Home_Draw',
#        'Away_Draw', 'Home_Loss', 'Away_Loss']]

# plt.style.use('ggplot')
# sns.set_style('darkgrid')
# HH.plot(kind='bar',figsize=(12,10))#
# plt.xticks(rotation=360)
# plt.tick_params(axis='both', which='major', labelsize=15,labelcolor='black') 
# plt.title('Performance at Home vs Away by Manager',fontsize=18)
# plt.ylabel('Outcome Matches')
# st.pyplot()

# st.write('Under Kloop the average target shot for both Home and away matches are lowest among his peers however he still has more wins compare to other managers. This is interesting, it would be good to look into the margin of victories?')


# #Difference Score 
# st.subheader("Liverpool's Score Difference")

# score = pd.pivot_table(data,index='Diff_Score',columns='Manager',values='Date',aggfunc='count')
# sns.set_style('darkgrid')
# ax =plt.figure(figsize=(15,12))
# ax = score.plot(kind='bar',figsize=(14,10))
# ax = plt.xlabel('Difference of Score')
# ax = plt.title('Difference of Score by Manager',fontsize=18)
# ax = plt.tick_params(axis='both', which='major', labelsize=15,labelcolor='black') 
# st.pyplot()

# st.write('Jürgen Klopp has a distribution toward right hand side, he has the most draws and majority of this winners are difference of 1 or 2 goals.')
# #Number of Shot 
# st.subheader("Average Number of Shots taken under Manager per Match")
# #shot = data[['FY','Manager','FT_Winner','FT_Draw','FT_Loss','HS', 'AS', 'HST', 'AST']]
# shots = data[['FY','Manager','HS', 'AS', 'HST', 'AST']]#pd.pivot_table(shot,index='Manager',columns=['HS', 'AS', 'HST', 'AST'],values='FY',aggfunc='mean')
# dd = shots.groupby('Manager').mean()

# #error at heroku deployed for index 
# dd1 = pd.DataFrame(dd).reset_index()
# dd1 = dd1.rename(columns={'Manager':'index'}).set_index('index')

# st.line_chart(dd1)
# st.write('Liverpool has more shots taken at Home(HS) and which correlates with shots on target at home matches (HST).So, we can say that liverpool win more matches at home because they take more shots and hit the target.')



# @st.cache
# def load_data(nrows):
#     data = pd.read_csv('transfer.csv',nrows=nrows)
#     return data

# transfer = load_data(1000)
# new_data = transfer.merge(data,left_on=transfer['Year'],right_on='FY')

# spend = new_data[['Year', 'Spending', 'FT_Draw', 'FT_Loss', 'FT_Winner']]

# tra =spend.groupby('Spending').sum().reset_index()
# fin = transfer.merge(tra,left_on='Spending',right_on='Spending')
# #fin = fin.set_index('Year')

# #error at heroku deployed for index 

# fin = fin.rename(columns={'Year':'index'}).set_index('index')

# st.subheader('Liverpool Spending on transfers')



# st.bar_chart(fin)
# st.write('From the graph above, Liverpool has spend on average £43.5M in transfer each season between 2011-2016 and last season liverpool spend £143M - Buying a new goalkeeper for £56M. The Correlation between transfers and winning can be seen through each season - more spending has resulted in more wins.')


# fin['Spending'] =-(fin['Spending'])
# corr = fin.corr()
# st.subheader('Correlation between spending and the outcome of the match')
# st.table(corr)



# if __name__ == "__main__":
#    main()