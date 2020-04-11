import pandas as pd
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
      st.title("Crypto Currency APP")


      text = """
          ## Note: ##
         **This is a Cryptocurrency App Demo.**\n
         In this demo,you will see many cool functions in streamlit and plotly.\n
         - selection
         - create graph and sync with selection
         - radio selelction
         - check box selection
         - Logic : if/elif/else
         - Make it more pretty\n
         
         **Author: Ivy Wang**
         - [Linkedin](https://www.linkedin.com/in/ivy-w-81871716b/)
         - [Email](mailto:ivyvan.w@gmail.com)
         ---------------------
        """
      st.sidebar.markdown(text)

      df = load_data()
      st.subheader('Select A Cryptocurrency')
      coin_names  = df.Currency.unique().tolist()
      def coin_selector():
          coin = st.selectbox("",coin_names)
          data =df[df.Currency == coin]
          return data
   
    
      selected_coin  = coin_selector()
      st.dataframe(selected_coin)




  
      def price_trend():
        
          fig = px.line(x = selected_coin.Date,y = selected_coin.Close,width = 1000)
          fig.update_layout(title =' Price Trend',yaxis_title ='USD',xaxis_title ='',xaxis_tickformat = '%d %B <br>%Y')
          st.plotly_chart(fig)

      def marketcap_trend():
          fig = px.line(x = selected_coin.Date,y = selected_coin['Market Cap'],width = 1000)
          fig.update_layout(title ='MarketCap Trend',yaxis_title ='USD',xaxis_title ='')
          st.plotly_chart(fig)

      if st.sidebar.checkbox("Price Trend in years"):
          #st.subheader('Price Trend')
          price_trend()


      if st.sidebar.checkbox("MarketCap Trend in years"):         
          #st.subheader('MarketCap Trend')
          marketcap_trend()


      
      df_asset = df[(df.Currency == "bitcoin")|(df.Currency == "ethereum")|(df.Currency == "litecoin")]
      st.sidebar.subheader("Which currency has the biggest volatility?")
      status =  st.sidebar.radio("Select",("Bitcoin","Ethereum","Litecoin"))
      if status =="Bitcoin":
          st.sidebar.success("Great! You are right!")
      else: 
          st.sidebar.warning("Oops ! Check the graph on the right side")
          fig = px.box(df_asset,y = 'Spread',color ='Currency',width = 1000)
          fig.update_layout(title ='Currency Spread Boxplot ',yaxis_title ='USD',xaxis_title ='')
          st.plotly_chart(fig)

    
      st.sidebar.subheader("Which currency has the biggest raise?")
      select_date =df.iloc[::-1, :]['Date'].unique().tolist()
      def date_selector():
           date_s = st.sidebar.selectbox("Select:",select_date)
           data1 =df[df.Date == date_s][['Currency','Open','Close']]
           data1['Delta'] = df['Close'] - df['Open']
           return data1

      date_selector = date_selector()

      fig = make_subplots(specs=[[{"secondary_y": True}]])
      fig.add_trace(go.Bar(x = date_selector['Currency'], y= date_selector['Open'],name = 'Open Price'),secondary_y =False)
      fig.add_trace(go.Scatter(x = date_selector['Currency'], y= date_selector['Delta'],name = 'Delta'),secondary_y =True)
      fig.update_layout(title ='Currency Delta in any specific day ',yaxis_title ='USD',xaxis_title ='',width = 1050)
      fig.update_yaxes(showline=True, linewidth=3, linecolor='red')

      st.subheader("Notice:")
      st.warning (" This is a multiaxes graph. The delta axis is on the right")
      st.plotly_chart(fig)






@st.cache
def load_data():
    df=pd.read_csv('/Users/ivyw/Desktop/cryptocurrency_app/cryptocurrency_data.csv')
    cols = ['Open','Close','High','Low','Market Cap']
    for c in cols:
        df[c] = df[c].apply(lambda x:x.replace(",",""))
        df[c] = pd.to_numeric(df[c],downcast='float')
    df['Spread'] = df['High'] - df['Low']
    df = df.drop('Volume',axis = 1)

    df = df.iloc[::-1, :]

    return df



if __name__ == "__main__":
    main()

