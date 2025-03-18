import pandas as pd
import os
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import ChatPromptTemplate  # Import the prompt template

def main():
        
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable.")

    # Load CSV data from a static file path using caching to avoid reloading
    @st.cache_data
    def load_data():
        return pd.read_csv('./cleaned_data/combined_df_after_fe_copy.csv')

    # Streamlit page title
    st.title("🤖 Chatbot for Reddit CSV")
    st.markdown("<h6> ⚠️ Due to Gemini API rate limits, CSV data has been truncated..</h6>", unsafe_allow_html=True)

    # Initialize chat history in streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Load the dataframe and store in session state if not already loaded
    if "df" not in st.session_state:
        st.session_state.df = load_data()

    st.write("CSV Preview:")
    st.dataframe(st.session_state.df.head())

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's message
    user_prompt = st.chat_input("Ask anything...")

    if user_prompt:
        # Add user's message to chat history and display it
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        # Define the prompt template using ChatPromptTemplate
        qa_prompt = ChatPromptTemplate.from_template(
            """You are an expert data assistant tasked with answering questions about a specific dataset. Your role is to provide accurate, concise, and helpful responses based solely on the dataset rows provided below. You will be given:
            - One or more rows from the dataset, each containing fields such as Title, Content, Author, and Date.
            - The user's question about the dataset.
            **Important**: Please ignore any columns that contain dictionary or list values or are related to images. Focus only on the columns with plain text or numeric data.

            **Instructions**:
            - Analyze the provided rows carefully and use them as your sole source of information.
            - If multiple rows are provided, synthesize the information to form a cohesive answer.
            - If the rows lack sufficient information to answer the question fully, clearly state: "The provided dataset rows do not contain enough information to answer this question."
            - Do not invent or assume information beyond what is given in the rows.
            - Keep your response clear, professional, and directly tied to the question.

            **Dataset Rows**:
            {retrieved_rows}

            **User's Question**:
            {user_query}

            **Response**:
            """
        )

        # Retrieve the rows of the dataset as CSV text
        retrieved_rows = st.session_state.df.head(1500).to_csv(index=False)
        
        # Format the prompt with the retrieved rows and the user query
        formatted_prompt = qa_prompt.format(retrieved_rows=retrieved_rows, user_query=user_prompt)
        
        # # Loading the Gemini LLM (Gemini 1.5 Flash)
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=GOOGLE_API_KEY)
        
        # llm = ChatOllama(model="llama2:latest", temperature=0)
        
        pandas_df_agent = create_pandas_dataframe_agent(
            llm,
            st.session_state.df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True
        )
        
        # Invoke the agent using the formatted prompt
        response = pandas_df_agent.invoke(formatted_prompt)
        assistant_response = response["output"]
        
        # Append and display the assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
