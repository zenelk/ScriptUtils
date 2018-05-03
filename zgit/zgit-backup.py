#!/usr/bin/python

import sys
import pygit2
import os
import json
import keyring
import time

CONFIG_FOLDER_PATH = os.path.abspath(os.path.expanduser("~/.zgit"))
REPO_REGISTRY_PATH = os.path.join(CONFIG_FOLDER_PATH, "config")
HELP_KEYS = [ "h", "-h", "help", "--help" ]
CONFIG_KEY_PUBLIC_KEY_PATH = "public_key"
CONFIG_KEY_PRIVATE_KEY_PATH = "private_key"
CONFIG_KEY_PRIVATE_KEY_PASSPHRASE = "private_key_passphrase"
CONFIG_KEY_REGISTRY = "registry"
KEYCHAIN_PASSPHRASE_NAME = "ids: identity-rsa-private-key"
KEYCHAIN_NAME = "login"

class ZGitCallbacks(pygit2.RemoteCallbacks):
	def __init__(self, config):
		self.config = config
		self.completed = False
		self.valid = False

	def credentials(self, url, username_from_url, allowed_types):
		public_key = self.config[CONFIG_KEY_PUBLIC_KEY_PATH]
		private_key = self.config[CONFIG_KEY_PRIVATE_KEY_PATH]
		passphrase = self.config[CONFIG_KEY_PRIVATE_KEY_PASSPHRASE]
		return pygit2.Keypair(username_from_url, public_key, private_key, passphrase)

	def push_update_reference(self, refname, message):
		print "Push update reference"
		self.completed = True
		self.valid = message == None

class SimpleGit(object):
	def __init__(self, repo, config):
		self.repo = repo
		self.config = config

	def fetch(self, remotes=None):
		cb = ZGitCallbacks(self.config)
		for remote in self.repo.remotes:
			remote.fetch(callbacks=cb)

	def push(self, branch, remote="origin", set_upstream=False):
		cb = ZGitCallbacks(self.config)
		remote_obj = self.repo.remotes[remote]
		refspec = "refs/heads/" + branch + ":refs/heads/" + branch
		try:
			remote_obj.push([refspec], callbacks=cb)
		except pygit2.GitError as e:
			while not cb.completed:
				time.sleep(0.1)
			if not cb.valid:
				raise e
		if set_upstream:
			self.repo.branches[branch].upstream = self.repo.branches.remote[remote + "/" + branch]

	def branch_exists(self, branch, include_local=True, include_remote=False):
		if include_local and include_remote:
			return any(map(lambda x: x.endswith(branch), self.repo.branches))
		elif include_local:
			return any(map(lambda x: x.endswith(branch), self.repo.branches.local))
		elif include_remote:
			return any(map(lambda x: x.endswith(branch), self.repo.branches.remote))
		else:
			raise ValueError("Both local and remote excluded!")

	def checkout(self, branch):
		self.repo.checkout(self.repo.lookup_branch(branch))

	def create_branch(self, name):
		return self.repo.branches.local.create(name, self.repo[self.repo.head.target])

class Command(object):
	def run(self, config, repo, args):
		if args and len(args) > 0 and args[0] in HELP_KEYS:
			print self.get_help_text()
			return False
		return True

	def get_help_text(self):
		return (self.friendly_name()
			+ "\n\tkeys: " + str(self.keys())
			+ "\n\texpected args: " + str(self.expected_args)
			+ "\n\tusage example: " + self.usage_example)

	def get_input_not_blank(self, prompt, error_prompt):
		result = ""
		while result == "":
			result = raw_input(prompt)
			if result != "":
				return result
			print error_prompt

class RepoOperationCommand(Command):
	def run(self, config, repo, args):
		if not super(RepoOperationCommand, self).run(config, repo, args):
			return False
		if len(config) == 0:
			print "This command requires a non-blank config. Use the 'register' command to set it up."
			return False
		if repo.path not in config[CONFIG_KEY_REGISTRY].keys():
			print "This repo is not registered! Use the 'register command to set it up."
			return False
		return True

class StartCommand(RepoOperationCommand):
	def __init__(self):
		self.expected_args = ["feature_number"]
		self.usage_example = "zgit s 12345"

	def friendly_name(self):
		return "Start Feature"

	def keys(self):
		return [ "s", "start" ]

	def run(self, config, repo, args):
		if not super(StartCommand, self).run(config, repo, args):
			return -3
		if args and len(args) < 1:
			print "Missing argument: feature_number!"
			return -5
		zgit_callbacks = ZGitCallbacks(config)
		prefix = config[CONFIG_KEY_REGISTRY][repo.path]
		full_name = "feature/" + prefix + args[0]
		git = SimpleGit(repo, config)
		git.fetch()
		exists_local = git.branch_exists(full_name)
		exists_remote = git.branch_exists(full_name, include_local=False, include_remote=True)
		if exists_local:
			print "Already exists locally!"
			return -7
		if exists_remote:
			print "Already exists on the remote!"
			return -8
		new_branch = git.create_branch(full_name)
		repo.checkout(repo.lookup_reference(new_branch.name))
		git.push(full_name, set_upstream=True)

