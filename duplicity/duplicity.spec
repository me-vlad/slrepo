%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:        Encrypted bandwidth-efficient backup using rsync algorithm
Name:           duplicity
Version:        0.6.13
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/Archiving
URL:            http://www.nongnu.org/duplicity/
Source:         http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.gz
Requires:       python-GnuPGInterface >= 0.3.2, gnupg >= 1.0.6
Requires:       openssh-clients, ncftp >= 3.1.9, rsync, python-boto >= 1.9b
%if 0%{?rhel}%{?fedora} <= 4
Requires:       python-abi = %(%{__python} -c "import sys; print sys.version[:3]")
%endif
BuildRequires:  python-devel >= 2.3, librsync-devel >= 0.9.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Duplicity incrementally backs up files and directory by encrypting
tar-format volumes with GnuPG and uploading them to a remote (or
local) file server. In theory many protocols for connecting to a
file server could be supported; so far ssh/scp, local file access,
rsync, ftp, HSI, WebDAV and Amazon S3 have been written.

Because duplicity uses librsync, the incremental archives are space
efficient and only record the parts of files that have changed since
the last backup. Currently duplicity supports deleted files, full
unix permissions, directories, symbolic links, fifos, device files,
but not hard links.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc CHANGELOG COPYING README
%{_bindir}/rdiffdir
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_mandir}/man1/rdiffdir*
%{python_sitearch}/%{name}*

%changelog
* Wed May 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 0.6.13-1
- Upgrade to 0.6.13

* Thu Dec 09 2010 Robert Scheck <robert@fedoraproject.org> 0.6.11-1
- Upgrade to 0.6.11 (#655870)

* Sun Oct 31 2010 Robert Scheck <robert@fedoraproject.org> 0.6.10-1
- Upgrade to 0.6.10
- Added a patch to avoid ternary conditional operators (#639863)

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 0.6.09-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Robert Scheck <robert@fedoraproject.org> 0.6.09-1
- Upgrade to 0.6.09 (#596018)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.08b-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Mar 28 2010 Robert Scheck <robert@fedoraproject.org> 0.6.08b-1
- Upgrade to 0.6.08b

* Sat Dec 26 2009 Robert Scheck <robert@fedoraproject.org> 0.6.06-1
- Upgrade to 0.6.06 (#550663)

* Sun Sep 27 2009 Robert Scheck <robert@fedoraproject.org> 0.6.05-1
- Upgrade to 0.6.05 (#525940)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Robert Scheck <robert@fedoraproject.org> 0.5.18-1
- Upgrade to 0.5.18

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.5.16-1
- Upgrade to 0.5.16

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> 0.5.15-1
- Upgrade to 0.5.15

* Sat Mar 21 2009 Robert Scheck <robert@fedoraproject.org> 0.5.12-1
- Upgrade to 0.5.12 (#490289)

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.5.06-2
- Rebuild for gcc 4.4 and rpm 4.6

* Sun Jan 25 2009 Robert Scheck <robert@fedoraproject.org> 0.5.06-1
- Upgrade to 0.5.06 (#481489)

* Sun Dec 07 2008 Robert Scheck <robert@fedoraproject.org> 0.5.03-1
- Upgrade to 0.5.03

* Fri Dec 05 2008 Jeremy Katz <katzj@redhat.com> 0.4.12-3
- Rebuild for python 2.6

* Fri Aug 08 2008 Robert Scheck <robert@fedoraproject.org> 0.4.12-2
- Added patch to get scp without username working (#457680)

* Sun Jul 27 2008 Robert Scheck <robert@fedoraproject.org> 0.4.12-1
- Upgrade to 0.4.12

* Sat Jun 28 2008 Robert Scheck <robert@fedoraproject.org> 0.4.11-2
- Added patch for incremental backups using python 2.3 (#453069)

* Mon May 05 2008 Robert Scheck <robert@fedoraproject.org> 0.4.11-1
- Upgrade to 0.4.11 (#440346)

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.4.9-1
- Upgrade to 0.4.9 (#293081, #431467)

* Sat Dec 08 2007 Robert Scheck <robert@fedoraproject.org> 0.4.7-1
- Upgrade to 0.4.7

* Sat Sep 15 2007 Robert Scheck <robert@fedoraproject.org> 0.4.3-1
- Upgrade to 0.4.3 (#265701)
- Updated the license tag according to the guidelines

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 0.4.2-7
- Rebuild

* Wed Dec 20 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-6
- fix broken sftp support by adding --sftp-command (#220316)

* Sun Dec 17 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-5
- own %%{python_sitearch}/%%{name} and not only %%{python_sitearch}

* Sat Dec 16 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-4
- added two small fixing patches (upstream items #4486, #5183)
- many spec file cleanups and try to silence rpmlint a bit more

* Fri Sep 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-3
- don't ghost pyo files

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-2
- Rebuild for FC6

* Tue May 16 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-1
- version bump

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Oct 05 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.4.1-0.fdr.3
- More hints from Fedora QA (ville.skytta@iki.fi)

* Sat Aug 09 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.4.1-0.fdr.2
- Repackaging for Fedora

* Sun Aug 30 2002 Ben Escoto <bescoto@stanford.edu>
- Initial RPM
