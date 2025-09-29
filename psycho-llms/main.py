##### TO-DO
# - BOS token adaptation
# - Model loading
import torch
import torch.nn.functional as F
import pandas as pd
import glob
import os 
import sys

from utils import sentence_surprisal
from data import nested_dict, Builder, Aligner
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTNeoXTokenizerFast, GPTNeoXForCausalLM




# GENERATE EXPERIMENTS
def generate(num_runs, builder=False):
    pass




# INFERENCE
# (handling context window)
# (handling EOS token)
def inference():
    pass


if __name__ == '__main__':
    import argparse 

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, default='sents.csv',
                        help='Input file.')
    
    parser.add_argument('-o', '-output_dir', type=str, default='runs',
                        help='Output directory.')
    
    parser.add_argument('-n', '--num_runs', type=int, default=10,
                        help='Number of runs to generate, if building.')
    
    parser.add_argument('-t', '--type', const='build', nargs='?', default='build',
                        choices=['build', 'align'])
    
    parser.add_argument('-m', '--model', nargs='+', default='gpt2',
                        choices=['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'])

    parser.add_argument('-r', '--runs', type=int, default=30,
                        help='Number of runs for experiment builder')
    
    args = parser.parse_args()


    if args.type == 'build':
        exp = Builder()
        exp.load_stimuli(args.input)

        
    else:
        exp = Aligner()
        exp.load_collected_data(args.input)