import numpy as np
import pandas as pd
import random

################################
##### FUNCTIONS 
################################

def nested_dict(df):
    nested_dict = {}
    
    for _, row in df.iterrows():
        item = row['item']
        condition = row['condition']
        sentence = row['sentence']
        
        # Initialize the item key if it doesn't exist
        if item not in nested_dict:
            nested_dict[item] = {}
        
        # Add the condition-sentence pair
        nested_dict[item][condition] = sentence
    
    return nested_dict



################################
##### CLASSES 
################################

class Builder():
    'Class that builds experiments from sentence conditions.'

    def __init__(self):
        self.items = set()
        self.conditions = set()
        self.sents = set()
        self.outputs = []

    # Load data from file
    def load_stimuli(self, filename):
        'Read in CSV file of stimuli | Get conditions'
        df = pd.read_csv(filename)

        # Add relevant items from df
        self.items.update(df['item'].unique())
        self.conditions.update(df['condition'])
        self.sents.update(df['sentence'])

        # Make nested dict: {item: {cond1:sent, cond2:sent, ... condN:sent}}
        self.item_sent_conditions = nested_dict(df)

    # Generate a random run
    def random_run(self, max_items=0):
        'Generate a random run, balanced by condition'
        # If no specifications on maximum number of items,
        #   default to number of total items.
        if max_items == 0:
            max_items = len(self.items)
        
        # You have N items
        items = list(range(1, max_items+1))

        # Number of items for each condition in the df
        possible_conditions = [[condition]*int(len(items)/len(self.conditions)) 
                                for condition in self.conditions]

        # Randomly order the trials
        order = random.sample(items, max_items)

        run = []
        for item in order:
            # Get condition
            label = random.choice(possible_conditions)
            possible_conditions.remove(label)
            run.append(self.item_sent_conditions[item][label[0]])

        return run


    def build_prefixes(self, run, bos_token='<|endoftext|>'):
        'Prepare files for generation'

        # Add special token to beginning 
        run[0] =   f'{bos_token} {run[0]}'

        self.outputs = [' '.join(run[:i+1]) for i, _ in enumerate(run)]
    
    def write_prefixes(self):
        raise NotImplementedError
    




class Aligner():
    'Class that loads experiments that have already been run.'

    def __init__(self):
        self.participants = set()

    def load_collected_data(self, filename):
        'Read in CSV file of participant stimuli'
        df = pd.read_csv(filename)

        self.participant_sents = df.groupby('participant')['sentence'].apply(list).to_dict()


    def build_prefixes(self, participant, bos_token='<|endoftext|>'):
        'Prepare files for generation'

        # Add special token to beginning 

        self.outputs = dict()
        for participant, sentences in self.participant_sents.items():
            sentences[0] =   f'{bos_token} {sentences[0]}'
            self.outputs[participant] = [' '.join(sentences[:i+1]) for i, _ in enumerate(sentences)]
    
    def write_prefixes(self):
        raise NotImplementedError
    



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, default='sents.csv',
                        help='Input file.')
    
    parser.add_argument('-o', '-output_dir', type=str, default='runs',
                        help='Output directory.')
    
    parser.add_argument('-n', '--num_runs', type=int, default=10,
                        help='Number of runs to generate.')
    
    parser.add_argument('-t', '--type', const='build', nargs='?', default='build',
                        choices=['build', 'align'])
    
    
    args = parser.parse_args()

    if args.type == 'build':
        exp = Builder()
        exp.load_stimuli('inputs/sentences.csv')


    else:
        exp = Aligner()
        exp.load_collected_data('inputs/participants.csv')


    # run = exp.random_run()
    
    # df = load_data(args.input)
    # master = add_conditions(df)
    # order = ['po_then_do', 'do_then_po', 'alternating']

    # for run in range(args.num_runs):
    #     random_runthrough, num_pos = build_prefixes(random_run(master, max_items=40))
    #     random_runthrough.to_csv(f'runs/random{run}_{num_pos}.csv', index=False)
        
    #     dataframes = controlled_run(master, max_items=40)

    #     for idx in range(len(order)):
    #         controlled_runthrough, _ = build_prefixes(dataframes[idx])
    #         controlled_runthrough.to_csv(f'runs/{order[idx]}{run}.csv', index=False)
    