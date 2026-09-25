# Linkit — Design System

Foundations reference for the Next.js + Tailwind build. Every value here is taken from the
Linkit design system source (`styles.css` → `tokens/*.css`). Where the system does not define
something, the row says **TBD** rather than guessing.

**Source of truth:** `tokens/colors.css`, `tokens/typography.css`, `tokens/spacing.css`,
`tokens/radius.css`, `tokens/elevation.css`, `tokens/motion.css`, `tokens/semantic.css`.

**Two-layer rule.** Raw ramps (`--mint-500`) exist so semantic aliases (`--btn-primary-bg`) can
point at them. **Application code references the semantic layer.** A raw ramp step in a
component is a bug unless the component *is* the thing defining that semantic (e.g. `Button`).

---

## 1. Tailwind config

Everything below assumes this config. It maps the CSS custom properties into Tailwind so both
layers stay in sync — change a token, every class follows.

```js
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    // NOTE: `colors`, `spacing`, `borderRadius`, `boxShadow`, `screens` below REPLACE
    // Tailwind's defaults rather than extending them. That is deliberate: it makes an
    // off-system value (bg-slate-500, p-7, rounded-3xl) a build error instead of a diff.
    colors: {
      transparent: "transparent",
      current: "currentColor",
      white: "var(--white)",          // #FFFFFF
      black: "var(--black)",          // #0A0A0A — not used in product UI, see §2
      mint:  { 100: "var(--mint-100)", 200: "var(--mint-200)", 300: "var(--mint-300)",
               400: "var(--mint-400)", 500: "var(--mint-500)", 600: "var(--mint-600)",
               700: "var(--mint-700)" },
      ink:   { 600: "var(--ink-600)", 700: "var(--ink-700)", 800: "var(--ink-800)", 900: "var(--ink-900)" },
      lemon: { 100: "var(--lemon-100)", 300: "var(--lemon-300)", 500: "var(--lemon-500)", 700: "var(--lemon-700)" },
      lilac: { 100: "var(--lilac-100)", 300: "var(--lilac-300)", 500: "var(--lilac-500)", 700: "var(--lilac-700)" },
      sky:   { 100: "var(--sky-100)", 300: "var(--sky-300)", 500: "var(--sky-500)", 700: "var(--sky-700)" },
      rose:  { 100: "var(--rose-100)", 500: "var(--rose-500)", 700: "var(--rose-700)" },
      grey:  { 50: "var(--grey-50)", 100: "var(--grey-100)", 200: "var(--grey-200)",
               300: "var(--grey-300)", 400: "var(--grey-400)", 500: "var(--grey-500)",
               600: "var(--grey-600)", 700: "var(--grey-700)" },
      warning: "var(--warning-500)",
    },
    fontFamily: {
      display: ["var(--font-display)"],
      sans:    ["var(--font-sans)"],
      mono:    ["var(--font-mono)"],
    },
    fontSize: {
      "2xs":  ["var(--text-2xs)",  { lineHeight: "1.5" }],
      xs:     ["var(--text-xs)",   { lineHeight: "1.5" }],
      sm:     ["var(--text-sm)",   { lineHeight: "1.5" }],
      base:   ["var(--text-base)", { lineHeight: "1.5" }],
      md:     ["var(--text-md)",   { lineHeight: "1.3" }],
      lg:     ["var(--text-lg)",   { lineHeight: "1.5" }],
      xl:     ["var(--text-xl)",   { lineHeight: "1.3" }],
      "d-xs": ["var(--display-xs)",  { lineHeight: "0.88", letterSpacing: "-0.015em" }],
      "d-sm": ["var(--display-sm)",  { lineHeight: "0.88", letterSpacing: "-0.015em" }],
      "d-md": ["var(--display-md)",  { lineHeight: "0.88", letterSpacing: "-0.015em" }],
      "d-lg": ["var(--display-lg)",  { lineHeight: "0.88", letterSpacing: "-0.015em" }],
      "d-xl": ["var(--display-xl)",  { lineHeight: "0.88", letterSpacing: "-0.015em" }],
      "d-2xl":["var(--display-2xl)", { lineHeight: "0.88", letterSpacing: "-0.015em" }],
    },
    spacing: {
      0: "0", px: "1px",
      1: "var(--space-1)", 2: "var(--space-2)", 3: "var(--space-3)", 4: "var(--space-4)",
      5: "var(--space-5)", 6: "var(--space-6)", 8: "var(--space-8)", 10: "var(--space-10)",
      12: "var(--space-12)", 16: "var(--space-16)", 20: "var(--space-20)",
      24: "var(--space-24)", 32: "var(--space-32)",
    },
    borderRadius: {
      none: "0",
      xs: "var(--radius-xs)", sm: "var(--radius-sm)", md: "var(--radius-md)",
      lg: "var(--radius-lg)", xl: "var(--radius-xl)", "2xl": "var(--radius-2xl)",
      full: "var(--radius-pill)",
    },
    boxShadow: {
      none: "none",
      xs: "var(--shadow-xs)", sm: "var(--shadow-sm)", md: "var(--shadow-md)", lg: "var(--shadow-lg)",
      pop: "var(--shadow-pop)", "pop-mint": "var(--shadow-pop-mint)",
      focus: "var(--ring-focus)", "focus-danger": "var(--ring-danger)",
    },
    screens: { sm: "640px", md: "768px", lg: "1024px", xl: "1280px" },
    extend: {
      maxWidth: { bio: "var(--bio-max)", page: "var(--page-max)" },
      transitionDuration: {
        instant: "var(--dur-instant)", fast: "var(--dur-fast)",
        base: "var(--dur-base)", slow: "var(--dur-slow)",
      },
      transitionTimingFunction: {
        out: "var(--ease-out)", "in-out": "var(--ease-in-out)", spring: "var(--ease-spring)",
      },
      keyframes: { marquee: { from: { transform: "translateX(0)" }, to: { transform: "translateX(-50%)" } } },
      animation: { marquee: "marquee var(--dur-marquee) linear infinite" },
    },
  },
} satisfies Config;
```

