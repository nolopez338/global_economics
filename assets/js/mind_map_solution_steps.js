document.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      const summary = event.target.closest('.solution-step > summary');
      if (!summary) return;
      event.preventDefault();
      event.stopPropagation();
      summary.parentElement.open = !summary.parentElement.open;
    });
