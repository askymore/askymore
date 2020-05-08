
dd if=/dev/zero of=/root/swapfile bs=1M count=8096
mkswap /root/swapfile
swapon /root/swapfile
apt-get update
apt-get -y install build-essential asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake libtool autopoint
useradd kevin  -m
passwd kevin


cd /home/kevin
git clone https://git.openwrt.org/openwrt/openwrt.git
git fetch --tags
git tag -l
git checkout v19.07.2
cd openwrt
./scripts/feeds update -a
./scripts/feeds install -a
wget  https://raw.githubusercontent.com/askymore/askymore/master/xm1.config -O .config
make defconfig
make download
nohup  make -j5  V=s &
