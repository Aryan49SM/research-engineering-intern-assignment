import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os
import json

def main():

    # Section navigation
    st.sidebar.markdown("## Dashboard Sections")
    sections = {
        'Description': "#description",
        'Time Patterns': "#time-patterns",
        'Community Spread': "#community-spread",
        'User Engagement': "#user-engagement",
        'Author Behavior': "#author-behavior",
        'Content Analysis': "#content-analysis"
    }

    for section, link in sections.items():
        st.sidebar.markdown(f"[{section}]({link})", unsafe_allow_html=True)

    # JavaScript for smooth scrolling
    scroll_script = """
    <script>
        function scrollToSection(id) {
            document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
        }
    </script>
    """
    st.markdown(scroll_script, unsafe_allow_html=True)

    # Header and Introduction
    st.title("Reddit Analysis Dashboard 🔎")

    st.header("Description", anchor="description")
    st.markdown("""
    This dashboard examines Reddit posts across various communities. The analysis tracks posting patterns and content characteristics to provide insights into user behavior and discussion trends.

    The dashboard includes post metrics, community statistics, and content analysis features such as topic classification and sentiment evaluation.

    The analysis covers:
    - **Time Patterns**: When misinformation appears and peaks
    - **Community Spread**: How content moves between subreddits,domains through crosspost
    - **User Engagement**: Reactions through votes and comments
    - **Content Analysis**: Language patterns and emotional tone
    - **Author Behavior**: Characteristics of users sharing unreliable content
    """, unsafe_allow_html=True)

    # Section 1: Time Patterns
    st.header("Time Patterns", anchor="time-patterns")

    st.write("### Daily Posting Trends by Reliability")
    st.write("This line chart tracks the number of posts per day, segmented by domain reliability (reliable vs. unreliable)")

    with st.expander("📈 What does this data reveal?"):
        st.markdown("""Spikes in posting activity, particularly from unreliable sources, can indicate significant events to spread content.
                    For example, a surge in unreliable posts might align with a news cycle or coordinated campaign.""")

    with open("plots/info_spread/daily_posting_trends.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)
        
    st.write("### Hourly Posting Heatmap")
    st.write("This heatmap visualizes posting frequency across days of the week and hours of the day, with darker shades representing higher activity.")

    with st.expander("📈 What does this data reveal?"):
        st.markdown("""Patterns such as increased posting during specific hours (e.g., 3-7 PM) could suggest activity or contributions from users in different time zones, hinting at coordinated behavior.""")

    with open("plots/info_spread/posting_heatmap.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)    

    # Section 2: Community Spread
    st.header("Community Spread", anchor="community-spread")
    st.write("### Subreddit Frequency Distribution")
    st.write("This bar chart displays the number of posts across ten politically-focused subreddits.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""Several major subreddits (neoliberal, politics, worldpolitics, socialism) show similar high post volumes of approximately 1,000 posts each, indicating these are primary hubs for political discourse. """)

    with open("plots/subreddit/subreddit_frequency.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)
        
        
    st.write("### Top Subreddits for Unreliable Content")
    st.write("This bar chart ranks the top 10 subreddits with the highest proportion of posts from unreliable domains.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""Communities with taller bars (Republican, Conservative) are hotspots for unreliable content, making them prime candidates for monitoring or intervention. """)

    with open("plots/subreddit/top_unreliable_subs.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)
        
        
    st.write("### Domain Frequency Analysis")
    st.write("This comprehensive three-panel visualization provides a detailed breakdown of content sources shared across political subreddits, comparing reliable and unreliable domains.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""The dominance of "self." domains suggests Reddit users engage more with platform-native content rather than external sources, potentially indicating greater trust in community-generated content over traditional media.""")

    with open("plots/engagement_analysis/top_domains_analysis.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)
        


    # Section 3: User Engagement
    st.header("User Engagement", anchor="user-engagement")
    st.write("### Engagement rate of post by Subreddit")
    st.write("This multi-line chart tracks engagement rates across ten political subreddits over approximately seven months, with each community represented by a uniquely colored line.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""While most communities maintained relatively stable engagement rates through 2024, nearly all experienced significant increases beginning in January 2025, with Liberal (blue), Republican (light blue), and neoliberal showing the most dramatic growth.""")

    with open("plots/engagement_analysis/engagement_rate.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)

    st.write("### Engagement Distribution")
    st.write('This violin plot displays the distribution of upvotes for posts from reliable domains (blue, labeled "false") and unreliable domains (orange, labeled "true"), with the width of each "violin" representing the frequency density at different upvote levels.')

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""reliable domains achieve the highest absolute upvote counts (approximately 50,000), unreliable domains also demonstrate the capacity to reach substantial engagement peaks exceeding 30,000 upvotes. This suggests that while misleading content may not typically outperform reliable content, it can occasionally achieve viral popularity comparable to legitimate sources.""")

    with open("plots/engagement_analysis/upvote_distribution.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)


    st.write("### Sentiment-Engagement Patterns")
    st.write("This scatter plot positions each post according to its title's sentiment score (x-axis, ranging from -1 for negative to +1 for positive) and the number of upvotes received (y-axis, ranging from 0 to approximately 50,000), with partial transparency to reveal density patterns where points overlap.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""The visualization reveals that the highest-upvoted content (exceeding 40,000 upvotes) comes exclusively from reliable sources, with only one unreliable source post reaching approximately 35,000 upvotes. This suggests that while unreliable content can achieve significant engagement, the most viral content on the platform predominantly comes from trusted sources.""")

    with open("plots/engagement_analysis/upvotes_vs_sentiment.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)



    # Section 4: Author Behavior
    st.header("Author Behavior", anchor="author-behavior")
    st.write("### Crosspost Connection Network")
    st.write("This directed network graph represents Reddit users as nodes (circles) with size proportional to their connectivity degree (number of connections), represents the crosspost between different users")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""Several prominent users (represented by larger circles) dominate the network structure, particularly the largest node function as a primary content propagation center. We can clearly observe that there are very few instances of unreliable content being crossposted.""")

    with open("plots/author_behavior/crosspost_network.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)


    st.write("### User Contribution for unreliable content")
    st.write("This vertical bar chart ranks the top 10 authors by number of posts from unreliable domains")

    with st.expander("📈 What does this data reveal?"):
            st.markdown(""" The visualization reveals extreme concentration of unreliable content posting, with user "M_i_c_K" responsible for approximately 100 posts – roughly 5 times more than the second-highest contributor. """)

    with open("plots/author_behavior/top_authors_posting_unreliable_domains.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)
        
        
        
        

    # Section 5: Content Analysis
    st.header("Content Analysis", anchor="content-analysis")
    st.write("### Average title sentiment over time")
    st.write("This line chart plots average daily sentiment scores of post titles over time, the sentiment scale ranges from -1 (negative) to +1 (positive), with 0 representing neutral sentiment.")

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""The most dramatic sentiment spikes occur in November 2024, potentially coinciding with the U.S. presidential election period, where sentiment rapidly oscillates between strongly positive and negative values within days.""")

    with open("plots/text_and_sentiment/avg_title_sentiment_over_time.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)


    st.write("### Sentiment Distribution Patterns")
    st.write('This box plot displays the distribution of title sentiment scores for posts from reliable domains (blue, labeled "false") and unreliable domains (orange, labeled "true") on a scale from -1 (negative) to +1 (positive).')

    with st.expander("📈 What does this data reveal?"):
            st.markdown("""Both distributions show similar median values indicating similar sentiment bias across political content regardless of source reliability. This suggests that emotional tone analysis, would be insufficient as a standalone approach for identifying potential misinformation.""")

    with open("plots/text_and_sentiment/title_sentiment.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, width=2000, scrolling=True)





    st.write("### Terminology Patterns")
    st.write(" This word cloud positions terms by frequency with size proportional to usage count.")

    with st.container():
        with st.expander("📈 What does this data reveal?"):
            st.markdown(""""Trump" appears as one of the most dominant terms, significantly larger than "Biden," indicating disproportionate focus on the former president in political discussions from reliable sources. This asymmetric attention suggests that Trump continued to be a central figure in political discourse.""")

        col1, col2= st.columns(2)
        with col1:
            st.write("#### Reliable domain wordcloud")
            st.image("plots/text_and_sentiment/reliable_titles.png", use_container_width=True)
        with col2:
            st.write("#### Unreliable domain wordcloud")
            st.image("plots/text_and_sentiment/unreliable_tiles.png", use_container_width=True)
            