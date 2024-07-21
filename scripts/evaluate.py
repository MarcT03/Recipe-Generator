import torch
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def get_latest_checkpoint(directory):
    checkpoints = [d for d in os.listdir(directory) if d.startswith('checkpoint-')]
    latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('-')[1]))
    return os.path.join(directory, latest_checkpoint)

def calc_perplexity(data, model, tokenizer):
    # sets the model to evaluation mode & initializes two variables
    model.eval()
    total_log_likelihood = 0 # Collects the log likelihood of the model's predictions
    total_length = 0 # Tracks the total num of tokens processed

    for text in data:
        inputs = tokenizer(text, return_tensors = 'pt', padding=True, truncation=True, max_length=512)
        
        # Disables gradient calculation, saving memory
        with torch.no_grad():
            outputs = model(**inputs,labels=inputs['input_ids'])
            loss = outputs.loss
            log_likelihood = -loss * inputs['input_ids'].size(1)
            total_log_likelihood += log_likelihood
            total_length += inputs['input_ids'].size(1)
    
    # Calculates the perplexity which is how well the model predicts the data
    perplexity = torch.exp(total_log_likelihood/total_length)
    return perplexity.item()


def calc_bleu(references, hypothesis):
    smooth = SmoothingFunction().method4
    scores = [] # Empty list to store Bleu scores
    
    # Loops throught pairs of reference and hypothesis texts, with the 'zip' function pairing each ref with its corresponding hypothesis
    for ref, hyp in zip(references, hypothesis):
        # Calculates the Bleu score for the current pair of hypothesis and reference texts
        score = sentence_bleu([ref], hyp, smoothing_function=smooth)
        scores.append(score)
    
    # Returns the average Bleu score
    return sum(scores)/len(scores)

def evaluate():
    results_dir = './results'
    latest_checkpoint = get_latest_checkpoint(results_dir)

    # Load pretrained model and tokenizer as seen throughout the code
    model = GPT2LMHeadModel.from_pretrained(latest_checkpoint)
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    example_imputs = [
        'tomato, beef, onion, potatoes',
        'chicken, garlic, beans, rice'
    ]

    references = [
        'Cook the onion in a pan with oil until caramelized. Add the beef and cook until golden brown. Add chopped tomatoes. In a separate pan, cook chopped potatoes with oil until soft.',
        'Slowly cook the chicken in a pan until the chicken is properly cooked and golden brown. Add garlic for flavor. Serve with beans and rice. '
    ]

    # Tokenizes example inputs into suitable format
    inputs = tokenizer(example_imputs, return_tensors = 'pt', padding=True, truncation=True, max_length=512)
    attention_mask = inputs['attention_mask']

    # Generates model predictions without calculating gradients
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,
            max_length=512,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            num_beams=5,
            early_stopping=True,
            pad_token_id = int(tokenizer.pad_token_id)
            )

    output_texts = []
    for i, output in enumerate(outputs):
        output_text = tokenizer.decode(output, skip_special_token=True)
        output_texts.append(output_text)
        print(f"Input: {example_imputs[i]}")
        print(f"Generated Recipe: {output_text}\n")
    
    perplexity = calc_perplexity(example_imputs, model, tokenizer)
    print(f"Perplexity: {perplexity}")

    bleu_score = calc_bleu(references, output_texts)
    print(f"Bleu score: {bleu_score}")

if __name__ == "__main__":
    evaluate()