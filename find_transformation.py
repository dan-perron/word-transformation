#!/usr/bin/python

from collections import deque
import string
import time
import thread
from multiprocessing import Process, Queue
import math


valid_letters = list(string.ascii_lowercase)
def find_transformations(word):
  transformations = set()
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

def search_word_set(word_objs, finish, dictionary, already_visited_words,
                    ret_val):
  queued_words = set()
  queued_word_objs = list()
  for word_obj in word_objs:
    transformations = find_transformations(word_obj[0])
    for transformation in transformations:
      if transformation == finish:
        path = list(word_obj[1])
        path.append(word_obj[0])
        path.append(transformation)
        ret_val.put((True, path))
        return
      if (transformation in dictionary and 
          transformation not in already_visited_words and
          transformation not in queued_words):
        queued_words.add(transformation)
        path = list(word_obj[1])
        path.append(word_obj[0])
        queued_word_objs.append((transformation, path))
  ret_val.put((False, queued_word_objs, queued_words))

def find_path(start, finish, dictionary):
#  word_queue = deque([(start, list())])
  queued_word_objs = list(([start, list()],))
  queued_words = set(start)
  # make this a global var, or something
  num_processes = 4.0
  while 1:
    queue_length = len(queued_word_objs)
    if queue_length == 0:
      # return an empty list if we couldn't find a path
      return list()
    process_returns = Queue()
    processes = list()
    chunk_size = int(math.ceil(queue_length/num_processes))
    for chunk_start in range(0, queue_length, chunk_size):
      p = Process(target=search_word_set, 
                  args=(queued_word_objs[chunk_start:chunk_start + chunk_size],
                        finish, dictionary, queued_words, process_returns))
      p.start()
      processes.append(p)

    # clear the work queue
    queued_word_objs = list()

    print len(dictionary)
    for process in range(0, queue_length, chunk_size):
      ret_val = process_returns.get()
      if ret_val[0]:
        # done!
        return ret_val[1]
      else:
        queued_word_objs.extend(ret_val[1])
        queued_words.update(ret_val[2])
        print len(queued_words)

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
      print ('could not find a series of transformations between word_one '
             'and word_two')
    else:
      print 'found a series of transformations:'
      for word in path:
        print word

if __name__ == '__main__':
  main()
