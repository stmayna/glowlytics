import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse
import kagglehub

# Set a background color and font style using HTML
st.markdown(
    """
    <style>
    .main {
        background-color: #fce4ec;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
path = kagglehub.dataset_download("kingabzpro/cosmetics-datasets")
data = pd.read_csv(f"{path}/cosmetics.csv")

# Sidebar for navigation
st.sidebar.title("🌸 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dataset Summary"])

if page == "Home":
    # User Inputs
    st.header("💖 Input Your Daily Skincare Routine")
    skin_type = st.selectbox("What's your skin type?", ["Combination", "Dry", "Normal", "Oily", "Sensitive"])
    concern = st.multiselect("What are your skin concerns?", 
                            ["Acne", "Aging", "Blackheads", "Dryness", "Dullness", "Pores"])
    
    cleanser = st.selectbox("Used Cleanser?", ["Yes", "No"])
    moisturizer = st.selectbox("Used Moisturizer?", ["Yes", "No"])
    sunscreen = st.selectbox("Used Sunscreen?", ["Yes", "No"])
    water_intake = st.slider("Water Intake (glasses)", 0, 15, 8)
    sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])

    # Product Recommendations based on skin type and concerns
    st.header("🌷 Personalized Product Recommendations")
    
    # Filter products based on skin type
    recommended_products = data[data[skin_type] == 1].copy()
    
    # Score products based on concerns
    recommended_products['relevance_score'] = 0
    
    # Create a scoring system based on product labels and concerns
    for c in concern:
        c = c.lower()
        recommended_products['relevance_score'] += recommended_products['Label'].str.lower().str.contains(c).astype(int)
        recommended_products['relevance_score'] += recommended_products['Ingredients'].str.lower().str.contains(c).astype(int)
    
    # Sort by relevance score and rank
    recommended_products = recommended_products.sort_values(['relevance_score', 'Rank'], ascending=[False, True])
    
    # Display top recommendations
    st.subheader("✨ Top Product Recommendations for Your Skin Type and Concerns:")
    top_recommendations = recommended_products.head(5)
    
    # Display recommendations in a more attractive format
    for _, product in top_recommendations.iterrows():
        with st.expander(f"{product['Name']} by {product['Brand']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Label:** {product['Label']}")
                st.write(f"**Rank:** {product['Rank']}")
                st.write(f"**Price:** ${product['Price']:.2f}")
                # Add hyperlinks to search by product name or brand
                product_name_encoded = urllib.parse.quote(product['Name'])
                brand_name_encoded = urllib.parse.quote(product['Brand'])
                search_by_name_url = f"https://incidecoder.com/search?query={product_name_encoded}"
                search_by_brand_url = f"https://incidecoder.com/search?query={brand_name_encoded}"
                st.markdown(f"[Search by Product Name]({search_by_name_url}) | [Search by Brand]({search_by_brand_url}) ")
            with col2:
                if product['relevance_score'] > 0:
                    st.write(f"Match Score: {product['relevance_score']}")

    # Routine Assessment
    st.header("🌺 Routine Assessment")
    
    # Create a scoring system for routine
    routine_score = 0
    feedback = []
    
    if cleanser == "Yes":
        routine_score += 20
        feedback.append("✅ Great job using a cleanser!")
    else:
        feedback.append("❌ Consider adding a cleanser to your routine")
        
    if moisturizer == "Yes":
        routine_score += 20
        feedback.append("✅ Good work with moisturizing!")
    else:
        feedback.append("❌ Adding a moisturizer could help your skin")
        
    if sunscreen == "Yes":
        routine_score += 20
        feedback.append("✅ Excellent sun protection!")
    else:
        feedback.append("❌ Don't forget your sunscreen")
        
    if water_intake >= 8:
        routine_score += 20
        feedback.append("✅ Great water intake!")
    else:
        feedback.append("❌ Try to drink more water")
        
    if sleep_hours >= 7:
        routine_score += 20
        feedback.append("✅ Good sleep habits!")
    else:
        feedback.append("❌ More sleep could benefit your skin")

    # Display routine assessment
    st.subheader("🌟 Your Skincare Routine Score")
    st.progress(routine_score/100)
    st.write(f"Overall Score: {routine_score}%")
    
    for msg in feedback:
        st.write(msg)

    # Price Analysis of Recommended Products
    st.header("💸 Price Analysis of Recommended Products")
    
    # Create a histogram for better understanding of price distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=recommended_products, x='Price', bins=20, kde=True, ax=ax)
    
    # Add labels and title for clarity
    ax.set_title('Price Distribution of Recommended Products')
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Number of Products')
    
    # Display the plot
    st.pyplot(fig)

elif page == "Dataset Summary":
    st.header("📊 Dataset Summary and Insights")

    # Add a redirect link to the dataset
    st.markdown("[View the full dataset on Kaggle](https://www.kaggle.com/datasets/kingabzpro/cosmetics-datasets/data)")

    # Display a sample of the dataset
    st.subheader("Sample of the Dataset")
    st.write("First 10 rows:")
    st.write(data.head(10))
    st.write("Last 10 rows:")
    st.write(data.tail(10))

    # Display basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Display top brands by product count
    st.subheader("Top Brands by Product Count")
    top_brands = data['Brand'].value_counts().head(10)
    st.bar_chart(top_brands)

    # Display average rank by skin type
    st.subheader("Average Rank by Skin Type")
    skin_types = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
    avg_rank_by_skin_type = {skin_type: data[data[skin_type] == 1]['Rank'].mean() for skin_type in skin_types}
    st.write(avg_rank_by_skin_type)

    # Distribution of Product Prices
    st.subheader("Distribution of Product Prices")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Price'], bins=30, kde=True, ax=ax)
    ax.set_title('Price Distribution')
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Top Ingredients by Frequency
    st.subheader("Top Ingredients by Frequency")
    ingredients = data['Ingredients'].str.split(',').explode().str.strip().value_counts().head(10)
    st.bar_chart(ingredients)

    # Average Price by Brand
    st.subheader("Average Price by Brand")
    avg_price_by_brand = data.groupby('Brand')['Price'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_price_by_brand)

    # Technologies Used
    st.header("🛠️ Technologies Used")
    st.write("""
    - **Streamlit**: A powerful tool for building interactive web applications 
      with Python. It's recommended for its simplicity and ability to quickly 
      turn data scripts into shareable web apps. Ideal for data scientists and 
      analysts who want to create dashboards and data visualizations without 
      needing extensive web development skills. 
      [Learn more about Streamlit](https://streamlit.io).
    - **Pandas**: Used for data manipulation and analysis. It provides 
      data structures and functions needed to work with structured data.
    - **NumPy**: A fundamental package for scientific computing with Python, 
      used here for numerical operations.
    - **Matplotlib & Seaborn**: Libraries for creating static, animated, and 
      interactive visualizations in Python. Seaborn is built on top of 
      Matplotlib and provides a high-level interface for drawing attractive 
      statistical graphics.
    - **KaggleHub**: A utility to download datasets directly from Kaggle, 
      simplifying the process of accessing and using datasets in your projects.
    """)