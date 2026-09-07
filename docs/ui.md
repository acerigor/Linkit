# Linkit — UI Components

Build reference for the Next.js + Tailwind implementation. Every component, variant, state,
layout pattern and accessibility requirement below is taken from the Linkit design system
source. Anything the system does not define is marked **TBD** — do not fill those in.

Read `design-system.md` first for the token layer. All class names referenced here
(`lk-btn`, `lk-tile`, …) ship in `components/components.css`; you can either keep that
stylesheet or reimplement each rule in Tailwind — the values are given either way.

**Inventory: 24 components in 6 groups.** No source codebase or Figma file defined this
inventory; it is authored to what the three product surfaces actually need. Anything a design
system "usually has" but Linkit does not use is listed under §9.

---

## Contents

1. [Core](#1-core) — Icon, Button, IconButton, Badge, Card, Avatar, Highlight
2. [Forms](#2-forms) — Input, Textarea, Select, Switch, Checkbox
3. [Navigation](#3-navigation) — SegmentedControl, Tabs, SidebarNav, Ticker
4. [Feedback](#4-feedback) — Dialog, Toast, Tooltip, EmptyState
5. [Bio page](#5-bio-page) — LinkTile, ProfileHeader, SocialRow, ThemeCard
6. [Dashboard](#6-dashboard) — LinkRow, StatCard
7. [Layout patterns](#7-layout-patterns)
8. [Accessibility](#8-accessibility)
9. [Not defined — TBD](#9-not-defined--tbd)

### Shared state vocabulary

Every interactive component follows these unless it says otherwise.

| State | Behaviour |
| --- | --- |
| Hover | Fills **lighten** one step (never darken). Outline/ghost gain a `grey-100` wash. Cards lift `-2px`, link tiles `-3px` |
| Press | `scale(0.97)`; fills darken one step |
| Focus | `--ring-focus` via `:focus-visible`. Never removed, never restyled per component |
| Disabled | `mint-100` bg + `grey-400` fg for **every** button variant; `cursor: not-allowed`; `opacity .45–.5` for checkbox/switch |
| Loading | **TBD** — no spinner or skeleton exists in the system |

---

## 1. Core

### Icon

Masked Lucide glyph. Colour follows `currentColor`, so one component works ink-on-mint and
mint-on-ink.

```tsx
<Icon name="link" size={20} />
<Icon name="bar-chart-3" size={16} className="text-mint-700" />
<Icon name="trash-2" size={18} title="Delete" />   // labelled = role="img"
```

| Prop | Type | Default | Notes |
| --- | --- | --- | --- |
| `name` | `string` | — | Lucide slug, kebab-case |
| `size` | `number` | `20` | Square px |
| `title` | `string` | — | Accessible label. Omitted ⇒ `aria-hidden="true"` |

**Implementation.** A `<span>` with `background-color: currentColor` and the SVG applied as a
CSS mask from `https://unpkg.com/lucide-static@0.469.0/icons/<slug>.svg`. `LUCIDE_BASE` in
`Icon.jsx` is the single place the URL appears — repoint it to vendor icons locally.

⚠️ **Lucide is a flagged substitution** — no icon set was supplied. 2px stroke, rounded caps.

| Size | Where |
| --- | --- |
| 14 | Inline meta, stat labels, tooltips triggers |
| 16 | Small buttons, row meta |
| 18 | Buttons (md), nav items, row actions |
| 20 | Default; link-tile thumb, trailing arrow |
| 22 | Large buttons, ticker items |
| 28 | Empty-state glyph |
| 44 | Marketing feature cards, bottom-right |

**Rules.** Never hand-roll an inline SVG. No emoji as icons. No Unicode arrows/symbols
(`→ ↗ ×`) — those are `arrow-right`, `arrow-up-right`, `x`. Where Lucide lacks a platform
(TikTok, Threads), use `message-circle` and flag it; do not draw the real mark.

**Working set:** `link` `plus` `pencil` `trash-2` `grip-vertical` `copy` `qr-code` `share-2`
`eye` `mouse-pointer-click` `percent` `users` `bar-chart-3` `trending-up` `trending-down`
`palette` `settings` `bell` `circle-help` `globe` `smartphone` `at-sign` `mail` `calendar`
`shopping-bag` `play` `book-open` `music` `check` `x-circle` `alert-triangle` `info`
`circle-check` `circle-minus` `badge-check` `crown` `chevron-down` `arrow-right`
`arrow-up-right` `zap` `infinity` `gift` `wand-2` `sparkles` `upload` `instagram` `youtube`
`twitter` `linkedin` `message-circle`.

---

### Button

```tsx
<Button variant="primary" size="lg" iconRight="arrow-right">Claim your link</Button>
<Button variant="secondary">Preview</Button>
<Button variant="dark" display>Let's go</Button>
<Button variant="danger" disabled>Delete</Button>
```

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `primary \| dark \| secondary \| ghost \| danger` | `primary` |
| `size` | `sm \| md \| lg` | `md` |
| `block` | `boolean` | `false` |
| `display` | `boolean` | `false` — display face, uppercase. **Marketing only** |
| `iconLeft` / `iconRight` | `string` (Lucide slug) | — |
| `as` | `"button" \| "a"` | `"button"` |

#### Variants

| Variant | Rest | Hover | Press | Use |
| --- | --- | --- | --- | --- |
| `primary` | `bg-mint-500 text-ink-900` | `bg-mint-400` | `bg-mint-600` | The one CTA per view |
| `dark` | `bg-ink-800 text-white` | `bg-ink-700` **+ `text-mint-500`** | — | Secondary CTA on coloured grounds |
| `secondary` | `bg-white text-ink-900 border-2 border-ink-900` | `bg-grey-100` | — | Paired action, "Cancel" |
| `ghost` | `bg-transparent` | `bg-grey-100` | — | Tertiary, in-row |
| `danger` | `bg-rose-500 text-white` | `bg-rose-700` | — | Destructive confirm only |

> The `dark` hover is the system's one label-colour change. It is deliberate — keep it.

#### Sizes

| Size | Height | Padding-x | Font | Glyph |
| --- | --- | --- | --- | --- |
| `sm` | 36px | 16px | `text-sm` | 16 |
| `md` | 46px | 24px | `text-base` | 18 |
| `lg` | 56px | 32px | `text-md` (17) | 22 |

#### States

| State | |
| --- | --- |
| Rest | `rounded-full border-2 border-transparent font-semibold` — the transparent border keeps fill and outline metrics identical |
| Hover | Per table above; 140ms `ease-out` |
| Press | `scale(0.97)`, 90ms |
| Focus | `shadow-focus` on `:focus-visible` |
| Disabled | `bg-mint-100 text-grey-400 border-transparent cursor-not-allowed` — **same for every variant** |
| Loading | **TBD** |

**Rules.** One `primary` per view. `display` only on marketing pages — product UI stays Figtree
semibold. Labels are sentence case (`Add link`, not `Add Link`).

---

### IconButton

```tsx
<IconButton icon="share-2" label="Share" variant="outline" />
<IconButton icon="trash-2" label="Delete link" size="sm" />
```

| Prop | Type | Default |
| --- | --- | --- |
| `icon` | `string` | — |
| `label` | `string` | — **required** |
| `variant` | `ghost \| solid \| outline \| dark \| lemon` | `ghost` |
| `size` | `sm \| md \| lg` | `md` |

| Variant | Rest | Hover |
| --- | --- | --- |
| `ghost` | transparent | `bg-grey-100` |
| `solid` | `bg-mint-500 text-ink-900` | `bg-mint-400` |
| `outline` | `border-2 border-ink-900` | `bg-mint-500` |
| `dark` | `bg-ink-800 text-white` | `bg-ink-700 text-mint-500` |
| `lemon` | `bg-lemon-500 text-ink-900` | `bg-lemon-300` |

Sizes: `sm` 32px (glyph 16) · `md` 40px (18) · `lg` 48px (22). All `rounded-full`.

**`label` is mandatory** and becomes both `aria-label` and `title`. `solid`/`lemon` are for the
public bio page; `ghost` for dashboard rows; `outline` for social rows.

⚠️ At `sm` (32px) the target is under the 44px minimum — only acceptable inside dashboard rows
on pointer devices. Use `md`+ on the public page.

---

### Badge

```tsx
<Badge tone="mint">Live</Badge>
<Badge tone="dark" icon="crown">Pro</Badge>
```

| Prop | Type | Default |
| --- | --- | --- |
| `tone` | `mint \| lemon \| lilac \| sky \| dark \| neutral \| danger \| outline` | `mint` |
| `size` | `md \| lg` | `md` |
| `icon` | `string` | — |

| Tone | Colours | Meaning |
| --- | --- | --- |
| `mint` | `bg-mint-500 text-ink-900` | Live / good |
| `neutral` | `bg-grey-100 text-grey-600` | Off / hidden |
| `danger` | `bg-rose-100 text-rose-700` | Problem |
| `dark` | `bg-ink-800 text-mint-500` | Plan / tier |
| `lemon` `lilac` `sky` | tint + `text-ink-900` | Decorative, marketing |
| `outline` | `inset 0 0 0 2px ink-900` | Marketing counts |

Sizes: `md` 24px / `text-xs` · `lg` 30px / `text-sm`. Always **UPPERCASE**, `font-bold`,
`tracking-wide` (0.04em), `rounded-full`, `whitespace-nowrap`. One or two words max.

Static — no hover, press or focus states.

---

### Card

```tsx
<Card tone="mint" title="One link, everything on it" body="Add every link you own…" />
<Card tone="lemon" pad="lg" pop title="Set up in 2 minutes flat" />
```

| Prop | Type | Default |
| --- | --- | --- |
| `tone` | `default \| neutral \| mint \| lemon \| lilac \| dark \| outline` | `default` |
| `pad` | `none \| sm \| md \| lg` | `md` |
| `interactive` | `boolean` | `false` |
| `elevated` | `boolean` | `false` |
| `pop` | `boolean` | `false` |
| `title` / `body` | `ReactNode` | — |

| Tone | Fill |
| --- | --- |
| `default` | `bg-white` |
| `neutral` | `bg-grey-100` |
| `mint` / `lemon` / `lilac` | `bg-mint-100` / `bg-lemon-500` / `bg-lilac-100` |
| `dark` | `bg-ink-800 text-white` |
| `outline` | `bg-white` + `inset 0 0 0 2px ink-900` |

Padding: `none` 0 · `sm` 16 · `md` 24 · `lg` 40. Radius `rounded-xl` (28px), `overflow-hidden`,
`flex flex-col`.

| Flag | Effect |
| --- | --- |
| `interactive` | `cursor-pointer`; hover `-translate-y-0.5` + `shadow-md`, 200ms |
| `elevated` | `shadow-md` at rest |
| `pop` | `border-2 border-ink-900` + `shadow-pop` (`4px 4px 0` ink) |

`title` renders in the display face at `text-d-sm` (28px); `body` is `text-sm text-grey-600`.

**Rules.** No border and no shadow by default — depth is not how Linkit signals importance,
colour is. In a six-card grid tint **two or three** and leave the rest `grey-100`/white; never
two saturated fills touching. `pop` is for the hero card and at most one feature card per page.

---

### Avatar

```tsx
<Avatar name="Maya Okonkwo" size={96} ring />
<Avatar name="Dev Patel" size={36} tone="lilac" />
```

| Prop | Type | Default |
| --- | --- | --- |
| `name` | `string` | `""` — first letters of the first two words become the fallback |
| `src` | `string` | — |
| `size` | `number` | `56` |
| `tone` | `mint \| lemon \| lilac \| sky \| dark` | `mint` |
| `ring` | `boolean` | `false` — white + ink double ring |
| `square` | `boolean` | `false` — `rounded-lg` instead of a circle |

Initials render in the display face at `0.38 × size`, ink on the tint (`dark` → mint on ink).
`<img>` gets `object-cover` and `alt={name}`.

**Initials-on-tint is the intended default, not a degraded state.** Rotate tones across a list so
adjacent avatars differ. `ring` only on the public bio page, where the avatar sits on a
coloured ground. Sizes in use: 96 (bio page), 72 (compact bio), 64 (settings), 40/36/32 (rows).

---

### Highlight

The brand's signature device. See `design-system.md` §3.

```tsx
<h1 className="linkit-display text-d-lg">
  One link.<br /><Highlight>Everything you make.</Highlight>
</h1>
```

| Prop | Type | Default |
| --- | --- | --- |
| `tone` | `lemon \| mint \| lilac \| sky \| dark` | `lemon` |
| `straight` | `boolean` | `false` — drops the `-1.6deg` rotation |

`inline-block`, `px-[0.28em] pt-[0.06em] pb-[0.1em]`, `-rotate-[1.6deg]`, `text-ink-900`
(`dark` tone → `bg-ink-800 text-mint-500`).

**Rules.** Display face only, uppercase, **one per headline** (two stacked at most, alternating
tones). Never on body copy, never on a button. Static — no states.

---

## 2. Forms

All fields share the shell: `rounded-md` (14px), `border` `grey-300`, `bg-white`, 52px tall
(`sm` 42px), hover `border-grey-400`, focus `border-mint-600` + `shadow-focus`.

### Input

```tsx
<Input label="Your Linkit" prefix="linkit.to/" placeholder="yourname" hint="You can change this later." />
<Input label="Email" icon="mail" error="That address is already taken." />
```

| Prop | Type | Notes |
| --- | --- | --- |
| `label` | `string` | Renders a `<label htmlFor>` |
| `hint` | `string` | `text-xs text-grey-500`; **hidden while `error` is set** |
| `error` | `string` | `text-xs font-medium text-rose-500` + rose border |
| `icon` | `string` | Lucide slug, leading edge, 18px, `text-grey-500` |
| `prefix` | `ReactNode` | Static leading text — **how the handle field is always presented** |
| `suffix` | `ReactNode` | Char count, unit, small button |
| `size` | `sm \| md` | `md` = 52px, `sm` = 42px |

| State | |
| --- | --- |
| Rest | `border-grey-300` |
| Hover | `border-grey-400` |
| Focus-within | `border-mint-600` + `shadow-focus` |
| Invalid | `border-rose-500`; focus ⇒ `shadow-focus-danger` |
| Disabled | `bg-grey-100 border-grey-200 text-grey-400` |

The focus ring lives on the **wrapper** (`:focus-within`), not the bare `<input>` — the inner
input has `border:0; outline:0; background:transparent`. Keep that so prefix/suffix sit inside
the ring.

`id` falls back to `name`, so pass one or the other for the label association to work.

---

### Textarea

```tsx
<Textarea label="Bio" maxLength={80} value={bio} onChange={e => setBio(e.target.value)} />
```

| Prop | Notes |
| --- | --- |
| `label` / `hint` / `error` | As `Input` |
| `maxLength` | With a **controlled string `value`**, a live `n/max` counter renders bottom-right |

`min-h-[112px]`, `resize-vertical`, `px-4 py-3`. Focus ring on the element itself.

Used for the profile bio (80-char cap) and link descriptions.

---

### Select

Native `<select>` in the Linkit shell — 52px, `rounded-md`, `appearance-none`, chevron affix
absolutely positioned right 16px, `pointer-events-none`.

```tsx
<Select label="Link type" options={[{ value: "url", label: "Website" }, { value: "embed", label: "Embed" }]} />
```

| Prop | Notes |
| --- | --- |
| `options` | `Array<string \| {value,label}>`. Ignored if `children` are passed |
| `label` / `hint` / `error` | As `Input` |

Native on purpose: correct mobile behaviour and keyboard support for free. A custom listbox is
**TBD** — the system has no popover/combobox component.

---

### Switch

```tsx
<Switch checked={live} onChange={setLive} label="Visible on my page" />
<Switch size="sm" checked={pinned} onChange={setPinned} />
```

| Prop | Type | Default |
| --- | --- | --- |
| `checked` | `boolean` | `false` |
| `onChange` | `(next: boolean) => void` | — |
| `label` | `string` | — inline, right of the track |
| `size` | `sm \| md` | `md` |
| `disabled` | `boolean` | `false` |

| Size | Track | Thumb | Travel |
| --- | --- | --- | --- |
| `md` | 52×30 | 24px | 22px |
| `sm` | 40×24 | 18px | 16px |

| State | |
| --- | --- |
| Off | Track `bg-grey-300` |
| On | Track `bg-mint-500` |
| Thumb | `bg-white shadow-xs`; travels on 200ms **`ease-spring`** — one of only two places overshoot is allowed |
| Disabled | `opacity .5 cursor-not-allowed` |

**Implementation.** A `<label>` wrapping a visually-hidden real `<input type="checkbox">`
(`position:absolute; opacity:0; w-1 h-1`) plus the painted track/thumb. Keep it — it gives
keyboard, screen-reader and form semantics for free. State is driven by `data-on` /
`data-disabled` on the label.

**Rules.** Switches are for **instantly-saved** settings (link visibility, theme options). A
setting behind a submit button is a `Checkbox`.

---

### Checkbox

Checkbox and radio are one component; the only difference is `type`.

```tsx
<Checkbox checked={agree} onChange={setAgree}>I agree to the terms</Checkbox>
<Checkbox type="radio" checked={plan === "pro"} onChange={() => setPlan("pro")}>Pro</Checkbox>
```

| Prop | Type | Default |
| --- | --- | --- |
| `checked` | `boolean` | `false` |
| `onChange` | `(next: boolean) => void` | — |
| `type` | `"checkbox" \| "radio"` | `"checkbox"` |
| `disabled` | `boolean` | `false` |

22×22 box, `border-2 border-ink-900`, `rounded-xs` (radio: `rounded-full`), `bg-white`.
Checked ⇒ `bg-mint-500` + a 14px `check` glyph (radio: a 10px ink dot). Disabled ⇒ `opacity .45`.
Label is `text-sm`, `items-start` so multi-line labels align to the box.

Same visually-hidden-real-input technique as `Switch`. For radios, **set a shared `name`** on the
inputs so the group is a real radio group.

---

## 3. Navigation

### SegmentedControl

```tsx
<SegmentedControl block items={["Links", "Appearance"]} value={tab} onChange={setTab} />
<SegmentedControl size="sm" items={["7d", "30d", "All"]} value={range} onChange={setRange} />
```

| Prop | Type | Default |
| --- | --- | --- |
| `items` | `Array<string \| {value,label}>` | — |
| `value` / `onChange` | `string` / `(next) => void` | — |
| `size` | `sm \| md` | `md` |
| `block` | `boolean` | `false` — stretch, segments share width |

Track: `inline-flex p-1 gap-1 bg-white border border-grey-300 rounded-full`.
Segments: 44px (`sm` 34px), `rounded-full`, **display face uppercase** `text-sm` (`sm`: `text-xs`).

| State | |
| --- | --- |
| Inactive | transparent; hover `bg-grey-100` |
| Active | `bg-ink-800 text-mint-500`; hover `bg-ink-700` |

Transition 200ms `ease-out`. `role="tablist"`, segments `role="tab"` + `aria-selected`.

**Rules.** Two or three items only. Four or more is a `Tabs`.

---

### Tabs

```tsx
<Tabs items={[{ value: "clicks", label: "Clicks", icon: "mouse-pointer-click" }]} value={t} onChange={setT} />
```

| Prop | Type |
| --- | --- |
| `items` | `Array<string \| {value,label,icon?}>` |
| `value` / `onChange` | `string` / `(next) => void` |

Bar: `flex gap-6 border-b border-grey-200`. Item: `pb-3 text-sm font-semibold text-grey-500`,
hover ⇒ `text-ink-900`. Active ⇒ `text-ink-900` plus a `::after` indicator, 3px,
`rounded-full bg-mint-500`, pinned `bottom-[-1px]` so it sits on the border.

For four or more views. Also used as the dashboard's collapsed navigation below 1140px.

---

### SidebarNav

The dashboard's fixed 240px left rail.

```tsx
<SidebarNav
  brand="Linkit"
  items={[{ value: "links", label: "Links", icon: "link", count: 8 }]}
  value={view} onChange={setView}
  footer={<AccountCard />}
/>
```

| Prop | Type | Notes |
| --- | --- | --- |
| `brand` | `string` | `"Linkit"`. **No logo file exists** — this is display-face text. See §9 |
| `items` | `{value,label,icon,count?}[]` | |
| `value` / `onChange` | | |
| `footer` | `ReactNode` | `margin-top:auto` — account card, upgrade CTA |

Rail: `w-60 p-4 bg-white border-r border-grey-200 flex flex-col gap-1`.
Wordmark: display face `text-d-xs`, padding `12px 12px 24px`.
Item: 44px, `rounded-md px-3 text-sm font-semibold text-grey-600`, hover `bg-grey-100 text-ink-900`.
**Active: `bg-mint-100 text-ink-900`, and the glyph turns `mint-700`.** `count` renders
`ml-auto text-xs text-grey-500`.

The active mint-100 pill is the **only** colour in the rail.

---

### Ticker

Full-bleed scrolling claim rail.

```tsx
<Ticker items={[{ label: "One link forever", icon: "infinity" }, { label: "Loads in 0.2s", icon: "zap" }]} />
```

| Prop | Type | Default |
| --- | --- | --- |
| `items` | `Array<string \| {label,icon?}>` | — |
| `tone` | `lemon \| mint \| dark \| lilac` | `lemon` |
| `speed` | `string` | `--dur-marquee` (28s) |

Rail: `overflow-hidden py-3`, `bg-lemon-500 text-ink-900` (`dark` ⇒ `bg-ink-800 text-mint-500`).
Track: `flex w-max animate-marquee` (28s linear infinite, `translateX(0 → -50%)`).
Item: display face uppercase `text-d-xs` (22px), `whitespace-nowrap`, gap 40px, 22px glyph.

**The content group renders twice** — the duplicate carries `aria-hidden="true"` — so the loop is
seamless. Keep it to 4–6 short claims.

Placement: directly under a hero or above a footer, **edge to edge, zero margin**. It is the only
continuous animation in the system; freeze it with `motion-reduce:animate-none`.

---

## 4. Feedback

### Dialog

```tsx
<Dialog
  title="Delete this link?"
  glyph="trash-2"
  confirmLabel="Yes, delete"
  confirmVariant="danger"
  onCancel={close}
  onClose={close}
>
  It disappears from your page right away. This cannot be undone.
</Dialog>
```

| Prop | Type | Default |
| --- | --- | --- |
| `open` | `boolean` | `true` — returns `null` when false |
| `title` | `ReactNode` | display face `text-d-sm` |
| `glyph` | `string` | Lucide slug in a 64px `bg-rose-100 text-rose-500` circle — **destructive only** |
| `align` | `center \| left` | `center` |
| `confirmLabel` / `onConfirm` | | |
| `cancelLabel` / `onCancel` | `"Cancel"` | |
| `confirmVariant` | `primary \| danger \| dark` | `primary` |
| `onClose` | `() => void` | Fires on scrim click |

Scrim: `fixed inset-0 z-[100] grid place-items-center p-6 bg-ink-900/45 backdrop-blur-[4px]`.
Panel: `w-full max-w-[460px] bg-white rounded-lg p-8 shadow-lg text-center`.
Actions: `flex gap-3 mt-8`, children `flex-1` — **always paired and equal width**, destructive on
the right.

| Requirement | Status |
| --- | --- |
| `role="dialog"` `aria-modal="true"` | ✅ shipped |
| Scrim click closes; inner click `stopPropagation` | ✅ shipped |
| **Focus trap** | ⚠️ **not implemented** — add it (Radix Dialog or `focus-trap-react`) |
| **Escape to close** | ⚠️ **not implemented** — wire `onClose` to `keydown` |
| **Return focus to trigger** | ⚠️ **not implemented** |
| **`aria-labelledby` → title** | ⚠️ **not implemented** — add an id and reference it |
| Body scroll lock | ⚠️ **not implemented** |

> The design system's `Dialog` is a visual spec. In Next.js, keep these visuals and put them on
> a headless primitive (Radix) rather than shipping the raw version.

Enter/exit animation: **TBD** — the system defines none (fades are sanctioned for scrims).

---

### Toast

```tsx
<Toast tone="success">Link copied</Toast>
<Toast tone="danger" action="Retry">Could not save</Toast>
```

| Prop | Type | Default |
| --- | --- | --- |
| `tone` | `neutral \| success \| warning \| danger` | `neutral` |
| `icon` | `string` | Per-tone default |
| `action` | `ReactNode` | Inline underlined affordance (undo/retry) |

| Tone | Colours | Default glyph |
| --- | --- | --- |
| `neutral` | `bg-ink-800 text-white` | `info` |
| `success` | `bg-mint-500 text-ink-900` | `check` |
| `warning` | `bg-lemon-500 text-ink-900` | `alert-triangle` |
| `danger` | `bg-rose-500 text-white` | `x-circle` |

`flex items-center gap-3 px-5 py-3 rounded-full text-sm font-semibold shadow-md`.

Placement: `fixed z-[120] left-1/2 -translate-x-1/2 bottom-6`. Auto-dismiss **1800ms** in the
kits.

`role="status"` is shipped (polite announcement). **Rules:** one line, no title, no close button,
never stack more than one. Anything with a title is a `Dialog`.

---

### Tooltip

```tsx
<Tooltip label="Clicks in the last 7 days"><Icon name="info" size={14} /></Tooltip>
```

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `ReactNode` | — |
| `placement` | `top \| bottom` | `top` |

Bubble: `absolute z-40 left-1/2 -translate-x-1/2 bottom-[calc(100%+8px)] bg-ink-800 text-white
rounded-sm px-3 py-2 text-xs font-medium whitespace-nowrap`. `opacity 0 → 1` on
`:hover` **and `:focus-within`**, 140ms.

Short labels only — it never wraps. No arrow, no delay, no collision detection (**TBD**).

⚠️ CSS-only, so it is not announced by screen readers. When a tooltip is the *only* label, also
put the text in `aria-label` on the trigger, or use `aria-describedby`.

---

### EmptyState

```tsx
<EmptyState
  title="Nothing here yet"
  body="Add your first link and it shows up on your page instantly."
  actionLabel="Add a link"
  onAction={add}
/>
```

| Prop | Type | Default |
| --- | --- | --- |
| `glyph` | `string` | `"link"` |
| `title` / `body` | `ReactNode` | |
| `actionLabel` / `onAction` | | Renders a `primary` button with `iconLeft="plus"` |

`flex flex-col items-center gap-4 py-16 px-6 text-center`, **`border-2 border-dashed
border-grey-300 rounded-xl`** — the only dashed border in the system. Glyph: 64px
`rounded-full bg-mint-100 text-mint-700` circle with a 28px icon. Title display face `text-d-sm`;
body `text-sm text-grey-600 max-w-[44ch]`.

**Copy rule.** Encouraging, never apologetic — say what to do next, not that something is
missing. "Nothing here yet", not "No links found".

---

## 5. Bio page

### LinkTile

**The single most important element in the product.** The row a visitor taps.

```tsx
<LinkTile label="New album out now" sublabel="open.spotify.com" icon="music" badge={<Badge tone="lemon">New</Badge>} />
<LinkTile variant="fill" label="Book a session" icon="calendar" />
<LinkTile variant="feature" label="Watch the trailer" thumb="/cover.jpg" />
```

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `ReactNode` | — display face uppercase `text-md` (17), LH 1.15 |
| `sublabel` | `ReactNode` | — bare domain, `text-xs text-grey-600`, truncates |
| `icon` | `string` | Lucide slug for the leading 44px square |
| `thumb` | `string` | Image URL. With `variant="feature"` becomes a 150px banner |
| `variant` | `outline \| soft \| fill \| feature` | `outline` |
| `pill` | `boolean` | `false` — `rounded-full` instead of 20px |
| `badge` | `ReactNode` | Rendered before the trailing icon |
| `trailingIcon` | `string \| null` | `"arrow-up-right"` |
| `as` | `"button" \| "a"` | `"button"` |

| Variant | Look |
| --- | --- |
| `outline` | `bg-[--bio-tile-bg] border-2 border-[--bio-tile-border]` — the default |
| `soft` | Borderless white; hover uses `shadow-md` instead of `shadow-pop` |
| `fill` | `bg-ink-800 text-white border-ink-900`; thumb `bg-ink-700 text-mint-500` |
| `feature` | Column layout, thumb becomes a full-width 150px banner, `rounded-md` |

| State | |
| --- | --- |
| Rest | `w-full flex items-center gap-4 px-5 py-4 rounded-lg text-left` |
| Hover | `-translate-y-[3px]` + **`shadow-pop`** (`4px 4px 0` ink), 200ms `ease-spring` |
| Press | `translate-y-0 scale-[0.97]`, shadow removed — reads as pushed flat against the page |
| Focus | `shadow-focus` |

**Theming.** The tile reads `--bio-tile-bg` / `--bio-tile-border` / `--bio-tile-fg` / `--bio-tile-radius`
from its ancestor. **Set them once on the page root per theme** — no tile needs to know which
theme is active:

```tsx
<div style={{ "--bio-tile-bg": "#fff", "--bio-tile-border": "var(--ink-900)" } as React.CSSProperties}>
```

**Rules.** One `feature` tile per page at most, and put it first. One `fill` tile per page — it is
the primary/paid action. Label is display-face uppercase; sublabel is the bare domain. Tap
target is 76px tall — comfortably over the 44px floor.

Render as `<a>` for real links so middle-click, long-press and "open in new tab" work.

---

### ProfileHeader

```tsx
<ProfileHeader name="Maya Okonkwo" handle="mayamakes" bio="Ceramics, in Lagos." verified />
```

| Prop | Type | Default |
| --- | --- | --- |
| `name` | `string` | — display face `text-d-sm` |
| `handle` | `string` | Rendered with a leading `@`, `text-sm font-semibold opacity-70` |
| `bio` | `ReactNode` | `text-sm max-w-[34ch] opacity-85` |
| `avatarSrc` / `avatarTone` / `size` | | `size` default 96 |
| `verified` | `boolean` | Adds a 22px `badge-check` glyph after the name |
| `align` | `center \| left` | `center` |

`flex flex-col items-center gap-3 text-center`; `align="left"` flips both. Avatar always
`ring`ed. Renders as `<header>` with the name as `<h1>` — correct on the public page, but
**demote it to `<h2>`/`<div>` when embedded** in the dashboard preview or a marketing hero.

The 34ch bio cap is deliberate: it makes line breaks predictable across themes.

---

### SocialRow

```tsx
<SocialRow variant="outline" items={[{ icon: "instagram", label: "Instagram" }, { icon: "mail", label: "Email" }]} />
```

| Prop | Type | Default |
| --- | --- | --- |
| `items` | `{icon,label,href?,onClick?}[]` | — |
| `variant` | passthrough to `IconButton` | `ghost` |
| `size` | `sm \| md \| lg` | `md` |
| `align` | `center \| left` | `center` |

`flex flex-wrap justify-center gap-2`. Sits between `ProfileHeader` and the link stack.

**Cap it at six** — anything beyond belongs in the link stack as a tile. Each glyph inherits
`IconButton`'s mandatory `label`.

⚠️ `items[].href` is accepted but the current implementation renders buttons and ignores it.
Render real anchors in the Next.js build.

---

### ThemeCard

Swatch card in the dashboard Appearance picker.

```tsx
<ThemeCard name="Mint" bg="var(--mint-500)" tileBg="#fff" tileBorder="var(--ink-900)" selected onSelect={pick} />
```

| Prop | Type |
| --- | --- |
| `name` | `string` |
| `bg` | `string` — page ground; any CSS colour |
| `tileBg` | `string` — tile fill in the preview |
| `tileBorder` | `string?` — omit for borderless themes |
| `selected` / `onSelect` | | 

Card: `border-2 border-grey-200 rounded-md bg-white overflow-hidden`.
Preview: 104px tall, three 12px `rounded-full` bars on the `bg` ground.
Name: `px-3 py-2 text-xs font-bold border-t border-grey-200`.

| State | |
| --- | --- |
| Hover | `-translate-y-0.5` |
| Selected | `border-ink-900` + a 22px `bg-ink-900 text-mint-500` check badge, top-right |

`<button aria-pressed={selected}>`. The preview is **abstract — three bars on a ground, never a
screenshot**.

**Shipped themes:** Mint, Lemon, Lilac, Ink, Paper.

| Theme | `bg` | Tile | `--bio-fg` |
| --- | --- | --- | --- |
| Mint | `mint-500` | white, ink border | `ink-900` |
| Lemon | `lemon-500` | white, ink border | `ink-900` |
| Lilac | `lilac-500` | white, ink border | `ink-900` |
| Ink | `ink-800` | `ink-700`, no border (`soft`) | `white` — **also add `.linkit-on-dark`** |
| Paper | `grey-100` | white, no border (`soft`) | `ink-900` |

---

## 6. Dashboard

### LinkRow

One editable link in the dashboard list.

```tsx
<LinkRow title="New album out now" url="open.spotify.com/album/…" clicks={1284} live onToggle={setLive} />
```

| Prop | Type | Notes |
| --- | --- | --- |
| `title` | `ReactNode` | `text-base font-bold`, truncates |
| `url` | `ReactNode` | **`font-mono text-xs text-grey-500`**, truncates |
| `clicks` | `number?` | Omit to hide the metric. Rendered `.toLocaleString()` with a 14px `mouse-pointer-click` glyph |
| `live` / `onToggle` | | Renders a `sm` `Switch` |
| `onEdit` / `onDelete` | | `sm` ghost `IconButton`s (`pencil`, `trash-2`) |
| `dragging` | `boolean` | `border-mint-600` + `shadow-md` |

Row: `flex flex-wrap items-center gap-x-4 gap-y-3 p-4 bg-white border border-grey-200
rounded-md`, hover `border-grey-300 shadow-sm`. Grip: `grip-vertical` 18px, `text-grey-400`,
`cursor-grab`. Main block `flex: 1 1 180px; min-width: 150px`; meta cluster `ml-auto`.

Stack rows with `gap-3`. URLs are **always mono** so they read as data, not copy.

| Requirement | Status |
| --- | --- |
| Reflow (title/URL never crushed) | ✅ wraps at narrow widths |
| **Keyboard reordering** | ⚠️ **not implemented.** The grip is mouse-only. Add keyboard reorder (`ArrowUp`/`ArrowDown` on a focused grip) plus an `aria-live` position announcement — see §8 |
| Drag-and-drop library | **TBD** — the system does not specify one |

---

### StatCard

```tsx
<StatCard icon="eye" label="Page views" value="12,480" delta="+12.4%" tone="mint" />
```

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `ReactNode` | Uppercase `text-xs font-bold tracking-[0.08em] opacity-65` |
| `value` | `ReactNode` | **Pre-formatted** — the component does not format numbers |
| `delta` | `ReactNode` | e.g. `"+12.4%"` |
| `direction` | `up \| down` | `up` → `text-mint-700` + `trending-up`; `down` → `text-rose-500` + `trending-down` |
| `icon` | `string` | 14px, before the label |
| `tone` | `neutral \| mint \| lemon \| lilac \| dark` | `neutral` (`bg-grey-100`) |

`flex flex-col gap-2 p-5 rounded-lg`. Value in the display face at `text-d-md` (40px), LH 1.

**One tinted tile per row of four** — the rest stay `grey-100`. Static; no states.

⚠️ `direction` drives colour **and** glyph, but colour alone would fail for colour-blind users —
the arrow glyph is doing the accessible work. Keep it; never render a delta without it.

---

## 7. Layout patterns

### Public bio page

```
┌─ page root: bg = theme, sets --bio-tile-* ─────────┐
│  [Share]                              (top-right)  │
│  ┌── max-w-bio (580px), mx-auto, px-5 ──────────┐   │
│  │  ProfileHeader        (avatar 96, ring)      │   │
│  │  SocialRow            (≤6, gap-2)            │   │
│  │  ── link stack, gap-3 ──                     │   │
│  │  LinkTile × n         (≤1 feature, ≤1 fill)  │   │
│  │  footer: "MADE WITH" + Linkit button         │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

- One column at every width — no breakpoints needed. `pb-16`.
- Theme sets four custom properties on the root; nothing below needs to know the theme.
- Ink theme adds `.linkit-on-dark`.
- The "Made with Linkit" footer badge is always present on free pages.
- Tap targets **never below 44px** here.

### Creator dashboard

```
┌ SidebarNav 240 ┬ top bar (sticky) ───────────────────────┐
│  wordmark      │  linkit.to/handle · Live ·  ⋯ View page │
│  nav items     ├──────────────────┬──────────────────────┤
│  ⋯             │  content         │  preview 400px       │
│  footer:       │  max-w-page      │  phone frame 320      │
│  account +     │  p-6             │  renders the REAL    │
│  Upgrade       │                  │  BioPage component   │
└────────────────┴──────────────────┴──────────────────────┘
```

- **Below 1140px:** the rail collapses into a `Tabs` row under the top bar and the preview moves
  behind a "Preview" toggle (`smartphone` glyph) in the header. Every view stays reachable.
- The preview imports the public page **verbatim** — never a second implementation of it.
- One `primary` button per view; everything else `secondary`/`dark`/`ghost`.
- Deleting always confirms via `Dialog`. Everything else saves instantly and reports via `Toast`.
- Fixed/sticky: rail, top bar, preview column, toasts (`fixed bottom-6`), scrims (`fixed inset-0`).

### Marketing page

Section grounds alternate as full-bleed bands, **never two saturated grounds touching**:

| Order | Ground | Content |
| --- | --- | --- |
| 1 | `bg-mint-500` | Hero — headline + `Highlight`, handle claim field, live product card (`shadow-pop`) |
| 2 | `bg-lemon-500` | `Ticker` — edge to edge, zero margin |
| 3 | `bg-white` | Feature grid — 6 cards, 2–3 tinted |
| 4 | `bg-ink-800` + `.linkit-on-dark` | How it works — 3 numbered steps |
| 5 | `bg-white` | Comparison table, mint column highlighted |
| 6 | `bg-lemon-500` | CTA band |
| 7 | `bg-ink-900` + `.linkit-on-dark` | Footer — 5 columns |

- Bands are edge-to-edge with **no rounded corners**; only the content inside is inset
  (`max-w-page mx-auto`, `px-6`).
- Header is `sticky top-0 z-50` with `bg-white/[.72]` + `backdrop-blur-[18px]`.
- Every headline: display face, uppercase, **at most one `Highlight`**.
- Body copy stays Figtree sentence case even inside loud sections.
- Prefer intrinsic grids over breakpoints:
  `[grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))]`.

### General layout rules

- **Flex/grid + `gap` for every sibling group** — never margins between inline siblings.
- Three widths only: 580 / 1200 / 240.
- Transparency and blur in exactly three places: sticky headers, modal scrims, the bio-page
  theme picker. Never decorative.
- Fluid everywhere except the fixed dashboard rail and preview column.

---

## 8. Accessibility

### What the system already does

| | |
| --- | --- |
| Focus visibility | One ring (`--ring-focus`) applied via `:focus-visible` globally. Mint halo + 1px ink hairline survives mint, lemon and white grounds |
| Contrast | Ink-on-brand-fill pairs run 12–15:1. `white`-on-`mint` is banned system-wide |
| Reduced motion | `prefers-reduced-motion` zeroes the duration/scale/lift tokens |
| Real inputs | `Switch` and `Checkbox` wrap visually-hidden native inputs — keyboard and AT semantics for free |
| Label association | `Input`/`Textarea`/`Select` use `<label htmlFor>`, `id` falling back to `name` |
| Icon semantics | `Icon` is `aria-hidden` unless given `title`; `IconButton` **requires** `label` |
| Live regions | `Toast` is `role="status"` |
| Roles | `SegmentedControl`/`Tabs` are `role="tablist"`/`"tab"` + `aria-selected`; `ThemeCard` is `aria-pressed`; `Dialog` is `role="dialog" aria-modal` |
| Decorative duplicates | The `Ticker`'s duplicated track is `aria-hidden="true"` |
| Colour never alone | `StatCard` deltas pair colour with a direction glyph; `Badge` tones pair with text |

### What you must add in the Next.js build

| Gap | Fix |
| --- | --- |
| **Dialog focus trap** | Not implemented. Put the visuals on Radix Dialog (or `focus-trap-react`) |
| **Escape to close** | Not implemented. Wire `onClose` to `keydown` |
| **Return focus to trigger** | Not implemented |
| **`aria-labelledby` on Dialog** | Give the title an id and reference it |
| **Body scroll lock** | Not implemented while a scrim is open |
| **Tooltip announcement** | CSS-only, so silent to AT. Add `aria-describedby`, or duplicate the text in `aria-label` when the tooltip is the only label |
| **Keyboard reordering in `LinkRow`** | The grip is mouse-only. Add `ArrowUp`/`ArrowDown` on a focused grip plus an `aria-live` announcement of the new position |
| **Tabs keyboard model** | `Tabs`/`SegmentedControl` set roles but not arrow-key navigation or `tabindex` management. Implement the full ARIA tabs pattern, or drop `role="tablist"` and ship them as plain buttons |
| **`tabpanel` wiring** | No `aria-controls` / `id` / `role="tabpanel"` links tabs to their panels |
| **`SocialRow` anchors** | Renders buttons; `href` is ignored. Render `<a>` so links behave like links |
| **`ProfileHeader` heading level** | Hard-codes `<h1>`. Correct standalone; demote when embedded in a preview or hero |
| **Skip link** | None exists. Add one on the dashboard and marketing site |
| **`prefers-reduced-motion` on literal utilities** | Token-backed classes stop for free; hard-coded `duration-200` and the marquee do not. Add `motion-reduce:` variants |
| **`lang` attribute** | Set it on `<html>` |

### Targets and sizing

| | |
| --- | --- |
| Public bio page | **Never below 44px.** `LinkTile` is 76px; social glyphs `md` (40px) minimum — do not use `sm` here |
| Dashboard | 36px floor (`Button sm`). `IconButton sm` is 32px — pointer-device rows only |
| Text | 11px (`text-2xs`) is the absolute floor, meta and legal only. Never below |
| Zoom | Everything is `rem`/token based, so 200% zoom reflows. Avoid fixed heights on text containers |

### Colour-blindness

Mint and lemon are close in luminance for deuteranopes. Never let mint-vs-lemon be the **only**
signal — pair with text (`Badge`) or a glyph (`StatCard`). The `Live`/`Hidden` distinction is
carried by the badge label and the switch position, not only by colour.

### Not defined

Screen-reader copy for the link stack, form validation announcement timing, and a formal WCAG
conformance target are all **TBD**.

---

## 9. Not defined — TBD

Do not invent these.

### Components deliberately absent

Accordion, Breadcrumb, Pagination, DataTable, DatePicker, Slider, Popover, Combobox, Drawer,
Menu/Dropdown, Skeleton, Spinner, Progress, Alert/Banner, Stepper, FileUpload.

None appears in the three product surfaces. Adding one invents a convention designers cannot
check against anything — if you need one, ask design first.

### Missing pieces

| Item | Status |
| --- | --- |
| Logo / brand mark | **None exists.** Wherever a mark would go, "Linkit" is set in the display face, uppercase. **Do not draw, generate or approximate one.** Once a real `logo.svg` lands, `SidebarNav`'s `brand` and the marketing header switch to it |
| Brand fonts | **TBD.** Archivo / Figtree / DM Mono are flagged substitutions |
| Icon set | **TBD.** Lucide is a flagged substitution |
| Illustrations | **None.** Kits use 44px Lucide glyphs in the corner of feature cards where illustrations would sit |
| Photography | **None.** Flat colour blocks and initials avatars are the accepted stand-in |
| Loading / skeleton states | **TBD** for every component |
| Dialog enter/exit animation | **TBD** |
| Tooltip delay / collision handling | **TBD** |
| Drag-and-drop library | **TBD** |
| Toast queueing (more than one at a time) | **TBD** — the rule today is "never stack" |
| Form validation timing (blur vs submit) | **TBD** |
| z-index scale | **TBD.** Ad-hoc today: header 50, tooltip 40, dialog 100, toast 120 |
| Chart / data-viz palette | **TBD.** Only precedent: `mint-500` current bar, `mint-200` rest |
| Breakpoint tokens | **TBD.** See `design-system.md` §7 |
| App-wide dark mode | **TBD.** Only the `.linkit-on-dark` section scope exists |
| RTL / localisation | **TBD** |

### Product model assumptions

These were **inferred**, not specified. Confirm before building:

- Five themes: Mint, Lemon, Lilac, Ink, Paper.
- Free tier: 10-link cap, "Made with Linkit" footer badge shown.
- Pro removes both; `Badge tone="dark" icon="crown"` marks Pro features.
- Per-link analytics: views, clicks, click rate, unique visitors, referrers, top links.
- Handle format `linkit.to/<handle>`.
