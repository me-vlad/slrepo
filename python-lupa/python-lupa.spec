%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pkgname lupa

Summary:	Python wrapper around LuaJIT
Name:		python-lupa
Version:	0.19
Release:	1%{?dist}
License:	MIT
Group:		Development/Languages
URL:		http://pypi.python.org/pypi/%{pkgname}
Source:		http://pypi.python.org/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRequires:	python-devel, python-setuptools-devel, luajit-devel >= 2.0
Requires:   python >= 2.4
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Lupa integrates the LuaJIT2 runtime into CPython. It is a partial rewrite
of LunaticPython in Cython with some additional features such as proper
coroutine support.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES.rst LICENSE.txt README.rst
%{python_sitelib}/%{pkgname}/
%if 0%{?rhel} >= 6
%{python_sitelib}/%{pkgname}-%{version}-py2.6.egg-info
%endif
%if 0%{?fedora} >= 14
%{python_sitelib}/%{pkgname}-%{version}-py2.7.egg-info
%endif


%changelog
* Sun Apr 3 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.19-1
- Update to 0.19

* Sat Jan 22 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.18-1
- Initial build for EL5
