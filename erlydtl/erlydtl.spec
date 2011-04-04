%define debug_package %{nil}

Summary:	Django templates for Erlang 
Name:		erlydtl
Version:	0.7.0
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPL
URL:		http://code.google.com/p/erlydtl/
Source:		http://erlydtl.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ErlyDTL implements most but not all of the Django Template Language.

%package devel
Summary:	Development files for ErlyDTL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for ErlyDTL

%prep
%setup -q 

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{name}-%{version}/{ebin,src,src/filter_lib,src/i18n}
install -m 644 ebin/* $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{name}-%{version}/ebin/
install -m 644 src/*.erl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{name}-%{version}/src
install -m 644 src/filter_lib/*.erl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{name}-%{version}/src/filter_lib
install -m 644 src/i18n/*.erl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{name}-%{version}/src/i18n
install -m 755 bin/erlydtl_compile $RPM_BUILD_ROOT%{_bindir}/erlydtl_compile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README_I18N  README.markdown
%dir %{_libdir}/erlang/lib/%{name}-%{version}
%{_libdir}/erlang/lib/%{name}-%{version}/ebin
%{_bindir}/erlydtl_compile

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/erlydtl-%{version}/src

%changelog
* Mon Apr 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 0.7.0-1
- Update to 0.7.0

* Fri Jul 2 2010 Vlad V. Teterya <vlad@server-labs.ua> 0.6.0-1.20100623git
- Initial build for EL5