Load `styles.css` once in the root layout so the custom properties exist:

```tsx
// app/layout.tsx
import "@/styles/linkit/styles.css"; // the design system's entry point
import "@/app/globals.css";          // your Tailwind directives
```

---

## 2. Colour

### Raw ramps

Hex values are exact — sampled from the visual reference, not rounded.

#### Mint — the one primary

| Token | Hex | Tailwind | Role |
| --- | --- | --- | --- |
| `--mint-100` | `#E3FEF7` | `mint-100` | Card fills, active nav pill, link-tile thumb |
| `--mint-200` | `#C8FDEE` | `mint-200` | Inactive chart bars |
| `--mint-300` | `#9DFDE0` | `mint-300` | — |
| `--mint-400` | `#7AFDD6` | `mint-400` | **Primary button hover** (fills lighten) |
| `--mint-500` | `#5CFDCB` | `mint-500` | **Primary. CTAs, "live" state, default bio ground** |
| `--mint-600` | `#33E7AE` | `mint-600` | **Primary button press**, focus border |
| `--mint-700` | `#1FBE8C` | `mint-700` | Accent *text* only (link hover, positive delta) |

> **Mint carries ink text only.** White on `mint-500` is 1.3:1 and is banned system-wide.

#### Ink — text and dark surfaces

| Token | Hex | Tailwind | Role |
| --- | --- | --- | --- |
| `--ink-900` | `#0B1F1C` | `ink-900` | All body text, thick borders, footer ground |
| `--ink-800` | `#152F2C` | `ink-800` | Dark section surface, dark button, toast |
| `--ink-700` | `#1F4A44` | `ink-700` | Dark button hover, card-on-dark |
| `--ink-600` | `#2D6D64` | `ink-600` | — |

> There is **no pure black** in product UI. `--black #0A0A0A` exists in the ramp but is unused.

#### Accents — strict roles, never text colours

