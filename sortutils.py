import re

def hasWords(string: str, words: list):  
     for word in words:
          if string.lower().find(str(word).lower()) != -1:
               return True
     
     return False

def findW(string: str, word):
     pattern = (f"\s+{word}\s+\d+")

     pattern = re.compile(pattern)

     finded_words = re.findall(pattern, string)
     
     if len(finded_words) > 0:
          return True
     
     return False

def findWP(string: str, pattern: str):
     pattern = re.compile(pattern)
     finded_words = re.findall(pattern, string)

     if len(finded_words) > 0:
          return True
     
     return False


def hasWordsCamel(string: str, words: list):
     for word in words:          
          if string.find(word) != -1:              
               return True
     
     return False


def hasWords2(string: str, words: list):
     string_tmp = string.split(' ')
     
     for word in words:
          for element in string_tmp:               
               if element.lower() == word:
                    return True
     
     return False


def copyPattern(string: str, words: list):
     for word in words:
          if string.lower().find(str(word).lower()) != -1:
               return word
     return ""