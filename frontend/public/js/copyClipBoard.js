console.log('==copyClipBoard.js  loaded');


// ===========================
// 🛒 Format function 
// ===========================
// 📄 Format recipe data into HTML + plain versions
function formatRecipesList(recipeData) {
  try {
    const data = typeof recipeData === "string"
      ? JSON.parse(recipeData)
      : recipeData;
    const results = data.results || [];

    return results.map((recipe, idx) => {
      const title = recipe.title_en?.trim() || "(no title)";
      const url = recipe.url_en?.trim() || "";
      return {
        plain: `${idx + 1}. ${title}: ${url}`,
        html: `${idx + 1}. ${title}: <a href="${url}">Link</a>`
      };
    });
  } catch {
    return [{
      plain: "# recipes\n(No valid recipes found)",
      html: "# recipes<br>(No valid recipes found)"
    }];
  }
}
function renderIngredientText(data) {
  let output = [`# Ingredients To Shop`];

  for (const category in data) {
    if (category.startsWith("Total_") || category === "Num_Servings") continue;

    output.push(`## ${category}`);
    data[category].forEach(item => {
      output.push(`- ${item.name} : ${item.quantity}`);
    });
  }

  if ("Num_Servings" in data) {
    output.push(`\n# num servings`);
    output.push(`- ${data["Num_Servings"]}`);
  }

  return output.join("\n");
}

// ===========================
// apply format to copy clipboard
// =========================== 

// 🔗 Set up copy button with clipboard-polyfill
// 🔗 Set up copy button with clipboard-polyfill
function setupCopyButton() {
  const button = document.getElementById('btn-copy-plan');
  if (!button) return;

  button.addEventListener('click', () => {
    const recipeRaw     = localStorage.getItem("RecipeData");
    const ingredientRaw = localStorage.getItem("IngredientSummary");

    if (!recipeRaw || !ingredientRaw) {
      console.warn("🔍 Missing data—cannot copy:", {
        RecipeData: recipeRaw,
        IngredientSummary: ingredientRaw
      });
      return;
    }

    // Build the text to copy
    const recipeEntries  = formatRecipesList(recipeRaw);
    const recipePlain    = recipeEntries.map(e => e.plain).join('\n');
    const ingredientText = renderIngredientText(JSON.parse(ingredientRaw));
    const plainText      = `# Recipes\n${recipePlain}\n\n${ingredientText}`;

    const showSuccess = () => {
      const msg = document.getElementById("copyMessage");
      if (msg) {
        msg.classList.remove("hidden");
        setTimeout(() => msg.classList.add("hidden"), 2000);
      }
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      // Modern API
      navigator.clipboard.writeText(plainText)
        .then(showSuccess)
        .catch(err => console.error("❌ Clipboard copy failed:", err));
    } else {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = plainText;
      textarea.style.position = 'fixed'; // avoid scroll jump
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();

      try {
        document.execCommand('copy');
        showSuccess();
      } catch (err) {
        console.error("❌ execCommand copy failed:", err);
      }

      document.body.removeChild(textarea);
    }
  });
}

document.addEventListener('DOMContentLoaded', setupCopyButton);




