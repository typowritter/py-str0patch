# \0~~S~~tring Patch

Patches in-binary strings to start with the null terminator, primarily intended so they never
get displayed in the server console (for things that MM:S / SM can't reach, like the Steam
libraries).

Needs a relatively recent Python 3 version.

License is BSD0.  Do whatever you want with the script as long as I'm not involved.

## Usage

Copy `str0.example.ini` to `str0.ini`, add your sections, then run `python3 str0.py ${FILE}` to
shut those "RecordSteamInterfaceCreation" messages up for good.

Additional configuration files may be provided by passing `-c ${CONFIGFILE}` to the script.

## Dealing with autoupdates

`incrontab` works great for automatically patching binaries after game updates.  Add the
following entry:

```
/path/containing/bin	IN_MOVED_TO	python3 /path/to/str0.py $@/$# -c /path/to/config.ini
```
