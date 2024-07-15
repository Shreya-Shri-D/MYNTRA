import streamlit as st
from PIL import Image
import numpy as np
import cv2
import base64
import pandas as pd
import plotly.express as px
import streamlit as st
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import seaborn as sns
from multimodal_search import MultimodalSearch
from VIRTUAL_TRIAL_ROOM import apply_mask


# Set page configuration
st.set_page_config(layout="wide")

def encode_image(image_path):
    with open(image_path, 'rb') as file:
        img_data = file.read()
    encoded_img = base64.b64encode(img_data).decode()
    return encoded_img

# Encode the images to base64
encoded_img = encode_image('Banner.jpg')
encoded_chat_img = encode_image('chat.jpg')
encoded_try_img = encode_image('try1.jpg')
encoded_trend_img = encode_image('trend.jpg')

# Custom CSS for styling
st.markdown(f"""
    <style>
    .navbar {{
        position: fixed;
        top: 0px;
        left: 0px;
        width: 100%;
        padding: 10px;
        background-color: #343a40;
        border-bottom: 1px solid #dee2e6;
        z-index: 100;
        display: flex;
        justify-content: space-between;
    }}
    .navbar a {{
        color: #ffffff;
        text-decoration: none;
        margin: 0 15px;
    }}
    .navbar a:hover {{
        text-decoration: underline;
    }}
    .content {{
        margin-top: 70px;
        padding: 20px;
    }}
    .hero-section {{
        background: url('data:image/jpg;base64,{encoded_img}') no-repeat center center;
        background-size: cover;
        height: 500px;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
    }}
    .hero-section h1 {{
        font-size: 4em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    .hero-section p {{
        font-size: 1.5em;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }}
    .feature-section {{
        display: flex;
        justify-content: space-around;
        padding: 50px 0;
        background-color: #f8f9fa;
    }}
    .feature {{
        text-align: center;
        max-width: 300px;
    }}
    .feature img {{
        width: 150px; /* Adjust according to your design */
        height: 150px; /* Adjust according to your design */
        object-fit: cover;
        border-radius: 50%;
    }}
    .feature h3 {{
        margin-top: 15px;
        font-size: 1.5em;
        color: #343a40;
        justify-content: center;
    }}
    .feature p {{
        margin-top: 10px;
        color: #6c757d;
    }}
    </style>
""", unsafe_allow_html=True)

# Custom HTML for navbar
st.markdown("""
    <nav class="navbar">
        <div>
            <a class="navbar-brand" href="?page=home">Home</a>
            <a class="navbar-brand" href="?page=fashiongpt">FashionGPT</a>
        </div>
        <div>
            <a class="navbar-brand" href="?page=vton">Try On</a>
        </div>
        <div>
            <a class="navbar-brand" href="?page=trendzy">Trendzy</a>
        </div>
    </nav>
""", unsafe_allow_html=True)

# Main Function to handle page navigation
def main():
    page = st.selectbox(
        "Select a page",
        ["Home", "FashionGPT", "Try On","Trendzy"]
    )

    if page == "Home":
        home_page()
    elif page == "FashionGPT":
        fashiongpt_page()
    elif page == "Try On":
        vton_page()
    elif page == "Trendzy":
        trendz_page()

