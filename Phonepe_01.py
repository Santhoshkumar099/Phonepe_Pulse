import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import json
import os
import mysql.connector
from PIL import Image



#page config
st.set_page_config(page_title="Phonepe Pulse",page_icon="F:\IT Field\Python01\MDTM20\Project02\ICN.png")
st.sidebar.image("F:\IT Field\Python01\MDTM20\Project02\img.png")

#MYSQL Connection
mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True)
mycursor.execute('use Phonepe_01')


# creating option menu in side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About Pulse"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    


#menu Home
if selected=="Home":
    col1,col2=st.columns([2,3],gap="small")
    with col1:
        st.image("F:\IT Field\Python01\MDTM20\Project02\img.png")
        st.markdown("###### :white PhonePe is a popular digital payment platform in India that enables users to make various transactions such as money transfers, bill payments, mobile recharges, and online shopping securely through their smartphones.PhonePe is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India.")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://www.youtube.com/watch?v=aXnNA4mv1dU")

        st.write("")
        st.write("")
        st.write("")

    col1,col2=st.columns([4,1],gap="small")
    with col1:
        st.image("F:\IT Field\Python01\MDTM20\Project02\Phonepe1.jpg")
    with col2:
        st.write(" ")
        st.write(" ")
        st.markdown("### :white[View Statements and manage Financial Consents]")
        
        st.write("")
        st.write("")
        st.write("")

    col1,col2=st.columns([1,4],gap="small")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("## :white[Beat of Progress]")
    
    with col2:
        st.image("F:\IT Field\Python01\MDTM20\Project02\Phonepe3.jpg")

    
        st.write("")
        st.write("")
        st.write("")
        
    col1,col2=st.columns([4,1],gap="small")
    with col1:
        st.image("F:\IT Field\Python01\MDTM20\Project02\Phonepe2.png")
    with col2:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Recharge, Pay Bills & Send money safely from home]")

