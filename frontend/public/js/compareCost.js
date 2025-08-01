console.log('✅ compareCost.js loaded');

document.addEventListener("DOMContentLoaded", () => {
  const costButton = document.getElementById('btn-cost-breakdown');

  function renderCostCards() {
    // Always comes back as a string (or null)
    const rawDataString = localStorage.getItem('IngredientSummary');
    console.log('📦 Type of rawDataString:', typeof rawDataString);
    console.log('🔍 Raw data from localStorage:', rawDataString);

    if (!rawDataString) {
      console.warn('⚠️ No IngredientSummary found in localStorage.');
      return;
    }

    let parsedData;
    try {
      // parse the JSON string into an object
      parsedData = JSON.parse(rawDataString);
    } catch (error) {
      console.error('❌ Invalid JSON in localStorage:', error);
      return;
    }

    // Safely pull out Num_Servings, defaulting to '--' if missing or not a number
    const servingsRaw = parsedData.Num_Servings;
    const servings = (typeof servingsRaw === 'string' || typeof servingsRaw === 'number')
      ? servingsRaw
      : '--';
    console.log('🔍 Parsed servings:', servings);

    const servingsNum = parseFloat(servings);
    const isValidNumber = !isNaN(servingsNum);

    // constants
    const yourPerServing = 5.00;
    const helloFreshPerServing = 10.99;

    // calculations
    const yourTotal = isValidNumber
      ? (yourPerServing * servingsNum).toFixed(2)
      : '--';
    const helloFreshTotal = isValidNumber
      ? (helloFreshPerServing * servingsNum).toFixed(2)
      : '--';
    const savingsPerServing = (helloFreshPerServing - yourPerServing).toFixed(2);
    const savingsTotal = isValidNumber
      ? (helloFreshPerServing * servingsNum - yourPerServing * servingsNum).toFixed(2)
      : '--';

    // helper to update an element’s textContent
    const update = (id, value) => {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    };

    // write results into the DOM
    update('num-servings-table', servings);
    update('you-per-serving', `$${yourPerServing.toFixed(2)}`);
    update('you-total-serving', isValidNumber ? `$${yourTotal}` : '--');
    update('hellofresh-total', isValidNumber ? `$${helloFreshTotal}` : '--');
    update('savings-per-serving', `$${savingsPerServing}`);
    update('savings-total', isValidNumber ? `$${savingsTotal}` : '--');
  }

  costButton?.addEventListener('click', renderCostCards);
  renderCostCards(); // initial render
});
