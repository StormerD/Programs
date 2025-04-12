from termcolor import colored

for guessNum in range(1, 7):
  guess = input(f"\nGuess {guessNum}: ").upper()
  if guess == "SNAKE":
    print(colored("Correct!", "green"))
    break
  print(colored("Wrong", "red"))