#menu Top charts

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
#Top charts Transactions

    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"""SELECT State, SUM(Transaction_count) as Total_Transactions_Count, 
                            SUM(Transaction_amount) as Total FROM aggregated_transaction WHERE 
                            Year = {Year} and
                            Quater = {Quarter} 
                            GROUP BY State ORDER BY Total desc limit 10""")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"""SELECT Districts , SUM(Transaction_count) as Total_Count, SUM(Transaction_amount)
                                as Total FROM map_transaction WHERE Year = {Year} and Quater = {Quarter} 
                                GROUP BY Districts ORDER BY Total desc limit 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        mycursor.execute(f"""SELECT State,Districts,Year, 
                        SUM(Transaction_count) as Total_Transactions
                        FROM map_transaction
                        WHERE Year = {Year} 
                        GROUP BY State,Districts,Year ORDER BY State,Districts""")

        df2 = pd.DataFrame(mycursor.fetchall(), columns=['State','Districts','Year','Total_Transactions'])
        
        fig=px.sunburst(df2,path=['Year','State','Districts'],values='Total_Transactions')
        st.plotly_chart(fig,use_container_width=True)


# top users

    if Type == "Users":
            col1,col2 = st.columns([2,3],gap="small")

            with col1:
                st.markdown("### :violet[Brands]")
                if Year == 2022 and Quarter in [2,3,4]:
                    st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
                else:
                    mycursor.execute(f"""SELECT User_brand, SUM(User_count) as Total_Count, avg(User_percentage)*100 as 
                                    Avg_Percentage FROM aggregated_user 
                                    WHERE Year = {Year} and 
                                    Quater = {Quarter} 
                                    GROUP BY User_brand ORDER BY Total_Count desc limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                    fig = px.bar(df,
                                title='Top 10',
                                x="Total_Users",
                                y="Brand",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True) 

            with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"""SELECT Districts, SUM(Registered_Users) as Total_Users, SUM(App_Opens) as 
                                Total_Appopens FROM map_user 
                                WHERE Year = {Year} and Quater = {Quarter}
                                GROUP BY Districts ORDER BY Total_Users desc limit 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                
                fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

            col3,col4 = st.columns([2,3],gap="small")
            
            with col3:
                st.markdown("### :violet[Pincode]")
                mycursor.execute(f"""SELECT Pincode, SUM(Registered_Users) as Total_Users 
                                FROM top_user 
                                WHERE Year = {Year} and Quater = {Quarter} 
                                GROUP BY Pincode ORDER BY Total_Users desc limit 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col4:
                st.markdown("### :violet[State]")
                mycursor.execute(f"""SELECT State, SUM(Registered_Users) as Total_Users, sum(App_Opens) as 
                                Total_Appopens FROM map_user 
                                WHERE Year = {Year} and Quater = {Quarter} 
                                GROUP BY State ORDER BY Total_Users desc limit 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)


# Explore Data 
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))


# transaction

    if Type == "Transactions":
        
    
    # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        
        st.markdown("## :red[Overall State Data - Transactions Amount]")
        mycursor.execute(f"""SELECT State, SUM(Transaction_count) as Total_Transactions, sum(Transaction_amount)
                        as Total_amount FROM map_transaction 
                        WHERE Year = {Year} and Quater = {Quarter}
                        GROUP BY State order by State""")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_amount',
                    color_continuous_scale='reds')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

        
        st.markdown("## :red[Overall State Data - Transactions Count]")
        mycursor.execute(f"""SELECT State, SUM(Transaction_count) as Total_Transactions, sum(Transaction_amount) 
                        as Total_amount FROM map_transaction 
                        WHERE Year = {Year} and Quater = {Quarter} 
                        GROUP BY State ORDER BY State""")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df1.Total_Transactions = df1.Total_Transactions.astype(int)

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='reds')
            
        

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :red[Top Payment Type]")
        mycursor.execute(f"""SELECT Transaction_type, SUM(Transaction_count) as Total_Transactions, 
                        sum(Transaction_amount) as Total_amount FROM aggregated_transaction 
                        WHERE Year= {Year} and Quater = {Quarter} GROUP BY Transaction_type ORDER BY 
                        Transaction_type""")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_Type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_Type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
            

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                            ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'),index=30)
                                    
        mycursor.execute(f"""SELECT State, Districts,Year,Quater, SUM(Transaction_count) 
                        as Total_Transactions, sum(Transaction_amount) as Total_amount FROM map_transaction
                        WHERE Year = {Year} and Quater = {Quarter} and State= '{selected_state}'
                        GROUP BY State, Districts,Year,Quater order by State,Districts""")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','Districts','Year','Quater',
                                                        'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                    title=selected_state,
                    x="Districts",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)



    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :red[Overall State Data - User App opening frequency]")
        mycursor.execute(f"""SELECT State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens 
                        FROM map_user 
                        WHERE Year = {Year} and Quater = {Quarter} 
                        GROUP BY State ORDER BY State""")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        
        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Appopens',
                    color_continuous_scale='sunset')
        

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                            ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'),index=30)
    
        mycursor.execute(f"""SELECT State,Year,Quater,Districts,SUM(Registered_Users) as Total_Users, 
                        sum(App_Opens) as Total_Appopens 
                        FROM map_user 
                        WHERE Year = {Year} and Quater = {Quarter} and State = '{selected_state}' 
                        GROUP BY State, Districts,Year,Quater ORDER BY State,Districts""")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['States','Transaction_Year', 'Quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                    title=selected_state,
                    x="District",
                    y="Total_Users",
                    orientation='v',
                    color='Total_Users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

#about

if selected == "About Pulse":
        st.write(" ")
        st.markdown("### :red[About PhonePe Pulse:] ")
        st.video("https://www.youtube.com/watch?v=Yy03rjSUIB8&t=1s")
        st.write("##### The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.")
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.write(" ")
        st.write(" ")
        st.write("##### PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
        st.write(" ")
        st.write(" ")
        st.video("https://www.youtube.com/watch?v=c_1H6vivsiA")