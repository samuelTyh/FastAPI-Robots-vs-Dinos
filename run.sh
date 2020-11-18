
python -m unittest tests.test_game_functions
docker build -f Dockerfile -t "fastapi-bundle" .
docker run -d --name fastapi-service -p "80:80" "fastapi-bundle"