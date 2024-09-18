# Combisum GPU.0

## It's an app now

... and it's fast as *heck.* There's a number of issues to go still, but this is a working beta that you can use pretty reliably. Just launch the .exe and you should be off to the races.

## Limitations

The theme is set by your system theme, history isn't persistent (do you even want that?), errors aren't very informative. Computation will be limited by your available VRAM or CPU cache depending on the hardware. I'm certain there's more, but you'll have to let me know when they come up. The best place to report bugs and get them squashed will be the [Github repo](https://github.com/kviking/combisum_fast/issues)

## Run from source
> ### Prerequisites
> * Python3 or later
> * `git` and `git lfs` installed
### Instructions
Clone the repo and cd into the directory
```
git clone https://github.com/kviking/combisum_fast && cd combisum_fast && git lfs pull
```
Install dependencies
```
pip install -r source/requirements.txt
```
Run app
```
flet run source/combisum_fast.py
```

## Roadmap

Planned features!

1. ~~Dark/light mode button~~
1. ~~Layout changes if needed~~
1. ~~Startup time considerations~~
1. Persistent history
