Name:           mod_rpaf
Version:        0.6
Release:        3%{?dist}
Summary:        Reverse proxy add forward module for Apache

Group:          System Environment/Daemons
License:        ASL 1.0
URL:            http://stderr.net/apache/rpaf/
Source0:        http://stderr.net/apache/rpaf/download/%{name}-%{version}.tar.gz
Source1:        rpaf.conf
Patch0:         mod_rpaf-0.6-Make.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
Requires:       httpd

%description
Reverse proxy add forward module for Apache


%prep
%setup -q
%patch0 -p1 -b .makefile


%build
%__make rpaf-2.0


%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir -pm 755 $RPM_BUILD_ROOT%{_libdir}/httpd/modules
%__install -m 755 .libs/mod_rpaf-2.0.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
%__mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
%__install -m 644 %_sourcedir/rpaf.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/rpaf.conf


%clean
%__rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README CHANGES
%{_libdir}/httpd/modules/mod_rpaf-2.0.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/rpaf.conf


%changelog
* Wed Sep 21 2009 Vlad V. Teterya <vlad@server-labs.ua> 0.6-3
- Add apache config file
- Sanitize spec file 
