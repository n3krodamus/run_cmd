#! /usr/bin/env bash

# Borrado de temporales
rm -f tmp/*
rm -f logs/*

# Vaciado de conf
for i in failed.txt processed.txt pending.txt
do
    echo > conf/$i
done

