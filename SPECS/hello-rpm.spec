Name:           hello-rpm
Version:        0.0.1
Release:        1%{?dist}
Summary:        a simple bash script that prints "hello rpm dev"
BuildArch:      noarch

License:        GPL
Source0:        %{name}-%{version}.tar.gz

Requires:       bash

%description
A demo RPM build

%prep
%autosetup

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp %{name}.sh $RPM_BUILD_ROOT/%{_bindir}

%files
%{_bindir}/%{name}.sh

%changelog
* Thu Dec 21 2023 Joshua Mack <mackncheesiest@gmail.com>
- First version being packaged
