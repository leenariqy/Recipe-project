import json
from pathlib import Path
from typing import Dict, List, Union

# Type aliases for better code readability
Recipe = Dict[str, Union[str, int, float, List[str]]]
RecipeDatabase = Dict[str, Recipe]

class RecipeFinder:
    """Main class for handling recipe operations."""
    
    def __init__(self, data_file: str = "data/recipes.json"):
        """Initialize with path to recipe data file."""
        self.data_file = Path(data_file)
        self.recipes = self._load_recipes()
        
    def _load_recipes(self) -> RecipeDatabase:
        """Load recipes from JSON file or use sample data if file doesn't exist."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return sample data if file doesn't exist or is invalid
            return {
                'Spaghetti Carbonara': {
                    'Cuisine': 'Italian',
                    'Ingredients': ['Pasta', 'Eggs', 'Cheese', 'Bacon'],
                    'Prep Time': 20,
                    'Difficulty': 'Medium',
                    'Rating': 4.5
                },
                'Chicken Tikka Masala': {
                    'Cuisine': 'Indian',
                    'Ingredients': ['Chicken', 'Yogurt', 'Spices', 'Tomato Sauce'],
                    'Prep Time': 45,
                    'Difficulty': 'Hard',
                    'Rating': 4.8
                },
                'Avocado Toast': {
                    'Cuisine': 'American',
                    'Ingredients': ['Bread', 'Avocado', 'Salt', 'Pepper'],
                    'Prep Time': 5,
                    'Difficulty': 'Easy',
                    'Rating': 3.7
                }
            }
    
    def save_recipes(self) -> None:
        """Save current recipes to JSON file."""
        self.data_file.parent.mkdir(exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, indent=4)
    
    def get_cuisine_recommendations(self, cuisine: str) -> List[str]:
        """Return recipe names matching the given cuisine."""
        return [name for name, recipe in self.recipes.items() 
                if recipe['Cuisine'].lower() == cuisine.lower()]
    
    def search_recipes(self, query: str) -> List[str]:
        """Search recipes by name (partial or full match)."""
        return [name for name in self.recipes.keys() 
                if query.lower() in name.lower()]
    
    def filter_recipes(self, difficulty: str = None, max_time: int = None, 
                      min_rating: float = None) -> List[str]:
        """
        Filter recipes by difficulty, max prep time, and min rating.
        Any parameter can be None to skip that filter.
        """
        filtered = []
        
        for name, recipe in self.recipes.items():
            matches = True
            
            if difficulty and recipe['Difficulty'].lower() != difficulty.lower():
                matches = False
            if max_time and recipe['Prep Time'] > max_time:
                matches = False
            if min_rating and recipe['Rating'] < min_rating:
                matches = False
                
            if matches:
                filtered.append(name)
                
        return filtered
    
    def get_recipe_details(self, name: str) -> Union[Recipe, None]:
        """Get full details for a specific recipe."""
        return self.recipes.get(name)
    
    def add_recipe(self, name: str, cuisine: str, ingredients: List[str], 
                   prep_time: int, difficulty: str, rating: float = None) -> bool:
        """Add a new recipe to the database."""
        if name in self.recipes:
            return False  # Recipe already exists
            
        self.recipes[name] = {
            'Cuisine': cuisine,
            'Ingredients': ingredients,
            'Prep Time': prep_time,
            'Difficulty': difficulty,
            'Rating': rating
        }
        self.save_recipes()
        return True

# Example usage (for testing)
if __name__ == "__main__":
    finder = RecipeFinder()
    print("Italian recipes:", finder.get_cuisine_recommendations("Italian"))
    print("Recipes with 'Chicken':", finder.search_recipes("Chicken"))
    print("Easy recipes under 30 mins:", 
          finder.filter_recipes(difficulty="Easy", max_time=30))
