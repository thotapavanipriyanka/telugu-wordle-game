import regex
import random


def random_word():
    file_path = '/home/pavani/work/wordle/telugu/TeluguOCR-master/telugu_words.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.readlines()  # Read all lines into a list
        return random.choice(words).strip()  # Pick a random word and strip newline characters


def cluster_split(word):
    # Match Telugu syllables using regex
    pattern = r'\X'  # Unicode grapheme clusters
    return regex.findall(pattern, word)


def encode_split(word):
    cluster = cluster_split(word)

    # Dictionary for positions of each cluster in the word
    positional_dict = {i + 1: cluster[i] for i in range(len(cluster))}

    # Dictionary for encoded data (Unicode points of each character in the cluster)
    data_dict = {
        i + 1: [ord(char) for char in cluster[i]] for i in range(len(cluster))
    }

    return positional_dict, data_dict


def feedback_guess_1(guess, target):
    """
    Generate feedback for a guess compared to the target.
    - Green (G): Exact match (letter, symbol, position).
    - Yellow (Y): Letter and position match but symbol mismatched.
    - Orange (O): Letter and symbol match but in a different position.
    - Pink (P): Only the letter matches but not the symbols or position.
    - Blank (-): No match.
    """
    # Get positional and data dictionaries
    guess_positional, guess_data = encode_split(guess)
    target_positional, target_data = encode_split(target)

    # Initialize feedback list
    feedback = ["-"] * len(guess_positional)

    # Keep track of used positions in the target to avoid double counting
    used_positions = set()

    # First Pass: Exact Match (Green)
    for pos, guess_cluster in guess_data.items():
        if pos in target_data and guess_cluster == target_data[pos]:  # Exact match
            feedback[pos - 1] = "G"  # Mark Green
            used_positions.add(pos)  # Mark position as used
            target_data.pop(pos)  # Remove matched cluster from target

    # Second Pass: Symbol Mismatch (Yellow)
    for pos, guess_cluster in guess_data.items():
        if pos in used_positions:
            continue  # Skip already matched positions
        if pos in target_data:
            guess_letter = guess_cluster[0]
            target_letter = target_data[pos][0]
            if guess_letter == target_letter:  # Letter matches
                feedback[pos - 1] = "Y"  # Mark Yellow
                used_positions.add(pos)  # Mark position as used
                target_data.pop(pos)  # Remove matched cluster

    # Third Pass: Position Mismatch (Orange)
    for pos, guess_cluster in guess_data.items():
        if pos in used_positions:
            continue  # Skip already matched positions
        guess_letter = guess_cluster[0]
        for target_pos, target_cluster in target_data.items():
            target_letter = target_cluster[0]
            if guess_letter == target_letter and guess_cluster == target_cluster:
                feedback[pos - 1] = "O"  # Mark Orange
                used_positions.add(target_pos)  # Mark position as used
                target_data.pop(target_pos)  # Remove matched cluster
                break

    # Fourth Pass: Letter Match Only (Pink)
    for pos, guess_cluster in guess_data.items():
        if feedback[pos - 1] != "-":  # Skip already processed positions
            continue
        guess_letter = guess_cluster[0]
        for target_pos, target_cluster in target_data.items():
            target_letter = target_cluster[0]
            if guess_letter == target_letter:
                feedback[pos - 1] = "P"  # Mark Pink
                used_positions.add(target_pos)  # Mark position as used
                target_data.pop(target_pos)  # Remove matched letter
                break

    # Remaining unmatched clusters stay Blank (-)
    return feedback


def main():
    print('Welcome to Telugu Wordle!')
    print('Feedback legend:')
    print('G - Green: Exact match (letter, symbol, position)')
    print('Y - Yellow: Letter and position match but symbol mismatched')
    print('O - Orange: Letter and symbol match but in a different position')
    print('P - Pink: Only the letter matches but not the symbols or position')
    print('_ - Blank: No match.')

    target = random_word()  # Get a random Telugu word
    target_clusters = cluster_split(target)
    print("Hint: Target word has", len(target_clusters), "clusters.")  # Display the number of clusters
    print("And the word is ",{target} )

    attempts = 6
    guessed_correctly = False

    for attempt in range(1, attempts + 1):
        guess = input(f"Attempt {attempt}/{attempts}: Enter your guess: ").strip()

        # Ensure the guess length matches the target
        guess_clusters = cluster_split(guess)
        if len(guess_clusters) != len(target_clusters):
            print(f"Invalid guess! Please enter a word with {len(target_clusters)} clusters.")
            continue

        feedback = feedback_guess_1(guess, target)
        print("Feedback:", "".join(feedback))

        if "".join(feedback) == "G" * len(target_clusters):
            guessed_correctly = True
            break

    if guessed_correctly:
        print(f"Congratulations! You guessed the word '{target}' correctly in {attempt} attempts.")
    else:
        print(f"Game over! The correct word was '{target}'.")


if __name__ == "__main__":
    main()