| Token | Hex | Tailwind | Role |
| --- | --- | --- | --- |
| `--lemon-100` | `#FDFECB` | `lemon-100` | Tint fill |
| `--lemon-300` | `#FCFE9D` | `lemon-300` | Lemon icon-button hover |
| `--lemon-500` | `#FAFD70` | `lemon-500` | Marker highlight, ticker rail, CTA band |
| `--lemon-700` | `#E6EA3C` | `lemon-700` | — |
| `--lilac-100` | `#F6E2FB` | `lilac-100` | Tint fill |
| `--lilac-300` | `#ECC4F9` | `lilac-300` | — |
| `--lilac-500` | `#D9A2F7` | `lilac-500` | Secondary marker, avatar tint |
| `--lilac-700` | `#B96EE6` | `lilac-700` | — |
| `--sky-100` | `#E2FBFF` | `sky-100` | Tint fill |
| `--sky-300` | `#B8F6FF` | `sky-300` | — |
| `--sky-500` | `#8EF3FF` | `sky-500` | Third marker tone only |
| `--sky-700` | `#4FD9EA` | `sky-700` | `--info-500` |

#### Rose — destructive only

| Token | Hex | Tailwind | Role |
| --- | --- | --- | --- |
| `--rose-100` | `#FFE4EB` | `rose-100` | Danger badge bg, dialog glyph circle |
| `--rose-500` | `#F43362` | `rose-500` | Destructive button, error text/border |
| `--rose-700` | `#D31146` | `rose-700` | Destructive hover, danger badge text |

> Nothing decorative is ever rose.

#### Neutrals — warm grey with a faint green tint

| Token | Hex | Tailwind | Role |
| --- | --- | --- | --- |
| `--white` | `#FFFFFF` | `white` | Page, card |
| `--grey-50` | `#F9FAF8` | `grey-50` | — |
| `--grey-100` | `#F4F6F3` | `grey-100` | **Workhorse surface** — neutral card, sunken panel, ghost hover |
| `--grey-200` | `#E8EBE6` | `grey-200` | Hairline borders, dividers |
| `--grey-300` | `#D6DAD3` | `grey-300` | Default input border, switch track off |
| `--grey-400` | `#B0B6AD` | `grey-400` | Input hover border, disabled text, drag grip |
| `--grey-500` | `#858C83` | `grey-500` | Muted text |
| `--grey-600` | `#5F665D` | `grey-600` | Secondary text |
| `--grey-700` | `#3D423B` | `grey-700` | — |

#### Status

| Token | Value | Tailwind | Notes |
| --- | --- | --- | --- |
| `--success-500` | `#1FBE8C` (= `mint-700`) | `mint-700` | Success reuses mint so the palette stays tight |
| `--warning-500` | `#FFB020` | `warning` | The only hue outside the five families |
| `--danger-500` | `#F43362` (= `rose-500`) | `rose-500` | |
| `--info-500` | `#4FD9EA` (= `sky-700`) | `sky-700` | |

### Semantic aliases — what app code should use

