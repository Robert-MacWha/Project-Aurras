# Project Aurras
Project Aurras is a virtual assistant I am building using intent classification and entity extraction.  This project's goals are to
1. Be able to understand direct and contextual commands
2. Be able to hold natural conversation
3. Be able to interact with extral APIs (IE turning on lights)

Here's a board showing all of the features I have planned for aurras:

[Public Micro Mindmap](https://miro.com/app/board/o9J_ltb8idc=/?invite_link_id=397704406891)

And here's a notion board used to keep track of features:

[Public notion page](https://www.notion.so/Project-Aurras-4a0a0059519f47769a94247117a41c50)

## Features

### Natural language processing
As a personal virtual assistant, Aurras should be able to understand a given natural language prompt.  This is accomplished using a fine-tuned branch of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased) which was trained to extract intents and entities.  Intents tell Aurras what you want to accomplish with a given sentence, and entities give her information to help fufill the intent.

### Skills
Once natural language has been processed, the intent and entities are given to a plugin which (a) executes commands and (b) returns a response.  More nuanced responses are planned, but at the moment plugins can only respond with a single string output.  

An example skill count be a weather API which responds to the get_weather intent.  This api might look up the weather and return it in plain text.  It might also have a special case if a datetime entitiy is located, where it returns the weather for the provided date instead of the current date.  More complex skills require more complex interactions, but fundementally they should allways be self-contained plugins.

### Interactions
Interactions are programs included with Aurras that allow plugins to interact with more complex external APIs.  An example of this might be the duckling API which is used to convert natural language into concrete measures.  Instead of each plugin handeling duckling by itself, all traffic is routed through the duckling interaction manager which significantly decreases overhead.

## Goals

My goal for project Aurras is to build a virtual assistant framework which I can use as a jumping-off point for future projects.  This means that interactions & natural language processing systems will be completely fleshed out while skills will likely remain lacking in quality, at least in the main branch.
