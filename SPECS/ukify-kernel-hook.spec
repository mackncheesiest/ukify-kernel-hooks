Name:           ukify-kernel-hooks
Version:        0.0.3
Release:        1%{?dist}
Summary:        Some hooks to build signed UKIs and maintain systemd-boot
BuildArch:      noarch

License:        GPL

%description
Provides two hooks:
1. Runs after files in /boot are modified and ensures the latest UKI is provided in /boot/efi/EFI/Linux for systemd-boot to use
2. Runs after /usr/lib/systemd/boot/efi/systemd-bootx64.efi is modified and ensures that a systemd-bootx64.efi.signed binary is provided

%transfiletriggerin -- /usr/lib/systemd/boot/efi
echo "I think systemd-bootx64.efi was modified. Signing and updating with bootctl"
sbsign \
  --key="/etc/EFI/sbkeys/my_keys/db/DB.key" \
  --cert="/etc/EFI/sbkeys/my_keys/db/DB.pem" \
  /usr/lib/systemd/boot/efi/systemd-bootx64.efi
bootctl update \
  --no-variables \
  --efi-boot-option-description="Systemd Boot"
if [ $? -eq 1 ]; then
  echo "oops...systemd-boot was already up to date"
fi

%transfiletriggerin -- /boot
LATEST_INITRAMFS=`ls -t /boot/initramfs-* | head -n 1`
LATEST_KERNEL=`ls -t /boot/vmlinuz-* | head -n 1`
VERSION=`echo ${LATEST_INITRAMFS} | grep -Eo "[0-9]\.[0-9]\.[0-9]-[0-9]+"`
OUTPUT_FILENAME="UKI-${VERSION}.efi"
echo "I think the initramfs or kernel were modified. Building UKI for ${LATEST_INITRAMFS}, ${LATEST_KERNEL} in /boot/efi/EFI/Linux/${OUTPUT_FILENAME}"
/usr/lib/systemd/ukify build \
  --linux="${LATEST_KERNEL}" \
  --initrd="${LATEST_INITRAMFS}" \
  --cmdline="root=UUID=81fce07c-cbcd-48c5-8330-9ae376f312f3 ro rootflags=subvol=root video=eDP-1:2256x1504 amdgpu.sg_display=0 modprobe.blacklist=nouveau rd.driver.blacklist=nouveau rhgb" \
  --stub="/usr/lib/systemd/boot/efi/linuxx64.efi.stub" \
  --secureboot-private-key="/etc/EFI/sbkeys/my_keys/db/DB.key" \
  --secureboot-certificate="/etc/EFI/sbkeys/my_keys/db/DB.pem" \
  --sign-kernel \
  --signtool=sbsign \
  --output=/boot/efi/EFI/Linux/${OUTPUT_FILENAME}

%files

%changelog
* Thu Dec 21 2023 Joshua Mack <mackncheesiest@gmail.com>
- Initial spec
