#!/usr/bin/python3
# Management script for dwyl smart home

import argparse
import subprocess
import os
import sys
import shlex

from contextlib import contextmanager

# Global verbose flag to toggle on/off verbose output
VERBOSE=True

# Declare global constants
HUB_SERVER_REPO="https://github.com/dwyl/smart-home-auth-server.git"
FIRMWARE_REPO="https://github.com/dwyl/smart-home-firmware.git"

# Declare the start message here so we don't clog up the rest of the code
START_MESSAGE="""
Smart home is now setup for development.

To setup your development evironment:
    source .env

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

def write_env(key):
  lines = []
  try:
    with open(".env", "r+") as f:
      keys = filter(
        lambda x: not "AUTH_API_KEY=" in x, 
        f.readlines()
      )
      lines = [x for x in keys]
  except FileNotFoundError:
    pass

  lines.append("AUTH_API_KEY=" + key + "\n")
  
  with open(".env", "w") as f:
    f.writelines(lines)

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
  key = input(">")
  os.environ["AUTH_API_KEY"] = key

  return key

# Check if we have an auth API key set before continuing
def check_for_api_key():
  key = os.environ.get("AUTH_API_KEY", None)
  if key:
    pass
  else:
    key = get_api_key()

  write_env(key)

# Get and display a local API development token for the user
def gen_token():
  with cd("./smart-home-auth-server"):
    proc = subprocess.run(["mix", "smart_home.gen_token"], capture_output=True)
    print("Your development API Bearer token: \n")
    print(proc.stdout.decode(sys.stdout.encoding))
    print("\nSet this as the authorization header in your favourite API development tool.")

# Install brew, otherwise exit
def must_install_brew():
  if input("Homebrew is needed to install dependencies, install? (y/N)")[0] == "y":
    run(shlex.split("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\""))
  else:
    exit(1)

def check_software(software):
  exists = True
  try:
    subprocess.run(shlex.split(software), capture_output=True)
  except FileNotFoundError:
    exists = False
  return exists

# Check that necessary dependencies are installed
def check_deps():
  deps = {"elixir": False, "brew": False, "psql": False, "node": False}
  # Check for brew
  out("Checking for homebrew (to install dependencies)...")
  if check_software("brew"):
    out("OK\n")
    deps["brew"]=True
  else:
    out("Error - You may need to install dependencies manually!\n")

  # Check for elixir
  out("Checking for Elixir...")
  if check_software("elixir -v"):
    out("OK!\n")
    deps["elixir"] = True
  else:
    out("ERROR\n")

  # check for postgres
  out("Checking for PostgreSQL...")
  if check_software("postgres -V"):
    out("OK\n")
    deps["psql"] = True
  else:
    out("ERROR\n")


  return deps

def install_deps(brew, missing):
  if not brew:
    must_install_brew()

  
  out("Installing Elixir...\n")
  run(shlex.split("brew install elixir"))

  out("Installing PostgreSQL...\n")
  run(shlex.split("brew install postgres"))

def install_nerves_dependencies():
  if input("Do you want to install build dependencies for nerves? (fwup squashfs coreutils xz pkg-config)? (y/N)")[0] == "y":
    run(shlex.split("brew install fwup squashfs coreutils xz pkg-config"))
  else:
    out("NERVES WILL FAIL TO BUILD WITHOUT DEPS INSTALLED \n")
    out("https://hexdocs.pm/nerves/installation.html#content\n")
  
def pre_install():
  deps = check_deps()
  brew = deps["brew"]

  del deps["brew"]

  missing = [ key for key in deps if deps[key] == False ]

  if len(missing) > 0:
    out("Missing dependencies!\n Would you like to install them now?")

    if input("(y/N)")[0] == "y":
      install_deps(brew, missing)
    else:
      out("Please install: " + " ,".join(missing) + "\n Then continue with download.")
      exit(1)


# Setup deps etc. for firmware
def setup():
  # Setup firmware
  with cd("./smart-home-firmware"):
    out("Installing firmware deps...")
    install_nerves_dependencies()
    run("mix", "deps.get")
    out("OK\n")

  with cd("./smart-home-auth-server"):
    out("Installing hub server deps...")
    run("mix", "setup")
    out("OK\n")


# Run necessary install functions
def install():
  download()
  pre_install()
  check_for_api_key()
  setup()
  gen_token()

  print(START_MESSAGE)

# Clean up everything we've installed
def clean():
  out("Cleaning up...")
  run("rm", "-rf", "./smart-home-auth-server")
  run("rm", "-rf", "./smart-home-firmware")
  run("rm", ".env")
  out("OK\n")

# Declare our command parsers and run the intended function
def main():
  parser = argparse.ArgumentParser(description="Manage Dwyl smart home install")
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


  if args.func:
    args.func()

# Don't run main if we're called from another script.
if __name__ == "__main__":
  main()