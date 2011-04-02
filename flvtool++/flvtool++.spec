Name: flvtool++
Version: 1.2.1
Release: 1%{?dist}
Summary: flvtool++ is a tool for hinting and manipulating the metadata of Macromedia Flash Video (FLV) files

Group: Applications/Multimedia
License: BSD 
Url: http://mirror.facebook.net/facebook/flvtool++/
Source: %name-%version.tar

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: scons gcc gcc-c++ boost-devel

%description
flvtool++ is a tool for hinting and manipulating the metadata of
Macromedia Flash Video (FLV) files. It was originally created for
Facebook's Video project (http://facebook.com/video/) for fast video
hinting. It is loosely based on the Ruby FLVTool2, but is written in
C++ for performance reasons.

%prep
%setup -q

%build
scons

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -Dp -m0755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGELOG LICENSE README
%{_bindir}/%{name}

%changelog
* Fri Nov 12 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.2.1-1
- initial build for EL5

