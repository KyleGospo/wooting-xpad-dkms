%global debug_package %{nil}
%global dkms_name wooting-xpad
%global kernel_version 5.18

Name:       %{dkms_name}-dkms
Version:    %{kernel_version}.{{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    xpad driver patched for Wooting keyboard support
License:    GPLv2
URL:        https://github.com/KyleGospo/wooting-xpad-dkms
BuildArch:  noarch

# Source file:
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/input/joystick/xpad.c
Source0:    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/input/joystick/xpad.c?h=v%{kernel_version}#/xpad.c
Source1:    Makefile
Source2:    dkms.conf
Source3:    README.md
Source4:    LICENSE

# Wooting Keyboard patch:
Patch0:     wooting.patch

Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms
Requires:   wooting-udev-rules

%description
xpad driver from kernel %{kernel_version} patched with support for Wooting analog keyboards

%prep
%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .
%patch0 -p0

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{dkms_name}-%{version}

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}