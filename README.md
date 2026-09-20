🤖 Basic Chatbot: Alpha

A friendly rule-based chatbot written in Python, built for the CodeAlpha Python Programming Internship (Task 4).

Alpha reads what you type, looks for keywords using if-elif rules, and answers with predefined replies. It also remembers your name, tells the time and date, shares jokes, and reacts to your mood.

✨ Features
Understands messages with if-elif keyword rules
Ignores CAPITALS, punctuation and extra spaces (HELLO!!! works just like hello)
Built-in replies from the task: hello → Hi!, how are you → I'm fine, thanks!, bye → Goodbye!
Remembers your name (my name is Ravi) and uses it in replies
Tells the time and date
Shares programming jokes and Python facts
Reacts to your mood ("I am tired", "I'm great")
Whole-word matching: "history" never triggers "hi"
Coloured chat display with a typing effect (set NO_COLOR=1 to turn it off)
Handles empty input, Ctrl+C and Ctrl+D without crashing
Counts the messages you sent when the chat ends
🧠 Concepts Used
Concept	Where it is used
if-elif	the rule chain in get_response()
Functions	one small function per reply type (greeting_reply(), time_reply(), ...)
Loops	the while chat loop in main()
Input / output	input() for messages, print() for replies
Strings and lists	cleaning text, keyword lists, joke list
Modules	re, random, datetime, textwrap
🚀 How to Run
bash
python chatbot.py

Requirements: Python 3.6 or newer. No external libraries needed.

💬 What You Can Say
You type	Alpha replies
hello, hi, hey, namaste, good morning	Hi! + a friendly line using your name
how are you, whats up	I'm fine, thanks! How about you?
hello, how are you?	Hi! I'm fine, thanks! ...
my name is Priya / call me Priya	remembers your name
what's your name? / who are you?	I'm Alpha, a rule-based chatbot written in Python.
who made you?	built in Python as part of the CodeAlpha internship
what time is it?	the current time
what's the date today?	today's date
tell me a joke	a random programming joke
tell me about python	a random Python fact
i am fine / im so tired	a matching mood reply
thanks / thank you	You're welcome!
help	a list of things Alpha can do
bye, goodbye, see you, quit, exit	Goodbye! and the chat ends

Anything Alpha doesn't understand gets a friendly fallback reply that points you to help.

🖥️ Sample Conversation
  ╔══════════════════════════════════════════════════════════════╗
  ║             ★  ALPHA · THE CODEALPHA CHATBOT  ★              ║
  ║            Task 4 · Rule-based chatbot in Python             ║
  ╚══════════════════════════════════════════════════════════════╝

  Type 'help' to see what I can do, or 'bye' to leave.

  Alpha ➤ Hello! What's your name? Ravi

  Alpha ➤ Nice to meet you, Ravi! Ask me anything, or say
          'hello'.

  Ravi ➤ hello
  Alpha ➤ Hi! Great to chat with you, Ravi!

  Ravi ➤ how are you
  Alpha ➤ I'm fine, thanks! How about you?

  Ravi ➤ i am good
  Alpha ➤ Glad to hear that! Anything I can help you with?

  Ravi ➤ what is your name
  Alpha ➤ I'm Alpha, a rule-based chatbot written in Python.

  Ravi ➤ tell me a joke
  Alpha ➤ Why do programmers prefer dark mode? Because light
          attracts bugs!

  Ravi ➤ blah blah
  Alpha ➤ That's beyond my rules for now. Type 'help' for
          ideas.

  Ravi ➤ thanks
  Alpha ➤ Happy to help!

  Ravi ➤ bye
  Alpha ➤ Goodbye! Have a great day, Ravi!

  Chat ended · messages sent: 7

Some replies are chosen at random, so your conversation may show different (but equally valid) wording.

⚙️ How It Works
Clean the text: normalize() lower-cases the message and removes punctuation, so "How ARE you???" becomes "how are you".
Match keywords: has_any() checks for whole words or phrases, so "hi" matches "hi there" but not "history".
Pick a rule: get_response() runs down an if-elif chain. The first matching rule wins (for example, bye is checked first so the chat can always end).
Reply: a small function builds the answer, sometimes choosing randomly from a list with random.choice().
Loop: main() repeats until the user says goodbye or presses Ctrl+C.
✅ Tested Cases
Case	Result
hello, how are you, bye	exact task replies
HELLO!!! and  How Are You??? 	handled correctly
history is fun, this is nice	do not trigger "hi"
empty input	asks you to say something
gibberish	friendly fallback
good night	polite goodbye
📁 Project Structure
CodeAlpha_BasicChatbot/
├── chatbot.py
└── README.md
md
👤 Author
Your Name: RAMYA DURGAM
