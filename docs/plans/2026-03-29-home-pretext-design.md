# Homepage Pretext Dynamic Text Layout Design

**Date:** 2026-03-29

**Status:** Approved

**Goal**

Use Cheng Lou's `pretext` library on the homepage article list so a small animated character can move through the content area while nearby titles and excerpts dynamically reflow around it.

## Project Context

- Repository: `I:\B-MioBlogSites`
- Stack: Jekyll static site with hand-written HTML/CSS and light client-side JavaScript
- Homepage entry points:
  - `index.html`
  - `_layouts/home.html`
  - `assets/css/home.css`
  - `_includes/home-categories.html`
- Current homepage structure:
  - Left side: article list rendered by Jekyll
  - Right side: fixed sidebar with categories and tags
- Current homepage article count across the selected collections: about 42 posts

## Scope

### In Scope

- Homepage only
- Desktop-only dynamic text reflow effect
- One animated character automatically moving inside the homepage article-flow area
- Use `pretext` as the text measurement and line-layout engine
- Preserve existing Jekyll-generated content as SEO and no-JS fallback

### Out of Scope

- Article pages
- Category pages
- Mobile dynamic layout
- Multiple characters
- User-controlled movement
- Full-page custom layout engine
- Canvas-only text rendering
- Physics-heavy collision system

## User Intent

The homepage should feel more like a living interface than a static list. The desired effect is not a fake card dodge animation. The text itself should visually reflow around the moving character, similar to the floating-object text-wrap behavior demonstrated in `pretext`, but applied to the blog homepage article flow.

## Considered Approaches

### 1. Fake Avoidance on Existing Cards

Keep the current card/list layout and only push entire cards sideways when the character passes nearby.

Pros:
- Fast to ship
- Low implementation risk

Cons:
- Not real text reflow
- Does not match the target effect

### 2. Hybrid Homepage Text Engine on Top of Existing Data

Keep Jekyll as the source of truth, but replace the visual rendering of the homepage article list with a client-side text scene driven by `pretext`.

Pros:
- Matches the intended effect
- Keeps existing content pipeline and SEO fallback
- Limits custom layout work to one homepage region

Cons:
- Requires a custom client-side rendering layer
- Requires font-measurement discipline and layout tuning

### 3. Fully Custom Homepage Layout Engine

Move most homepage layout responsibilities into a bespoke runtime engine.

Pros:
- Maximum flexibility

Cons:
- Too much complexity for a first version
- High maintenance cost

## Chosen Approach

Adopt approach 2: a hybrid homepage text engine powered by `pretext`.

This gives the homepage a true text-wrap interaction while keeping the Jekyll source markup intact as the fallback layer. The custom behavior stays limited to the left article-flow region instead of taking over the entire site layout.

## Architecture

The homepage will have two representations of the article flow:

1. Static source list rendered by Jekyll
2. Dynamic visual layer rendered by client-side JavaScript

The static source list remains in the DOM and continues to provide:

- SEO-visible content
- No-JS fallback
- Parsing source for article metadata

The dynamic layer takes over only when all startup conditions pass:

- Desktop viewport
- `prefers-reduced-motion` is not enabled
- `pretext` loads successfully
- Runtime initialization succeeds

If any condition fails, the homepage stays in its normal static mode.

## Component Model

### 1. Static Fallback Layer

The existing `.article-list` remains the real Jekyll output. It will not be removed. When dynamic mode is active, it becomes visually hidden or demoted to a fallback state rather than being deleted.

### 2. Article Data Extraction Layer

Client-side code reads each homepage article entry from the existing DOM and extracts:

- Title
- Excerpt
- Target URL

This avoids changing the site content generation pipeline.

### 3. Pretext Layout Layer

Each article's title and excerpt are prepared with `pretext`. Layout is performed line by line, not as fixed-height cards.

Important behavior:

- Article order remains stable
- Vertical article slots remain stable
- Only line wrapping inside nearby articles changes
- The character influences local line widths, not the page's global order

### 4. Character Motion Layer

The moving character is an independent sprite element that lives in the homepage dynamic stage.

It exposes geometry only:

- `x`
- `y`
- `width`
- `height`
- avoidance padding

The layout engine does not need to know animation details. It only needs the current obstacle box.

### 5. Interaction Mapping Layer

The dynamic text remains clickable. The rendered lines for each article should be output as real HTML, with line-level clickable regions linking to the same article URL.

This avoids a large invisible click rectangle that could block unrelated interactions.

## Layout Rules

- The character only moves inside the left homepage article-flow region
- It does not enter the sidebar, footer, or top title area
- Character motion is automatic in v1
- Article ordering is fixed
- Reflow is local and line-based
- Nearby articles can rewrap around the character
- Distant articles remain unchanged
- A hard obstacle region is surrounded by a softer avoidance margin so text does not hug the sprite too tightly

## Reflow Strategy

The design explicitly avoids full-page reflow on every animation frame.

### Recommended Strategy

Use smooth character animation with discrete text reflow.

Text relayout should trigger only when:

- The character moves beyond a pixel threshold
- The character enters a new vertical band
- The viewport changes enough to require a fresh layout

This keeps the animation feeling alive without recomputing all article lines every frame.

## Rendering Strategy

Use HTML for the dynamic text layer in v1, not a pure canvas renderer.

Reasons:

- Better typography consistency with the rest of the site
- Real link semantics
- Easier debugging
- Easier hover/focus styling
- Lower risk for accessibility regressions

`pretext` is used as the measurement and line-break engine, while HTML absolutely positioned line elements provide the visible output.

## Typography Constraints

Because `pretext` relies on accurate measurement, the dynamic layout must use the same effective font settings as the rendered text.

This includes:

- font family
- font size
- line height
- letter spacing if relevant

Font mismatch would cause measured lines and displayed lines to diverge, so font calibration is a first-class implementation concern.

## Responsive and Motion Behavior

### Desktop

Enable the dynamic `pretext` experience.

### Mobile

Fall back to the current static homepage list.

### Reduced Motion

If the user prefers reduced motion, disable the moving character and dynamic reflow entirely and keep the static homepage list.

## Failure and Recovery

Any runtime problem should fail safely back to the original homepage list.

Fallback conditions include:

- `pretext` failed to load
- runtime initialization error
- unsupported or narrow viewport
- font measurement mismatch severe enough to break layout
- reduced-motion environment

The page must never end in a half-rendered broken state.

## Performance Constraints

The homepage currently surfaces about 42 articles, so v1 should not attempt a naive full-layout pass on every frame.

The implementation should prefer:

- local relayout for only nearby articles
- throttled resize handling
- position-threshold relayout triggers

The target is a visually smooth character with stable readable text and no obvious layout thrashing.

## Acceptance Criteria

The implementation is considered successful when all of the following are true:

- On desktop, the homepage shows an animated character moving through the left article-flow area
- Nearby article titles and excerpts visibly reflow around the character
- The effect is line-level text avoidance, not just whole-card displacement
- Article order remains stable
- The page does not jump vertically as the character moves
- Sidebar, header, and footer remain unaffected
- Article links remain usable
- Mobile falls back to the existing static list
- Reduced-motion environments fall back to the existing static list
- If the dynamic system fails, the existing static list still works normally

## References

- X post announcing the text measurement and layout work:
  - `https://x.com/_chenglou/status/2037713766205608234`
- `pretext` repository:
  - `https://github.com/chenglou/pretext`

