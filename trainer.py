import random
import unicodedata
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import string

from nltk.util import pr

with open('spa.txt', 'r', encoding="utf-8") as f:
  lines = f.readlines()

def toLowerAscii(s):
  return ''.join(
    c for c in unicodedata.normalize('NFD', s.lower())
    if unicodedata.category(c) != 'Mn'
    and c in string.ascii_lowercase + ' '
  ).strip()

lines = [line.split('\t') for line in lines]

random.shuffle(lines)

smooth = SmoothingFunction().method4
save_file = open('hard.txt', 'a')
total_bleu = 0
i = 0
for eng, spa in lines:
  ref = toLowerAscii(spa)
  reference = ref.split()
  answer = input(eng + '\nAnswer: ')
  hypothesis = toLowerAscii(answer).split()
  
  #print(hypothesis, reference)
  if hypothesis == reference:
    bleu = 1
  else:
    try:
      bleu = sentence_bleu([reference], hypothesis, smoothing_function=smooth)
    except:
      print('Oops! Nltk is dumb!\n\n')
      continue
  total_bleu += bleu
  i += 1
  print('Reference: ' + spa.strip())
  print("bleu: %.2f, average bleu: %.2f" % (bleu, total_bleu/i))
  while True:
    action = input('action? ').strip()
    if action == '':
      break
    elif action == 's':
      save_file.write(eng + '\t' + spa)
      print('Saved to hard sentences!')
      break
    else:
      print('Unknown option')

