%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pkgname redis

Summary:	Python interface to the Redis key-value store
Name:		python-redis
Version:	2.2.4
Release:	1%{?dist}
Source0:	https://github.com/downloads/andymccurdy/redis-py/%{pkgname}-%{version}.tar.gz
License:	MIT
Group:		Development/Languages
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://github.com/andymccurdy/redis-py
Requires:	python >= 2.4
BuildRequires: python >= 2.4

%description
Python interface to the Redis key-value store.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --no-compile --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES LICENSE README.md
%{python_sitelib}/%{pkgname}
%{python_sitelib}/%{pkgname}-%{version}-py2.4.egg-info/

%changelog
* Mon Apr 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.2.4-1
- Update to release 2.2.4

* Fri Jan 21 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.2.2-1
- Update to release 2.2.2

* Thu Oct 21 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.1-1.20101020git
- Update to latest git (20101020)

* Fri Oct 15 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.1-1.20101008git
- Update to latest git (20101008)

* Wed Sep 1 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.1-1.20100905git
- major version bump (2.0.1)
- Update to latest git (20100905)

* Wed Sep 1 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1.20100819git
- Update to latest git (20100819)

* Mon Jul 12 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1.20100628git
- major version bump (2.0.0)
- Update to latest git (20100628)

* Fri Jun 11 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100601git
- Update to latest git (20100601)

* Wed May 26 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100523git
- Update to latest git (20100523)

* Mon May 17 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100510git
- Update to latest git (20100510)

* Mon May 3 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100503git
- Update to latest git (20100503)

* Mon Apr 26 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100420git
- Update to latest git (20100420) - added support for APPEND and SUBSTR commands

* Tue Apr 20 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100419git
- Update to latest git (20100419)

* Tue Apr 6 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.36-1.20100406git
- Update to 1.36 from git

* Sun Mar 7 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.34.1-1
- Initial build for EL5
