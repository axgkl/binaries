set unstable
set script-interpreter := ['uv', 'run', '--script']

test:
  uv run tests/test-binenv.py
