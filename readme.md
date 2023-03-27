GHOSTS ADAPTIVE AMBIENCE SYSTEM (Python Version)
---------------------------------------------------------------------------
---------------------------------------------------------------------------

To install, run setup.py, this will install the required python libraries if they don't exist already, and it will then pull the system assets from my website and unpack them.

If you've ran setup in this enviroment before, and just need to unpack the assets, run unpack.py

The "assets" I speak of are audio files. These are used for ambience generation.

<br>
<br>

----------------------
*Running The System*
----------------------

<br>

To Run the ambience system, you will first need an API Key from Open Weather Map. 
https://openweathermap.org/api

Once obtained, there are 2 ways of launching the ambience system (the easiest at least). I will first outline the user client method.


User Client Method
------------------

Launch the file "console.py" in a command prompt window using python with the following command line switches:
```cmd
py console.py --run
```

Once ran, an information panel should appear looking something like this:

![alt text](repo_images/console_offline.png?raw=true)

Press "m" and than "enter" to enter the main menu for the console.

It should look something like this:

![alt text](repo_images/console_menu.png?raw=true)

Follow the menu prompt and press "s" to start the system.
The system will than ask for your apiKey, enter it in the following prompt:

![alt text](repo_images/console_apikey_prompt.png?raw=true)

Once entered you should hear audio, and it should take you back to the main menu.
Once in the menu, press "r" to go back to the console window.

The console window should now look something like this:

![alt text](repo_images/console_online.png?raw=true)

Here is an explaination of the different sections:

![alt text](repo_images/console_online_explain.png?raw=true)

<br>
<br>

Server Method
-------------

This method is best used if the ambience system is being ran as a permenant server.

To run the ambience system in this mode, run the following command:

```cmd
py console.py --run --start --apiKey=<API KEY>
```

Extras
------

To get more information on the console utility, run the following command:

```cmd
py console.py --help
```