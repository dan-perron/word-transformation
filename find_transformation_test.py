#!/usr/bin/python

import find_transformation
import inspect

def test_same_word():
  path = find_transformation.find_path('until', 'until',
                                       find_transformation.import_file())
  assert len(path) == 1

def test_bread_break():
  path = find_transformation.find_path('bread', 'break',
                                       find_transformation.import_file())
  assert len(path) == 2

def test_brain_bread():
  path = find_transformation.find_path('brain', 'bread',
                                       find_transformation.import_file())
  assert len(path) == 7

def test_smart_brain():
  path = find_transformation.find_path('smart', 'brain',
                                       find_transformation.import_file())
  assert len(path) == 9

def test_no_connection():
  path = find_transformation.find_path('smart', 'until',
                                       find_transformation.import_file())
  assert len(path) == 0

def test_wrong_length():
  # todo: decide if it's an error case that
  # 1) the provided words don't exist in the dictonary
  # 2) there are no 3 letter words in the dictionary
  path = find_transformation.find_path('abc', 'def',
                                       find_transformation.import_file())
  assert len(path) == 0

def main():
  # run tests
  # todo: inspect this and just run all methods that start with test_
  test_same_word()
  test_bread_break()
  test_brain_bread()
  test_smart_brain()
  test_no_connection()
  test_wrong_length()

if __name__ == '__main__':
  main()
