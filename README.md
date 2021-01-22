# works-in-progress
Works in progress for future implementation on the website or for local use.

### _Required Packages:_
- `python3`
- `ffmpeg`
- `zip`
- `scp`
- `selenium`

## pull-tapes-term

Pulls show tapes for all weeks of a given show for a single term from the server, merges audio files into one mp3 file for each show, and zips the folder of shows into one zip file.

__Usage:__ `python3 pull-tapes-term.py showName Term(F/W/S) Year DayOfWeek(Mon/Tue/...) showStartTime showEndTime` 

## pull-tapes-individual

Pulls show tapes for a given show (or shows) from the server, merges audio files into one mp3 file for each show, and zips the folder of shows into one zip file.

__Usage:__ `python3 pull-tapes-individual.py showName startYear startMonth startDay showStartTime showEndTime [NumberOfWeeks]`

### _Note:_
- Not compatible with shownames containing special characters such as `'`, `"`, `&`, `:`, `;`, `/`, `\`, `|`, `$`, etc.
  - Same as any other valid arguments on UNIX-like systems
- If show tapes are missing or start at times other than the top and bottom of the hour, merge process may fail or not include some portion of the tapes.

## showScheduler
Books shows from a pre processed csv on our libretime instance, stream.krlx.org.

__Usage:__ `python3 showScheduler`
###  _Note:_
- You must set the `user` and `pass` varribles with a login.