| Token | Resolves to | Tailwind |
| --- | --- | --- |
| **Text** | | |
| `--text-primary` | `ink-900` | `text-ink-900` |
| `--text-secondary` | `grey-600` | `text-grey-600` |
| `--text-muted` | `grey-500` | `text-grey-500` |
| `--text-disabled` | `grey-400` | `text-grey-400` |
| `--text-inverse` | `white` | `text-white` |
| `--text-on-mint` | `ink-900` | `text-ink-900` |
| `--text-accent` | `mint-700` | `text-mint-700` |
| `--text-danger` | `rose-500` | `text-rose-500` |
| `--text-link` | `ink-900` | `text-ink-900` |
| `--text-link-hover` | `mint-700` | `hover:text-mint-700` |
| **Surfaces** | | |
| `--surface-page` | `white` | `bg-white` |
| `--surface-page-alt` | `grey-100` | `bg-grey-100` |
| `--surface-card` | `white` | `bg-white` |
| `--surface-card-alt` | `grey-100` | `bg-grey-100` |
| `--surface-sunken` | `grey-100` | `bg-grey-100` |
| `--surface-dark` | `ink-800` | `bg-ink-800` |
| `--surface-mint` | `mint-500` | `bg-mint-500` |
| `--surface-mint-soft` | `mint-100` | `bg-mint-100` |
| `--surface-lemon` | `lemon-500` | `bg-lemon-500` |
| `--surface-lilac` | `lilac-500` | `bg-lilac-500` |
| `--surface-lilac-soft` | `lilac-100` | `bg-lilac-100` |
| `--surface-sky` | `sky-500` | `bg-sky-500` |
| `--surface-danger-soft` | `rose-100` | `bg-rose-100` |
| `--surface-overlay` | `white` | `bg-white` |
| `--surface-glass` | `rgba(255,255,255,.72)` | `bg-white/[.72]` |
| **Borders** | | |
| `--border-subtle` | `grey-200` | `border-grey-200` |
| `--border-default` | `grey-300` | `border-grey-300` |
| `--border-strong` | `ink-900` | `border-ink-900` |
| `--border-focus` | `mint-600` | `border-mint-600` |
| `--border-danger` | `rose-500` | `border-rose-500` |
| **Controls** | | |
| `--btn-primary-bg` / `-hover` / `-active` / `-fg` | `mint-500` / `mint-400` / `mint-600` / `ink-900` | |
| `--btn-dark-bg` / `-hover` / `-fg` / `-fg-accent` | `ink-800` / `ink-700` / `white` / `mint-500` | |
| `--btn-secondary-bg` / `-hover` / `-fg` / `-border` | `white` / `grey-100` / `ink-900` / `ink-900` | |
| `--btn-ghost-bg-hover` | `grey-100` | |
| `--btn-danger-bg` / `-hover` / `-fg` | `rose-500` / `rose-700` / `white` | |
| `--btn-disabled-bg` / `-fg` | `mint-100` / `grey-400` | Same for **every** variant |
| **Marker** | | |
| `--marker-lemon` / `-mint` / `-lilac` / `-sky` / `-dark` | `lemon-500` / `mint-500` / `lilac-500` / `sky-500` / `ink-800` | |
| `--marker-skew` | `-1.6deg` | |
| **Bio page (theme-driven)** | | |
| `--bio-bg` / `--bio-fg` | `mint-500` / `ink-900` (Mint theme default) | |
| `--bio-tile-bg` / `-fg` / `-border` / `-radius` | `white` / `ink-900` / `ink-900` / `radius-lg` | Set on the page root per theme |
| **Overlays** | | |
| `--overlay-scrim` | `rgba(11,31,28,.45)` | `bg-ink-900/45` |
| `--blur-glass` | `saturate(180%) blur(18px)` | `backdrop-saturate-[1.8] backdrop-blur-[18px]` |

### Dark scope

There is **no global dark mode.** Dark is a *section* treatment: add `.linkit-on-dark` to any
block sitting on `--surface-dark`, which re-points the text/border/link tokens.

```tsx
<section className="linkit-on-dark bg-ink-800 text-white">…</section>
```

| Token inside `.linkit-on-dark` | Value |
| --- | --- |
| `--text-primary` | `white` |
| `--text-secondary` | `rgba(255,255,255,.72)` |
| `--text-muted` | `rgba(255,255,255,.54)` |
| `--surface-card` / `--surface-card-alt` | `ink-700` |
| `--border-subtle` / `--border-default` | `rgba(255,255,255,.14)` / `.24` |
| `--border-strong` | `mint-500` |
| `--text-link` / `--text-accent` | `mint-500` |

A user-toggled app-wide dark mode is **TBD** — the system does not define one.

### Contrast

Floor: **4.5:1** body text, **3:1** display-scale headlines. Measured pairs:

| Pair | Ratio | |
| --- | --- | --- |
| `ink-900` on `mint-500` | 12.4:1 | ✅ |
| `ink-900` on `lemon-500` | 14.9:1 | ✅ |
| `mint-500` on `ink-800` | 10.6:1 | ✅ |
| `grey-600` on `white` | 6.4:1 | ✅ |
| `grey-500` on `white` | 3.9:1 | ⚠️ ≥14px only, non-essential text |
| `white` on `mint-500` | 1.3:1 | ❌ **banned** |

Never set text in a transparent colour to look secondary — use `--text-secondary`. The one
sanctioned exception is `opacity: .65` on a decorative label inside a coloured card, where the
fill guarantees contrast.

---

## 3. Type

### Faces

