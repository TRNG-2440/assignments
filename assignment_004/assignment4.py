"""
Assignment 4
# Python Coding Activity 4 — Word Frequency Counter

## Objective

Build a console-based Word Frequency Counter that takes a sentence from the user, counts how many times each word appears, and displays the results. The user should be able to analyse multiple sentences in a loop until they choose to exit. This activity focuses on **dictionaries** and practices string methods, `for` loops, `while` loops, `if-else`, and `input()`.

---

## Background

A dictionary is the natural choice for counting word frequencies because:

- Each **word** maps directly to a **count** — this is exactly what a key:value pair represents
- Dictionary lookups are fast — checking whether a word already exists is simple using `get()` or `in`
- The results are easy to iterate over using `.items()` for display

---

## Requirements

### Data

- Maintain a dictionary called `word_count`
- Each **key** is a word (str) from the user's input
- Each **value** is the number of times (int) that word has appeared

### Menu Options

The program should present the following menu in a loop until the user exits:

```
1. Analyse a sentence
2. View word counts
3. View most frequent word
4. Clear results
0. Exit
```

### Feature Instructions

**1. Analyse a sentence**
- Prompt the user to enter a sentence
- Your program should ignore casing (i.e. 'The' and 'the' are counted as the same word)
- Split the sentence into individual words using
- Loop over each word and update the `word_count` dictionary:
  - If the word **already exists** increment its count by 1
  - If the word **does not exist** add it with a count of 1
- Print a confirmation showing how many words were processed

**2. View word counts**
- If `word_count` is empty, print a message saying no words have been analysed yet
- Otherwise loop over itmes in `word_count` and display each word and its count in a formatted list, sorted alphabetically

**3. View most frequent word**
- If `word_count` is empty, print a message saying no words have been analysed yet
- Otherwise find and display the word with the highest count

**4. Clear results**
- Clear the `word_count` dictionary
- Print a confirmation message

**0. Exit**
- Print a goodbye message and exit the loop

---

## Requirements Checklist

- A `word_count` dictionary with word keys and integer count values
- A main menu with selectable options
- Casing is ignored when processing the word count (i.e. "The" and 'the' are treated the same)
- Feature to display the count of all words
- Message when no words have been processed
- Feature to display the most frequent word
- Feature to reset the `word_count`

---

## Example Interaction

```
════════════════════════════════════════
       WORD FREQUENCY COUNTER
════════════════════════════════════════
1. Analyse a sentence
2. View word counts
3. View most frequent word
4. Clear results
0. Exit
════════════════════════════════════════
Select an option: 1

Enter a sentence: the cat sat on the black cat mat
✔ Processed 8 words.

════════════════════════════════════════
Select an option: 1

Enter a sentence: the dog sat on the log
✔ Processed 6 words.

════════════════════════════════════════
Select an option: 2

Word Counts:
────────────────────────────────────────
  black        : 1
  cat          : 2
  dog          : 1
  log          : 1
  mat          : 1
  on           : 2
  sat          : 2
  the          : 4
────────────────────────────────────────
  Total unique words: 8

════════════════════════════════════════
Select an option: 3

Most frequent word: "the" (4 times)

════════════════════════════════════════
Select an option: 0
Goodbye!
```

---

## Stretch Goals

Once the core program is working, try adding:

- **Punctuation stripping** — words like `"hello,"` and `"hello"` should be counted as the same word.
- **Top 3 most frequent words** — instead of just the single most frequent word, display the top 3 in order
- **Word search** — add a menu option that lets the user enter a word and see how many times it has appeared
- **Display Words by frequency** — instead of always displaying word counts in alphabetic order, word counts can be displayed from most to least frequent (or least to most frequent).
"""

MENU: list[str] = [
    "Analyse a sentence",
    "View word counts",
    "View most frequent words",
    "Clear results",
]

DIVIDER: str = "════════════════════════════════════════"
MINOR_DIVIDER: str = "────────────────────────────────────────"
NO_WORDS: str = "No words have been analysed yet."


def main() -> None:
    """
    The main control flow
    :return:
    """

    word_count: dict[str, int] = {}
    print_header()
    while(True):
        try:
            print_menu()
            print("0. Exit")
            print(DIVIDER)
            selection: int = int(input("Select an option: "))
            print("")
            if selection > len(MENU) or selection < 0:
                #only allow valid options
                raise ValueError

            match selection:
                case 1:
                    analyse_sentence(word_count)
                case 2:
                    view_word_counts(word_count)
                case 3:
                    view_most_frequent_words(word_count)
                case 4:
                    clear_results(word_count)
                case 0:
                    print("Goodbye!")
                    return

        except ValueError:
            continue

        except KeyboardInterrupt:
            break

def print_header() -> None:
    """
    Prints the header
    :return:
    """
    print(DIVIDER)
    print("\t\tWORD FREQUENCY COUNTER\t\t")
    print(DIVIDER)

def print_menu() -> None:
    """
    Prints the menu
    :return:
    """
    for i in range (0, len(MENU)):
        item = MENU[i]
        print(f"{i+1}. {item}")

def analyse_sentence(word_count: dict[str, int]) -> None:
    """
    Prompts for a sentence and updates the word count dict
    :param word_count:
    :return:
    """
    sentence: str = input("Enter a sentence: ")

    #clean of punctuation
    words: list[str] = sentence\
                .replace('.', '')\
                .replace('!', '')\
                .replace('?', '')\
                .replace(',', '')\
                .replace('"', '')\
                .replace(';', '')\
                .replace(':', '')\
                .replace('/', '')\
                .replace('\\', '')\
                .split()

    for word in words:
        word_count[word.lower()] = word_count.get(word.lower(), 0) + 1

    print(f"✔ Processed {len(words)} words.")
    print("")
    print(DIVIDER)

def view_word_counts(word_count: dict[str, int]) -> None:
    """
    Views the word count output
    :param word_count:
    :return:
    """
    if len(word_count) == 0:
        print(NO_WORDS)
        print(DIVIDER)
        return
    print("Word Counts: ")
    print(MINOR_DIVIDER)
    #TODO sort by v
    for k, v in word_count.items():
        print(f"\t{v} - {k}")
    print(MINOR_DIVIDER)
    print(f"\tTotal unique words: {len(word_count)}")
    print("")
    print(DIVIDER)

def view_most_frequent_words(word_count: dict[str, int], num_to_show: int = 3) -> None:
    """
    Views the most frequent word
    :param word_count:
    :return:
    """

    if len(word_count) == 0:
        print(NO_WORDS)
        print(DIVIDER)
        return

    #dictionary sorting https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_word_count: list[tuple[str, int]] = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    print("Most frequent words: ")
    for i in range(0, num_to_show):
        current_word: tuple[str, int] = sorted_word_count[i]
        #https://www.geeksforgeeks.org/python/ternary-operator-in-python/
        print(f"`{current_word[0]}` ({current_word[1]} time{"" if current_word[1] == 1 else "s"})")
    print("")
    print(DIVIDER)

def clear_results(word_count: dict[str, int]) -> None:
    """
    Clears the results an informs the user
    :param word_count:
    :return:
    """

    word_count.clear()
    print("Cleared analysed words!")
    print("")
    print(DIVIDER)


if __name__ == "__main__":
    main()
