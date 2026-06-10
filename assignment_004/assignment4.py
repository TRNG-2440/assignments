from operator import itemgetter
import re
from typing import Dict, List, Optional, Tuple


class WordCounter:
    """A console-based word frequency counter that analyzes sentences and tracks word occurrences.
    
    This class maintains a dictionary of words and their frequencies, providing methods
    to analyze sentences, view statistics, search for words, and manage the data.
    """
    
    def __init__(self) -> None:
        """Initialize the WordCounter with an empty word count dictionary."""
        self.word_count: Dict[str, int] = {}

    def analyze(self, sentence: str) -> None:
        """Analyze a sentence and update word frequency counts.
        
        Processes the input sentence by:
        - Removing punctuation
        - Converting to lowercase
        - Splitting into individual words
        - Updating the word count dictionary
        
        Args:
            sentence: The input sentence to analyze
        """
        if sentence:
            # Remove punctuation and convert to lowercase for consistent counting
            sentence = re.sub(r"[^\w\s]", "", sentence).lower()
            words: List[str] = sentence.split()

            # Update word counts for each word in the sentence
            for word in words:
                if word in self.word_count:
                    self.word_count[word] += 1
                else:
                    self.word_count[word] = 1
            print(f"✔ Processed {len(words)} words.")
        else:
            print("✔ Processed 0 words.")

    def view_word_counts(self, sort_by_frequency=False) -> None:
        """Display all words and their counts in a formatted table.
        
        Args:
            sort_by_frequency: If True, sort by frequency (ascending);
                             if False (default), sort alphabetically
        """
        if self.word_count:
            print("Word Counts:")
            print("────────────────────────────────────────")
            # Sort alphabetically or by frequency based on parameter
            sorted_word_counts = (
                sorted(self.word_count.items(), key=itemgetter(1))
                if sort_by_frequency
                else sorted(self.word_count.items())
            )
            # Display each word with its count
            for k, v in sorted_word_counts:
                print(f"{k:<20}: {v}")
            print("────────────────────────────────────────")
            print(f"  Total unique words: {len(self.word_count)}")
            print()
        else:
            print("No words analyzed yet.")

    def top_n_words(self, n: int) -> None:
        """Display the top N most frequent words.
        
        Args:
            n: The number of top words to display
        """
        if self.word_count:
            # Get the N most frequent words, sorted in descending order
            most_freq_words: List[Tuple[str, int]] = sorted(
                self.word_count.items(), key=itemgetter(1), reverse=True
            )[:n]

            # Display each word with its frequency count
            for idx, word_freq in enumerate(most_freq_words):
                print(f'{idx}: "{word_freq[0]}" ({word_freq[1]} times)')
        else:
            print("No words analyzed yet.")

    def clear(self) -> None:
        """Clear all word count data and reset the dictionary."""
        self.word_count = {}
        print("Cleared word counts")

    def word_search(self, word: str) -> None:
        """Search for a word and display how many times it appears.
        
        Args:
            word: The word to search for (case-insensitive)
        """
        word = word.lower()
        if word in self.word_count:
            print(f"{word} appears {self.word_count[word]} times.")
        else:
            print(f"{word} appears 0 times.")


def print_menu() -> None:
    """Display the main menu options to the user."""
    print("════════════════════════════════════════")
    print("       WORD FREQUENCY COUNTER           ")
    print("════════════════════════════════════════")
    print("1. analyse a sentence")
    print("2. View word counts")
    print("3. View most frequent word")
    print("4. Clear results")
    print("5. Top 3 most frequent words")
    print("6. Word search")
    print("7. Display word count by frequency")
    print("0. Exit")


def try_cast_to_int(prompt: str) -> Optional[int]:
    """
    Prompt the user for input and attempt to convert it to an integer.

    Args:
        prompt: The message to display to the user.

    Returns:
        The integer value if conversion is successful, None if a ValueError occurs.
    """
    input_str: str = input(prompt)
    try:
        return int(input_str)
    except ValueError as e:
        print(f"Error encountered while converting to int: {e}")


if __name__ == "__main__":
    # Initialize the word counter and display the main menu
    word_counter = WordCounter()
    print_menu()

    # Main program loop - continue until user selects option 0 (exit)
    while True:
        print("════════════════════════════════════════")
        selection: Optional[int] = try_cast_to_int(prompt="Select an option: ")

        # Route to the appropriate function based on user selection
        match selection:
            case 0:
                print("Goodbye!")
                break
            case 1:
                sentence: str = input("Enter a sentence: ")
                word_counter.analyze(sentence)
            case 2:
                word_counter.view_word_counts()
            case 3:
                word_counter.top_n_words(n=1)
            case 4:
                word_counter.clear()
            case 5:
                word_counter.top_n_words(n=3)
            case 6:
                word: str = input("Enter the word to search: ")
                word_counter.word_search(word)
            case 7:
                word_counter.view_word_counts(sort_by_frequency=True)
            case _:
                print("Invalid choice! Try again..")
                continue
