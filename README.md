# \0~~S~~tring Patch

Patches in-binary strings to start with the null terminator, primarily intended so they never
get displayed in the server console (for things that MM:S / SM can't reach, like the Steam
libraries).

Needs a relatively recent Python 3 version.

License is BSD0. Original credits to https://git.csrd.science/nosoop/py-str0patch

## Usage

Run `python3 str0.py ${FILE}` to shut those "RecordSteamInterfaceCreation" messages up for good.

Additional configuration files may be provided by passing `-c ${CONFIGFILE}` to the script.
You can add your sections following the syntax of `str0.ini`

Here is a useful bash snippet to spot the string you want to patch:

```bash
find -name "*.so" -exec sh -c "strings {} | grep -E '<ADD your strings here>'" \;
```

**NOTE**: The patch process is *NOT* whole string matching, so don't write a partial string, as this may corrupt the file.

## Dealing with autoupdates

`incrontab` works great for automatically patching binaries after game updates.  Add the
following entry:

```
/path/containing/bin	IN_MOVED_TO	python3 /path/to/str0.py $@/$# -c /path/to/config.ini
```
