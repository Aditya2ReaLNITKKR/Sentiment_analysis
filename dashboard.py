import streamlit as st
import redis
import json
import pandas as pd
import time

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Fetch sentiment data from Redis
def get_sentiment_data():
    data = []
    for key in r.keys("sentiment:*"):
        comment_data = json.loads(r.get(key).decode('utf-8'))
        data.append(comment_data)
    return pd.DataFrame(data)

# Streamlit dashboard
st.title("Real-Time Reddit Sentiment Analysis")
st.write("Displaying sentiment analysis of live comments from r/technology")

# Placeholder for chart and table
chart_placeholder = st.empty()
table_placeholder = st.empty()

while True:
    df = get_sentiment_data()
    if not df.empty:
        # Sentiment distribution
        sentiment_counts = df["sentiment"].value_counts()
        chart_placeholder.bar_chart(sentiment_counts)
        
        # Recent comments table
        table_placeholder.table(df[["text", "sentiment", "compound_score"]].tail(5))
    
    time.sleep(2)  # Update every 2 seconds