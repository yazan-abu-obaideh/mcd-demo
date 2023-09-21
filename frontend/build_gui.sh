cd web
./bundle_all.sh
cd ..

export GUI_DIR_TARGET=gui/src/resources/target
rm -r $GUI_DIR_TARGET
mkdir -p $GUI_DIR_TARGET
cp -r web/dist/* $GUI_DIR_TARGET
rm -r $GUI_DIR_TARGET/web-target
cp -r static/gui-target $GUI_DIR_TARGET
