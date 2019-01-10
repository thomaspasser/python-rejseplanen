from setuptools import setup
setup(
  name = 'rejseplanen',         # How you named your package folder (MyLib)
  packages = ['rejseplanen'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Interface with Rejseplanen API',   # Give a short description about your library
  author = 'Thomas Passer Jensen',                   # Type in your name
  author_email = 'tomatpasser@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/tomatpasser/python-rejseplanen',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/tomatpasser/python-rejseplanen/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['transport', 'rejseplanen', 'timetable', 'journey', 'public transport'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests>=2.9.1',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)