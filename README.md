# Quantum Game
This is a collection of Jupyter notebooks created with the aim of helping computer science students learn the basics of quantum mechanics.

## Installation


### 1. Clone the repository
Open a terminal in the directory where you want the project, then run:

```bash
git clone https://github.com/seppedijkstra/Quantum_Game.git
cd Quantum_Game
````

### 2. Install dependencies

Install all required packages by using requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Build the notebooks

To build the Jupyter Book from the notebooks, run:

```bash
python -c "from jupyter_book.cli.main import main; import sys; sys.argv = ['jupyter-book', 'build','.'];main()"
```

The built book will be available inside the **`_build/`** folder.

## Quantum game Rules
To learn more about the quantum rules of this game, read [here](./Quantum_Blackjack_Rules.pdf).

## Google Colab
You can try all the notebooks using Google Colab! To do so, just click on the following links.
- [Classical notebook](https://colab.research.google.com/github/seppedijkstra/Quantum_Game/blob/master/notebooks/1_Classical_Game.ipynb)
- [Physics notebook](https://colab.research.google.com/github/seppedijkstra/Quantum_Game/blob/master/notebooks/2_physics_nb.ipynb)
- [Quantum Game notebook](https://colab.research.google.com/github/seppedijkstra/Quantum_Game/blob/master/notebooks/3_Quantum_Game.ipynb)

## License
[License](./LICENSE.txt)