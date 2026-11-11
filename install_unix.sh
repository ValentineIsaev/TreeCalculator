#!/bin/bash

if command -v psql >/dev/null 2>&1; then
	echo "PostgreSQL установлен"
else
	echo "Установка PostgreSQL"
	sudo apt install -y postgresql
fi

echo "Настройка базы данных"
DB_EXIST=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='calculator'")

if [ "$DB_EXIST" = "1" ]; then
	echo "База данных Calculator существует"
else
	echo "Создание базы данных"
	sudo -u postgres psql -c "CREATE DATABASE calculator;"
fi

USER_EXIST=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='calculate'")
if [ "$USER_EXIST" = "1" ]; then
	echo "Пользователь Calculate существует"
else
	echo "Создание пользователя Calculate"
	sudo -u postgres psql -c "CREATE USER calculate WITH PASSWORD '13119';"
fi

sudo -u postgres psql -c "ALTER DATABASE calculator OWNER TO calculate;"

echo "База данных настроена"

echo "Настройка приложения"

cd MainBackend/backend || exit 1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd ../../TreeBackend/treebase || exit 1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

#deactivate
echo "Создание схем"

#cd ./TreeBackend/treebas || exit 1
ls
export PYTHONPATH="$(pwd)/.."

cd postgres/alembic || exit 1
alembic upgrade 803e7b79f3ad

echo "Схемы созданы"

sudo -u postgres psql -d calculator -c "
INSERT INTO soils (name, soil_c) 
VALUES ('Чернозём', 40000),
('Суглинок', 45000),
('Глина', 60000),
('Подзол', 38000);
INSERT INTO trees (name, height, weight, center_gravity_height, diameter, c_d, crown_square, max_stress, type_root, info, is_new) 
VALUES
('Дуб', 4.5, 1800, 2.0, 0.12, 0.45, 8.0, 100000000, 'стержневая', 'Дуб — медленнорастущее дерево. В 7 лет имеет компактную крону и развитую стержневую корневую систему.', false);
INSERT INTO roots (tree_id, soil_id, a, b) VALUES
(1, 1, 2.2, 2.2), (1, 2, 2.0, 2.0), (1, 3, 2.6, 2.6), (1, 4, 1.8, 1.8);"

echo "Данные добавлены в базу данных"
