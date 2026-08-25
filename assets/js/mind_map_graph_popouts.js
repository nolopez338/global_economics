(() => {
      const presentationRoot = document.querySelector('[data-mind-map-presentation]');
      if (!presentationRoot) return;

      const graphSelector = 'figure.density-graph, figure.procedure-figure, svg.procedure-mini-graph';
      const openGraphs = new Map();
      let idSequence = 0;
      let panelStack = 0;
      let floatingLayer = null;

      const nextUniqueId = (prefix) => {
        let candidate;
        do {
          idSequence += 1;
          candidate = `${prefix}-${idSequence}`;
        } while (document.getElementById(candidate));
        return candidate;
      };

      const getGraphTitle = (graph) => {
        const svgTitle = graph.matches('svg')
          ? graph.querySelector(':scope > title')
          : graph.querySelector('svg title');
        const caption = graph.matches('figure') ? graph.querySelector('figcaption') : null;
        const title = svgTitle?.textContent || caption?.textContent || 'Graph';
        return title.replace(/\s+/g, ' ').trim() || 'Graph';
      };

      const getViewportBounds = () => {
        const viewport = window.visualViewport;
        return {
          left: viewport?.offsetLeft || 0,
          top: viewport?.offsetTop || 0,
          width: viewport?.width || window.innerWidth,
          height: viewport?.height || window.innerHeight
        };
      };

      const setPanelPosition = (panel, requestedLeft, requestedTop) => {
        const margin = 6;
        const bounds = getViewportBounds();
        const panelRect = panel.getBoundingClientRect();
        const minimumLeft = bounds.left + margin;
        const minimumTop = bounds.top + margin;
        const maximumLeft = Math.max(minimumLeft, bounds.left + bounds.width - panelRect.width - margin);
        const maximumTop = Math.max(minimumTop, bounds.top + bounds.height - panelRect.height - margin);
        const left = Math.min(Math.max(requestedLeft, minimumLeft), maximumLeft);
        const top = Math.min(Math.max(requestedTop, minimumTop), maximumTop);
        panel.style.left = `${left}px`;
        panel.style.top = `${top}px`;
      };

      const constrainPanel = (state) => {
        if (!state.panel.classList.contains('is-collapsed')) {
          const bounds = getViewportBounds();
          const margin = 6;
          const rect = state.panel.getBoundingClientRect();
          const width = Math.min(rect.width, Math.max(1, bounds.width - margin * 2));
          const height = Math.min(rect.height, Math.max(1, bounds.height - margin * 2));
          state.panel.style.width = `${width}px`;
          state.panel.style.height = `${height}px`;
        }
        const rect = state.panel.getBoundingClientRect();
        const left = Number.parseFloat(state.panel.style.left);
        const top = Number.parseFloat(state.panel.style.top);
        setPanelPosition(
          state.panel,
          Number.isFinite(left) ? left : rect.left,
          Number.isFinite(top) ? top : rect.top
        );
      };

      const constrainAllPanels = () => {
        openGraphs.forEach((state) => constrainPanel(state));
      };

      const bringToFront = (state) => {
        panelStack += 1;
        state.panel.style.zIndex = String(panelStack);
      };

      const ensureFloatingLayer = () => {
        if (!floatingLayer) {
          floatingLayer = document.createElement('div');
          floatingLayer.className = 'graph-popout-layer';
          floatingLayer.id = nextUniqueId('graph-popout-layer');
          floatingLayer.setAttribute('aria-label', 'Floating graphs');
        }
        const destination = document.fullscreenElement || presentationRoot;
        if (floatingLayer.parentElement !== destination) destination.append(floatingLayer);
        return floatingLayer;
      };

      const returnGraphToSlide = (state, { restoreFocus = true } = {}) => {
        if (!openGraphs.has(state.graph)) return;
        state.dragCleanup?.();
        state.resizeCleanup?.();
        state.drag = null;
        state.resize = null;
        state.sourceParent.insertBefore(state.graph, state.sourceNextSibling);
        state.placeholder.remove();
        state.sourceParent.classList.remove('is-graph-open');
        state.panel.remove();
        state.launchButton.setAttribute('aria-expanded', 'false');
        state.launchButton.removeAttribute('aria-controls');
        openGraphs.delete(state.graph);
        if (restoreFocus && state.launchButton.isConnected) state.launchButton.focus({ preventScroll: true });
      };

      const returnAllGraphs = () => {
        Array.from(openGraphs.values()).forEach((state) => returnGraphToSlide(state, { restoreFocus: false }));
      };

      const togglePanelBody = (state) => {
        const collapsing = !state.panel.classList.contains('is-collapsed');
        if (collapsing) {
          const rect = state.panel.getBoundingClientRect();
          state.expandedGeometry = {
            left: rect.left,
            top: rect.top,
            width: rect.width,
            height: rect.height
          };
          state.panel.style.height = 'auto';
          state.panel.style.width = '';
          state.panel.classList.add('is-collapsed');
          state.body.hidden = true;
          state.toggleSymbol.textContent = '▴';
          state.toggleButton.setAttribute('aria-label', 'Restore graph');
          state.toggleButton.title = 'Restore graph';
          state.toggleButton.setAttribute('aria-expanded', 'false');
          constrainPanel(state);
          return;
        }

        state.panel.classList.remove('is-collapsed');
        state.body.hidden = false;
        state.toggleSymbol.textContent = '▾';
        state.toggleButton.setAttribute('aria-label', 'Collapse graph');
        state.toggleButton.title = 'Collapse graph';
        state.toggleButton.setAttribute('aria-expanded', 'true');
        requestAnimationFrame(() => {
          const previous = state.expandedGeometry;
          if (previous) {
            state.panel.style.width = `${previous.width}px`;
            state.panel.style.height = `${previous.height}px`;
            setPanelPosition(state.panel, previous.left, previous.top);
            constrainPanel(state);
          } else {
            constrainPanel(state);
          }
        });
      };

      const installResizing = (state) => {
        const { panel } = state;
        const handles = ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se'].map((edge) => {
          const handle = document.createElement('span');
          handle.className = 'graph-resize-handle';
          handle.dataset.resizeEdge = edge;
          handle.setAttribute('aria-hidden', 'true');
          panel.append(handle);
          return handle;
        });

        const moveResize = (event) => {
          const resize = state.resize;
          if (!resize || resize.pointerId !== event.pointerId) return;
          const bounds = getViewportBounds();
          const margin = 6;
          const minWidth = Math.min(280, bounds.width - margin * 2);
          const minHeight = Math.min(180, bounds.height - margin * 2);
          const rightLimit = bounds.left + bounds.width - margin;
          const bottomLimit = bounds.top + bounds.height - margin;
          let left = resize.left;
          let top = resize.top;
          let right = resize.left + resize.width;
          let bottom = resize.top + resize.height;
          if (resize.edge.includes('w')) left = Math.min(event.clientX, right - minWidth);
          if (resize.edge.includes('e')) right = Math.max(event.clientX, left + minWidth);
          if (resize.edge.includes('n')) top = Math.min(event.clientY, bottom - minHeight);
          if (resize.edge.includes('s')) bottom = Math.max(event.clientY, top + minHeight);
          left = Math.max(bounds.left + margin, left);
          top = Math.max(bounds.top + margin, top);
          right = Math.min(rightLimit, right);
          bottom = Math.min(bottomLimit, bottom);
          if (right - left < minWidth) {
            if (resize.edge.includes('w')) left = right - minWidth;
            else right = left + minWidth;
          }
          if (bottom - top < minHeight) {
            if (resize.edge.includes('n')) top = bottom - minHeight;
            else bottom = top + minHeight;
          }
          panel.style.left = `${left}px`;
          panel.style.top = `${top}px`;
          panel.style.width = `${right - left}px`;
          panel.style.height = `${bottom - top}px`;
          event.preventDefault();
        };

        const endResize = (event) => {
          if (!state.resize || state.resize.pointerId !== event.pointerId) return;
          const handle = state.resize.handle;
          state.resize = null;
          document.documentElement.style.removeProperty('user-select');
          try {
            if (handle.hasPointerCapture(event.pointerId)) handle.releasePointerCapture(event.pointerId);
          } catch (error) {
            // Capture can already be gone after pointer cancellation.
          }
        };

        const lostCapture = (event) => endResize(event);
        handles.forEach((handle) => {
          handle.addEventListener('pointerdown', (event) => {
            if (panel.classList.contains('is-collapsed')) return;
            if (event.pointerType === 'mouse' && event.button !== 0) return;
            const rect = panel.getBoundingClientRect();
            state.resize = {
              pointerId: event.pointerId,
              edge: handle.dataset.resizeEdge,
              handle,
              left: rect.left,
              top: rect.top,
              width: rect.width,
              height: rect.height
            };
            bringToFront(state);
            document.documentElement.style.userSelect = 'none';
            handle.setPointerCapture(event.pointerId);
            event.preventDefault();
            event.stopPropagation();
          });
          handle.addEventListener('lostpointercapture', lostCapture);
        });
        window.addEventListener('pointermove', moveResize);
        window.addEventListener('pointerup', endResize);
        window.addEventListener('pointercancel', endResize);
        state.resizeCleanup = () => {
          document.documentElement.style.removeProperty('user-select');
          window.removeEventListener('pointermove', moveResize);
          window.removeEventListener('pointerup', endResize);
          window.removeEventListener('pointercancel', endResize);
          handles.forEach((handle) => handle.removeEventListener('lostpointercapture', lostCapture));
        };
      };

      const installDragging = (state) => {
        const { titleBar, panel } = state;

        titleBar.addEventListener('pointerdown', (event) => {
          if (event.target.closest('button')) return;
          if (event.pointerType === 'mouse' && event.button !== 0) return;
          const rect = panel.getBoundingClientRect();
          state.drag = {
            pointerId: event.pointerId,
            offsetX: event.clientX - rect.left,
            offsetY: event.clientY - rect.top
          };
          bringToFront(state);
          titleBar.classList.add('is-dragging');
          try {
            titleBar.setPointerCapture(event.pointerId);
          } catch (error) {
            // Document-level listeners below keep dragging functional if capture is unavailable.
          }
          event.preventDefault();
        });

        const moveDrag = (event) => {
          if (!state.drag || state.drag.pointerId !== event.pointerId) return;
          setPanelPosition(
            panel,
            event.clientX - state.drag.offsetX,
            event.clientY - state.drag.offsetY
          );
        };

        const endDrag = (event) => {
          if (!state.drag || state.drag.pointerId !== event.pointerId) return;
          try {
            if (titleBar.hasPointerCapture(event.pointerId)) titleBar.releasePointerCapture(event.pointerId);
          } catch (error) {
            // The pointer may already have been released by the user agent.
          }
          state.drag = null;
          titleBar.classList.remove('is-dragging');
        };

        window.addEventListener('pointermove', moveDrag);
        window.addEventListener('pointerup', endDrag);
        window.addEventListener('pointercancel', endDrag);
        titleBar.addEventListener('lostpointercapture', () => {
          if (state.drag) {
            state.drag = null;
            titleBar.classList.remove('is-dragging');
          }
        });
        state.dragCleanup = () => {
          window.removeEventListener('pointermove', moveDrag);
          window.removeEventListener('pointerup', endDrag);
          window.removeEventListener('pointercancel', endDrag);
        };
        panel.addEventListener('pointerdown', () => bringToFront(state));
        panel.addEventListener('focusin', () => bringToFront(state));
      };

      const openFloatingGraph = (graph, sourceParent, launchButton) => {
        const existingState = openGraphs.get(graph);
        if (existingState) {
          bringToFront(existingState);
          existingState.panel.focus({ preventScroll: true });
          return;
        }

        const graphTitle = getGraphTitle(graph);
        const panelId = nextUniqueId('graph-floating-panel');
        const titleId = nextUniqueId('graph-floating-title');
        const bodyId = nextUniqueId('graph-floating-content');
        const placeholder = document.createElement('div');
        const panel = document.createElement('section');
        const titleBar = document.createElement('div');
        const dragIcon = document.createElement('span');
        const heading = document.createElement('h4');
        const actions = document.createElement('div');
        const toggleButton = document.createElement('button');
        const toggleSymbol = document.createElement('span');
        const returnButton = document.createElement('button');
        const closeSymbol = document.createElement('span');
        const body = document.createElement('div');

        placeholder.className = 'graph-popout-placeholder';
        placeholder.textContent = 'Graph opened in floating view.';
        placeholder.setAttribute('role', 'status');
        sourceParent.insertBefore(placeholder, launchButton);
        sourceParent.classList.add('is-graph-open');

        panel.className = 'graph-floating-panel';
        panel.id = panelId;
        panel.tabIndex = -1;
        panel.setAttribute('role', 'dialog');
        panel.setAttribute('aria-modal', 'false');
        panel.setAttribute('aria-labelledby', titleId);

        titleBar.className = 'graph-floating-titlebar';
        titleBar.setAttribute('aria-label', `Drag floating graph: ${graphTitle}`);
        dragIcon.className = 'graph-floating-drag-icon';
        dragIcon.setAttribute('aria-hidden', 'true');
        dragIcon.textContent = '⠿';
        heading.className = 'graph-floating-title';
        heading.id = titleId;
        heading.textContent = graphTitle;
        actions.className = 'graph-floating-actions';

        toggleButton.type = 'button';
        toggleButton.className = 'graph-floating-control';
        toggleButton.title = 'Collapse graph';
        toggleButton.setAttribute('aria-label', 'Collapse graph');
        toggleButton.setAttribute('aria-expanded', 'true');
        toggleButton.setAttribute('aria-controls', bodyId);
        toggleSymbol.className = 'graph-floating-control-symbol';
        toggleSymbol.setAttribute('aria-hidden', 'true');
        toggleSymbol.textContent = '▾';
        toggleButton.append(toggleSymbol);

        returnButton.type = 'button';
        returnButton.className = 'graph-floating-control';
        returnButton.title = 'Close graph window and return graph to slide';
        returnButton.setAttribute('aria-label', 'Close graph window and return graph to slide');
        closeSymbol.className = 'graph-floating-control-symbol';
        closeSymbol.setAttribute('aria-hidden', 'true');
        closeSymbol.textContent = '×';
        returnButton.append(closeSymbol);

        body.className = 'graph-floating-body';
        body.id = bodyId;
        body.append(graph);

        actions.append(toggleButton, returnButton);
        titleBar.append(dragIcon, heading, actions);
        panel.append(titleBar, body);
        ensureFloatingLayer().append(panel);

        const state = {
          graph,
          graphTitle,
          sourceParent,
          sourceNextSibling: launchButton,
          launchButton,
          placeholder,
          panel,
          titleBar,
          toggleButton,
          toggleSymbol,
          returnButton,
          body,
          expandedGeometry: null,
          sourceSlide: sourceParent.closest('[data-mind-map-slide]'),
          drag: null,
          resize: null
        };
        openGraphs.set(graph, state);
        launchButton.setAttribute('aria-expanded', 'true');
        launchButton.setAttribute('aria-controls', panelId);
        toggleButton.addEventListener('click', () => togglePanelBody(state));
        returnButton.addEventListener('click', () => returnGraphToSlide(state));
        installDragging(state);
        installResizing(state);
        bringToFront(state);

        requestAnimationFrame(() => {
          const bounds = getViewportBounds();
          const rect = panel.getBoundingClientRect();
          const cascade = Math.min((openGraphs.size - 1) * 18, 72);
          setPanelPosition(
            panel,
            bounds.left + (bounds.width - rect.width) / 2 + cascade,
            bounds.top + (bounds.height - rect.height) / 2 + cascade
          );
          panel.focus({ preventScroll: true });
        });
      };

      const initializeGraphPopouts = (scope = document) => {
        ensureFloatingLayer();
        scope.querySelectorAll(graphSelector).forEach((graph) => {
          if (graph.dataset.graphPopoutReady === 'true') return;

          const graphTitle = getGraphTitle(graph);
          const sourceParent = graph.parentNode;
          const host = document.createElement('div');
          const launchButton = document.createElement('button');
          const icon = document.createElement('span');
          const label = document.createElement('span');

          host.className = 'graph-popout-host';
          host.dataset.graphPopout = '';
          if (graph.classList.contains('solution-graph')) host.classList.add('graph-popout-host--solution');
          if (graph.classList.contains('procedure-figure')) host.classList.add('graph-popout-host--procedure');
          if (graph.classList.contains('procedure-mini-graph')) host.classList.add('graph-popout-host--mini');

          launchButton.type = 'button';
          launchButton.className = 'graph-popout-button';
          launchButton.title = 'Pop out graph';
          launchButton.setAttribute('aria-label', `Pop out graph: ${graphTitle}`);
          launchButton.setAttribute('aria-expanded', 'false');
          icon.className = 'graph-popout-icon';
          icon.setAttribute('aria-hidden', 'true');
          icon.textContent = '↗';
          label.className = 'graph-popout-button-text';
          label.textContent = 'Pop out graph';
          launchButton.append(icon, label);

          sourceParent.insertBefore(host, graph);
          host.append(graph, launchButton);
          graph.dataset.graphPopoutReady = 'true';
          launchButton.addEventListener('click', () => openFloatingGraph(graph, host, launchButton));
        });
      };

      window.initializeGraphPopouts = initializeGraphPopouts;
      initializeGraphPopouts();
      document.addEventListener('fullscreenchange', () => {
        ensureFloatingLayer();
        requestAnimationFrame(constrainAllPanels);
      });
      window.addEventListener('resize', constrainAllPanels);
      window.visualViewport?.addEventListener('resize', constrainAllPanels);
      window.visualViewport?.addEventListener('scroll', constrainAllPanels);

      let activeSlide = presentationRoot.querySelector('[data-mind-map-slide][aria-current="step"]');
      let wasPresenting = presentationRoot.classList.contains('is-presenting');
      const presentationObserver = new MutationObserver(() => {
        const nextActiveSlide = presentationRoot.querySelector('[data-mind-map-slide][aria-current="step"]');
        const isPresenting = presentationRoot.classList.contains('is-presenting');
        if ((activeSlide && nextActiveSlide !== activeSlide) || (wasPresenting && !isPresenting)) {
          returnAllGraphs();
        }
        activeSlide = nextActiveSlide;
        wasPresenting = isPresenting;
      });
      presentationObserver.observe(presentationRoot, {
        subtree: true,
        attributes: true,
        attributeFilter: ['aria-current', 'class']
      });
    })();
