# Combisum

### Quickstart
2. Click the green "code" button above and right of this ^
3. Click "download as zip"
4. The .exe is in the dist (distribution) folder

It'll open after a few seconds, so give it time. Because I didn't create any custom splash screen for loading, it may pop up a blank window until it loads. Eventually it should load a simple interface. After you've run a calculation, the button to copy it to your clipboard is on the bottom right and may be hidden if the window is too small.

### It's an app!
... but it's still not perfect. This beta version supports .tsv style copy and should run much faster than the previous web based version. It may hammer your CPU, it may hammer your GPU. It has essentially no safe operating limits, preferring instead to attempt to run larger and larger sets of numbers until there's not enough memory to hold them all. Among the known issues are:

- ~~No installer, requires a whole folder of crap~~ 
    - Fixed!
- Startup time is long and I don't know why yet
    - Working theory now!
- Layout shifts depending on content
- Content is not scrollable and hides copy button in some window sizes
- Error messages are not very descriptive and there's no way for a user to access more useful information

### Anticipated issues
- I don't have a GPU in the machine that can run Windows right now, so GPU acceleration may or may not work. 
- CPU computation limits were set against a laptop and should probably rely on a try/except loop rather than an integer I literally just made up
- I'm hoping this will essentially "just run" but there are a number of libraries used in this project that could be a headache soon (pytorch is the main worry)
- Pyperclip previously didn't work great with Windows 11 from a web distribution, so I'm not 100% sure it'll work in native


### Roadmap
I'm still planning on polishing this a bit more, and hopefully getting the startup time much lower. Some of the libraries that are integral are quite large. The general plan for now is:

1. Any blocking issues with the build
2. Layout issues
3. Error messages
4. Startup time
5. Customization (icon, splashes, app name, etc.)
5. Create an installer