cd ~/klipper
git init
cd ~
ssh-keygen -t ed25519 -C "collapsednut@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
cd ~/klipper
git init
git remote add origin git@github.com:53Aries/Q2-Klipper.git
git add .
git commit -m "Initial commit of klipper files"
git config --global user.email "collapsednut@gmail.com"
git config --global user.name "53Aries"
git commit -m "Initial commit of klipper files"
git branch -M main
git push -u origin main
git remote add upstream https://github.com/Klipper3d/klipper.git
git fetch upstream
git grep -n "c_sensor" klippy/extras
cd ~
ssh -T git@github.com
cd /home/mks
cd ~/home/mks
git init
git remote add origin git@github.com:53Aries/Q2-Firmware.git
git add .
git commit -m "Initial commit of Q2-Firmware contents"
git branch -M main
git push -u origin main
systemctl status klipper
dmesg | grep -Ei 'dsi|drm|panel|mipi'
cat /sys/class/graphics/fb0/modes
cat /sys/class/graphics/fb0/name
ls /sys/class/drm/
grep -i touch /proc/bus/input/devices
sudo cat /sys/kernel/debug/dri/0/state
sudo lsusb -t
sudo reboot
