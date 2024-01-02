echo "working direction should be the same as the script directory..."
source ./../../venv/bin/activate
python3 ../static/html_builders.py
rm -r ./dist/
mkdir -p dist/
cp -r ../static/web-target/ dist/
cp -r ../static/assets/ dist/
cp -r ../static/css/ dist/
npx webpack
