# Evolution Simulator

The evolution simulator is an interactive program which displays evolution taking place. Organisms are represented as nodes which evolve over time. Each organism is initially created with a unique set of genes which determines its movement. Organisms only survive if they reach a target location (chosen by the user). The surviving organisms are then used to create children (by combining the genes of the best surviving organisms). Mutations can also occur at a small probability. A genetic algorithm is used to implement this entire process. The fitness score of the genetic algorithm is calculated by ranking the organisms by their distance from the target location.

Demo Video: https://youtu.be/Ut49G4NN-nY

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/edwi-n/Evolution-Simulator/
cd Evolution-Simulator
```

### 2. Create a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

The app will be available at http://127.0.0.1:5000/

