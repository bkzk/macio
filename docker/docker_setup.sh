#/bin/sh

echo "Building docker image .."
echo

docker build --tag macio:v1.0 .

echo
echo "GET YOUR API KEY and run: export MIO_APIKEY=<YOUR_API_KEY>"
echo ".. or add it to your .bashrc"
echo 
echo "RUN this temporary alias or add it to your ~/.bashrc"
echo 'alias macio="docker run --rm -e MIO_APIKEY --name macio macio:v1.0"'
echo
echo "DO NOT forget to run: source ~/.bashrc" 
echo
echo "Try it: macio -h 44:38:39:ff:ef:57"
