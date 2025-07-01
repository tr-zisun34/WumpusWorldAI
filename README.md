# 🧠 Wumpus World AI Simulation

A logic-based AI agent that navigates a 10×10 Wumpus World, infers safe paths using percepts (Breeze, Stench, Glitter), and avoids danger using logical reasoning.

## 🔍 Project Overview

This project simulates an AI agent in the Wumpus World environment using **Propositional Logic**. The agent:

- Starts at the bottom-left corner (0, 9)
- Explores unknown terrain
- Uses **forward chaining** on percepts
- Avoids pits and Wumpus
- Finds the gold and stops

---

## 🎯 Features

- ✅ 10×10 Wumpus World grid
- ✅ Logical reasoning with a knowledge base
- ✅ Loop detection and visited cell tracking
- ✅ Random environment generation
- ✅ Tkinter-based GUI with emoji visualization:
  - 💰 Gold
  - 🐉 Wumpus
  - 🧍‍♂️ Agent
  - 🕳️ Pit
- ✅ Color-coded cells: visited, safe, unsafe

---

## 📁 Project Structure

```
WumpusWorldAI/
│
├── main.py
├── worlds/
│   └── random.txt
├── agent/
│   ├── agent.py
│   ├── inference.py
│   └── knowledge_base.py
├── environment/
│   ├── world.py
│   └── cell.py
├── utils/
│   └── random_world.py
└── ui/
    └── gui.py
```

---

## 💻 Requirements

- Python 3.7+
- Tkinter (comes with Python by default on Windows)

---

## 🚀 How to Run

### 1. Clone or Download the Project

```bash
git clone https://github.com/your-username/WumpusWorldAI.git
cd WumpusWorldAI
```

Or just extract your ZIP and open the folder in **VS Code**.

### 2. Run the Simulation

Use the command line or VS Code terminal:

```bash
python -m main
```

Make sure you're in the project root directory (where `main.py` is located).

> ❗ If you see a module import error, ensure you're running with `-m` to treat the folder as a module.

---

## 📸 UI Preview

- Agent 🧍‍♂️ starts at bottom-left
- 💰 Gold: Collectable goal
- 🐉 Wumpus: Danger!
- 🕳️ Pit: Deadly trap
- Colors indicate safety & visitation

---

## 🧠 AI Logic

The agent uses:

- Forward inference on percepts (Breeze → Pit nearby, etc.)
- Avoids re-visiting cells
- Marks cells safe/unsafe
- Stops upon collecting gold or hitting dead-end

---

## 📃 License

This project is for educational purposes (CSE 604: Artificial Intelligence Project 2).

---

## 🙋 Author

Developed by Md. Touhidur rahman, IIT, DU  
Under the guidance of Dr. Ahmedul Kabir