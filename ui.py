import streamlit as st
from urllib.parse import quote_plus
from app import recipe_graph

st.set_page_config(page_title="🍳 AI Recipe Finder", page_icon="🍽️", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 14px;
        border: 1px solid #ccc;
        background-color: #2c2c2c;
        color: #f1f1f1;
    }
    .button-group {
        display: flex;
        gap: 10px;
        margin-top: 12px;
        flex-wrap: wrap;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #FF6F61;
        color: white;
        padding: 12px 20px;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #ff4c3b;
        transition: 0.3s;
    }
    .recipe-box {
        background-color: #fff1e6;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #f8d4c6;
        color: #333;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 20px;
    }
    .copy-button {
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        padding: 10px 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .copy-button:hover {
        background-color: #45a049;
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍳 AI-Powered Recipe Finder")
st.write("Enter the ingredients you have, and I’ll suggest a recipe for you!")

# Initialize session state
if "ingredients" not in st.session_state:
    st.session_state.ingredients = ""
if "recipe" not in st.session_state:
    st.session_state.recipe = ""
if "generated" not in st.session_state:
    st.session_state.generated = False

# Input field
st.session_state.ingredients = st.text_input(
    "📝 Ingredients (comma-separated):",
    placeholder="e.g. chicken, rice, garlic",
    value=st.session_state.ingredients
)

# Number of recipes dropdown
num_recipes = st.selectbox(
    "📑 How many recipes would you like?",
    options=[i for i in range(1, 11)],
    index=2
)

# Button group layout
st.markdown('<div class="button-group">', unsafe_allow_html=True)

# Generate Recipe button
if st.button("🔍 Generate Recipe"):
    user_input = st.session_state.ingredients.strip()
    if user_input == "":
        st.warning("Please enter some ingredients to proceed!")
    elif any(conj in user_input.lower() for conj in [" and ", " or ", "&"]):
        st.error("❌ Only comma-separated ingredient values are accepted.")
    else:
        try:
            with st.spinner("Cooking up some ideas... 🍽️"):
                state = {"user_input": user_input, "num_recipes": num_recipes}
                result = recipe_graph.invoke(state)
                st.session_state.recipe = result["final_output"]
                st.session_state.generated = True
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Clear button
if st.button("🧹 Clear"):
    if not st.session_state.ingredients and not st.session_state.recipe:
        st.info("Nothing to clear yet — please enter ingredients first.")
    else:
        st.session_state.ingredients = ""
        st.session_state.recipe = ""
        st.session_state.generated = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # Close button-group div

# Display recipe if generated
if st.session_state.recipe:
    st.markdown("<h3>🍽️ Here's your recipe:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='recipe-box'>{st.session_state.recipe}</div>", unsafe_allow_html=True)

    # Copyable text area
    with st.expander("📋 Copyable Recipe Text"):
        st.text_area("Copy this recipe:", value=st.session_state.recipe, height=300)

st.markdown("---")
st.write("👨‍🍳 Powered by LangGraph, Groq & Streamlit")
