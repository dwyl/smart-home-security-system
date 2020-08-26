# Management script for dwyl smart home

import argparse
import subprocess
import os

from contextlib import contextmanager

# Global verbose flag to toggle on/off verbose output
VERBOSE=False

# Declare global constants
HUB_SERVER_REPO="https://github.com/dwyl/smart-home-auth-server.git"
FIRMWARE_REPO="https://github.com/dwyl/smart-home-firmware.git"

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

def get_api_key():
  print("AUTH_API_KEY not set!\n")
  print("No Auth API key set, found out how at:")
  print("https://git.io/JJ6sS")
  print("")
  print("Please enter your API key once your done to continue setup")
  os.environ["AUTH_API_KEY"] = input(">")

def check_for_api_key():
  if os.environ.get("AUTH_API_KEY", None):
    # API key set
    pass
  else:
    get_api_key()

def setup():
  print(os.getcwd())
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


def main():
  parser = argparse.ArgumentParser(description="Manage Dwyl smart home install")
  parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
  subparsers = parser.add_subparsers(help="Commands")

  install_parser = subparsers.add_parser("install")
  install_parser.set_defaults(func=install)
  args = parser.parse_args()

  global VERBOSE
  VERBOSE = args.verbose

  print(args.verbose)
  if args.func:
    args.func()


if __name__ == "__main__":
  main()