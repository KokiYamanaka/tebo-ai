import { fetchAndSaveIngrSummaryFromCache } from './api.js'; // Adjust path if needed

console.log('✅ getShopList.js loaded');

/**
 * Updates the shopping list UI with categorized ingredient data.
 * @param {object} data - The shopping list data object with categories as keys.
 */
function updateShoppingList(data) {
  const categories = ['Meat', 'Vegetables', 'Seasonings', 'Oils & Fats', 'Others'];
  const idMap = {
    'Meat': 'content-meat',
    'Vegetables': 'content-vegetables',
    'Seasonings': 'content-seasonings',
    'Oils & Fats': 'content-oils',
    'Others': 'content-others'
  };

  // Helper function to display a message (e.g., for loading or empty states)
  const showMessage = (container, message, isItalic = true) => {
    container.innerHTML = ''; // Clear previous content
    const p = document.createElement('p');
    // ✅ FIX: Removed 'text-white' class
    p.className = 'text-sm'; 
    if (isItalic) {
      p.classList.add('italic');
    }
    p.textContent = message;
    container.appendChild(p);
  };

  if (!data) {
    // If data is null/undefined, show an error in all panels
    categories.forEach(cat => {
      const container = document.getElementById(idMap[cat]);
      if (container) showMessage(container, 'Could not load items.');
    });
    return;
  }

  categories.forEach(cat => {
    const ingredients = data[cat] || [];
    const container = document.getElementById(idMap[cat]);
    if (!container) return;

    // Clear previous items before adding new ones
    container.innerHTML = '';

    // Add each ingredient to its category container
    if (ingredients.length === 0) {
      showMessage(container, 'No items');
    } else {
      ingredients.forEach(item => {
        const p = document.createElement('p');
        // ✅ FIX: Removed 'text-white' class
        p.className = 'text-sm';
        p.textContent = `${item.name}: ${item.quantity} (${item.store_package_price})`;
        container.appendChild(p);
      });
    }
  });
}

/**
 * Initializes the event listener for the 'Generate Shopping List' button.
 */
function initializeShoppingListButton() {
  const shoppingListButton = document.getElementById('btn-shopping-list');
  
  if (!shoppingListButton) {
    console.error('Shopping list button not found!');
    return;
  }

  shoppingListButton.addEventListener('click', async () => {
    const originalButtonText = shoppingListButton.textContent;
    shoppingListButton.disabled = true;
    shoppingListButton.textContent = 'Generating...';

    try {
      // 1. Call the imported function from api.js to get the data payload
      const shoppingData = await fetchAndSaveIngrSummaryFromCache();
      console.log('🧪 LocalStorage.RecipeData:', localStorage.getItem("RecipeData"));

      // 2. Update the UI with the fetched payload
      updateShoppingList(shoppingData);

    } catch (error) {
      console.error('Failed to generate shopping list:', error);
      updateShoppingList(null); // Clear the list and show an error state
      alert('Error: Could not generate the shopping list. Make sure a meal plan is selected.');
    } finally {
      // 3. Restore the button to its original state
      shoppingListButton.disabled = false;
      shoppingListButton.textContent = originalButtonText;
    }
  });
}

// Run the setup function when the script loads
initializeShoppingListButton();