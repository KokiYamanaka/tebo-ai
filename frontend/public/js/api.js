// API URLS
const API_URL_RECIPE = "https://aircook-light.onrender.com/get-recipe";
const API_URL_INGREDIENTS = "https://aircook-light.onrender.com/summarize-ingredients";

// ==============================
// 📦 Section: API Functions Definitions
// ==============================

// IN : text 
// OUT :  x4 recommended recipes
export async function fetchRecipeFromText(text) {
  try {
    const url = `${API_URL_RECIPE}`;
    const payload = { text };

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Server error:", response.status, errorData);
      throw new Error(errorData.detail || errorData.message || "Unknown error");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error calling API:", error);
    throw error;
  }
}

// in : x4 recommended recipes
// out : aggregrated ingredients + quantities, total cost 
export async function generateIngredientSummary(data) {
  try {
    const response = await fetch(API_URL_INGREDIENTS, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Request failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching ingredients:", error);
    throw error;
  }
}


// ==============================
// 📦 Section: API Functions + save to browser memory
// ============================== 

export async function fetchAndSaveRecipe(text) {
  const data = await fetchRecipeFromText(text);
  localStorage.setItem("RecipeData", JSON.stringify(data));
  return data; // return for immediate use if needed
}


export async function fetchAndSaveIngrSummaryFromCache() {
  const raw = localStorage.getItem("RecipeData");

  if (!raw) {
    throw new Error("No RecipeData found in localStorage.");
  }

  const latestRecipeData = JSON.parse(raw);

  const data = await generateIngredientSummary(latestRecipeData);
  localStorage.setItem("IngredientSummary", JSON.stringify(data));
  return data;
}
