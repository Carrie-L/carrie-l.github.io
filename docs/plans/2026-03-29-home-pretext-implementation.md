# Homepage Pretext Dynamic Layout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a desktop-only homepage experience where a small animated character moves through the homepage article flow and nearby titles/excerpts reflow around it using `@chenglou/pretext`.

**Architecture:** Keep Jekyll's homepage list as the source-of-truth and fallback layer, then mount a client-side dynamic stage on top of it. Vendor `@chenglou/pretext` into a local static asset, parse the existing article DOM, prepare text runs with `pretext`, and render line-positioned HTML that reroutes around a moving sprite using `layoutNextLine()`.

**Tech Stack:** Jekyll, vanilla ES modules, local vendored `@chenglou/pretext@0.0.3`, existing homepage CSS, existing GIF asset `assets/images/anime13.gif`, manual browser smoke checks via local Jekyll serve.

---

### Task 1: Vendor `pretext` Locally and Add a Smoke Harness

**Files:**
- Modify: `I:\B-MioBlogSites\package.json`
- Modify: `I:\B-MioBlogSites\package-lock.json`
- Create: `I:\B-MioBlogSites\scripts\vendor-pretext.mjs`
- Create: `I:\B-MioBlogSites\assets\vendor\pretext\layout.js`
- Create: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Create `debug-pretext-home.html` with a minimal smoke panel that tries to import the vendored module path and prints PASS/FAIL:

