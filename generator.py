#!/usr/bin/python3
import json
import random

tense_map = {"root" : 0, "past" : 1, "present" : 2}
def lookup_verb(path, vocab):
    if not len(path) == 3:
        return 'The path length was not valid for a verb lookup'
    item = path[1]
    #figure out what index holds the tense we want (this data is laid out strangely if you ask me)
    tense_index = tense_map[path[2]]
    #pick a random verb (comes in a list with 3 tenses)
    choice = random.choice(vocab['verb'][item])
    #now get the tensed item from the list
    return choice[tense_index]

def lookup_noun(path, vocab):
    if not len(path) == 2:
        return 'Path length not valid for noun lookup'
    item = path[1]
    #pick random choice from nouns for given key
    return random.choice(vocab['noun'][item])

def lookup_simile(path, vocab):
    if not len(path) == 2:
        return 'Path length not valid for simile lookup'
    item = path[1]
    #pick random choice from nouns for given key
    return random.choice(vocab['simile'][item])

def lookup_target(path, vocab):
    type = path[0]
    return vocab[type]

type_map = {"verb" : lookup_verb, "simile" : lookup_simile, "noun" : lookup_noun, "target" : lookup_target, "targets" : lookup_target, "recipient" : lookup_target, "recipients" : lookup_target}
def lookup_replacement(path, vocab):
    type = path[0]
    #get parsing function for this type
    if type in type_map:
        func = type_map[type]
        return func(path, vocab)
    else:
        return ' No parser function for {0} '.format(type)
        
def parse_sentence(sentence, vocab):
    '''
    Parse sentence and generate final based on the vocabulary
    '''
    #find the first item to replace
    start_pos = sentence.find('[') 
    while start_pos > -1:
        #find first ] after the [
        end_pos = sentence.find(']', start_pos)
        #cut marker out (does not cut out ] or [)
        marker = sentence[start_pos+1:end_pos]
        #split to find appropriate lookup path
        marker_path = marker.split('-')
        replacement = lookup_replacement(marker_path, vocab)
        #slice in replacement
        sentence = sentence[:start_pos] + replacement + sentence[end_pos+1:]
        #find next [ (we start from start_pos to speed lookup slightly)
        start_pos = sentence.find('[', start_pos)
    return sentence

def generate_sentences(num):
    with open('sentences.json') as sentencesfp, open('vocabulary.json') as vocabfp:
        sentences = json.load(sentencesfp)
        vocab = json.load(vocabfp)
        finals = []
        while len(finals) < num:
            sentence = random.choice(sentences["nontargeted"])
            finals.append(parse_sentence(sentence, vocab))
        return finals

def generate_sentences_with_target(num, target, recipient):
    with open('sentences.json') as sentencesfp, open('vocabulary.json') as vocabfp:
        sentences = json.load(sentencesfp)
        vocab = json.load(vocabfp)
        #Add target/recipient to vocab
        vocab['target'] = target
        vocab['recipient'] = recipient
        vocab['targets'] = target+"'s"
        vocab['recipients'] = recipient+"'s"
        finals = []
        while len(finals) < num:
            sentence = random.choice(sentences["targeted"])
            finals.append(parse_sentence(sentence, vocab))
        return finals



finals = generate_sentences(1)
print(finals)

finals = generate_sentences_with_target(1, "bill", "gina")
print(finals)
    
