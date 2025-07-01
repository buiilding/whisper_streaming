import time
import random
import sys
import argparse

try:
    from pynput.keyboard import Controller
except ImportError:
    print("pynput is not installed. Please install it with 'pip install pynput'", file=sys.stderr)
    sys.exit(1)


def simulate_typing(text: str):
    """
    Simulates typing the given text with random delays between keystrokes.
    """
    keyboard = Controller()
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(random.uniform(0.05, 0.1))
    
    keyboard.press(' ')
    keyboard.release(' ')


def type_instantly(text: str):
    """
    Types the given text instantly.
    """
    keyboard = Controller()
    keyboard.type(text)
    keyboard.press(' ')
    keyboard.release(' ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to simulate typing or type instantly from stdin.")
    parser.add_argument(
        '--mode', 
        type=str, 
        default='simulate', 
        choices=['simulate', 'instant'],
        help="Typing mode: 'simulate' for realistic typing, 'instant' for fast typing."
    )
    args = parser.parse_args()

    # This part of the script will run when you execute it directly.
    # It's designed to read from standard input, which is perfect for piping.
    #
    # Example usage:
    # echo "hello world" | python3 typing_simulator.py
    #
    # Or with your whisper streaming setup:
    # arecord -f S16_LE -c1 -r 16000 -t raw -D default | nc localhost 43007 | python3 typing_simulator.py

    # Give user time to switch to another window
    print("Starting typing simulation in 5 seconds. Focus on your text editor.", file=sys.stderr)
    time.sleep(5)
    print(f"Ready to type in '{args.mode}' mode.", file=sys.stderr)

    typing_function = simulate_typing if args.mode == 'simulate' else type_instantly

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # The output from whisper_online_server is "start_ms end_ms text"
        # We need to extract the text part.
        parts = line.split(maxsplit=2)
        if len(parts) < 3:
            # Maybe the input is just plain text
            text_to_type = line
        else:
            text_to_type = parts[2]
        
        typing_function(text_to_type) 