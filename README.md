# Natural Language Processing
This repo uses [spaCy](https://spacy.io/) by OpenAI and on [Stanza](https://stanfordnlp.github.io/stanza/) by Stanford NLP Group for syntactic structure of sentences.

## Setup

1. Create an env of your choice.

e.g.

First, create a workspace:

```
cd ~
mkdir -p speech_ws/src
```

Then, clone this repository into the src folder:

```
cd ~/speech_ws/src
git clone https://github.com/ARTenshi/speech_rec.git
```

2. Run ```pip install -r requirements.txt```

3. Build the project:

e.g 

```
cd ~/speech_ws
catkin_make
```

## Conceptual Dependencies Server

### Structure

Topics:

```
/conceptual_dependencies/final_result
```

of type `conceptual_deps/StringArray`

where StringArray.msg:

```
string[]  data
```

Services:

```
/conceptual_dependencies/condep_service
```

of type `conceptual_deps/GetConDep` 

where GetConDep.srv:

```
---
StringArray  cds
```

and 

```
/conceptual_dependencies/text_condep_service
```

of type `conceptual_deps/GetTextConDep` 

where GetTextSpeech.srv:

```
string text
---
StringArray  cds
```

### Initialization

To start a service (only one at a time), run:

**Whisper**

```
source ~/speech_ws/devel/setup.bash
roslaunch conceptual_deps condep_whisper.launch
```

**Vosk**

```
source ~/speech_ws/devel/setup.bash
roslaunch conceptual_deps condep_vosk.launch
```

### Usage

**1. Command line example**

In one terminal, subsribe to the topic:

```
source ~/speech_ws/devel/setup.bash
rostopic echo /conceptual_dependencies/final_result
```

And in a different terminal, call the service:

```
source ~/speech_ws/devel/setup.bash
rosservice call /conceptual_dependencies/condep_service "{}"
```

or

```
source ~/speech_ws/devel/setup.bash
rosservice call /conceptual_dependencies/text_condep_service "text: 'fake sentence'"
```

**2.Client Example**

In one terminal start the client:

```
source ~/speech_ws/devel/setup.bash
rosrun conceptual_deps condep_client.py
```

And in a different terminal, call it:

```
source ~/speech_ws/devel/setup.bash
rostopic pub /conceptual_dependencies/condep_text_client std_msgs/String "data: 'fake sentence'"
```
Read the code in the file `condep_client.py` for details.
