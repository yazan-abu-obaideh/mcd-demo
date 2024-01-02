echo "working direction should be the same as the script directory..."
rm -r ./dist/
mkdir -p dist/
npx webpack
