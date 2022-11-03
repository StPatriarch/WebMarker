#! usr/bin/env python3
from moduls import commands as comm
import pyshorteners


class Option:
	def __init__(self, name, command, other_cell=None):
		self.name = name
		self.command = command
		self.other_cell = other_cell

	def choose(self):
		data = self.other_cell() if self.other_cell else None
		message = self.command.execute(data) if data else self.command.execute()
		print(message)

	def __str__(self):
		return self.name


def shorten_url(url):
	type_bitly = pyshorteners.Shortener(api_key='95ba5d410ce554921b546629e268f295ba4e3796')
	short_url = type_bitly.bitly.short(url)
	return f'{short_url}'


def get_user_input(label, required=True):
	value = input(f'{label}: ') or None
	if label == 'Url':
		value = shorten_url(value)
	while required and not value:
		value = input(f'{label}: ') or None
	return value


def adding_new_bookmark():
	return {
		'Title': get_user_input('Title'),
		'Url': get_user_input('Url'),
		'Notes': get_user_input('Notes', required=False)
	}


def bookmark_deletion():
	return get_user_input(f'Enter bookmark ID to delete')


user_options = {
	'A': Option('Add Bookmark', comm.AddBookmarkCommand(), other_cell=adding_new_bookmark),
	'B': Option('Show list of bookmarks by date', comm.SelectBookmarkCommand()),
	'T': Option('Show list of bookmarks by title', comm.SelectBookmarkCommand(ordered_by='title')),
	'D': Option('Delete bookmark', comm.DeleteBookmarkCommand(), other_cell=bookmark_deletion),
	'Q': Option('Quit from WebMarker', comm.QuitCommand()),
}


def print_options(options):
	for short, option in options.items():
		print(f'({short}) {option}')
	print()


def correct_choice(choice, options):
	return choice in options or choice.upper() in options


def getting_user_choice(options):
	choice = input('Choice a turn')
	while not correct_choice(choice, options):
		choice = input('incorrect choice try again...')
	return options[choice.upper()]
