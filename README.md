## Generate key

```sh
gpg --full-gen-key --expert
```

Make sure to use `secp256k1`.

## Export public key

```sh
gpg --output pubkey.gpg --export <KEY_ID>
```

Replace <KEY_ID> with the Key ID of the key you're interested in.
You can find it using the following command:
```sh
gpg --list-keys --with-fingerprint
```

## Sign message

Edit the key ID in `makesig.sh` and run

```sh
./makesig.sh
```

This will sign the message inside the file `testmsg` and create a signature `testmsg.sig`.

## Parse signature

Run:

```
./parsesig.py
```

This will print the data you need for the verification using sCrypt:

```
pubkey.gpg loaded, key ID AF73C8F7B546F94B39317588BC4509E6210D4B78

Public key point coordinates:
x = 48421684640566418104679532805542050894296452248858999768503364580534732096841
y = 27832515582888013475460648727797934257300201948678282835754427898215825506626

Message: b'Hello world!\n'
Message hex: 48656c6c6f20776f726c64210a04001308001d162104af73c8f7b546f94b39317588bc4509e6210d4b7805026453693704ff00000023

Sig:
r: 64359296802826103123327210017080540130282890114880640962625134547151700407256
s: 8795100933587794005356181940782496292717652651227485898667966611241902738847

Signature validity on message: True
```

