# Insert the following code into your script to use the techman library
'''
# techman_init (ver 1.4)
import sys, os
techman_config = {'min_ver': 1.6, 'path': '{}'.format(os.path.dirname(
    sys.argv[0])), 'link': 'https://resources.techmandev.com/libraries/techman.py'}  # Init params
try:
    sys.path.append('{}/'.format(techman_config['path']))
    import techman
    if not techman.library.is_compatible(techman_config['min_ver']):
        raise ModuleNotFoundError
except ModuleNotFoundError:
    try:
        import requests
        library = requests.get(techman_config['link']).text
        with open('{}/techman.py'.format(techman_config['path']), 'w') as file:
            file.write(library)
        sys.path.append('{}/'.format(techman_config['path']))
        import techman
    except ConnectionError as error:  # Internet error
        raise ConnectionError('{error}: \n\nPlease check your connection\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))
    except PermissionError as error:  # Write permission error
        raise PermissionError('{error}: \n\nPlease confirm that you have permission to write to this directory\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))
    # requests library missing (most likely) or library import error
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError('{error}: \n\nPlease confirm that you have installed the requests library with \'pip3 install requests\'\n\nIf all else fails, you could download the techman.py file from {link} and save it to {path}'.format(
            link=techman_config['link'], error=error, path=techman_config['path']))

'''

#Techman's python3 function library
class library:

	version = 1.6
	defaults = {
		'link': 'https://resources.techmandev.com/libraries/techman.py',
		'path': '/tmp'
	}
		
	def is_compatible(min_ver): #checks if this version of library is >= to min_ver param
		return library.version >= min_ver

	def download_latest(**params): # download_latest('filename'='techman.py','link'='http://...') Downloads the latest copy of the library from the server and replaces the old one
		from techman import library
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = library.defaults['path']
			if params.get('link') is None:
				params['link'] = library.defaults['link']
		if params.get('filename') is None:
			params['filename'] = 'techman.py'

		try:
			import requests, sys, os
			library = requests.get(params['link']).text
			with open('{}/{}'.format(params['path'], params['filename']), 'w') as file:
				file.write(library)
		except ConnectionError as error: #Internet error
			raise ConnectionError('{error}: \n\nPlease check your connection'.format(link=params['link'], error=error))
		except ModuleNotFoundError as error: #requests library missing (most likely) or library import error
			raise ModuleNotFoundError('{error}: \n\nPlease confirm that you have installed the requests library with \'pip3 install requests\''.format(link=params['link'], error=error))

	def latest_version(**params): # latest_version('link'='https://..')
		from techman import library
		import os, sys
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = library.defaults['path']
			if params.get('link') is None:
				params['link'] = library.defaults['link']

		library.download_latest(path=params['path'], link=params['link'], filename='techman_latest.py')
		from techman_latest import library as version_check
		result = version_check.version
		del version_check
		os.remove('{}/{}'.format(params['path'], 'techman_latest.py'))
		return result
		
	def check_for_update(**params): #check_for_update('current_ver'=1.0, 'link'='http://..', 'update'=True) Checks if an update is avalible, and if 'update' param is True, will attempt to update the library
		from techman import library
		import os, sys
		if params.get('config') is not None:
			params['link'] = params['config']['link']
			params['path'] = params['config']['path']
		else:
			if params.get('path') is None:
				params['path'] = library.defaults['path']
			if params.get('link') is None:
				params['link'] = library.defaults['link']
		if params.get('current_ver') is None:
			params['current_ver'] = library.version
		if params.get('update') is None:
			params['update'] = False

		if (library.latest_version(link=params['link'], path=params['path']) <=
		    params['current_ver']):
			return False

		if params['update']:
			import importlib, techman
			library.download_latest(link=params['link'], path=params['path'])
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
			print('Invaild Option, use {yes} or {no}\n'.format(yes=yes_list[0], no=no_list[0]))
			return yn.ask(prompt, yes_list, no_list)

	#yn.check => Takes in a string and returns True for "yes" and False for "no" based on string, also returns None for invaild option (Syntax: yn.ask('yes'))
	def check(string, yes_list = ["yes","y", '1'], no_list = ['no', 'y', '0']):
		string = string.lower()
		if string in yes_list:
			return True
		elif string in no_list:
			return False
		else:
			return None


class quicksetup:
	
	import os, sys
	defaults = {
		'path': '{}'.format(os.path.dirname(sys.argv[0]))
	}

	def is_first_open(name, **params):
		from techman import quicksetup
		if params.get('message') is None:
			params['message'] = None
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

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
		from techman import quicksetup
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

		import os
		try:
			os.remove("{}/.{}.cashe".format(params['path'], name))
			return True
		except FileNotFoundError:
			return False

	def does_config_exist(name, **params):
		from techman import quicksetup
		if params.get('path') == None:
			params['path'] = quicksetup.defaults['path']
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
		from techman import quicksetup
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

		import json
		try:
			with open("{}/.{}.config".format(params['path'], name), 'w') as file:
				file.write(str(config).replace('\'', '\"').replace('True', 'true').replace('False', 'false'))
				return config
		except:
			return None

	def read_config(name, **params):
		from techman import quicksetup
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

		import json
		if quicksetup.does_config_exist(name, path=params['path']):
			with open("{}/.{}.config".format(params['path'], name), 'r') as file:
				return json.loads(file.read().replace('\'', '\"'))
		else:
			return None

	def update_config(name, new_values, **params):
		from techman import quicksetup
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

		if quicksetup.does_config_exist(name, path=params['path']):
			config = quicksetup.read_config(name, path=params['path'])
		else:
			config = {}
		config.update(new_values)
		return quicksetup.write_config(name, config, path=params['path'])

	def reset_config(name, **params):
		from techman import quicksetup
		if params.get('path') is None:
			params['path'] = quicksetup.defaults['path']

		import os
		try:
			os.remove("{}/.{}.config".format(params['path'], name))
			return True
		except FileNotFoundError:
			return False