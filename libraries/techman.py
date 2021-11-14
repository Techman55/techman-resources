"""
Techman.py Library
	by Techman (https://techmandev.com)

	Changelog (v1.9):
		- Adds Packages class for installing from pip within a script and checking if script installed
"""

# Insert the following code into your script to use the techman Library
'''
# techman_init (ver 1.5)
import sys, os
techman_config = {'min_ver': 1.7, 'path': '{}'.format(os.path.dirname(
    sys.argv[0])), 'link': 'https://resources.techmandev.com/libraries/techman.py'}  # Init params
try:
    sys.path.append('{}/'.format(techman_config['path']))
    import techman
    if not techman.Library.is_compatible(techman_config['min_ver']):
        raise ModuleNotFoundError
except ModuleNotFoundError:
    try:
        import requests
        Library = requests.get(techman_config['link']).text
        try:
          with open('{}/techman.py'.format(techman_config['path']), 'w') as file:
              file.write(Library)
        except OSError:
          techman_config['path'] = '/tmp'
          with open('{}/techman.py'.format(techman_config['path']), 'w') as file:
              file.write(Library)
        sys.path.append('{}/'.format(techman_config['path']))
        import techman
    except ConnectionError as error:  # Internet error
        raise ConnectionError('{error}: \n\nPlease check your connection\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))
    except PermissionError as error:  # Write permission error
        raise PermissionError('{error}: \n\nPlease confirm that you have permission to write to this directory\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))
    # requests Library missing (most likely) or Library import error
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError('{error}: \n\nPlease confirm that you have installed the requests Library with \'pip3 install requests\'\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))

'''

#Techman's python3 function Library
class Library:

	VERSION = 1.11
	DEFAULTS = {
		'link': 'https://resources.techmandev.com/libraries/techman.py',
		'path': '/tmp'
	}
		
	def is_compatible(min_ver): #checks if this version of Library is >= to min_ver param
		return Library.VERSION >= min_ver

	def download_latest(**params): # download_latest('filename'='techman.py','link'='http://...') Downloads the latest copy of the Library from the server and replaces the old one
		from techman import Library
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = Library.DEFAULTS['path']
			if params.get('link') is None:
				params['link'] = Library.DEFAULTS['link']
		if params.get('filename') is None:
			params['filename'] = 'techman.py'

		try:
			import requests, sys, os
			Library = requests.get(params['link']).text
			with open('{}/{}'.format(params['path'], params['filename']), 'w') as file:
				file.write(Library)
		except ConnectionError as error: #Internet error
			raise ConnectionError('{error}: \n\nPlease check your connection'.format(link=params['link'], error=error))
		except ModuleNotFoundError as error: #requests Library missing (most likely) or Library import error
			raise ModuleNotFoundError('{error}: \n\nPlease confirm that you have installed the requests Library with \'pip3 install requests\''.format(link=params['link'], error=error))

	def latest_version(**params): # latest_version('link'='https://..')
		from techman import Library
		import os, sys
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = Library.DEFAULTS['path']
			if params.get('link') is None:
				params['link'] = Library.DEFAULTS['link']

		Library.download_latest(path=params['path'], link=params['link'], filename='techman_latest.py')
		from techman_latest import Library as version_check
		result = version_check.VERSION
		del version_check
		os.remove('{}/{}'.format(params['path'], 'techman_latest.py'))
		return result
		
	def check_for_update(**params): #check_for_update('current_ver'=1.0, 'link'='http://..', 'update'=True) Checks if an update is available, and if 'update' param is True, will attempt to update the Library
		from techman import Library
		import os, sys
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = Library.DEFAULTS['path']
			if params.get('link') is None:
				params['link'] = Library.DEFAULTS['link']
		if params.get('current_ver') is None:
			params['current_ver'] = Library.VERSION
		if params.get('update') is None:
			params['update'] = False

		if (Library.latest_version(link=params['link'], path=params['path']) <=
		    params['current_ver']):
			return False

		if params['update']:
			import importlib, techman
			Library.download_latest(link=params['link'], path=params['path'])
			importlib.reload(techman)
			return True


class yn:

	#yn.ask => Takes in a prompt, asks for input, and returns True for "yes" and False for "no" based on response (Syntax: yn.ask('Yes or no? '))
	def ask(prompt, yes_list = ["yes","y",'1'], no_list = ['no', 'n','0']):
		response = input(prompt).lower()
		if response in yes_list:
			return True
		elif response in no_list:
			return False
		else:
			print('Invalid Option, use {yes} or {no}\n'.format(yes=yes_list[0], no=no_list[0]))
			return yn.ask(prompt, yes_list, no_list)

	#yn.check => Takes in a string and returns True for "yes" and False for "no" based on string, also returns None for invalid option (Syntax: yn.ask('yes'))
	def check(string, yes_list = ["yes","y", '1'], no_list = ['no', 'y', '0']):
		string = string.lower()
		if string in yes_list:
			return True
		elif string in no_list:
			return False
		else:
			return None


