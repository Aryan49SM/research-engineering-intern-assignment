# Data Analysis and Visualization of Reddit Posts

## Overview

This project analyzes reddit posts to uncover patterns in engagement, source reliability, and crossposting behavior. Starting with a raw JSON dataset, the project involves data cleaning, preprocessing, exploratory data analysis (EDA), feature engineering, and culminates in an interactive Streamlit application. The application allows users to explore the data visually and query it interactively, providing insights into reddit posts dynamics.

## Data Cleaning

The project begins with a raw dataset in JSONL format, featuring nested structures, especially in the "crosspost" fields. The cleaning process includes:

- **Flattening Nested JSON:** Using json_normalize to convert nested JSON into a flat, tabular structure for easier analysis.
- **Handling Dynamic Crosspost Nesting:** A recursive function extracts data from varying levels of nesting in crosspost fields, ensuring no information is lost.
- **Dropping Irrelevant Columns:** Redundant or unnecessary columns (e.g., image previews, excess metadata) are removed to focus on key data.
- **Ensuring Consistency:** Timestamps are converted to datetime objects, data types are standardized, and duplicates are eliminated.

  
## Data Preprocessing

The dataset is preprocessed to prepare it for analysis:

- **Missing Values:**
    - Columns with <5% missing data are imputed with the mean (numerical) or mode (categorical).
    - Columns with >80% missing data are dropped unless critical to the analysis.
- **Data Type Corrections:** Ensures proper types, such as integers for counts and strings for text fields.
- **Feature Preparation:** Sets the stage for feature engineering by organizing the data into a usable format.

## Exploratory Data Analysis (EDA)

EDA reveals trends and relationships in the data through visualizations:

- **Histograms:** Show distributions of engagement metrics (e.g., upvotes, comments).
- **Bar Plots:** Compare post frequency across subreddits and the prevalence of unreliable domains.
- **Scatter Plots:** Examine relationships, such as upvotes vs. comments.
- **Heatmaps:** Display correlations between numerical features.
- **Line Plots:** Track temporal trends, like post volume over time.

Key observations include higher engagement for unreliable domains and subreddit-specific content patterns.

## Feature Engineering

New features are created to enrich the analysis:

- ```is_unreliable_domain```: Binary flag indicating if a post’s domain is unreliable, based on a predefined list.
- ```title_length``` and ```selftext_length```: Measures of post title and content length to assess their effect on engagement.
- ```is_breaking_news```: Identifies posts tagged as breaking news.
- ```time_lag_hours```: Time difference between a post and its crossposts.
- ```ups_per_subscriber``` and ```comments_per_subscriber```: Normalized engagement metrics based on subreddit subscriber counts.

## Streamlit Application

The project concludes with an interactive Streamlit app:

- **Data Visualization:** Displays EDA plots (e.g., histograms, scatter plots) for user exploration.
- **Chatbot:** Query the whole CSV file OR the selected any post

## Key Insights

- Posts from unreliable domains often garner more upvotes and comments than reliable ones.
- Specific subreddits show a higher tendency to share unreliable content, suggesting moderation focus areas.
- A strong positive correlation exists between comments and upvotes, indicating discussion drives popularity.

## Potential Improvements
- **Sentiment Analysis:** Adding sentiment scoring to posts and comments for tone insights.
- **Expanded Dataset:** Including more sources or time periods for broader trends.
- **Dynamic Reliability Model:** Developing a custom model to classify domain reliability instead of using a static list.

## Run the Project


1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aryan49SM/research-engineering-intern-assignment.git
   cd research-engineering-intern-assignment
   ```
   
2. **Create and Activate a Virtual Environment**
  
  ```bash
    python -m venv venv
    venv\Scripts\activate    # On Windows:
    source venv/bin/activate    # On macOS/Linux:
   ```

3. **Install the Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a ```.env``` file in the root directory and add:

   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application

  ```bash
  streamlit run app.py
  ```