| Role | Family | Weights | Tailwind |
| --- | --- | --- | --- |
| Display | **Archivo** variable, `wght 900` / `wdth 88%` | 900 only | `font-display` |
| Body / UI | **Figtree** | 400, 500, 600, 700 | `font-sans` |
| Mono | **DM Mono** | 400, 500 | `font-mono` |

⚠️ **All three are substitutions.** No font binaries were supplied with the brand. Archivo
approximates the reference's licensed heavy poster face (matching weight, narrowness, squared
counters); Figtree approximates its UI face. **Confirm or replace before launch.**

Currently loaded from Google Fonts inside `tokens/fonts.css`. For Next.js, switch to
`next/font` and keep the variable names:

```ts
// app/fonts.ts
import { Archivo, Figtree, DM_Mono } from "next/font/google";
export const display = Archivo({ subsets: ["latin"], weight: "900", axes: ["wdth"], variable: "--font-display" });
export const sans    = Figtree({ subsets: ["latin"], variable: "--font-sans" });
export const mono    = DM_Mono({ subsets: ["latin"], weight: ["400", "500"], variable: "--font-mono" });
```

### Display scale

Uppercase, `font-stretch: 88%`, `font-weight: 900`, `line-height: .88`, `letter-spacing: -.015em`.
Use the `.linkit-display` utility (shipped in `tokens/base.css`) — it sets all five properties
including `font-stretch`, which Tailwind has no class for.

| Token | px | Tailwind | Use |
| --- | --- | --- | --- |
| `--display-2xl` | 104 | `text-d-2xl` | Poster / full-bleed hero |
| `--display-xl` | 80 | `text-d-xl` | Landing hero |
| `--display-lg` | 60 | `text-d-lg` | Desktop section title |
| `--display-md` | 40 | `text-d-md` | Section title, mobile hero, `StatCard` value |
| `--display-sm` | 28 | `text-d-sm` | Card title, dialog title, page heading |
| `--display-xs` | 22 | `text-d-xs` | Eyebrow, tag, ticker item, sidebar wordmark |

Hero headlines should be fluid, since 80px does not fit a phone:

```tsx
<h1 className="linkit-display text-[clamp(2.75rem,7vw,var(--display-xl))]">
  One link.<br />Everything<br /><span className="linkit-marker">you make.</span>
</h1>
```

**Rules.** Display is caps-only and never below weight 700. Body copy never appears in the
display face, even inside loud sections. Headlines are set tight enough that lines nearly touch
— that stacked-poster density is the brand more than any single colour.

### Body scale

Figtree, sentence case, `line-height 1.5` unless noted.

| Token | px | Tailwind | Use |
| --- | --- | --- | --- |
| `--text-xl` | 24 | `text-xl` | Card heading (sans) |
| `--text-lg` | 20 | `text-lg` | Lead paragraph under a hero |
| `--text-md` | 17 | `text-md` | Link-tile label (LH 1.15) |
| `--text-base` | 16 | `text-base` | **Body default** |
| `--text-sm` | 14 | `text-sm` | Secondary copy, form labels, nav items, buttons |
| `--text-xs` | 12 | `text-xs` | Hints, badges, counters, URLs in rows |
| `--text-2xs` | 11 | `text-2xs` | Legal, meta, footer |

### Weights, leading, tracking

| Token | Value | Tailwind | Use |
| --- | --- | --- | --- |
| `--weight-regular` | 400 | `font-normal` | Body paragraphs |
| `--weight-medium` | 500 | `font-medium` | Input values, list meta |
| `--weight-semibold` | 600 | `font-semibold` | Buttons, nav, labels |
| `--weight-bold` | 700 | `font-bold` | Row titles, small headings, badges |
| `--weight-black` | 900 | `font-black` | Display face only |
| `--leading-tight` | 1.1 | `leading-tight` | |
| `--leading-snug` | 1.3 | `leading-snug` | Card headings |
| `--leading-normal` | 1.5 | `leading-normal` | Body default |
| `--leading-relaxed` | 1.65 | `leading-relaxed` | Long-form |
| `--tracking-tight` | -0.02em | `tracking-tight` | |
| `--tracking-normal` | 0 | `tracking-normal` | |
| `--tracking-wide` | 0.04em | `tracking-wide` | Badges |
| `--tracking-caps` | 0.08em | `tracking-[0.08em]` | Uppercase eyebrows, stat labels |

