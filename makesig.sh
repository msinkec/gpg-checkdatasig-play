#!/bin/sh

gpg -b --default-key AF73C8F7B546F94B39317588BC4509E6210D4B78 testmsg 
gpg -vv --verify testmsg.sig testmsg

