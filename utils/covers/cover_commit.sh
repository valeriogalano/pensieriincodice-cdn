#!/bin/bash

read -p "PIC Number: " NUMBER
git pull
git add ../../public/covers/PIC$NUMBER.png && git commit -m "Added upscaled PIC$NUMBER's cover"
git push
