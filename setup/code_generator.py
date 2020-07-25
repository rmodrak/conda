#!/usr/bin/env python

from __future__ import print_function

import os, re, sys

if sys.version_info[:2] <= (2, 7):
    input = raw_input


ACTIVATE = """#!/bin/bash

if [ "${BASH_SOURCE[0]}" == "${0}" ];
then
    echo
    echo "This script must be sourced"
    echo
    exit
fi

__conda_setup="$('$CONDA_PATH/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "$CONDA_PATH/etc/profile.d/conda.sh" ]; then
        . "$CONDA_PATH/etc/profile.d/conda.sh"
    else
        export PATH="$CONDA_PATH/bin:$PATH"
    fi
fi
unset __conda_setup
"""


DEACTIVATE = """#!/bin/bash

if [ "${BASH_SOURCE[0]}" == "${0}" ];
then
    echo \
"
This script must be sourced
"
    exit
fi

conda deactivate
remove-path "$CONDA_PATH/bin"
remove-path "$CONDA_PATH/condabin"
unset conda
"""


PROMPT2 = """
Miniconda2 will be activated from this location:
%s

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

"""


PROMPT3 = """
Miniconda3 will be activated from this location:
%s

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

"""




if __name__=='__main__':

    home = os.getenv('HOME')


    #
    # write miniconda2 scripts
    #

    default_path = os.path.join(home, 'virtual', 'miniconda2')
    print(PROMPT2 % default_path)
    input_path = input('>>> ')

    install_path = input_path
    if install_path=='':
        install_path = default_path

    with open('activate-miniconda2', 'w') as file:
        SOURCE = re.sub('\$CONDA_PATH',install_path, ACTIVATE)
        file.write(SOURCE)

    with open('deactivate-miniconda2', 'w') as file:
        SOURCE = re.sub('\$CONDA_PATH',install_path, DEACTIVATE)
        file.write(SOURCE)
    

    #
    # write miniconda3 scripts
    #

    default_path = os.path.join(home, 'virtual', 'miniconda3')
    print(PROMPT3 % default_path)
    input_path = input('>>> ')

    if input_path!='':
        install_path = input_path
    else:
        install_path = default_path

    with open('activate-miniconda3', 'w') as file:
        SOURCE = re.sub('\$CONDA_PATH',install_path, ACTIVATE)
        file.write(SOURCE)

    with open('deactivate-miniconda3', 'w') as file:
        SOURCE = re.sub('\$CONDA_PATH',install_path, DEACTIVATE)
        file.write(SOURCE)

