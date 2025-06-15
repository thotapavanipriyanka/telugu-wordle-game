# Telugu Wordle Game 🎯

A command-line Wordle-style game built for Telugu! Guess the hidden word within 6 attempts, and get color-coded feedback to guide you.

---

## 🎮 Features

- Supports Telugu Unicode characters and grapheme clusters.
- Feedback Legend:
  - 🟩 `G`: Exact match (letter, symbol, position)
  - 🟨 `Y`: Letter and position match but symbol mismatched
  - 🟧 `O`: Letter and symbol match but in a different position
  - 💗 `P`: Only letter matches (not symbol or position)
  - `-`: No match
- Custom word list support

---

## 🚀 How to Play

1. Add Telugu words (one per line) in `data/words.txt`
2. Run the game:

```bash
python3 game.py

