# Installation

As tested on Tahoe 26.1:

- move the `.saver` archive into ~/Library/Screen\ Saversodysseasvavourakis 
- make sure it's properly signed for; use codesign (possibly --deep and --force)
- use xattr to see if it worked or if the quarantine attribute is still there
- make sure to re-start preferences, and if it doesn't work also the mac, before trying to set it in preferences