class CheckoutCommand(RepoOperationCommand):
	def __init__(self):
		self.expected_args = ["feature_number"]
		self.usage_example = "zgit c 12345"

	def friendly_name(self):
		return "Checkout Feature"
		
	def keys(self):
		return [ "c", "checkout" ]

	def run(self, config, repo, args):
		if not super(CheckoutCommand, self).run(config, repo, args):
			return -3
		if args and len(args) < 1:
			print "Missing argument: feature_number!"
			return -5
		zgit_callbacks = ZGitCallbacks(config)
		prefix = config[CONFIG_KEY_REGISTRY][repo.path]
		full_name = "feature/" + prefix + args[0]
		git = SimpleGit(repo, config)
		git.fetch()
		exists_local = git.branch_exists(full_name)
		exists_remote = git.branch_exists(full_name, include_local=False, include_remote=True)
		if exists_local:
			git.checkout(full_name)
		else:
			if exists_remote:
				new_local = git.create_branch(full_name)
				repo.branches[full_name].upstream = repo.branches.remote["origin/" + full_name]
				repo.checkout(new_local)
			else:
				print "Branch does not exist on local or remote!"
				return -6

class RegisterRepoPrefixCommand(Command):
	def __init__(self):
		self.expected_args = ["feature_number"]
		self.usage_example = "zgit r 12345"

	def friendly_name(self):
		return "Register Repo Feature Prefix"
		
	def keys(self):
		return [ "r", "register" ]

	def run(self, config, repo, args):
		if not super(RegisterRepoPrefixCommand, self).run(config, repo, args):
			return -3
		if args and len(args) > 0:
			prefix = args[0]
		else:
			prompt = "Using the current working directory, what would you like the prefix to be? "
			error_prompt = "Prefixes can't be blank! Try again."
			prefix = self.get_input_not_blank(prompt, error_prompt)
		config[CONFIG_KEY_REGISTRY][repo.path] = prefix
		write_config(config)

COMMANDS = [
	StartCommand(),
	CheckoutCommand(),
	RegisterRepoPrefixCommand(),
]

def print_help():
	help_string = "zgit usage: 'zgit <command> [args]'\nAvailable Commands:\n"
	for command in COMMANDS:
		help_string += "\t" + command.friendly_name() + ": " + str(command.keys()) + "\n"
	help_string += "Run 'zgit <command> help' for command details."
	print help_string

def write_config(config):
	with open(REPO_REGISTRY_PATH, "w") as f:
		json.dump(config, f, sort_keys=True, indent=2, separators=(",", ": "), ensure_ascii=False)
	print "Changes saved!"

def get_config():
	if not os.path.isdir(CONFIG_FOLDER_PATH):
		os.makedirs(CONFIG_FOLDER_PATH)

	if os.path.isfile(REPO_REGISTRY_PATH):
		with open(REPO_REGISTRY_PATH, "r") as f:
			try:
				return json.loads(f.read())
			except ValueError:
				print "Config is in an invalid format!"
	
	print "No config, using default dictionary."
	return {
		CONFIG_KEY_PUBLIC_KEY_PATH: os.path.abspath(os.path.expanduser("~/.ssh/id_rsa.pub")),
		CONFIG_KEY_PRIVATE_KEY_PATH: os.path.abspath(os.path.expanduser("~/.ssh/id_rsa")),
		CONFIG_KEY_PRIVATE_KEY_PASSPHRASE: "<FILL ME IN>",
		CONFIG_KEY_REGISTRY: {},
	}

def main(argc, argv):
	if argc < 2:
		print_help()
		return -1
	command = argv[1].lower()
	if command in HELP_KEYS:
		print_help()
		return 0

	try:
		repo = pygit2.Repository(pygit2.discover_repository(os.getcwd()))
	except KeyError:
		print "Could not find git repository in cwd!"
		return -4

	config = get_config()
	function_args = argv[2:] if len(argv) > 2 else None
	for registered_command in COMMANDS:
		if command in registered_command.keys():
			return registered_command.run(config, repo, function_args)

	print "\"" + str(argv[1]) + "\" is not a valid command!"
	print_help()
	return -2

if __name__ == "__main__":
	exit(main(len(sys.argv), sys.argv))