Name:           luajit
Version:        2.0.0
Release:        2%{?dist}
Summary:        LuaJIT is a Just-In-Time Compiler for the Lua* programming language
Group:          Development/Languages
License:        MIT
URL:            http://luajit.org
Source0:        http://luajit.org/download/LuaJIT-%{version}-beta6.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides:       luajit = 2.0.0

%description
LuaJIT is a Just-In-Time Compiler for the Lua* programming language.


%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.


%package static
Summary:        Static library for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.


%prep
%setup -q -n LuaJIT-%{version}-beta6


%build
make %{?_smp_mflags} PREFIX=%{_usr}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{_usr} DESTDIR=$RPM_BUILD_ROOT 
mv $RPM_BUILD_ROOT%{_bindir}/%{name}-%{version}-beta6 $RPM_BUILD_ROOT%{_bindir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}-beta6 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYRIGHT README doc/
%{_bindir}/luajit
%{_libdir}/libluajit-*.so*
%{_mandir}/man1/luajit.1.gz
%{_datadir}/%{name}-%{version}/jit/*.lua
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.1
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.1


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-2.0/*.h
%{_includedir}/%{name}-2.0/*.hpp
%{_libdir}/pkgconfig/luajit.pc


%files static
%defattr(-,root,root,-)
%{_libdir}/libluajit-*.a


%changelog
* Tue Feb 15 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-2
- Update to 2.0.0-beta6

* Wed Feb 9 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1.20110209git
- Update to latest git revision

* Sat Jan 22 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1.20110121git
- Rebuild for fc14

* Fri Jan 21 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1.20110121git
- Initial build for EL5
