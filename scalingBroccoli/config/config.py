import configparser, time, os, termcolor, mysql.connector

config = configparser.ConfigParser()
colored = termcolor.colored
#mysqlDB = mysql.connector.connect

verbose = False # If true the script will preform in respect to the definition of verbose.
debug = False # For simple output.

def sleep(n=0): # made a shortcut to the time.sleep() function because I was feeling lazy.
    time.sleep(n)

def clear(): # Clears the terminal in case the previous script run had lots errors.
    os.system('cls' if os.name == 'nt' else 'clear')

def green(text, delay=0):
    sleep(delay)
    print(colored(str(text),'green'))

def red(text, delay=0):
    sleep(delay)
    print(colored(str(text),'red'))

def color(text,color,attrs='bold',delay=0):
    sleep(delay)
    print(colored(str(text),str(color),attrs=[str(attrs)]))

loopCount = 0

while True: # Initial script loop where most of the user interface and script functions take place.

    def envVars(): # A cute organized place for per-loop variables
        # Global vars
        global configExist
        global fileMeta
        global userConfigFile
        global defaultConfig
        global yesList
        global noList
        global editorList
        # Var definition
        try: # User config file path.
            userConfigFile = str(os.environ.get('HOME')+'/.backupDB.ini')
        except:
            userConfigFile = null
        try: # Does the config exist?
            configExist = os.path.isfile(userConfigFile)
        except:
            configExist = False
        try: # Config file meta data.
            fileMeta = os.stat(userConfigFile)
        except:
            pass
        try: # Default config dict.
            defaultConfig = {'Required': {'host': "'localhost'",'user': "'username'"
                ,'password': "'password'",'database': "'dbname'"},'Optional':
                {'auth_plugin': "'mysql_native_password'"},'config validation':{'skip stage 1':'false'}}
        except:
            pass       
        try: # A list containing words related to 'yes'.
            yesList = ['yes','Yes','y','Y','true','True']
        except:
            pass
        try: # A list containing words related to 'no'.
            noList = ['no','No','n','N','False','false']
        except:
            pass
        try: # A list of command line based editors.
            editorList = ['nano','vim']
        except:
            pass

        # Var return
        return configExist
        return fileMeta
        return userConfigFile
        return defaultConfig
        return yesList
        return noList
        return editorList

    envVars()
    
    def createConfigFile(): # Creates a config file and sets file permissions.
        config.read_dict(defaultConfig)      
        with open(userConfigFile, 'w') as configfile:
            config.write(configfile)
        os.system('chmod 600 ' + userConfigFile)
        

    def configCheck():        
        if fileMeta.st_mode != 33152: # Makes sure the config file is stored securely.
            red('CONFIG ERROR:')
            red('The config permissions have been changed!.')
            red('The script will not run unless the config is protected.')
            red('Run "chmod 600 ' + str(userConfigFile) +'" to stop this error.')
            sleep(3)
            quit()
        
        while True:
            if verbose or debug is True:
                pass
            else:
                clear()
            badValueCount = 0
            badValues = []
            config.read(userConfigFile)
            requiredInput = config['Required']
            optionalInput = config['Optional']
            color('stage 1: begin','green')
            for key in requiredInput: # Checks the config input for errors.
                if config['Required'][key] == defaultConfig['Required'][key]:
                    badValues.append(str(key + ': ' + config['Required'][key]))
                    badValueCount = badValueCount + 1
            if badValueCount > 0:
                color('\nConfig Warning:','yellow')
                color('The config seems to contain values that will cause the script to fail.','yellow')
                color('Please review the config for errors. Otherwise this may be a bug.','yellow')
                color('If you believe you are experiencing a bug you may skip this part of the config check.','yellow')
                color('\nWould you like to review the config?','green')
                userInputReview1 = input("Enter yes|no: ")
                if userInputReview1.lower() in yesList:
                    pass                                        
                    color('\nEnter the name of your prefered terminal based editor.','green')
                    userInputTerminalEditor1 = input('Enter name: ')
                    if userInputTerminalEditor1.lower() in editorList:
                        pass
                        os.system(str(userInputTerminalEditor1+' '+userConfigFile))
                elif userInputReview1.lower() in noList:
                    pass
                    if config['config validation']['skip stage 1'] in yesList:
                        break                        
                    color('\nWarning:','red')
                    color('you may be experiencing a bug','red')
                    color('You may skip this step and proceed, but the script is likely to fail.','red')
                    userInputStage1 = input("Enter yes|no: ")
                    if userInputStage1.lower() in yesList:
                        config['config validation'] = {'skip stage 1':'true'}
                        with open(userConfigFile, 'w') as configfile:
                            config.write(configfile)
                        break
                    elif userInputStage1.lower() in noList:
                        quit()
                    else:
                        color('Invalid:','red')
                        sleep(.5)
                else:
                    color('Invalid','red')
                    sleep(.5)


            elif badValueCount is 0:
                break

        def mysqlVars():

            global host
            global user
            global database
            global password
            global auth_plugin

            host = config['Required']['host'].replace("'",'')
            user = config['Required']['user'].replace("'",'')
            database = config['Required']['database'].replace("'",'')
            password = config['Required']['password'].replace("'",'')
            auth_plugin = config['Optional']['auth_plugin'].replace("'",'')

            return host
            return user
            return database
            return password
            return auth_plugin

        mysqlVars()
        
        
    clear()
    #print('Hello!') # Friendly greeting.
    print('Thank you for using backupDB!')
    if loopCount is 0 and configExist is False:
        input('Press enter to begin: ')
    if configExist is True: # if config file is found.
       
        # Fun verbose file is found:
        if verbose is True: # verbose about the config file.
            green('\nVerbose:')
            green('Config file exists!', 0)
            green('Where is it?', .1)
            green('"' + userConfigFile + '"',)
       
        # Boring verbose file is found:
        elif debug is True and verbose is False: # boring verbose about the config file.
            print('Simple verbose:')
            print('Config file exists:',configExist)
            print('config file location:', userConfigFile)

        configCheck()
        mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin=auth_plugin
            )
        #sleep(1)
        break

        
    elif configExist is False: # if config is not found.
        color('creating config file...','green')
        sleep(.5)
        loopCount = loopCount + 1
        createConfigFile()
        # Fun verbose file is not found
        if verbose is True: # verbose about the config file.
            green('\nVerbose:')           
            red('Config file does not exist!')
            green('Creating config...')
            green('\n###NOTICE###',.1)
            green('The config file has been created with default values.')
            green('This script will not run with default values.')
            green('The config is located at '+ str(userConfigFile))
            
        
        # Boring verbose file is not found
        elif debug is True: # boring verbose about the config file.
            print('Simple verbose:')
            print('Does config file exist?:',configExist)
            print('config file location:', userConfigFile)
            print('Config file has been created with default values.')
            print('The script will not run with default values.')
            print('The config is located at ~/.backupDB.ini')
                        
            
    sleep(.25)
    

