from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import List, Any
from dotenv import load_dotenv
import pandas as pd
import os

# Load .env variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load HuggingFace embedding model (set device if GPU is available)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # or "cuda"
)

# Load recipes dataset
csv_path = "Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
recipes = pd.read_csv(csv_path, usecols=["Title", "Cleaned_Ingredients", "Instructions"])
recipes.dropna(subset=["Title", "Cleaned_Ingredients", "Instructions"], inplace=True)
recipes = recipes.head(50)

# Initialize Chroma vector store
db = Chroma(
    embedding_function=embeddings,
    persist_directory="./recipe_index"
)

# Batch insert recipes to vector store
batch_size = 16
texts, metadatas = [], []

for idx, recipe in recipes.iterrows():
    content = f"{recipe['Title']} - Ingredients: {recipe['Cleaned_Ingredients']}"
    metadata = {
        "title": recipe['Title'],
        "instructions": recipe['Instructions']
    }
    texts.append(content)
    metadatas.append(metadata)

    if len(texts) == batch_size:
        db.add_texts(texts, metadatas=metadatas)
        print(f"✅ Added batch up to {idx+1}")
        texts, metadatas = [], []

if texts:
    db.add_texts(texts, metadatas=metadatas)
    print("✅ Added final batch.")

print("✅ All recipes added to vector database.")

# Recipe retrieval function
def retrieve_recipes(user_input, k=3):
    return db.similarity_search(user_input, k=k)

# Load Groq LLM
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-70b-8192")

# Define LangGraph state schema
class RecipeState(BaseModel):
    user_input: str
    ingredients: str = ""
    retrieved_recipes: List[Any] = []
    final_output: str = ""
    num_recipes: int = 3

# Build LangGraph workflow
graph = StateGraph(state_schema=RecipeState)

def get_ingredients(state: RecipeState):
    return {"ingredients": state.user_input}

def fetch_recipes(state: RecipeState):
    results = retrieve_recipes(state.ingredients)
    return {"retrieved_recipes": results}

def generate_response(state: RecipeState):
    prompt = f"""You are a responsible AI chef. 
You must only generate recipes for edible, legal, and safe ingredients. 
If a provided ingredient is inappropriate or unknown, respond: 'Ingredient not recognized as safe for consumption.' 
Do not attempt to make recipes with human parts, unsafe items, or unverified terms.
Mention the **name of place/country** where the recipe is popular, compulsorily and the **source of your knowledge** for each recipe.

The user has provided the following ingredients: {state.ingredients}

Based on these ingredients, and referring to similar recipes listed below, suggest **{state.num_recipes} new, creative recipe ideas** the user could try. 
Also mention the exact or approximate **quantity** of the ingredients. 
Do not say the user provided a recipe. If an ingredient is not a known food item, respond by saying 'Unknown ingredient: <term>' and skip it in the recipe. 
Only generate recipes for common, edible food ingredients. If any ingredient appears unethical, illegal, or non-consumable (like human organs), refuse to generate a recipe and respond with an appropriate message.
Only refer to the ingredients provided.

Remember, you are a chef, not a doctor or scientist. Focus on culinary creativity and safety. Also, do not generate same recipes multiple times.

After each recipe, include a YouTube video search link in this exact format:
YouTube Video Link: https://www.youtube.com/results?search_query=RECIPE_TITLE+recipe

Where RECIPE_TITLE is the exact name of that recipe.

Similar recipe inspirations:
"""
    for recipe in state.retrieved_recipes:
        prompt += f"\n- {recipe.metadata['title']}: {recipe.metadata['instructions']}\n"

    prompt += "\nNow, suggest your recipes in a clear, numbered list format with steps."

    response = llm.invoke(prompt).content
    return {"final_output": response}

# Add graph nodes
graph.add_node("get_ingredients", get_ingredients)
graph.add_node("fetch_recipes", fetch_recipes)
graph.add_node("generate_response", generate_response)

# Connect graph edges
graph.add_edge("get_ingredients", "fetch_recipes")
graph.add_edge("fetch_recipes", "generate_response")
graph.add_edge("generate_response", END)
graph.set_entry_point("get_ingredients")

# Compile and execute graph
recipe_graph = graph.compile()
