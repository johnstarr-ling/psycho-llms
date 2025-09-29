import torch
import torch.nn.functional as F
import pandas as pd
import glob
import os 
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTNeoXTokenizerFast, GPTNeoXForCausalLM


# # Load GPT-2
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2LMHeadModel.from_pretrained('gpt2')
# model.eval()


### SENTENCE SURPRISAL
def sentence_surprisal(text, model, tokenizer, device='cpu'):
    'Compute surprisal for only the *last* sentence in a text.'
    # Split sentences naively (you can swap in nltk/sent_tokenize if needed)
    sentences = text.strip().split('. ')
    if not sentences:
        return None
    
    # Get last sentence and the preceding context
    last_sentence = sentences[-1].strip()
    if not last_sentence.endswith('.'):
        last_sentence += '.'
    context = '. '.join(sentences[:-1]).strip()
    if context and not context.endswith('.'):
        context += ' '

    # Tokenize
    context_ids = tokenizer.encode(context, add_special_tokens=False)
    last_ids = tokenizer.encode(last_sentence, add_special_tokens=False)
    input_ids = context_ids + last_ids
    input_tensor = torch.tensor([input_ids]).to(device)

    with torch.no_grad():
        outputs = model(input_tensor, labels=input_tensor)
        log_likelihood = -outputs.loss.item() * len(last_ids)  # total log prob of last sentence
    
    # Sentence-level surprisal = -log p(last sentence | context)
    return -log_likelihood



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_dir', type=str, default='runs')
    
    parser.add_argument('-o', '--output_dir', type=str, default='surprisals')

    args = parser.parse_args()

    for run in glob.glob(f'{args.input_dir}/*'):
        # print(run)
        filename = run.split('/')[1]
        df = pd.read_csv(run)

        
        df['last_surprisal'] = df['gpt2'].apply(lambda x: sentence_surprisal(x, model, tokenizer))

        df.to_csv(f'{args.output_dir}/{filename}', index=False)