Paragraphs get `text-wrap: pretty` (`text-pretty`) globally via `tokens/base.css`. Bios cap at
`34ch` so they break predictably.

### The marker highlight

The brand's signature device: the last clause of a headline sits on a skewed block of colour.

```tsx
// The shipped utility (tokens/base.css) — prefer this over re-deriving it
<span className="linkit-marker">Everything you make.</span>
<span className="linkit-marker linkit-marker--mint">the only one.</span>

// Equivalent Tailwind, if you must inline it
<span className="inline-block bg-lemon-500 text-ink-900 px-[0.28em] pt-[0.06em] pb-[0.1em] -rotate-[1.6deg]">
```

Tones: `linkit-marker` (lemon, default), `--mint`, `--lilac`, `--sky`, `--dark` (ink bg + mint text).
**Rules:** display face only, one per headline (two stacked at most, alternating tones), never on
body copy, never on a button.

---

## 4. Spacing

4px base grid.

| Token | px | Tailwind | Common use |
| --- | --- | --- | --- |
| `--space-1` | 4 | `p-1` `gap-1` | Icon-button clusters |
| `--space-2` | 8 | `p-2` `gap-2` | Icon↔label, social row |
| `--space-3` | 12 | `p-3` `gap-3` | **Link-tile stack gap**, form row gap |
| `--space-4` | 16 | `p-4` `gap-4` | Tile padding-y, small card padding |
| `--space-5` | 20 | `p-5` `gap-5` | Tile padding-x, stat-card padding |
| `--space-6` | 24 | `p-6` `gap-6` | **Card padding default**, page gutter |
| `--space-8` | 32 | `p-8` `gap-8` | Dashboard content padding, dialog padding |
| `--space-10` | 40 | `p-10` `gap-10` | Large card padding, ticker item gap |
| `--space-12` | 48 | `p-12` `gap-12` | Heading→grid gap |
| `--space-16` | 64 | `p-16` | Tight section padding, footer top |
| `--space-20` | 80 | `p-20` | Hero padding-top |
| `--space-24` | 96 | `p-24` | `--section-y` — between marketing bands |
| `--space-32` | 128 | `p-32` | Reserved |

### Layout tokens

| Token | Value | Tailwind | Meaning |
| --- | --- | --- | --- |
| `--bio-max` | 580px | `max-w-bio` | The public link column. Never wider |
| `--page-max` | 1200px | `max-w-page` | Marketing + dashboard content |
| `--gutter` | 24px (`--space-6`) | `px-6` | Horizontal page inset |
| `--section-y` | 96px | `py-24` | Between marketing bands |
| `--section-y-tight` | 64px | `py-16` | Between dense bands |
| `--stack-gap` | 12px | `gap-3` | Between link tiles |
| Dashboard rail | 240px (fixed, in `.lk-side`) | `w-60` | Not a token — hard-coded in the rail |
| Dashboard preview | 400px (fixed) | `w-[400px]` | Not a token |

**Three widths only.** 580 / 1200 / 240. Anything else needs a reason.

---

## 5. Radius

| Token | Value | Tailwind | Applies to |
| --- | --- | --- | --- |
| `--radius-xs` | 6px | `rounded-xs` | Checkbox box |
| `--radius-sm` | 10px | `rounded-sm` | Link-tile thumb, tooltip, chart bars |
| `--radius-md` | 14px | `rounded-md` | Inputs, select, textarea, dashboard rows, nav items |
| `--radius-lg` | 20px | `rounded-lg` | **Link tiles**, dialogs, stat cards, URL card |
| `--radius-xl` | 28px | `rounded-xl` | Feature cards, panels |
| `--radius-2xl` | 40px | `rounded-2xl` | Full-bleed media blocks, hero product card |
| `--radius-pill` | 999px | `rounded-full` | Buttons, chips, badges, avatars, toggles, segmented tracks |

Nothing in the system has square corners **except the marker highlight**.

### Border widths

| Token | Value | Tailwind | Meaning |
| --- | --- | --- | --- |
| `--border-hairline` | 1px | `border` | Product chrome — inputs, rows, rails, dividers |
| `--border-thick` | 2px | `border-2` | Anything that should look *drawn*: link tiles, outline buttons, checkboxes, hero card |

