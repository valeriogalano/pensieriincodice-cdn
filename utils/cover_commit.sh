#!/bin/bash

clear && read -p "PIC Number: " NUMBER
echo ""
git pull
echo ""
git add ../public/covers/PIC$NUMBER.png && git commit -m "Added upscaled PIC$NUMBER's cover"
echo ""
git push
