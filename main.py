import streamlit as st
import pages.posts as posts
import pages.dashboard as dashboard
import pages.chat_bot as chat_bot

def main():            
    # Set page title and layout
    st.set_page_config(
        page_title="Reddit Analysis Dashboard", 
        page_icon=":bar_chart:",
        layout="wide"
    )
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("", ["Dashboard", "Posts", "CSV Chat bot"])

    if selection == "Dashboard":
        dashboard.main()
    elif selection == "Posts":
        posts.main()
    else:
        chat_bot.main()

if __name__ == "__main__":
    main()