The 2px ink border is a deliberate flat-poster move, not a default. Buttons carry
`border-2 border-transparent` at rest so fill and outline variants share exact metrics.

---

## 6. Shadows

Emphasis comes from **colour, not depth.** Ambient shadows are quiet and cool-neutral
(`rgba(11,31,28,·)`); one shadow is loud.

| Token | Value | Tailwind | Use |
| --- | --- | --- | --- |
| `--shadow-none` | `none` | `shadow-none` | Default for cards |
| `--shadow-xs` | `0 1px 2px rgba(11,31,28,.06)` | `shadow-xs` | Switch thumb |
| `--shadow-sm` | `0 2px 8px rgba(11,31,28,.06)` | `shadow-sm` | Dashboard row hover, panel cards |
| `--shadow-md` | `0 8px 24px rgba(11,31,28,.08)` | `shadow-md` | Card hover, toast, floating picker |
| `--shadow-lg` | `0 20px 48px rgba(11,31,28,.10)` | `shadow-lg` | Dialog, phone preview frame |
| `--shadow-pop` | `4px 4px 0 var(--ink-900)` | `shadow-pop` | **Hard offset, no blur.** Poster moments + link-tile hover |
| `--shadow-pop-mint` | `4px 4px 0 var(--mint-500)` | `shadow-pop-mint` | The pop shadow on dark grounds |

**No inner shadows anywhere. No coloured glows.** `--shadow-pop` is limited to the hero product
card and one feature card per page — plus link-tile hover, where it is the interaction.

### Focus rings

| Token | Value | Tailwind |
| --- | --- | --- |
| `--ring-focus` | `0 0 0 3px rgba(92,253,203,.55), 0 0 0 1px var(--ink-800)` | `shadow-focus` |
| `--ring-danger` | `0 0 0 3px rgba(244,51,98,.35)` | `shadow-focus-danger` |

One ring for the whole system. The mint halo plus the 1px ink hairline means it survives on
mint, lemon and white grounds alike — do not substitute Tailwind's default `ring-*`.

---

## 7. Breakpoints

⚠️ **The design system defines no breakpoint tokens.** No `@media` width query exists in
`tokens/*.css` — the only media query is `prefers-reduced-motion`. The values below are the
**observed behaviour of the UI kits**, offered as the recommended set. Ratify them with design
before treating them as canon.

| Name | Min-width | Tailwind | Behaviour observed in the kits |
| --- | --- | --- | --- |
| (base) | 0 | — | Single column. Bio page is unchanged at every width — it is already one 580px column |
| `sm` | 640px | `sm:` | **TBD** — no kit changes at this width |
| `md` | 768px | `md:` | Marketing feature grid goes 1→2 up (auto-fit at 260px min) |
| `lg` | 1024px | `lg:` | Feature grid reaches 3-up; footer columns spread |
| `xl` | 1280px | `xl:` | Full desktop marketing layout |
| **1140px** | — | `min-[1140px]:` | **Dashboard-specific.** Below it the 240px rail collapses into a `Tabs` row and the 400px preview moves behind a "Preview" toggle. Above it, the three-pane layout |

The 1140px dashboard threshold is a JS `window.innerWidth` check in `DashboardShell.jsx`, not a
media query — it needs a real value to switch layout *structure*. In Next.js prefer a
`useMediaQuery("(min-width: 1140px)")` hook, or restructure with CSS container queries.

Kit grids use intrinsic sizing rather than breakpoints wherever possible, which is the preferred
pattern — fewer thresholds to maintain:

```tsx
// Reflows with no media query at all
<div className="grid gap-4 [grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))]">
```

### Fixed vs fluid

| Surface | Behaviour |
| --- | --- |
| Public bio page | Fluid; one column capped at `max-w-bio` (580px) |
| Dashboard | Fluid content, **fixed** 240px rail + 400px preview, both dropped below 1140px |
| Marketing | Fluid; content capped at `max-w-page` (1200px), bands full-bleed |

---

## 8. Motion

Short and springy. Nothing eases longer than 320ms.

