Name:           duply
Version:        1.5.5
Release:        1%{?dist}
Summary:        Wrapper for duplicity
Group:          Applications/Archiving
License:        GPLv2
URL:            http://duply.net/
Source0:        http://downloads.sourceforge.net/ftplicity/%{name}_%{version}.tgz
Source1:        %{name}.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       duplicity


%description
duply deals as a wrapper for the mighty duplicity magic. It simplifies
running duplicity with cron or on command line by:

- keeping recurring settings in profiles per backup job
- enabling batch operations e.g. backup_verify_purge
- executing pre/post scripts
- precondition checking for flawless duplicity operation

Since version 1.5.0 all duplicity backends are supported. Hence the
name changed from ftplicity to duply.


%prep
%setup -q -n %{name}_%{version}
iconv -f iso-8859-1 -t utf-8 %{name} > %{name}.tmp
mv %{name}{.tmp,}


%build


%install
rm -rf %{buildroot}
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/%{name}.1
gzip -9 %{buildroot}%{_mandir}/man1/%{name}.1


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc gpl-2.0.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_sysconfdir}/%{name}


%changelog
* Wed May 4 2011 Vlad V. Teterya <vlad@server-labs.ua> - 1.5.5-1
- Initial build
