console.log("ga4Feedback.js loaded")
  // Track Find Meal Plan click
  document.getElementById('btn-find-plan')?.addEventListener('click', () => {
    gtag('event', 'click_find_meal_plan', {
      event_category: 'engagement',
      event_label: 'Find Meal Plan Button'
    });
  });

  // Track Generate Shopping List click
  document.getElementById('btn-shopping-list')?.addEventListener('click', () => {
    gtag('event', 'click_generate_shopping_list', {
      event_category: 'engagement',
      event_label: 'Generate Shopping List Button'
    });
  });

  // Track Copy Plan click
  document.getElementById('btn-copy-plan')?.addEventListener('click', () => {
    gtag('event', 'click_copy_plan', {
      event_category: 'engagement',
      event_label: 'Copy Plan Button'
    });
  });

  // Track feedback text
  document.getElementById('btn-submit-feedback')?.addEventListener('click', () => {
    const feedback = document.getElementById('feedback-input')?.value.trim();
    if (feedback.length === 0) {
      alert('Please enter feedback before submitting.');
      return;
    }

    gtag('event', 'user_feedback', {
      feedback_text: feedback
    });

    document.getElementById('feedback-input').value = '';
    alert('Thanks for your feedback!');
  });
