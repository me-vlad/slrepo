%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define pkgname urwid

Summary: Console UI Library for Python
Name: python-urwid
Version: 0.9.9.1
Release: 1%{?dist}
License: LGPL
Group: Development/Libraries
URL: http://excess.org/urwid/
Source0: http://excess.org/urwid/%{pkgname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel >= 2.1 
BuildRequires: python-setuptools
Requires: python >= 2.1
Obsoletes: urwid < %{version}-%{release}
Provides: urwid = %{version}-%{release}

%description
Urwid is a Python library for making text console applications. It has
many features including fluid interface resizing, support for UTF-8 and CJK
encodings, standard and custom text layout modes, simple markup for setting
text attributes, and a powerful, dynamic list box that handles a mix of
widget types. It is flexible, modular, and leaves the developer in control.

%prep
%setup -n %{pkgname}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root="%{buildroot}" --prefix="%{_prefix}"

%{__install} -d -m0755 examples/
%{__install} -p -m0755 {browse,calc,dialog,edit,fib,graph,tour}.py examples/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc reference.html tutorial.html examples/
%{python_sitearch}/%{pkgname}/
%{python_sitearch}/%{pkgname}-0.9.9-py2.4.egg-info/

%changelog
* Mon Apr 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 0.9.9.1-1
- Update to 0.9.9.1

* Mon Jan 18 2010 Vlad V. Teterya <vlad@server-labs.ua> - 0.9.9-1
- Initial build for EL5
