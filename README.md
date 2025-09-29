# psycho-llms

Welcome! The goal of this repository is to simulate psycholinguistic experiments with the LLM of your choice: the tool incrementally builds prefixes for the model and calculates word-level & sentence-level surprisals for each new trial. For example, consider an experiment with three items (1, 2, 3). Given that trials are often shuffled (to reduce any item order effects), there are six possible runs:

| 1 > 2 > 3 | **1 > 3 > 2** | 2 > 3 > 1| 2 > 1 > 3 | 3 > 1 > 2 | 3 > 2 > 1 |

Let's focus on the bolded run **1 > 3 > 2**. Using `psycho-llms`, you will get the probability estimates for each item, based on the items that have already been provided: **1**, then 1 > **3**, then 1 > 3 > **2**, where bold indicates the item for which surprisal values are calculated. As such, your surprisal values will *vary* in a manner that may explain possible sources of by-participant variation.

**NOTE: This repository is currently under active development.**


#### Table of Contents <a name="toc"></a>:
- [Installation](#installation)
- [Use](#use)
- [Citation](#citation)


## Installation: <a name="installation"></a> | [back to top](#toc)
Required dependencies are listed in the `requirements.txt` file, which you can install in your virtual environment with:

```
python -m pip install -r requirements.txt
```

## Use: <a name="use"></a> | [back to top](#toc)

### `data.py` builds the runs.
`data.py` takes in a `csv` file of either a) human experiment data that contains participant labels and sentence strings, or b) sentence strings & their corresponding item number and conditions. Think ABCs:

For a), use the `Aligner`:
```python data.py -i $INPUT_FILE -o $OUTPUT_DIR -t builder`
where `$INPUT_FILE` is the human experiment data and `$OUTPUT_DIR` is the directory where you want to store the runs.

For b), use the `Builder`:
```python data.py -i $INPUT_FILE -o $OUTPUT_DIR -n $NUM_RUNS -t aligner`
where `$INPUT_FILE` and `$OUTPUT_DIR` are used as they are in the `Aligner`, and where `$NUM_RUNS` is the total number of runs you want to generate. Note that the `Builder` creates two kinds of runs: random runs (where conditions are balanced across items randomly and then prefixed in a random order), and controlled runs (where conditions are balanced across items randomly and then ordered in a specific way). There are two kinds of controlled runs: alternating (where conditions alternate back and forth every item) and block (where all items for one condition are placed in a row). These two kinds of controlled runs allow you to establish effect baselines. *This script is currently being adopted from some util functions that I've been using the past few years.*



### `main.py` calculates the surprisal values.
*This script is currently being adopted from some util functions that I've been using the past few years.*


## Citation: <a name="citation"></a> | [back to top](#toc)
If you use this repository, please use the following citation:
```
Starr, J.R. (2025). `psycho-llms`. GitHub repository.
```

