#!/bin/bash

HEAD='^    ### BEGIN GENERATED CONTENT$'
TAIL='^    ### END GENERATED CONTENT$'

# Backup and replace in place
# Keep the command on two lines !!!!
sed -i".bak" -e "/$HEAD/,/$TAIL/{ /$HEAD/{p; r $1
        }; /$TAIL/p; d }"  $2


