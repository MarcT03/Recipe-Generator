import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

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

