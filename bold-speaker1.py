import argparse
import re

def bold_speaker_turns(input_filepath, output_filepath, speaker_label_to_bold):
    """
    Reads a diarized transcript, adds Markdown bold formatting to the
    entire turn of the specified speaker (tag and subsequent speech lines),
    and saves it to a new file.

    Args:
        input_filepath (str): The path to the input transcript .txt file.
        output_filepath (str): The path to save the modified transcript .txt file.
        speaker_label_to_bold (str): The speaker label (content inside brackets)
                                     whose turns should be bolded (e.g., "Speaker 1", "Bob").
    """
    try:
        in_target_speaker_turn = False
        # Pattern to match any speaker tag like "[Speaker Name]" or "[Bob]"
        # It matches an opening bracket, one or more characters that are not a closing bracket,
        # and then a closing bracket, ensuring the tag is on its own line.
        speaker_tag_pattern = re.compile(r"^\[[^\]]+\]$")
        target_speaker_tag = f"[{speaker_label_to_bold}]"

        with open(input_filepath, 'r', encoding='utf-8') as infile, \
             open(output_filepath, 'w', encoding='utf-8') as outfile:
            for line in infile:
                stripped_line = line.strip() # Remove leading/trailing whitespace for checks

                if speaker_tag_pattern.match(stripped_line):
                    # This line is a speaker tag
                    if stripped_line == target_speaker_tag:
                        in_target_speaker_turn = True
                        outfile.write(f"**{stripped_line}**\n")
                    else:  # It's another speaker's tag
                        in_target_speaker_turn = False
                        outfile.write(line) # Write the original line (e.g., "[Speaker 2]\n")
                else:
                    # This line is not a speaker tag (it's speech or a blank line)
                    if in_target_speaker_turn:
                        if stripped_line:  # If there's actual content (not just a blank line)
                            outfile.write(f"**{stripped_line}**\n")
                        else:
                            # Preserve blank lines within the target speaker's turn without bolding them
                            outfile.write(line) # Writes the original blank line with its newline
                    else:
                        # Speech/content not belonging to the target speaker's current turn
                        outfile.write(line) # Write the original line

        print(f"Processing complete for speaker '{speaker_label_to_bold}'.\nModified transcript saved to: {output_filepath}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bolds the entire turn of a specified speaker in a transcript file using Markdown."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input transcript (.txt) file."
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path for the output (modified) transcript (.txt) file."
    )
    parser.add_argument(
        "--speaker",
        type=str,
        required=True,
        help="The label of the speaker whose turns should be bolded (e.g., 'Speaker 1', 'Bob'). Do not include brackets."
    )

    args = parser.parse_args()
    bold_speaker_turns(args.input_file, args.output_file, args.speaker)
