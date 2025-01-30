import streamlit as st  # type: ignore
import time
from openai import OpenAI  # type: ignore

# Set the title of the app
st.title("Stock News Generator")

# Input for stock symbol, converted to uppercase
symbol = st.text_input("Enter Stock Symbol").upper()

# Load API key securely (avoid hardcoding in production)
try:
    OPENAI_API_KEY = "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"  # Replace with a secure method like os.getenv("OPENAI_API_KEY")
except KeyError as e:
    st.error(f"Environment variable {e} not set. Please check your .env file or environment configuration.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Main app logic
if symbol:  # Ensure 'symbol' is defined before using it
    try:
        # List of prompts
        prompts = [
            f"Stock {symbol} short interest",
            f"What is the cost to borrow of {symbol} stock?",
            f"What is the lending rate of {symbol} stock?",
            f"What is the short volume of {symbol} stock?",
        ]

        # Iterate through prompts
        for prompt in prompts:
            # Display user prompt
            with st.chat_message("user"):
                st.write(prompt)

            # Initialize an empty article string
            article = ""

            # Get streaming response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.2,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            # Stream response chunks
            for chunk in response:
                if chunk.choices[0].delta.content:
                    article += chunk.choices[0].delta.content
                    time.sleep(0.1)  # Reduced sleep time for faster response

            # Display assistant's response
            if article:
                with st.chat_message("assistant"):
                    st.write(article)

    except Exception as e:
        st.error(f"An error occurred while generating the article: {e}")
