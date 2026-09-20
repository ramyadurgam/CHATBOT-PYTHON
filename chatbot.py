"""
CodeAlpha Python Programming Internship
Task 4: Basic Chatbot
------------------------------------------------------------
A friendly rule-based chatbot called "Alpha". It reads what you type,
looks for keywords with if-elif rules, and answers with predefined
replies. It remembers your name, tells the time and jokes, and more.

Try: hello | how are you | what's your name | tell me a joke
     what time is it | help | bye

Tip: set NO_COLOR=1 to switch off colours and the typing effect.
"""

import datetime
import os
import random
import re
import sys
import textwrap
import time

BOT_NAME = "Alpha"
WIDTH = 64

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why was the Python developer calm? Because everything was under control... with indentation.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "Why did the developer go broke? Because he used up all his cache!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
]

PYTHON_FACTS = [
    "Python is named after the comedy group Monty Python, not the snake!",
    "Python was created by Guido van Rossum and first released in 1991.",
    "In Python, indentation is part of the syntax. It's how code blocks are defined.",
]

FALLBACKS = [
    "Hmm, I didn't catch that. Type 'help' to see what I can do.",
    "I'm still learning! Try 'hello', 'how are you', 'joke' or 'time'.",
    "That's beyond my rules for now. Type 'help' for ideas.",
]

# ------------------------------------------------------------------
#  Colour helpers
# ------------------------------------------------------------------
USE_COLOR = (sys.stdout.isatty() or "FORCE_COLOR" in os.environ) \
    and "NO_COLOR" not in os.environ
ANIMATE = sys.stdout.isatty() and "NO_COLOR" not in os.environ

if os.name == "nt":
    os.system("")  # lets Windows terminals understand colour codes

CODES = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
}


def paint(text, *styles):
    """Wrap text in colour/style codes (does nothing if colour is off)."""
    if not USE_COLOR:
        return text
    return "".join(CODES[s] for s in styles) + text + CODES["reset"]


def visible_len(text):
    """Length of text as seen on screen (ignores colour codes)."""
    length = 0
    skipping = False
    for ch in text:
        if ch == "\033":
            skipping = True
        elif skipping and ch == "m":
            skipping = False
        elif not skipping:
            length += 1
    return length


def center(text, width):
    space = width - visible_len(text)
    left = space // 2
    return " " * left + text + " " * (space - left)


def box(lines, color):
    inner = WIDTH - 2
    out = [paint("╔" + "═" * inner + "╗", color)]
    for line in lines:
        out.append(paint("║", color) + center(line, inner) + paint("║", color))
    out.append(paint("╚" + "═" * inner + "╝", color))
    return out


# ------------------------------------------------------------------
#  Understanding the user
# ------------------------------------------------------------------
def normalize(text):
    """Lower-case the text and remove punctuation so matching is easy."""
    text = text.lower().replace("'", "").replace("’", "")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def has_any(clean, phrases):
    """True if any whole word/phrase appears in the cleaned text."""
    padded = f" {clean} "
    for phrase in phrases:
        if f" {phrase} " in padded:
            return True
    return False


def has_word_from(clean, words):
    return any(word in words for word in clean.split())


def find_name(clean):
    """Look for 'my name is X' or 'call me X'. Returns a name or None."""
    match = re.search(r"(?:my name is|call me) ([a-z]+)", clean)
    if match:
        return match.group(1).title()
    return None


# ------------------------------------------------------------------
#  Replies (each intent has its own small function)
# ------------------------------------------------------------------
def greeting_reply(state, clean):
    if has_any(clean, ["good morning"]):
        opener = "Good morning!"
    elif has_any(clean, ["good afternoon"]):
        opener = "Good afternoon!"
    elif has_any(clean, ["good evening"]):
        opener = "Good evening!"
    elif has_any(clean, ["namaste"]):
        opener = "Namaste!"
    else:
        opener = "Hi!"
    extras = [f"Nice to see you, {state['name']}.",
              "How can I help you today?",
              f"Great to chat with you, {state['name']}!"]
    return opener + " " + random.choice(extras)


def how_are_you_reply(state, clean):
    opener = "Hi! " if has_any(clean, ["hello", "hi", "hey", "namaste"]) else ""
    return opener + "I'm fine, thanks! " + random.choice(["How about you?", "What about you?"])


def farewell_reply(state):
    return f"Goodbye! Have a great day, {state['name']}!"


def time_reply():
    return "It's " + datetime.datetime.now().strftime("%I:%M %p") + " right now."


def date_reply():
    return "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y") + "."


def help_reply():
    return ("I can chat about these: say hello, ask 'how are you', tell me your name "
            "('my name is ...'), ask 'what time is it' or 'what's the date', "
            "request a 'joke', or ask about Python. Type 'bye' to leave.")


