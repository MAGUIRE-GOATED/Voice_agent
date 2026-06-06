# Architecture

This Multi-agent has 4 components:

- **agents.py** — the workforce , carry out their designated and unique work assigned by the supervisor and then return it back to the supervisor
- **graph.py** — the brain, defines the multi_agent graph and decision making
- **supervisor.py** — the inspector, decides what work has to be assigned to which agent
- **state.py** — conversation memory, tracks messages across turns

Helper files:

- **__init__.py** — exposes only graph as the public interface

Think of it like a car — graph is the steering wheel (what you interact with), 
everything else is the engine running internally.