| Token | Value | Tailwind | Use |
| --- | --- | --- | --- |
| `--dur-instant` | 90ms | `duration-instant` | Press / scale |
| `--dur-fast` | 140ms | `duration-fast` | Colour, border, opacity |
| `--dur-base` | 200ms | `duration-base` | Transform, switch thumb, tile lift |
| `--dur-slow` | 320ms | `duration-slow` | **Ceiling.** Nothing is slower |
| `--dur-marquee` | 28s | — | Ticker loop |
| `--ease-out` | `cubic-bezier(.22,1,.36,1)` | `ease-out` | Entrances, colour, most things |
| `--ease-in-out` | `cubic-bezier(.65,0,.35,1)` | `ease-in-out` | Symmetric moves |
| `--ease-spring` | `cubic-bezier(.34,1.56,.64,1)` | `ease-spring` | **Overshoot — switch thumbs and link-tile lifts only** |
| `--press-scale` | 0.97 | `active:scale-[0.97]` | Every interactive element |
| `--hover-lift` | -2px | `hover:-translate-y-0.5` | Cards (tiles use -3px) |

**Fades are for scrims only.** Elements arrive by *moving*, not by appearing. No ripples, no
flashes, no parallax, no scroll-triggered animation defined by the system.

The `Ticker` marquee is the only continuous animation.

### Reduced motion

`tokens/motion.css` already zeroes the tokens, so anything driven by them stops for free:

```css
@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0ms; --dur-base: 0ms; --dur-slow: 0ms; --press-scale: 1; --hover-lift: 0px; }
}
```

**But Tailwind's literal utilities bypass this.** If you write `duration-200` instead of
`duration-base`, or `transition-transform` with a hard-coded value, add `motion-reduce:` variants
yourself. Prefer the token-backed classes. The marquee needs an explicit guard:

```tsx
<div className="animate-marquee motion-reduce:animate-none">
```

---

## 9. Global CSS the system ships

Three things live in `tokens/base.css` that Tailwind cannot express and that you should keep
rather than re-derive:

| Class | Why it can't be Tailwind |
| --- | --- |
| `.linkit-display` | Sets `font-stretch: 88%`, which has no Tailwind utility |
| `.linkit-marker` (+ `--mint` `--lilac` `--sky` `--dark`) | The signature treatment; keeping it one class keeps the skew and padding consistent |
| `.linkit-on-dark` | Re-points custom properties for a section scope |

Plus resets: `box-sizing`, `margin: 0` on headings/paragraphs, `text-wrap: pretty`, `font: inherit`
on form elements, `img/svg { display: block }`, `:focus-visible { box-shadow: var(--ring-focus) }`,
and `::selection { background: mint-500; color: ink-900 }`.

`a` and `a:hover` colours are defined globally (`ink-900` → `mint-700`) so a bare `<a>` never
renders browser-default blue.

---

## 10. Not defined — TBD

Do not invent these; ask design.

| Area | Status |
| --- | --- |
| Breakpoint **tokens** | **TBD.** §7 lists observed kit behaviour, not ratified values |
| App-wide dark mode | **TBD.** Only the `.linkit-on-dark` *section* scope exists |
| Logo / brand mark | **TBD — none exists.** The wordmark is "Linkit" set in the display face, uppercase. Do **not** draw, generate or approximate a mark |
| Brand font files | **TBD.** Archivo / Figtree / DM Mono are flagged substitutions |
| Illustration style | **TBD — none supplied.** Kits use large (44px) Lucide glyphs in the corner of feature cards where illustrations would sit |
| Photography | **TBD — none supplied.** Direction, if any is commissioned: cool and clean, daylight, saturated but not graded; no warm filter, no b&w, no grain |
| z-index scale | **TBD.** Kits use ad-hoc values (header 50, tooltip 40, dialog 100, toast 120). Ratify a scale before shipping |
| Chart / data-viz palette | **TBD.** The analytics view uses `mint-500` for the current bar and `mint-200` for the rest — that is the only precedent |
| Loading / skeleton states | **TBD.** No spinner, skeleton or progress component exists |
| Email / print styles | **TBD** |
| Localisation, RTL | **TBD.** Nothing in the system is RTL-aware |
