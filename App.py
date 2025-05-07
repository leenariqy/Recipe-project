import streamlit as st
from recipe_finder import RecipeFinder
from typing import List

# Initialize session state and recipe finder
if 'finder' not in st.session_state:
    st.session_state.finder = RecipeFinder()

# Helper functions for UI
def display_recipe_details(name: str) -> None:
    """Display detailed information for a recipe."""
    recipe = st.session_state.finder.get_recipe_details(name)
    if recipe:
        st.subheader(name)
        st.write(f"**Cuisine:** {recipe['Cuisine']}")
        st.write("**Ingredients:**")
        for ingredient in recipe['Ingredients']:
            st.write(f"- {ingredient}")
        st.write(f"**Prep Time:** {recipe['Prep Time']} minutes")
        st.write(f"**Difficulty:** {recipe['Difficulty']}")
        st.write(f"**Rating:** {recipe['Rating']}" if recipe['Rating'] else "**Rating:** Not rated")
    else:
        st.error("Recipe not found.")

def display_recipe_list(recipes: List[str]) -> None:
    """Display a list of recipes with options to view details."""
    if recipes:
        for recipe in recipes:
            if st.button(recipe, key=f"btn_{recipe}"):
                display_recipe_details(recipe)
    else:
        st.warning("No recipes found matching your criteria.")

# Main application
def main():
    """Main Streamlit application function."""
    st.title("🍳 Recipe Finder System")
    st.write("Discover and manage your favorite recipes!")
    
    menu = [
        "Get Recommendations",
        "Search Recipes",
        "Filter Recipes",
        "Add New Recipe",
        "View All Recipes"
    ]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Get Recommendations":
        st.header("Get Recipe Recommendations")
        cuisine = st.text_input("Enter your preferred cuisine:")
        if cuisine:
            recommendations = st.session_state.finder.get_cuisine_recommendations(cuisine)
            if recommendations:
                st.success(f"Based on your love for {cuisine}, try these recipes:")
                display_recipe_list(recommendations)
            else:
                st.warning(f"No {cuisine} recipes found. Try another cuisine!")
    
    elif choice == "Search Recipes":
        st.header("Search Recipes")
        query = st.text_input("Enter recipe name (full or partial):")
        if query:
            results = st.session_state.finder.search_recipes(query)
            display_recipe_list(results)
    
    elif choice == "Filter Recipes":
        st.header("Filter Recipes")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty = st.selectbox(
                "Difficulty", 
                ["Any", "Easy", "Medium", "Hard"]
            )
            difficulty = None if difficulty == "Any" else difficulty
            
        with col2:
            max_time = st.slider(
                "Maximum Prep Time (minutes)", 
                0, 120, 60
            )
            max_time = None if max_time == 120 else max_time
            
        with col3:
            min_rating = st.slider(
                "Minimum Rating", 
                0.0, 5.0, 0.0, 0.1
            )
            min_rating = None if min_rating == 0.0 else min_rating
            
        if st.button("Apply Filters"):
            filtered = st.session_state.finder.filter_recipes(
                difficulty, max_time, min_rating
            )
            display_recipe_list(filtered)
    
    elif choice == "Add New Recipe":
        st.header("Add a New Recipe")
        with st.form("add_recipe_form"):
            name = st.text_input("Recipe Name*")
            cuisine = st.text_input("Cuisine*")
            ingredients = st.text_area(
                "Ingredients (one per line)*",
                help="Enter each ingredient on a new line"
            )
            prep_time = st.number_input("Prep Time (minutes)*", min_value=1)
            difficulty = st.selectbox(
                "Difficulty*", 
                ["Easy", "Medium", "Hard"]
            )
            rating = st.slider("Rating (optional)", 0.0, 5.0, 0.0, 0.1)
            rating = None if rating == 0.0 else rating
            
            submitted = st.form_submit_button("Add Recipe")
            if submitted:
                if not all([name, cuisine, ingredients, prep_time, difficulty]):
                    st.error("Please fill all required fields (*)")
                else:
                    ingredient_list = [i.strip() for i in ingredients.split('\n') if i.strip()]
                    success = st.session_state.finder.add_recipe(
                        name, cuisine, ingredient_list, prep_time, difficulty, rating
                    )
                    if success:
                        st.success(f"'{name}' added successfully!")
                    else:
                        st.error(f"A recipe with name '{name}' already exists.")
    
    elif choice == "View All Recipes":
        st.header("All Recipes")
        all_recipes = list(st.session_state.finder.recipes.keys())
        display_recipe_list(all_recipes)

if __name__ == "__main__":
    main()
