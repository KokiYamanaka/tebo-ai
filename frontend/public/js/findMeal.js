import { fetchAndSaveRecipe } from './api.js';

console.log('✅ findMeal.js loaded');

// 2. Reusable single-card populator
function populateRecipe(data, cardElement) {
  cardElement.querySelector('.card-title').textContent = data.title;
  cardElement.querySelector('.card-desc').textContent  = data.description;

  const img = cardElement.querySelector('.card-image');
  if (img) img.src = data.image_url;

  const link = cardElement.querySelector('.card-link');
  if (link && data.link) link.href = data.link;
}



// 3. Fill all four cards in order
function populateAllRecipes(dataArray) {
const cards = document.querySelectorAll('.card');
cards.forEach((card, i) => {
  if (dataArray[i]) populateRecipe(dataArray[i], card);
});
}

// 4. Wire up the button
function setupMealPlanButton() {
  const button = document.getElementById('btn-find-plan');
  const input = document.getElementById('recipe-input');

  if (!button || !input) return;

  button.addEventListener('click', async () => {
    const userText = input.value.trim();
    if (!userText) return;

    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = 'AI finding recipes...';

    try {
      // 1️⃣ Fetch from API using user input
      const data = await fetchAndSaveRecipe(userText);

      // 2️⃣ Extract recipes array (from `data.results`)
      const recipes = data.results.map(item => ({
        title: item.title_en,
        description: "",
        image_url: item.image_url,
        link: item.url_en || item.url
      }));

      // 3️⃣ Fill the UI
      populateAllRecipes(recipes);
    } catch (err) {
      console.error("❌ Failed to fetch recipes:", err);
      alert("Error: Could not find recipes. Please try again.");
    } finally {
      button.disabled = false;
      button.textContent = originalText;
    }
  });
}



setupMealPlanButton(); // 🔁 Trigger once on load
