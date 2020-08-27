#!/usr/bin/python3
# Management script for dwyl smart home

import argparse
import subprocess
import os
import sys

from contextlib import contextmanager

# Global verbose flag to toggle on/off verbose output
VERBOSE=False

# Declare global constants
HUB_SERVER_REPO="https://github.com/dwyl/smart-home-auth-server.git"
FIRMWARE_REPO="https://github.com/dwyl/smart-home-firmware.git"

# Declare the start message here so we don't clog up the rest of the code
START_MESSAGE="""
Smart home is now setup for development.

To run the hub server:

    cd smart-home-auth-server
    mix phx.server

To run the firmware development build:
    cd smart-home-firmware
    iex -S mix

If these error, please run:
    ./manage.py clean
    ./manage.py --verbose install
and file and issue with the output.
"""

# Emulate a shells `cd`
# https://stackoverflow.com/questions/431684/
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# Helper function to allow for same line I/O without repeating ourselves
def out(line):
  print(line, end="", flush=True)

# Run a command, and display the result based on wether VERBOSE is set or not
def run(*args):
  return subprocess.run(args, capture_output=not VERBOSE)

# Dowload required files from github.
def download():
  out("Downloading Hub Server...")
  process = run("git", "clone", HUB_SERVER_REPO)
  out("OK\n")

  out("Downloading firmware...")
  process = run("git", "clone", FIRMWARE_REPO)
  out("OK\n")

# Prompt user for an auth API key so we can finish setup
def get_api_key():
  print("AUTH_API_KEY not set!\n")
  print("No Auth API key set, found out how at:")
  print("https://git.io/JJ6sS")
  print("")
  print("Please enter your API key once your done to continue setup")
  os.environ["AUTH_API_KEY"] = input(">")

# Check if we have an auth API key set before continuing
def check_for_api_key():
  if os.environ.get("AUTH_API_KEY", None):
    # API key set
    pass
  else:
    get_api_key()

# Get and display a local API development token for the user
def gen_token():
  with cd("./smart-home-auth-server"):
    proc = subprocess.run(["mix", "smart_home.gen_token"], capture_output=True)
    print("Your development API Bearer token: \n")
    print(proc.stdout.decode(sys.stdout.encoding))
    print("\nSet this as the authorization header in your favourite API development tool.")

# Setup deps etc. for firmware
def setup():
  # Setup firmware
  with cd("./smart-home-firmware"):
    out("Installing firmware deps...")
    run("mix", "deps.get")
    out("OK\n")

  with cd("./smart-home-auth-server"):
    out("Installing hub server deps...")
    run("mix", "setup")
    out("OK\n")


# Run necessary install functions
def install():
  download()
  check_for_api_key()
  setup()
  gen_token()

  print(START_MESSAGE)

# Clean up everything we've installed
def clean():
  out("Cleaning up...")
  run("rm", "-rf", "./smart-home-auth-server")
  run("rm", "-rf", "./smart-home-firmware")
  out("OK\n")

# Declare our command parsers and run the intended function
def main():
  parser = argparse.ArgumentParser(description="Manage Dwyl smart home install")
  parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
  subparsers = parser.add_subparsers(help="Commands")
  subparsers.default = "help"

  install_parser = subparsers.add_parser("install", help="Install the smart home system")
  install_parser.set_defaults(func=install)

  clean_parser = subparsers.add_parser("clean", help="Clean up everything")
  clean_parser.set_defaults(func=clean)

  gen_token_parser = subparsers.add_parser("gen-token", help="Genereate a JWT token for development")
  gen_token_parser.set_defaults(func=gen_token)

  if len(sys.argv)==1:
    parser.print_usage(sys.stderr)
    sys.exit(1)

  args = parser.parse_args()

  global VERBOSE
  VERBOSE = args.verbose

  if args.func:
    args.func()

# Don't run main if we're called from another script.
if __name__ == "__main__":
  main()