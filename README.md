# works-in-progress
Works in progress for future implementation on the website or for local use.

## pull-tapes
Pulls show tapes from the server, merges audio files into one mp3 file for each show, and zips the folder of shows into one zip file.

_Note:_
- Not compatible with shownames containing characters such as ':', ';', '\', '|', etc.
  - Same as any other valid arguments on UNIX-like systems
- If show tapes are missing or start at times other than the top and bottom of the hour, merge process may fail or not include some portion of the tapes.
