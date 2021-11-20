# Project Aurras
Project Aurras is a NLP framework designed to parse natural language inputs into structured data.  Aurras is designed to act as a base for future NLP projects and thus focuses on modularity and customizability.  To help accomplish these goals Aurras uses a combination of core systems, interactions, and plugins.

## Overview
### Core
At its core Aurras is a wrapper for a trainable natural language processing model.  Aurras' core model is responsible for intent classification and entity extraction and is built on top of HuggingFace's pre-trained [distilbert](https://huggingface.co/transformers/model_doc/distilbert.html) model.  Due to its flexible nature, Aurras can be re-trained for many different tasks by simply changing the dataset.

### Integrations
Aurras' integrations handel interactions between its core systems and external or custom APIs.  Integrations are used to increase modularity which means that custom systems can easily be added to Aurras without interfering with the core.  Integrations will generally be used as a wrapper for talking to external programs, such as Google or Notion.  Because of this they should be made to easily work with plugins.

### Plugins
Plugins are used to add intent-specific functionality to Aurras.  Handeled by the plugins integration, they act as flexible modules that can interact with other plugins or integrations in order to create intent and entity-specific responses.

## Project Board
https://github.com/Robert-MacWha/Project-Aurras/projects/1

## Sample of interaction
#### From top to bottom: Intent classification, Intent classification & Entity extraction (x2), Plugin integration
![Sample image](https://github.com/Robert-MacWha/Project-Aurras/blob/main/docs/Interactions-Sample.PNG?raw=true)
