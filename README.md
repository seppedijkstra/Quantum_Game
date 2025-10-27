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
- [Classical notebook](https://colab.research.google.com/drive/1c4wySMz1_JNjpkCsH8jxuNyjv7F725yD?usp=sharing)
- [Physics notebook](https://colab.research.google.com/drive/1lG2jHOXz7Yet5KiIV_mwwfdSnISV5r06?usp=sharing)
- [Quantum Game notebook](https://colab.research.google.com/drive/1_v93UL_mLW3f0_iEQyst4Q8MRmlYqfh3?usp=sharing)

## License
[License](./LICENSE.txt)