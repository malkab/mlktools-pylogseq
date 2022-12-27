- #Procesar Encriptación: GPG, PGP, GNUPG2
  id:: 633a8109-88ec-4ad9-b663-f6c7ba4a794a
  - Installation of Keys
    - In most cases is just a matter of copying the **~/.gnupg** folder. Check available keys with commands explained below.
    - Owner of folder **.gnupg** and its contents must be the user. Folder permissions must be 700, and permissions for file **gpg.conf** must be 600.
  - Usage
    collapsed:: true
    - **IMPORTANT!!!** When creating a new key, make an export of public and private keys and store them somewhere (a USB key or hard drive at home). DON'T FORGET TO STORE THE PASSWORD ALONG WITH IT, DON'T STORE THE PASSWORD UNDER THE SAME FILE THAT HAS BEEN ENCRYPTED WITH IT.  AND ALWAYS STORE THE GPG FILES UNDER A GIT REPO TO RECOVER POTENTIALLY CORRUPTED FILES!!!
    - ```shell
      # List the keys in the public key ring:
      gpg --list-keys
      
      # List the Keys in the Secret Key Ring:
      gpg --list-secret-keys
      
      # To generate a short list of numbers that you can use via an
      # alternative method to verify a public key, use:
      gpg --fingerprint > fingerprint
      
      # Create a key
      gpg --gen-key
      
      # generally you can select the defaults.
      
      # Export a Public Key
      gpg --export -a "User Name" > public.key
      
      # This will create a file called public.key with the ASCII
      # representation of the public key for User Name.
      
      # Export a Private Key
      gpg --export-secret-key -a "User Name" > private.key
      
      # This will create a file called private.key with the ASCII
      # representation of the private key for User Name. It's pretty much
      # like exporting a public key, but you have to override some
      # default protections.
      
      # Import a Public Key
      gpg --import public.key
      
      # This adds the public key in the file "public.key" to your
      # public key ring.
      
      # Import a Private Key
      gpg --allow-secret-key-import --import private.key
      
      # This adds the private key in the file "private.key" to your
      # private key ring.
      
      # Delete a Public Key
      gpg --delete-key "User Name"
      
      # This removes the public key from your public key ring.
      # NOTE! If there is a private key on your private key ring
      # associated with this public key, you will get an error! You
      # must delete your private key for this key pair from your
      # private key ring first.
      
      # Delete an Private Key
      gpg --delete-secret-key "User Name"
      
      # This deletes the secret key from your secret key ring.
      ```
    -
  - Trusting Keys
    collapsed:: true
    - Keys can be set to be trust at different levels, so it won't ask for pass phrase when using them
    - ```shell
      gpg --edit-key whatever@dom.com
      
      gpg> trust
      
      # select and option and...
      
      gpg> quit
      ```
  - File Encryption and Decryption
    - To encrypt a file:
      ```shell
      # Check first available keys
      gpg --list-keys
      gpg --list-secret-keys
      
      # To generate a short list of numbers that you can use via an alternative method to verify a public key, use:
      gpg --fingerprint > fingerprint
      
      This creates the file fingerprint with your fingerprint info.
      
      # To send it to another person
      gpg -e -u "Sender User Name" -r "Receiver User Name" somefile
      
      # To encrypt for yourself
      gpg -e -u "Key" -r "Key" somefile
      gpg -e -u "some.email.here@gmail.com" \
      	-r "some.email.here@gmail.com" afile
      ```
    - **-u** is the secret key to use for encrypting, **-r** is the public key of the person recieving the message. They can be the same (encrypting for yourself).
    - This should create a **.gpg** file that contains the encrypted data. I think you specify the senders username so that the recipient can verify that the contents are from that person (using the fingerprint?). NOTE!: the original file is not removed, you end up with two files, so if you want to have only the encrypted file in existance, you probably have to delete the original file yourself.
    - To decrypt data, use:
      ```shell
      gpg -d mydata.tar.gpg >> out
      ```
  - Renewing Expired Keys
    collapsed:: true
    - Follow these steps:
      ```shell
      # Check for the expired key
      gpg --list-keys
      
      # Edit the key, this lands on a kind of console
      gpg --edit-key [keyname]
      
      # In the gpg console
      list
      
      # Select the key by number
      key 1
      
      # Cancel expiration
      expire
      
      # Save
      save
      ```
  - #procesar Más para procesar
    - ```txt
      GPG and PGP and GNUPG2
      ======================
      __TAGS:__ gpg, pgp, gnupg, encryption, open, source
      
      
      Usage
      -----
      __TAGS:__ gpg, pgp, gnupg
      
      List the Keys in the Public Key Ring:
      
      
      
      This creates the file fingerprint with your fingerprint info.
      
      Create a key:
      
      ```Shell
      gpg --gen-key
      ```
      
      Generally you can select the defaults.
      
      Export a Public Key:
      
      ```
      gpg --export -a "User Name" > public.key
      ```
      
      This will create a file called public.key with the ASCII representation of the public key for User Name.
      
      Export a Private Key:
      
      ```Shell
      gpg --export-secret-key -a "User Name" > private.key
      ```
      
      This will create a file called private.key with the ASCII representation of the private key for User Name. It's pretty much like exporting a public key, but you have to override some default protections.
      
      Import a Public Key:
      
      ```Shell
      gpg --import public.key
      ```
      
      This adds the public key in the file "public.key" to your public key ring.
      
      Import a Private Key:
      
      ```Shell
      gpg --allow-secret-key-import --import private.key
      ```
      
      This adds the private key in the file "private.key" to your private key ring.
      
      Delete a Public Key:
      
      ```Shell
      gpg --delete-key "User Name"
      ```
      
      This removes the public key from your public key ring. NOTE! If there is a private key on your private key ring associated with this public key, you will get an error! You must delete your private key for this key pair from your private key ring first.
      
      Delete an Private Key:
      
      ```Shell
      gpg --delete-secret-key "User Name"
      ```
      
      This deletes the secret key from your secret key ring.
      
      
      Data Encryptation
      -----------------
      __TAGS:__ data, encryptation, gnupg, pgp, gpg
      
      To encrypt data, use:
      
      ```Shell
      # To send it to another person
      
      gpg -e -u "Sender User Name" -r "Receiver User Name" somefile
      
      # To encrypt for yourself
      
      gpg -e -u "Key" -r "Key" somefile
      ```
      
      There are some useful options here, such as -u to specify the secret key to be used, and -r to specify the public key of the recipient.
      
      As an example:
      
      ```Shell
      gpg -e -u "Charles Lockhart" -r "A Friend" mydata.tar
      
      gpg -e -u "jp.alcantara@geo-st.com" -r "jp.alcantara@geo-st.com" mydata.md
      ```
      
      This should create a file called "mydata.tar.gpg" that contains the encrypted data. I think you specify the senders username so that the recipient can verify that the contents are from that person (using the fingerprint?). NOTE!: mydata.tar is not removed, you end up with two files, so if you want to have only the encrypted file in existance, you probably have to delete mydata.tar yourself. An interesting side note, I encrypted the preemptive kernel patch, a file of 55,247 bytes, and ended up with an encrypted file of 15,276 bytes.
      
      To decrypt data, use:
      
      ```Shell
      gpg -d mydata.tar.gpg >> out
      ```
      
      If you have multiple secret keys, it'll choose the correct one, or output an error if the correct one doesn't exist. You'll be prompted to enter your passphrase. Afterwards there will exist the file "mydata.tar", and the encrypted "original," mydata.tar.gpg. Ok, so what if you're a paranoid bastard and want to encrypt some of your own files, so nobody can break into your computer and get them? Simply encrypt them using yourself as the recipient.
      
      Sharing Secret Keys
      -------------------
      __TAGS:__ secret, keys, pgp, gpg
      
      NOTE!: the following use cases indicate why the secret-key import/export commands exist, or at least a couple ideas of what you could do with them. HOWEVER, there's some logistics required for sharing that secret-key. How do you get it from one computer to another? I guess encrypting it and sending it by email would probably be ok, but I wouldn't send it unencrypted with email, that'd be DANGEROUS.
      
      Use Case 1: Mentioned above were the commands for exporting and importing secret keys, and I want to explain one reason of why maybe you'd want to do this. Basically if you want one key-pair for all of your computers (assuming you have multiple computers), then this allows you export that key-pair from the original computer and import it to your other computers.
      
      Use Case 2: Mentioned above were the commands for exporting and importing secret keys, and I want to explain one reason of why maybe you'd want to do this. Basically, if you belonged to a group, and wanted to create a single key-pair for that group, one person would create the key-pair, then export the public and private keys, give them to the other members of the group, and they would all import that key-pair. Then a member of the group or someone outside could use the group public key, encrypt the message and/or data, and send it to members of the group, and all of them would be able to access the message and/or data. Basically you could create a simplified system where only one public key was needed to send encrypted stuffs to muliple recipients.
      
      
      
      ```