class QuickSetup:
	
	import os, sys
	DEFAULTS = {
		'path': '{}'.format(os.path.dirname(sys.argv[0]))
	}

	def is_first_open(name, **params):
		from techman import QuickSetup
		if params.get('message') is None:
			params['message'] = None
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		try:
			open("{}/.{}.cashe".format(params['path'], name), "r").close()
			return False
		except FileNotFoundError:
			if params['message'] != None:
				print(params['message'])
			with open("{}/.{}.cashe".format(params['path'], name), "w") as cashe:
				cashe.write("first_open was completed")
			return True
		
	def reset_first_open(name, **params):
		from techman import QuickSetup
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		import os
		try:
			os.remove("{}/.{}.cashe".format(params['path'], name))
			return True
		except FileNotFoundError:
			return False

	def does_config_exist(name, **params):
		from techman import QuickSetup
		if params.get('path') == None:
			params['path'] = QuickSetup.DEFAULTS['path']
		if params.get('key_to_check') == None:
			params['key_to_check'] = None

		import json
		try:
			with open("{}/.{}.config".format(params['path'], name), 'r') as file:
				config = json.loads(file.read().replace('\'', '\"'))
				if params['key_to_check'] != None:
					if config.get(params['key_to_check']) == None:
						print('[ERROR]: Corrupt config file'.format(key=params['key_to_check']))
						return False
				return True
		except FileNotFoundError:
			return False
		except json.decoder.JSONDecodeError:
			print('[ERROR]: JSON Decode Error')
			return False

	def write_config(name, config, **params):
		from techman import QuickSetup
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		import json
		try:
			with open("{}/.{}.config".format(params['path'], name), 'w') as file:
				file.write(str(config).replace('\'', '\"').replace('True', 'true').replace('False', 'false'))
				return config
		except:
			return None

	def read_config(name, **params):
		from techman import QuickSetup
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		import json
		if QuickSetup.does_config_exist(name, path=params['path']):
			with open("{}/.{}.config".format(params['path'], name), 'r') as file:
				return json.loads(file.read().replace('\'', '\"'))
		else:
			return None

	def update_config(name, new_values, **params):
		from techman import QuickSetup
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		if QuickSetup.does_config_exist(name, path=params['path']):
			config = QuickSetup.read_config(name, path=params['path'])
		else:
			config = {}
		config.update(new_values)
		return QuickSetup.write_config(name, config, path=params['path'])

	def reset_config(name, **params):
		from techman import QuickSetup
		if params.get('path') is None:
			params['path'] = QuickSetup.DEFAULTS['path']

		import os
		try:
			os.remove("{}/.{}.config".format(params['path'], name))
			return True
		except FileNotFoundError:
			return False

class Functions:

	def set_clipboard(value, *args):
		try:
			import clipboard
			module = 'clipboard'
		except ModuleNotFoundError:
			try:
				import pyperclip
				module = 'pyperclip'
			except ModuleNotFoundError:
				import techman
				if techman.Packages.install('pyperclip') == False:
					module = None
					return False
				else:
					module = 'pyperclip'
		if module == 'clipboard':
			clipboard.set(value)
			return True
		elif module is not None:
			pyperclip.copy(value)
			return True

class Packages:
				
	def is_package_installed(module):
		import sys, importlib.util
		if module in sys.modules:
			return True
		elif importlib.util.find_spec(module) is not None:
			return True
		else:
			return False
				
	def install(module, **params):
		import subprocess, sys, techman
		if not techman.Packages.is_package_installed(module):
			try:
				if params.get('pip_v') is not None:
					subprocess.check_call([params['pip_v'], "install", module])
				else:
					try:
						subprocess.check_call([sys.executable, "-m", "pip", "install", module])
					except:
						try:
							subprocess.check_call(["pip3", "install", module])
						except:
							subprocess.check_call(["pip", "install", module])
			except:
				print('Failed to install dependency "{m}", please install it manually with "pip3 install {m}"'.format(m=module))
				return False
			finally:
				return True
		else:
			return True

#Backwards Compatibility
class library:
	version = Library.VERSION
	defaults = Library.DEFAULTS	
	def is_compatible(min_ver): #checks if this version of Library is >= to min_ver param
		return Library.is_compatible(min_ver)
	def download_latest(**params): # download_latest('filename'='techman.py','link'='http://...') Downloads the latest copy of the Library from the server and replaces the old one
		return Library.download_latest(**params)
	def latest_version(**params): # latest_version('link'='https://..')
		return Library.latest_version(**params)	
	def check_for_update(**params): #check_for_update('current_ver'=1.0, 'link'='http://..', 'update'=True) Checks if an update is available, and if 'update' param is True, will attempt to update the Library
		return Library.check_for_update(**params)
class quicksetup:
	defaults = QuickSetup.DEFAULTS
	def is_first_open(name, **params):
		QuickSetup.is_first_open(name, **params)
	def reset_first_open(name, **params):
		QuickSetup.reset_first_open(name, **params)
	def write_config(name, config, **params):
		QuickSetup.write_config(name, config, **params)
	def read_config(name, **params):
		QuickSetup.read_config(name, **params)
	def update_config(name, new_values, **params):
		QuickSetup.update_config(name, new_values, **params)
	def reset_config(name, **params):
		QuickSetup.reset_config(name, **params)
