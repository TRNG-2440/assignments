# Function Refactor

## Objective
Practice breaking a long, repetitive script into clean, reusable functions.

## Setup
Create a new file called `function_refactor.py` and paste in the following script:

```python
text = "The quick brown fox jumps over the lazy dog. The dog barked. The fox ran away quickly! Did the dog chase the fox? Of course the dog chased the fox."

word_count = 0
for char in text:
    if char == " ":
        word_count += 1
word_count += 1
print("Word count: " + str(word_count))

sentence_count = 0
for char in text:
    if char == "." or char == "!" or char == "?":
        sentence_count += 1
print("Sentence count: " + str(sentence_count))

longest = ""
current_word = ""
for char in text:
    if char == " " or char == "." or char == "!" or char == "?":
        if len(current_word) > len(longest):
            longest = current_word
        current_word = ""
    else:
        current_word += char
if len(current_word) > len(longest):
    longest = current_word
print("Longest word: " + longest)

word_counts = {}
current_word = ""
for char in text:
    if char == " " or char == "." or char == "!" or char == "?":
        if current_word != "":
            lower_word = current_word.lower()
            if lower_word in word_counts:
                word_counts[lower_word] += 1
            else:
                word_counts[lower_word] = 1
            current_word = ""
    else:
        current_word += char
if current_word != "":
    lower_word = current_word.lower()
    if lower_word in word_counts:
        word_counts[lower_word] += 1
    else:
        word_counts[lower_word] = 1
print("Word frequencies:")
for word in word_counts:
    print("  " + word + ": " + str(word_counts[word]))

most_common = ""
highest_count = 0
for word in word_counts:
    if word_counts[word] > highest_count:
        highest_count = word_counts[word]
        most_common = word
print("Most common word: " + most_common + " (" + str(highest_count) + " times)")

total_length = 0
total_words = 0
current_word = ""
for char in text:
    if char == " " or char == "." or char == "!" or char == "?":
        if current_word != "":
            total_length += len(current_word)
            total_words += 1
            current_word = ""
    else:
        current_word += char
if current_word != "":
    total_length += len(current_word)
    total_words += 1
average_length = total_length / total_words
print("Average word length: " + str(round(average_length, 2)))
```

## Instructions
1. Run the script and confirm it works
2. Identify the repeated patterns and logic
3. Refactor the script into functions — aim for each function to do one thing
4. The output should be identical before and after refactoring

## Things to Consider
- What logic is duplicated across multiple sections?
- Which sections could share a helper function?
- What should each function accept as parameters and return?