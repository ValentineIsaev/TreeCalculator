#!/bin/bash

echo "Директория сборки: " $1

if [ ! -d "$1" ]; then
    echo "Создание директории"
    mkdir "$1"

cp ./backend "$1"

cp ./frontend/* "$1"/backend/frontend