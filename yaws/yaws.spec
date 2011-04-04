%define debug_package %{nil}

Summary:	High perfomance webserver written in Erlang
Name:		yaws
Version:	1.89
Release:	1%{?dist}
Group:	    System Environment/Daemons
License:	LGPL
URL:		http://yaws.hyber.org
Source:		%{name}-%{version}.tar.gz
BuildRequires:	erlang
BuildRequires: latex2html, tetex-latex, tetex-dvips
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Yaws is a high perfomance 1.1 webserver written in Erlang particularly well suited for 
dynamic-content webapplications.

%prep
%setup -q 

%build
export DESTDIR=%{buildroot}
%configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
%{__make} %{?_smp_mflags}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=%{buildroot} make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/yaws.pdf
%{_bindir}/%{name}
%config %{_sysconfdir}/init.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-cert.pem
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-key.pem
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_libdir}/%{name}/ebin
%{_libdir}/%{name}/include
%{_libdir}/%{name}/priv
%{_libdir}/pkgconfig/yaws.pc
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}.conf.5.gz
%{_mandir}/man5/%{name}_api.5.gz
%{_var}/%{name}/ebin
%{_var}/%{name}/www


%changelog
* Fri Oct 15 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.89-1
- update to 1.89

* Fri Jul 2 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.88-1
- Initial build for EL5
