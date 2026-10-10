# Multilingual Birthday Cake 🎂

A generative typographic visual and interactive animation in Python that constructs a multi-tiered birthday cake composed of "Happy Birthday" greetings in 25 different languages—complete with flickering candle flames, realistic smoke dissipation, and a step-by-step "eating" animation.


<img width="1231" height="740" alt="image" src="https://github.com/user-attachments/assets/e7f4228e-1f30-44aa-a993-498560bcf94b" />



## Features
- **Typographic Geometry:** Calculates scanlines and horizontal spans to sculpt a plate, cake tiers, icing drips, and cherries entirely out of text fragments and glyphs.
- **25 Global Languages:** Cycles dynamically through birthday wishes across multiple scripts (Latin, Cyrillic, Greek, Hangul, Kanji/Hanzi, Devanagari, Thai, Arabic, Hebrew, and Persian).
- **Dynamic Flame Physics:** Animated multi-layer candle flames with organic flickering, variable sway, and soft glow lighting.
- **Blow-Out & Smoke Simulation:** Candles extinguish sequentially, lifting upward while spawning particle-based drifting smoke trails with sinusoidal turbulence.
- **Bite & Dissolve Mechanics:** Radial bite algorithms procedurally devour cake tiers over time until the plate dissolves away.
- **Zero External Dependencies:** Built purely with Python standard libraries (`tkinter`, `turtle`, `math`, `random`).

## How to Run

```bash
python birthday_cake.py
