#!/usr/bin/python3


"""
Finds the location of strings and patches the first character to the null terminator,
preventing the messages from being displayed in the server console.

This can be executed while the server is running (on Linux; may not be successful on Windows).
"""

import sys
import argparse
import ast
import configparser
import mmap
import os

def patch_to_null(mbin, target, fully_zero):
	patched = 0
	while True:
		mbin.seek(0)
		offset = mbin.find(target.encode('ascii'))
		if offset == -1:
			return patched
		mbin.seek(offset)
		# read up to the next null terminator and zero out the range if we fullclear it
		mbin.write(b'\0' * (mbin.find(b'\0', offset) - offset if fully_zero else 1))
		patched += 1

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			description = "Patches various strings out of the given binary")

	parser.add_argument('binaries', help = "Binary files to patch", nargs='*', type = argparse.FileType(mode = 'rb+'))
	parser.add_argument('-c', '--config', help = "List of files / strings to match",
			action = 'append', default = [])
	parser.add_argument('-p', '--patch-list', help = "File list of binaries to patch",
			type = argparse.FileType(mode = 'r'))

	args = parser.parse_args()
	if args.patch_list is None and len(args.binaries) == 0:
		sys.exit("No input. Stop.")

	config = configparser.ConfigParser(converters = {
		# return multiline value as an evaluated Python literal
		'pyliteral': ast.literal_eval,
	}, interpolation = None)
	dir_path = os.path.dirname(__file__)
	config.read([ os.path.join(dir_path, "str0.ini") ] + args.config, encoding = "utf8")

	filehandles = args.binaries
	if args.patch_list is not None:
		for line in args.patch_list:
			filename = line.strip()
			if len(filename) > 0:
				filehandles.append(open(filename, 'rb+'))

	for binary in filehandles:
		mbin = mmap.mmap(binary.fileno(), length = 0, access = mmap.ACCESS_WRITE)

		for target in config.getpyliteral(os.path.basename(binary.name), "strings"):
			fully_zero = config.getboolean(os.path.basename(binary.name), "fully_zero", fallback = True)
			if patch_to_null(mbin, target, fully_zero) < 1:
				print(f'{binary.name}: Failed to locate string "{target}"')
		mbin.close()
