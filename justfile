set unstable
set script-interpreter := ['uv', 'run', '--script']

test-binenv:
  uv run tests/test-binenv.py
