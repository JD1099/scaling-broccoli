# scalingBroccoli

Feb 27 2022:

This is an incomplete project.

Coming up with a name for this project has been very difficult for me. For now I am using a name suggested by github's repo creator.

As of Feb 27 2022. This script does a single task of creating a config file in the user folder and maintaining security over the file as the config is intended to hold passwords in the future.

ToDo list:
I want to restructure how the script works. At some point I had been just throwing my ideas into a script and proceeding with whatever didn’t cause errors. As a result many parts of my script seem arbitrary.

The destination of the config file will move to the data folder within the project instead of littering the user folder with unsolicited ini files. In hindsight This will make the uninstall script much simpler.

Due to my lack of knowledge and experience with file intrusion prevention I am going to overcompensate by encrypting the config with gpg.

DO NOT use this package unless you have thoroughly reviewed how the scripts work. I do not have any professional experience with creating secure scripts. I am naturally bound to make mistakes because I am actively learning new things as I develop this project.

Despite my project resembling an application-like structure. The package will not work because I still need to learn how to set up runners and bin files.

