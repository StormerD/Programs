import os
from pathlib import Path

class Line:
  def __init__(self, content, lineNo):
    self.content = content
    self.lineNo = lineNo
    
class Result:
  def __init__(self, first, second):
    self.first = first
    self.second = second

def ReadFile(_inputFile):
  _file = []
  i = 1
  
  while True:
    _content = _inputFile.readline().strip()
    _lineNo = i
    if _content == "---":
      break
    else:
      _Line = Line(_content, _lineNo)
      _file.append(_Line)
    i += 1
  return _file

def CompareArray(_file):
  _results = []
  i = 0
  
  while i < len(_file):
    j = i + 1
    _first = _file[i]
    
    while j < len(_file):
      _second = _file[j]
      if _first.content == _second.content:
        _Result = Result(_first, _second)
        _results.append(_Result)
      j += 1
    i += 1
  return _results

def PrintArray(_results):
  print("- - - - - - - - - -")
  
  if len(_results) == 0:
    print("no duplicates found in file")
    print("- - - - - - - - - -")
    return
    
  i = 0
  
  while i < len(_results):
    _Result = _results[i]
    _first = _Result.first
    _second = _Result.second
    _firstSpacing = " "
    _secondSpacing = " "
    if _first.lineNo < 1000:
      _firstSpacing = "  "
    if _first.lineNo < 100:
      _firstSpacing = "   "
    if _first.lineNo < 10:
      _firstSpacing = "    "
    if _second.lineNo < 1000:
      _secondSpacing = "  "
    if _second.lineNo < 100:
      _secondSpacing = "   "
    if _second.lineNo < 10:
      _secondSpacing = "    "
      
    print(f"First:    Line: {str(_first.lineNo)},{_firstSpacing}Content: {_first.content}")
    print(f"Second:   Line: {str(_second.lineNo)},{_secondSpacing}Content: {_second.content}")
    print("- - - - - - - - - -")
    i += 1

def main():
  _input = input("Configure inputFile.txt? (y/n): ")
  if _input == "y":
    _path = os.getcwd()
    os.startfile(_path)
    input("Press enter to continue...")
  _inputName = "inputFile.txt"
  _inputPath = Path(_inputName)
  if _inputPath.exists():
    _inputFile = open(_inputName, "rt")
    _file = ReadFile(_inputFile)
    _results = CompareArray(_file)
    PrintArray(_results)
  else:
    print("inputFile.txt does not exist!")
  input("Press enter to continue...")
  
if __name__ == "__main__":
  main()