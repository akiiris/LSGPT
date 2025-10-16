# LSGPT

## Overview

Lickity Split GPT is a productivity tool for Windows designed to expedite the ChatGPT prompting workflow. It allows you to prompt the OpenAI API and get a response without ever leaving the window you're working in.

## Dependencies

 - Python 3.11+
 - Python openai package
 - AutoHotkey v2
 - VBScript
   - As of 2025, VBS is built into Windows, however Microsoft plans to deprecate it by 2027.

## Setup

1. Ensure the following files are in the same directory:
   - hotkey.ahk
   - server_clipboard.py
   - start_server_hidden.vbs
2. Run the following files:
   - hotkey.ahk
   - start_server_hidden.vbs
3. You're good to go!

OPTIONAL if you want the program to launch on startup:
1. Press Start + R
2. Type 'shell:startup' and hit enter
3. Place shortcuts to hotkey.ahk and start_server_hidden.vbs in this directory
 
## Usage

1. Ctrl + C --> Copy text to clipboard
2. Ctrl + Alt + Shift + Home --> Use clipboard text as user prompt
   - The Python server makes an API call and copies the response to your clipboard
3. (After waiting for LLM to generate response) Ctrl V --> Paste response

So in short...

1. Ctrl + C --> Select user prompt
2. Ctrl + Alt + Shift + Home --> Generate response
3. Wait
4. Ctrl + V --> Paste response

## Todo

 - Package everything into a binary to simplify process and remove need for dependencies
