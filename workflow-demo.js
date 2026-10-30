// A deterministic, local simulation. No external requests or generated claims.
(() => {
  const demo = document.getElementById('workflow-demo');
  if (!demo) return;
  const steps = [...demo.querySelectorAll('.workflow-step')];
  const panels = [...demo.querySelectorAll('.stage-panel')];
  const run = document.getElementById('run-workflow');
  const reset = document.getElementById('reset-workflow');
  const status = document.getElementById('workflow-status');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const labels = ['Collected 4 sample articles.', 'Removed 1 duplicate. 3 unique stories remain.', 'Prepared 3 example summaries.', 'Sample complete. Your digest is ready for review.'];
  let timer = null;
  let running = false;
  const stageFromHash = () => panels.findIndex(panel => `#${panel.id}` === location.hash);
  function showStage(index) {
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    steps.forEach((step, i) => {
      if (i === index) step.setAttribute('aria-current', 'step');
      else step.removeAttribute('aria-current');
      step.classList.toggle('is-complete', i < index);
    });
  }
  function stop() {
    clearTimeout(timer);
    timer = null;
    running = false;
    run.disabled = false;
    demo.removeAttribute('data-running');
  }
  function inspect(index) {
    stop();
    showStage(index);
    status.textContent = labels[index];
    run.textContent = 'Run sample again →';
  }
  steps.forEach((step, index) => {
    // These are native fragment links; modified clicks retain normal behavior.
    step.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      inspect(index);
    });
  });
  window.addEventListener('hashchange', () => {
    const index = stageFromHash();
    if (index >= 0) inspect(index);
  });
  run.addEventListener('click', () => {
    stop();
    running = true;
    run.disabled = true;
    demo.dataset.running = 'true';
    let stage = 0;
    function advance() {
      if (!running) return;
      showStage(stage);
      status.textContent = labels[stage];
      if (stage === panels.length - 1) {
        stop();
        run.textContent = 'Run sample again →';
        return;
      }
      stage += 1;
      timer = setTimeout(advance, reducedMotion.matches ? 0 : 1200);
    }
    advance();
  });
  reset.addEventListener('click', () => {
    stop();
    showStage(0);
    status.textContent = 'Reset. Ready to explore.';
    run.textContent = 'Run sample →';
  });
  showStage(Math.max(0, stageFromHash()));
  demo.querySelector('.demo-controls').hidden = false;
})();
