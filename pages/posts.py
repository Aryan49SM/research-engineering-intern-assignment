import streamlit as st
import pandas as pd

def main():
    # Cache the data loading for performance
    @st.cache_data
    def load_data():
        return pd.read_csv('./cleaned_data/combined_df_after_fe_copy.csv')

    # Load the dataset
    df = load_data()

    # Initialize session state for pagination
    if 'rows_to_show' not in st.session_state:
        st.session_state['rows_to_show'] = 1000

    # Page title
    st.title("📋 Reddit Post Overview")
    st.write("---")

    # Display posts up to the current number of rows to show
    for index, row in df.head(st.session_state['rows_to_show']).iterrows():
        with st.container():
            # Create a URL to the dashboard page with the post's id_original
            url = f"/post_details?id={row['id_original']}"
            
            # Use smaller font size for the title
            st.markdown(
                f'<h5>{index+1}. <a href="{url}" target="_self"> {row["title_original"]}</a></h5>',
                unsafe_allow_html=True
            )
            
            # Show a preview of the selftext (first 200 characters) with smaller font
            st.markdown(
                f'<p style="font-size: 5px; color: gray;">{str(row.get("selftext", ""))[:200]}...</p>',
                unsafe_allow_html=True
            )

    # Button to load more posts if there are more rows to display
    if st.session_state['rows_to_show'] < len(df):
        if st.button("Load more"):
            st.session_state['rows_to_show'] += 1000
            if st.session_state['rows_to_show'] > len(df):
                st.session_state['rows_to_show'] = len(df)
            # No explicit rerun needed; Streamlit automatically reruns on widget interaction.

    # Instructions for the user
    st.markdown('<p style="font-size: 14px;">🔗 <em>Click on the post title to view full details.</em></p>', unsafe_allow_html=True)
