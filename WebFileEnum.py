import requests
import argparse
import sys
import pdb

# Configure CLI argument parsing.
parser = argparse.ArgumentParser(
		description="Enumerate files & directories with the ability to exclude results based on string-matching against HTML content body."
)
parser.add_argument('-u', metavar='"https://example.com/"', type=str, required=True)
parser.add_argument('-w', metavar='"~/Wordlist.txt"', type=str, required=True)
parser.add_argument('-e', metavar='"login,sign-in"', required=False, type=str, help='Comma-separated list of strings to exclude.')
parser.add_argument('--v', required=False, action='store_true', help='Verbose output.')

# Assign arguments.
base_url = parser.parse_args().u
wordlist = parser.parse_args().w
exclusions = parser.parse_args().e
verbose = parser.parse_args().v

# Parse exclusions.
if exclusions is not None:
		if "," in exclusions:
				exclusions_list = exclusions.split(",")
		else:
				exclusions_list = [exclusions]
else:
		exclusions_list = []

# Append trailing / if not in URL.
if not base_url.endswith('/'):
	base_url = base_url + "/"

wordlist_lines = open(wordlist, encoding='latin-1').readlines()
output_file = open(f"WebFileEnum.log", 'a')

# Loop through wordlist.
for line in wordlist_lines:

	# Remove trailing newline.
	line = line.strip()

	_r = requests.get(base_url + line)

	# Continue w/ loop if an exclusion matches response body.
	is_excluded = False

	for e in exclusions_list:
		if e.lower() in _r.text.lower():
			is_excluded = True
			
	if is_excluded:
		if verbose: print(f"[EXCLUSION HIT] {base_url}{line}")
		continue
	
	# Write output to console & log if status code is anything but 404 (Not Found).
	if _r.status_code != 404:
		print(f"[{_r.status_code}] {base_url}{line}")
		output_file.write(f"[{_r.status_code}] {base_url}{line}\n")
