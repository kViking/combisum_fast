# Combisum

### It's an app!
... but it's still not perfect. This beta version supports .tsv style copy and should run much faster than the previous web based version. It may hammer your CPU, it may hammer your GPU. It has essentially no safe operating limits, preferring instead to attempt to run larger and larger sets of numbers until there's not enough memory to hold them all. Among the known issues are:

- Startup time is long and I don't know why yet
- Layout shifts depending on content (a mistake I will rectify)
- Content is not scrollable
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
