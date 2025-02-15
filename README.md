# Platform Layer for Consumer AI

## Setup

The `create_python_env` script creates a `venv` at the root of the `coeus` project and installs the dependencies for our API.

```sh
./scripts/create_python_env.sh
```

## Miscellaneous thoughts

- Website actions as a state machine
  - I'm environing replayabiliy of actions taken by operator. Should be easy to replay up to a certain point, maybe undo, etc... to build easy web-based agentic workflows.
