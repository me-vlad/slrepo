%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           gitosis
Version:        0.2
Release:        8.20090916git%{?dist}
Summary:        Git repository hosting application

Group:          Applications/System
License:        GPL+
URL:            http://eagain.net/gitweb/?p=gitosis.git;a=summary
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# $ git clone --bare git://eagain.net/gitosis.git gitosis
# $ cd gitosis
# $ git archive --format=tar --prefix=gitosis-0.2/ dedb3dc63f413ed6eeba8082b7e93ad136b16d0d | gzip > ../gitosis-0.2.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        README.fedora
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires(pre):  shadow-utils
Requires:       python-setuptools
Requires:       openssh-clients
Requires:       git

%description
Gitosis aims to make hosting git repos easier and safer. It manages
multiple repositories under one user account, using SSH keys to identify
users. End users do not need shell accounts on the server, they will talk
to one shared account that will not let them run arbitrary commands.

%prep
%setup -q -n %{name}-%{version}

# add PATH to post-update hook script, 
# change git-update-server-info command to avoid "command not found" errors
sed -i -e "2s|^|PATH=\"/usr/bin:/usr/sbin:/bin:/sbin\"\n|" \
   -e "s|git-update-server-info|git update-server-info|" \
   gitosis/templates/admin/hooks/post-update

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d -m 0755 %{buildroot}%{_localstatedir}/lib/gitosis
cp %{SOURCE1} .
 
%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add "gitosis" user per http://fedoraproject.org/wiki/Packaging/UsersAndGroups
getent group gitosis >/dev/null || groupadd -r gitosis
getent passwd gitosis >/dev/null || \
useradd -r -g gitosis -d %{_localstatedir}/lib/gitosis -s /bin/sh \
-c "git repository hosting" gitosis
exit 0

%files
%defattr(-,root,root,-)
%doc COPYING example.conf README.fedora README.rst TODO.rst gitweb.conf lighttpd-gitweb.conf
%{_bindir}/gitosis-init
%{_bindir}/gitosis-run-hook
%{_bindir}/gitosis-serve
%{python_sitelib}/*
%dir %attr(0755,gitosis,gitosis) %{_localstatedir}/lib/gitosis

%changelog
* Wed Mar 9 2011 Vlad V. Teterya <vlad@server-labs.ua> 0.2-8.20090916git
- minor fixes in post-update hook script

* Mon Mar 7 2011 Vlad V. Teterya <vlad@server-labs.ua> 0.2-7.20090916git
- update to 20090916git

* Tue Sep  2 2008 John A. Khvatov <ivaxer@fedoraproject.org> 0.2-6.20080825git
- upstream update for compatibility with git 1.6.

* Wed Aug 13 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-5.20080730git
- Changed license tag GPL+
- Wrote Source URL comment
- Moved README.fedora in Source1
- Fixed requires
- Added /var/lib/gitosis

* Thu Aug 7 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-4.20080730git
- Created README.fedora
- Added creation 'gitosis' user

* Tue Aug 5 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-1.20080730git
- Initial release