# Home Page Function
def home_page():
    st.markdown(f"""
    <div class="hero-section">
       
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #343a40;'>Explore Our Features</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f"""
    <div class="feature-section">
        <div class="feature">
            <img src="data:image/jpg;base64,{encoded_chat_img}" alt="FashionGPT">
            <h3>FashionGPT</h3>
            <p>Your Style, Your Way</p>
        </div>
        <div class="feature">
            <img src="data:image/jpg;base64,{encoded_try_img}" alt="Virtual Try On">
            <h3>Virtual Try On</h3>
            <p>See It, Wear It, Love It</p>
        </div>
        <div class="feature">
            <img src="data:image/jpg;base64,{encoded_trend_img}" alt="Trendzy">
            <h3>    Trendzy</h3>
            <p>Stay Ahead of Fashion Trends</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("Done By Team HackerSpace")

# FashionGPT Page Function
def fashiongpt_page():
    st.markdown("<h1 style='text-align: center; color: black;'>FashionGPT</h1>", unsafe_allow_html=True)
    st.markdown("---")

    query = st.text_input("Enter your query:")
    if st.button("Search"):
        if len(query) > 0:
            multimodal_search = MultimodalSearch()
            results = multimodal_search.search(query)
            st.warning(f"Your query was '{query}'")
            st.subheader("Search Results:")
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                st.write(f"Score: {round(results[0].score*100, 2)}%")
                st.image(results[0].content, use_column_width=True)
            with col2:
                st.write(f"Score: {round(results[1].score*100, 2)}%")
                st.image(results[1].content, use_column_width=True)
            with col3:
                st.write(f"Score: {round(results[2].score*100, 2)}%")
                st.image(results[2].content, use_column_width=True)
        else:
            st.warning("Please enter a query.")

# VTON Page Function
def vton_page():
    st.markdown("<h1 style='text-align: center; color: black;'>Virtual Trial Room </h1>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_main_image = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png"])
    if uploaded_main_image is not None:
        original_image = np.array(Image.open(uploaded_main_image))
        st.image(original_image, caption='Original Image', width = 300)

        uploaded_design_image = st.file_uploader("Upload T-Shirt Design", type=["jpg", "jpeg", "png"])
        if uploaded_design_image is not None:
            design_image = np.array(Image.open(uploaded_design_image))
            st.image(design_image, caption='T-Shirt Design', width = 300)

            if st.button('Try on'):
                final_image = apply_mask(original_image, design_image)
                final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
                st.image(final_image_rgb, caption='Final Image with T-Shirt Design', width =300)

def trendz_page():
    # Load the CSV file
    df = pd.read_csv("Myntra Fasion Clothing.csv") 

    # Main page title with styled markdown
    st.markdown("<h1 class='title'>TRENDZY</h1>", unsafe_allow_html=True)
    st.markdown("---")  # Horizontal line for separation

    st.subheader("Top 10 Popular Brands")
    brand_counts = df['BrandName'].value_counts().head(10).reset_index()
    brand_counts.columns = ['BrandName', 'Count']

    # Create a bar chart with Plotly Express
    fig = px.bar(
        brand_counts,
        y='Count',
        color='BrandName'   
    )
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

    st.markdown("---")  # Horizontal line for separatio
    #-----------------------------------------------------------------------------------

    categories = df['Individual_category'].unique()
    selected_category = st.selectbox('Select a category', categories)

    top_brands = df[df['Individual_category'] == selected_category ]['BrandName'].value_counts().nlargest(10)
    st.header(f"Top Brands selling {selected_category}")

    fig = px.pie(values=top_brands.values, names=top_brands.index)
    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig)

    st.markdown("---")  # Horizontal line for separatio
    #-----------------------------------------------------------------------------------
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display a subheader for the distribution plot
    st.subheader("Distribution of Product Ratings")


    # Create a distribution plot (histogram) using matplotlib
    plt.figure(figsize=(10, 6))
    counts, bins, _ = plt.hist(df['Ratings'], bins=20, edgecolor='pink',color='purple')  # Adjust the number of bins as needed
    plt.xlabel('Ratings')
    plt.ylabel('Frequency')
    plt.title('Distribution of Product Ratings')

    # Plot a line connecting the tops of the histogram bars (wave form)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    plt.plot(bin_centers, counts, '-o', color='orange', linewidth=2, markersize=8)



    st.pyplot()

    st.markdown("---")  # Horizontal line for separation
    #-----------------------------------------------------------------------------------
    st.subheader("Highest Rating Products")

    top_rating_products = df.sort_values(by='Ratings', ascending=False).head(20)

    # Plot top rating products
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Category', y='Ratings', data=top_rating_products, palette='rocket')
    plt.xticks(rotation=90)
    plt.title('Top 20 Highest Rated Products')
    plt.xlabel('Product')
    plt.ylabel('Rating')
    st.pyplot()
    st.markdown("---")  # Horizontal line for separation
    #-----------------------------------------------------------------------------------

    st.markdown("---")






if __name__ == "__main__":
    main()
