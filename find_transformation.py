from collections import deque
import string
import time


valid_letters = list(string.ascii_lowercase)
def find_transformations(word):
  transformations = set()
#  original_word = list(word)
  for x in range(0, len(word)):
    for y in range(0, len(valid_letters)):
      # new_word is a poor name here... it's probably not an actual word
      new_word = list(word)
      if new_word[x] == valid_letters[y]:
        continue
      new_word[x] = valid_letters[y]
      transformations.add("".join(new_word))
  return transformations
  

def import_file():
  words = set()
  for word in open('word_list.txt', 'r').read().split():
    words.add(word)
  return words

def copy_and_append(current_list, new_item):
  new_list = list(current_list)
  new_list.append(new_item)
  return new_list

def find_path(start, finish, dictionary):
  word_queue = deque([(start, list())])
  queued_words = set(start)
  while 1:
    if len(word_queue) == 0:
      # return an empty list if we couldn't find a path
      return list()
    word_obj = word_queue.popleft()
    transformations = find_transformations(word_obj[0])
    for word in transformations:
      if word == finish:
        path = list(word_obj[1])
        path.append(word_obj[0])
        path.append(word)
        return path
      if word in dictionary and word not in queued_words:
        queued_words.add(word)
        path = list(word_obj[1])
        path.append(word_obj[0])
        word_queue.append((word, path))

def timed_find_path(start, finish, dictionary):
  start_time = time.time()
  path = find_path(start, finish, dictionary)
  print 'search took', time.time() - start_time, 'seconds'
  return path

def main():
  valid_words = import_file()
  # Consider computing the graph of transformations that exist in the set of
  # valid_words.
  while 1:
    word_one = raw_input('Please enter the first word: ')
    word_two = raw_input('Please enter the second word: ')
    path = timed_find_path(word_one, word_two, valid_words)
    if len(path) == 0:
      print ('could not find a series of transformations between ', word_one,
             'and', word_two)
    else:
      print 'found a series of transformations:'
      for word in path:
        print word

if __name__ == '__main__':
  main()
