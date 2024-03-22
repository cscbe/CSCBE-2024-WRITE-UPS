
cp ../Challenge/Public/Challenge-OutOfBounds_v1.0.4.x86_64.tar.lzma game.64.tar.lzma

lzma -cd game.64.tar.lzma | tar xvf -
mv Challenge-OutOfBounds_v1.0.4.x86_64 game.64

wget -nc "https://github.com/bruvzg/gdsdecomp/releases/download/v0.6.2/GDRE_tools-v0.6.2-linux.zip"
unzip -n "GDRE_tools-v0.6.2-linux.zip"
chmod +x gdre_tools.x86_64

./gdre_tools.x86_64 --headless --recover=game.64 --output-dir=recover/

sha256sum game.64
