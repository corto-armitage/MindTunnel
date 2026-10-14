# MindTunnel

An interactive psychedelic neon tunnel written in Python with pygame-ce. Includes adaptive detail and cached angle calculations for smoother animation.

## Run

Use Python 3.9 or newer. From this folder:

```sh
python -m pip install -r requirements.txt
python MindTunnel.py
```

## Controls

- Mouse left/right: twist the tunnel.
- Mouse up/down: change the petals.
- Hold a mouse button: accelerate.
- Space: pause or resume.
- R: randomize colors.
- L: toggle extra-light mode.
- S: save a timestamped PNG in the current folder.
- Esc: exit.

The window is 900 × 675 pixels. Detail adjusts automatically to frame rate; use L to reduce drawing work further.
