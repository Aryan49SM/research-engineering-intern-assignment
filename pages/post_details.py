import streamlit as st
import pandas as pd
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
import urllib.parse

# Get the post ID from query parameters
query_params = st.query_params
post_id = query_params.get("id")

# Check if an ID was provided
if not post_id:
    st.error("No post ID provided.")
    st.stop()

# Cache the data loading for performance
@st.cache_data
def load_data():
    return pd.read_csv('./cleaned_data/combined_df_after_fe_copy.csv')

# Load the dataset
df = load_data()

# Filter to get the specific row based on id_original
specific_row = df[df['id_original'] == post_id]

# Check if the post exists
if specific_row.empty:
    st.error("Post not found.")
    st.stop()

# Extract the post as a single row (Series)
post = specific_row.iloc[0]

# Display post details
st.title("📝 Post Details")
st.write("---")
st.markdown(f"### [{post['title_original']}](https://reddit.com/{post['permalink_original']})")

# Check and display media from 'url_overridden_by_dest_original'
url = post['url_overridden_by_dest_original']
if pd.notna(url):
    # Ensure the URL has a scheme (e.g., https://)
    if not urllib.parse.urlparse(url).scheme:
        url = 'https://' + url
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc.lower()
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()
    
    # List of common image extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
    
    # Check if the URL is an image
    if extension in image_extensions:
        st.markdown(
            f'<img src="{url}" alt="Attached Image" style="max-width:400px; height:auto;">',
            unsafe_allow_html=True
        )
    
    # Check if the URL is a YouTube video
    elif 'youtube.com' in domain or 'youtu.be' in domain:
        video_id = None
        if 'youtube.com' in domain and 'watch' in path:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            video_id = query_params.get('v', [None])[0]
        elif 'youtu.be' in domain:
            video_id = path.strip('/').split('?')[0]
        if video_id:
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            st.video(embed_url)
        else:
            st.write(f"Unable to parse YouTube video ID. View externally: [Click here]({url})")
    
    # For all other URLs, provide a clickable link
    else:
        st.write(f"Attached media: [View here]({url})")

# Display selftext if it exists and is not empty
if pd.notna(post['selftext_original']) and post['selftext_original'].strip() != '':
    st.write(post['selftext_original'])

st.write("")
st.write(f"**Author:** [{post['author_original']}](https://reddit.com/user/{post['author_original']})")
st.write(f"**Date:** {post['created_utc_original']}")
st.write("")
# Display the engagement matrix in a single row with emojis
cols = st.columns(4)
with cols[0]:
    st.markdown(f"👍 **Upvotes:** \n{post['ups_original']}")
with cols[1]:
    st.markdown(f"⭐ **Post Score:**\n{post['score_original']}")
with cols[2]:
    st.markdown(f"💬 **Comments:**\n{post['num_comments_original']}")
with cols[3]:
    st.markdown(f"🔁 **Crossposts:**\n{post['num_crossposts_original']}")

st.write("---")

# Create a single-row dataframe for the chatbot
single_row_df = specific_row

# Initialize the LLM with Google API key
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
if not GOOGLE_API_KEY:
    st.error("GEMINI_API_KEY not set. Please set it in your environment variables.")
    st.stop()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=GOOGLE_API_KEY)

# Create the pandas dataframe agent with the single-row dataframe
pandas_df_agent = create_pandas_dataframe_agent(
    llm,
    single_row_df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True
)

# Define the prompt template for the chatbot
qa_prompt = ChatPromptTemplate.from_template(
    """You are an expert data assistant tasked with answering questions about a specific dataset row. Your role is to provide accurate, concise, and helpful responses based solely on the dataset row provided below. You will be given:
    - One row from the dataset, containing fields such as Title, Content, Author, and Date.
    - The user's question about this row.
    **Important**: Focus only on the columns with plain text or numeric data. Ignore any columns that contain dictionary or list values or are related to images.

    **Instructions**:
    - Analyze the provided row carefully and use it as your sole source of information.
    - If the row lacks sufficient information to answer the question fully, clearly state: "The provided dataset row does not contain enough information to answer this question."
    - Do not invent or assume information beyond what is given in the row.
    - Keep your response clear, professional, and directly tied to the question.

    **Dataset Row**:
    {retrieved_row}

    **User's Question**:
    {user_query}

    **Response**:
    """
)

# Chat interface
st.write("### 💬 Chat with the Bot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's question
user_prompt = st.chat_input("Ask a question about this post...")

if user_prompt:
    # Add user's message to chat history
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # Convert the single row to CSV for the prompt
    retrieved_row = single_row_df.to_csv(index=False)
    
    # Format the prompt with the row data and user query
    formatted_prompt = qa_prompt.format(retrieved_row=retrieved_row, user_query=user_prompt)
    
    # Get the response from the agent
    response = pandas_df_agent.invoke(formatted_prompt)
    assistant_response = response["output"]
    
    # Add and display the assistant's response
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)