def get_response(user_text, state):
    """Return (reply, keep_chatting). The heart of the chatbot: if-elif rules."""
    clean = normalize(user_text)
    new_name = find_name(clean)

    if clean == "":
        return "Say something and I'll reply!", True

    elif has_any(clean, ["bye", "goodbye", "see you", "see ya", "quit", "exit", "good night"]):
        return farewell_reply(state), False

    elif new_name:
        state["name"] = new_name
        return f"Nice to meet you, {new_name}! I'll remember your name.", True

    elif has_any(clean, ["how are you", "how are you doing", "how do you do", "how r u",
                         "whats up", "sup", "hows it going"]):
        return how_are_you_reply(state, clean), True

    elif has_any(clean, ["hello", "hi", "hey", "hii", "hiya", "namaste", "good morning",
                         "good afternoon", "good evening"]):
        return greeting_reply(state, clean), True

    elif has_any(clean, ["i am", "im", "feeling"]) and has_word_from(
            clean, {"fine", "good", "great", "awesome", "happy", "well", "okay", "ok", "amazing"}):
        return "Glad to hear that! Anything I can help you with?", True

    elif has_any(clean, ["i am", "im", "feeling"]) and has_word_from(
            clean, {"sad", "bad", "tired", "stressed", "upset", "sick", "angry", "bored"}):
        return "Sorry to hear that. Hope things get better soon. Want to hear a joke?", True

    elif has_any(clean, ["your name", "who are you", "what are you"]):
        return f"I'm {BOT_NAME}, a rule-based chatbot written in Python.", True

    elif has_any(clean, ["who made you", "who created you", "who built you",
                         "who developed you", "your creator"]):
        return "I was built in Python as part of the CodeAlpha internship.", True

    elif has_any(clean, ["how old are you", "your age"]):
        return "I was born the moment this script started running!", True

    elif has_any(clean, ["thanks", "thank you", "thx", "thankyou"]):
        return random.choice(["You're welcome!", "Anytime!", "Happy to help!"]), True

    elif has_any(clean, ["help", "what can you do", "commands"]):
        return help_reply(), True

    elif has_any(clean, ["time", "what time", "clock"]):
        return time_reply(), True

    elif has_any(clean, ["date", "what day", "day is it", "today"]):
        return date_reply(), True

    elif has_any(clean, ["joke", "funny", "make me laugh"]):
        return random.choice(JOKES), True

    elif has_any(clean, ["python"]):
        return random.choice(PYTHON_FACTS), True

    elif has_any(clean, ["codealpha", "internship"]):
        return "CodeAlpha is a software company that runs hands-on internships. Great choice!", True

    elif has_any(clean, ["weather"]):
        return "I can't check live weather, but I hope it's sunny where you are!", True

    elif has_any(clean, ["you are", "youre"]) and has_word_from(
            clean, {"smart", "cool", "awesome", "great", "nice", "amazing", "good", "funny"}):
        return "Aww, thank you! You're pretty great too.", True

    else:
        return random.choice(FALLBACKS), True


# ------------------------------------------------------------------
#  Chat display
# ------------------------------------------------------------------
def bot_say(text):
    """Print the bot's reply, wrapped, with a small typing effect."""
    label = paint(f"{BOT_NAME} ➤ ", "bold", "cyan")
    wrapped = textwrap.fill(text, width=WIDTH - 12, subsequent_indent=" " * 10)
    print("  " + label, end="", flush=True)
    for ch in wrapped:
        print(paint(ch, "cyan") if ch.strip() else ch, end="", flush=True)
        if ANIMATE:
            time.sleep(0.012)
    print("\n")


def ask_name():
    raw = input("  " + paint(f"{BOT_NAME} ➤ ", "bold", "cyan") + "Hello! What's your name? ")
    clean = normalize(raw)
    match = re.search(r"(?:my name is|call me|i am|im) ([a-z]+)", clean)
    if match:
        return match.group(1).title()
    if clean:
        return clean.split()[0].title()
    return "Friend"


def main():
    print()
    title = [paint(f"★  {BOT_NAME.upper()} · THE CODEALPHA CHATBOT  ★", "bold", "cyan"),
             paint("Task 4 · Rule-based chatbot in Python", "dim")]
    for line in box(title, "cyan"):
        print("  " + line)
    print()
    print("  " + paint("Type 'help' to see what I can do, or 'bye' to leave.", "dim"))
    print()

    state = {"name": "Friend"}
    messages = 0

    try:
        state["name"] = ask_name()
        print()
        bot_say(f"Nice to meet you, {state['name']}! Ask me anything, or say 'hello'.")

        chatting = True
        while chatting:
            user_text = input("  " + paint(f"{state['name']} ➤ ", "bold", "green"))
            print()
            reply, chatting = get_response(user_text, state)
            bot_say(reply)
            if user_text.strip():
                messages += 1
    except (EOFError, KeyboardInterrupt):
        print()
        bot_say("Goodbye!")

    print("  " + paint(f"Chat ended · messages sent: {messages}", "dim"))
    print()


if __name__ == "__main__":
    main()
