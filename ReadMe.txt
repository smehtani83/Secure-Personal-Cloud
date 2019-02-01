Uncompress the MyPackage.tar.gz in your home directory, Copy the complete structure inside MyPackage folder to the home folder and then run the command:
bash ~/install.sh

1)spc login: User needs to do this before going forward with anything else. Requires Username and Password
2)spc register: To be done after login. For first time user-initialize Private Key, Encryption Schema, Sharing key. For old user: enter previous Private key, encryption schema and sharing key to authenticate "
3)spc observe: Go into the directory that you want to sync and then use this command.
4)spc sync: To be done after observe. Used to sync the observed directory and server
5)spc rec <file_name> user_A : To be used by user to receive <file_name> from user_A
6)spc send <file_name> user_B : To be used to send <file_name> to user_B
7)spc version:view version of SPC
8)spc server: prints public info about server
9)spc status: print prints sync status of each of the files on server and observed directory
10)spc en-de list:show all supported encryption schemas
11)spc en-de update:update encryption schema, private key and sharing key
12)spc en-de show:shows present encryption schema 
