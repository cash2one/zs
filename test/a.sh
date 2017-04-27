#!/bin/bash
#if [ $# -ne 0 ]
#then
#[[ $1 =~ "AAA=" ]] || (echo "AAA is wrong" ; exit)
#return -1
#
#[[ $2 =~ "BBB=" ]] || (echo "BBB is wrong" ; exit)
#fi

if [ $# -ne 0 ]
then
    if [[ $1 =~ ^AAA= ]] ; then :
    else
    echo "AAA is wrong" ; return -1
    fi

    if [[ $2 =~ ^BBB= ]] ; then :
    else
    echo "BBB is wrong" ; return -1
    fi
fi

echo ---

echo 1