```html
---
layout: bare
title: Pretext Home Debug
---
<main id="pretext-debug">
  <p id="pretext-import-status">PENDING</p>
</main>
<script type="module">
  const status = document.getElementById('pretext-import-status');
  try {
    await import('{{ "/assets/vendor/pretext/layout.js" | relative_url }}');
    status.textContent = 'PASS';
  } catch (error) {
    status.textContent = `FAIL: ${error.message}`;
  }
</script>
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because `assets/vendor/pretext/layout.js` does not exist yet.

**Step 3: Write minimal implementation**

Install and vendor `pretext` as a local static asset instead of relying on a CDN:

```json
{
  "scripts": {
    "vendor:pretext": "node ./scripts/vendor-pretext.mjs"
  },
  "dependencies": {
    "@chenglou/pretext": "0.0.3",
    "@tailwindcss/postcss": "^4.1.13"
  }
}
```

`scripts/vendor-pretext.mjs`:

```js
import { mkdir, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const from = path.join(root, 'node_modules', '@chenglou', 'pretext', 'dist', 'layout.js');
const toDir = path.join(root, 'assets', 'vendor', 'pretext');
const to = path.join(toDir, 'layout.js');

await mkdir(toDir, { recursive: true });
await copyFile(from, to);
console.log(`Vendored pretext to ${to}`);
```

Run:

```bash
npm install
npm install @chenglou/pretext@0.0.3 --save-exact
npm run vendor:pretext
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: PASS and no module import error in the browser.

**Step 5: Commit**

```bash
git add package.json package-lock.json scripts/vendor-pretext.mjs assets/vendor/pretext/layout.js debug-pretext-home.html
git commit -m "chore: vendor pretext for homepage"
```

### Task 2: Create the Homepage Dynamic Stage Shell and Guard Logic

**Files:**
- Modify: `I:\B-MioBlogSites\index.html`
- Modify: `I:\B-MioBlogSites\assets\css\home.css`
- Create: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Test: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Export a pure eligibility helper from `assets/js/home-pretext.js` and update the debug page to call it:

```js
export function shouldEnableHomePretext({
  viewportWidth,
  prefersReducedMotion,
  hasSourceList,
}) {
  return false;
}
```

Debug assertion:

```js
import { shouldEnableHomePretext } from '{{ "/assets/js/home-pretext.js" | relative_url }}';
const eligible = shouldEnableHomePretext({
  viewportWidth: 1440,
  prefersReducedMotion: false,
  hasSourceList: true,
});
status.textContent = eligible ? 'PASS' : 'FAIL: ineligible';
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because the helper intentionally returns `false`.

**Step 3: Write minimal implementation**

Add a minimal homepage shell and activation script.

In `index.html`, wrap the existing article list with stable hooks:

```html
<main class="container" data-home-pretext-root>
  <div class="article-list" data-home-pretext-source>
    ...
  </div>
  <div class="home-pretext-stage" data-home-pretext-stage hidden></div>
  {% include home-categories.html posts=site.Android %}
</main>
<script type="module" src="{{ '/assets/js/home-pretext.js' | relative_url }}"></script>
```

In `assets/js/home-pretext.js`, implement:

```js
export function shouldEnableHomePretext({ viewportWidth, prefersReducedMotion, hasSourceList }) {
  return viewportWidth >= 1100 && !prefersReducedMotion && hasSourceList;
}
```

In `assets/css/home.css`, add a hidden-but-reserved stage shell:

```css
.home-pretext-stage[hidden] {
  display: none !important;
}
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: PASS for the helper test.

Then open: `http://127.0.0.1:4000/`

Expected: new `data-home-pretext-*` hooks exist in DOM and the static homepage still renders normally.

**Step 5: Commit**

```bash
git add index.html assets/css/home.css assets/js/home-pretext.js debug-pretext-home.html
git commit -m "feat: add homepage pretext stage shell"
```

### Task 3: Parse Homepage Articles into Stable Source Data

**Files:**
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Test: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Add a pure extraction helper and a fixture-based assertion in the debug page:

```js
export function extractHomeArticles(root) {
  return [];
}
```

Debug fixture:

```html
<section id="fixture-root">
  <article class="post-preview">
    <div class="post-content">
      <h3 class="glow-text"><a href="/a">Alpha</a></h3>
      <p class="item-text">First excerpt</p>
    </div>
  </article>
  <article class="post-preview">
    <div class="post-content">
      <h3 class="glow-text"><a href="/b">Beta</a></h3>
      <p class="item-text">Second excerpt</p>
    </div>
  </article>
</section>
```

Debug assertion:

```js
const articles = extractHomeArticles(document.getElementById('fixture-root'));
status.textContent = articles.length === 2 ? 'PASS' : `FAIL: got ${articles.length}`;
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because extraction returns an empty array.

**Step 3: Write minimal implementation**

Implement stable parsing of title, excerpt, and href:

```js
export function extractHomeArticles(root) {
  const cards = [...root.querySelectorAll('.post-preview')];
  return cards.map((card, index) => {
    const link = card.querySelector('h3 a');
    const excerpt = card.querySelector('.item-text');
    return {
      id: `article-${index}`,
      href: link?.getAttribute('href') ?? '#',
      title: link?.textContent?.trim() ?? '',
      excerpt: excerpt?.textContent?.trim() ?? '',
    };
  }).filter(article => article.title);
}
```

Also add a homepage-only runtime hook:

```js
const source = document.querySelector('[data-home-pretext-source]');
const articles = source ? extractHomeArticles(source) : [];
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: PASS with 2 extracted fixture articles.

Open: `http://127.0.0.1:4000/`

Expected: `extractHomeArticles` finds the real homepage list without changing visible layout yet.

**Step 5: Commit**

```bash
git add assets/js/home-pretext.js debug-pretext-home.html
git commit -m "feat: parse homepage article source data"
```

### Task 4: Prepare Text Runs and Render a Fixed-Width Article Scene

**Files:**
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Modify: `I:\B-MioBlogSites\assets\css\home.css`
- Test: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Add a fixed-width renderer test to the debug page:

```js
import { buildPreparedArticleRuns, layoutArticleAtWidth } from '{{ "/assets/js/home-pretext.js" | relative_url }}';
const prepared = buildPreparedArticleRuns([
  { id: 'a', href: '/a', title: 'Alpha title', excerpt: 'Alpha excerpt that should wrap' },
]);
const layout = layoutArticleAtWidth(prepared[0], { width: 220 });
status.textContent = layout.lines?.length > 0 ? 'PASS' : 'FAIL: no lines';
```

Stub the exports first:

```js
export function buildPreparedArticleRuns(articles) {
  return articles;
}

export function layoutArticleAtWidth(article, { width }) {
  return { lines: [] };
}
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because the renderer returns zero lines.

**Step 3: Write minimal implementation**

Import `pretext` and prepare separate title/excerpt runs:

```js
import { prepareWithSegments, layoutWithLines } from '../vendor/pretext/layout.js';

export function buildPreparedArticleRuns(articles) {
  return articles.map(article => ({
    ...article,
    titlePrepared: prepareWithSegments(article.title, '500 17px "LXGW WenKai"'),
    excerptPrepared: prepareWithSegments(article.excerpt, '400 13px "Arial"'),
  }));
}

export function layoutArticleAtWidth(article, { width }) {
  const title = layoutWithLines(article.titlePrepared, width, 26);
  const excerpt = layoutWithLines(article.excerptPrepared, width, 21);
  return {
    titleLines: title.lines,
    excerptLines: excerpt.lines,
    lines: [...title.lines, ...excerpt.lines],
  };
}
```

Add minimal stage styles:

```css
.home-pretext-stage {
  position: relative;
  min-height: 600px;
}

.home-pretext-line {
  position: absolute;
  left: 0;
  white-space: pre;
}
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: PASS and visible wrapped lines inside the debug stage.

**Step 5: Commit**

```bash
git add assets/js/home-pretext.js assets/css/home.css debug-pretext-home.html
git commit -m "feat: render fixed-width pretext article lines"
```

### Task 5: Route Lines Around a Dynamic Obstacle with `layoutNextLine()`

**Files:**
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Test: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Add an obstacle-aware layout helper and a debug assertion that fails when lines overlap the obstacle band:

```js
export function layoutArticleAroundObstacle(article, options) {
  return { placedLines: [] };
}
```

Debug scenario:

```js
const obstacle = { x: 120, y: 24, width: 64, height: 64, padding: 16 };
const result = layoutArticleAroundObstacle(prepared[0], {
  width: 320,
  obstacle,
  top: 0,
});
const overlaps = result.placedLines.some(line => {
  const withinY = line.top < obstacle.y + obstacle.height && line.top + line.height > obstacle.y;
  const withinX = line.left < obstacle.x + obstacle.width && line.left + line.width > obstacle.x;
  return withinY && withinX;
});
status.textContent = overlaps ? 'FAIL: overlap' : 'PASS';
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because the stub does not respect the obstacle.

**Step 3: Write minimal implementation**

Use `layoutNextLine()` to vary width per line:

```js
import { layoutNextLine } from '../vendor/pretext/layout.js';

function computeLineBox(top, lineHeight, obstacle, width) {
  const paddedLeft = obstacle.x - obstacle.padding;
  const paddedRight = obstacle.x + obstacle.width + obstacle.padding;
  const intersectsY = top < obstacle.y + obstacle.height + obstacle.padding &&
    top + lineHeight > obstacle.y - obstacle.padding;

  if (!intersectsY) {
    return { left: 0, width };
  }

  return { left: 0, width: Math.max(0, paddedLeft) };
}

export function layoutPreparedBlock(prepared, width, lineHeight, obstacle, startTop) {
  const placedLines = [];
  let cursor = { segmentIndex: 0, graphemeIndex: 0 };
  let top = startTop;

  while (true) {
    const box = computeLineBox(top, lineHeight, obstacle, width);
    const line = layoutNextLine(prepared, cursor, box.width);
    if (line === null) break;
    placedLines.push({
      text: line.text,
      left: box.left,
      top,
      width: line.width,
      height: lineHeight,
    });
    cursor = line.end;
    top += lineHeight;
  }

  return { placedLines, nextTop: top };
}
```

Then use this for both title and excerpt blocks.

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: PASS and visible text wrapping around the debug obstacle box.

**Step 5: Commit**

```bash
git add assets/js/home-pretext.js debug-pretext-home.html
git commit -m "feat: add obstacle-aware pretext line routing"
```

### Task 6: Mount the Dynamic Scene on the Real Homepage Without Breaking Fallback

**Files:**
- Modify: `I:\B-MioBlogSites\index.html`
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Modify: `I:\B-MioBlogSites\assets\css\home.css`

**Step 1: Write the failing test**

Add a runtime invariant: the static list must stay visible until the dynamic scene has rendered at least one line.

Stub:

```js
function activateDynamicScene({ stage, source }) {
  source.hidden = true;
}
```

Expected invariant:

```js
if (!renderResult.lineCount) {
  throw new Error('Cannot hide static source before dynamic render succeeds');
}
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/`

Expected: either console error or obviously broken homepage because the source list is hidden too early.

**Step 3: Write minimal implementation**

Only hide the static source after a successful dynamic render:

```js
function renderHomepageScene(context) {
  const renderResult = renderArticlesToStage(context);
  if (!renderResult.lineCount) return false;

  context.stage.hidden = false;
  context.source.classList.add('home-pretext-source--fallback');
  return true;
}
```

CSS:

```css
.home-pretext-source--fallback {
  position: absolute !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/`

Expected:
- the homepage still works if the dynamic scene throws
- the static source only becomes visually hidden after the dynamic lines appear

**Step 5: Commit**

```bash
git add index.html assets/js/home-pretext.js assets/css/home.css
git commit -m "feat: mount homepage pretext scene safely"
```

### Task 7: Add the Animated Character and Discrete Relayout

**Files:**
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Modify: `I:\B-MioBlogSites\assets\css\home.css`

**Step 1: Write the failing test**

Add a sprite state helper and a relayout-threshold helper with a failing debug case:

```js
export function shouldRelayout(lastObstacle, nextObstacle) {
  return false;
}
```

Debug assertion:

```js
const changed = shouldRelayout(
  { x: 40, y: 40, width: 64, height: 64, padding: 16 },
  { x: 80, y: 40, width: 64, height: 64, padding: 16 },
);
status.textContent = changed ? 'PASS' : 'FAIL: relayout not triggered';
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because the helper always returns `false`.

**Step 3: Write minimal implementation**

Add the moving sprite with thresholded relayout:

```js
const RELAYOUT_DISTANCE = 24;
const RELAYOUT_BAND = 28;

export function shouldRelayout(lastObstacle, nextObstacle) {
  if (!lastObstacle) return true;
  const dx = Math.abs(lastObstacle.x - nextObstacle.x);
  const dy = Math.abs(lastObstacle.y - nextObstacle.y);
  const bandChanged = Math.floor(lastObstacle.y / RELAYOUT_BAND) !== Math.floor(nextObstacle.y / RELAYOUT_BAND);
  return dx >= RELAYOUT_DISTANCE || dy >= RELAYOUT_DISTANCE || bandChanged;
}

function nextSpritePosition(time, bounds) {
  return {
    x: bounds.left + 40 + Math.sin(time / 1100) * (bounds.width * 0.28),
    y: bounds.top + 60 + Math.cos(time / 1400) * (bounds.height * 0.18),
    width: 64,
    height: 64,
    padding: 18,
  };
}
```

Add sprite styling:

```css
.home-pretext-sprite {
  position: absolute;
  width: 64px;
  height: 64px;
  background-image: url('../images/anime13.gif');
  background-size: contain;
  background-repeat: no-repeat;
  pointer-events: none;
}
```

**Step 4: Run test to verify it passes**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/`

Expected:
- the sprite moves smoothly
- nearby text reflows only when thresholds are crossed
- distant article blocks stay stable

**Step 5: Commit**

```bash
git add assets/js/home-pretext.js assets/css/home.css
git commit -m "feat: animate homepage sprite with discrete relayout"
```

### Task 8: Add Guardrails, Polish Clickability, and Document the Workflow

**Files:**
- Modify: `I:\B-MioBlogSites\assets\js\home-pretext.js`
- Modify: `I:\B-MioBlogSites\assets\css\home.css`
- Modify: `I:\B-MioBlogSites\docs\我的博客操作方法.md`
- Test: `I:\B-MioBlogSites\debug-pretext-home.html`

**Step 1: Write the failing test**

Add final smoke checks for:

- reduced motion fallback
- mobile-width fallback
- clickable dynamic lines
- static fallback when runtime throws

Example assertion hooks:

```js
export function buildRuntimeMode({ viewportWidth, prefersReducedMotion, renderOk }) {
  return 'dynamic';
}
```

Expected cases:

```js
buildRuntimeMode({ viewportWidth: 390, prefersReducedMotion: false, renderOk: true }) === 'static'
buildRuntimeMode({ viewportWidth: 1440, prefersReducedMotion: true, renderOk: true }) === 'static'
buildRuntimeMode({ viewportWidth: 1440, prefersReducedMotion: false, renderOk: false }) === 'static'
```

**Step 2: Run test to verify it fails**

Run: `bundle exec jekyll serve`

Open: `http://127.0.0.1:4000/debug-pretext-home.html`

Expected: FAIL because the runtime mode helper and click behavior are not fully implemented.

**Step 3: Write minimal implementation**

Finish runtime guards and article-line links:

```js
export function buildRuntimeMode({ viewportWidth, prefersReducedMotion, renderOk }) {
  if (viewportWidth < 1100) return 'static';
  if (prefersReducedMotion) return 'static';
  if (!renderOk) return 'static';
  return 'dynamic';
}
```

Render lines as anchors when they belong to an article:

```js
const node = document.createElement('a');
node.className = 'home-pretext-line home-pretext-line--title';
node.href = article.href;
node.textContent = line.text;
```

Document the local workflow in `docs\我的博客操作方法.md`:

- `npm install @chenglou/pretext@0.0.3 --save-exact`
- `npm run vendor:pretext`
- `bundle exec jekyll serve`
- verify `/` and `/debug-pretext-home.html`

**Step 4: Run test to verify it passes**

Run:

```bash
npm run vendor:pretext
bundle exec jekyll serve
```

Verify:

- `http://127.0.0.1:4000/` on desktop: dynamic scene active
- narrow viewport: static list remains
- reduced motion enabled: static list remains
- `http://127.0.0.1:4000/debug-pretext-home.html`: smoke checks PASS

**Step 5: Commit**

```bash
git add assets/js/home-pretext.js assets/css/home.css docs/我的博客操作方法.md debug-pretext-home.html
git commit -m "feat: finalize homepage pretext interaction"
```

### Final Verification

Use `@superpowers/verification-before-completion` before claiming success.

Run:

```bash
npm run vendor:pretext
bundle exec jekyll serve
```

Manual verification checklist:

- Homepage desktop view shows the sprite moving inside the article-flow area
- Nearby titles and excerpts wrap around the sprite
- Article order does not jump
- Sidebar remains untouched
- Static fallback still works if the module is disabled
- Mobile fallback remains the original list
- Reduced-motion fallback remains the original list
- Debug route `http://127.0.0.1:4000/debug-pretext-home.html` passes smoke checks

