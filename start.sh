cd api
touch database.db
cd ..
python -m init_db
sleep 1
python -m api.app
