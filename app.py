import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('whats app chat analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data= uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df= preprocessor.preprocess(data)

    st.dataframe(df) #This is optional if we want to display all dataframes then we can print 

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification') 
    user_list.sort()
    user_list.insert(0,'Overall') #inserting overall as complete analysis wrt overall(all members) and inserting in 0th position
    selected_user = st.sidebar.selectbox('show analysis wrt',user_list)

    if st.sidebar.button('Show Analysis'):
        
        num_messages, words, num_media_messages, num_links = helper.fetch_starts(selected_user,df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)

        with col4:
            st.header('Links Shared')
            st.title(num_links)

        #Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color= 'yellow')
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color= 'purple')
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)

        #Day wise activity map
        st.title('Day wise activity map')
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day= helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy Month')
            busy_month= helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color= 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Weekly Activity Map')
        user_heatmap = helper.activty_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group(group level only)
        if selected_user == 'Overall':
            st.title('Most Busy User')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color = 'green') # color is optional
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title('WordCloud')
        df_wc= helper.create_wordcloud(selected_user,df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
            
        #most common frequent words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        # ax.bar(most_common_df[0],most_common_df[1]) # for vertcil graph
        ax.barh(most_common_df[0],most_common_df[1])# for horizontal graph
        plt.xticks(rotation= 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig) # for plotting graph
        
        st.dataframe(most_common_df) # for dispaying without graph


        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels= emoji_df[0],autopct="%0.2f") # first parameter starts always with value not index for pie chart
            # ax.pie(emoji_df[1].head(),labels= emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)