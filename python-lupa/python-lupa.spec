%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pkgname lupa

Summary:	Python wrapper around LuaJIT
Name:		python-lupa
Version:	0.18
Release:	1%{?dist}
License:	MIT
Group:		Development/Languages
URL:		http://pypi.python.org/pypi/%{pkgname}
Source:		http://pypi.python.org/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz
Patch0:		python-lupa-0.18-setup.patch
BuildRequires:	python-devel, python-setuptools-devel, luajit-devel >= 2.0
Requires:   python >= 2.4
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Lupa integrates the LuaJIT2 runtime into CPython. It is a partial rewrite
of LunaticPython in Cython with some additional features such as proper
coroutine support.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .setup

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt
%{python_sitelib}/%{pkgname}/


%changelog
* Sat Jan 22 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.18-1
- Initial build for EL5
