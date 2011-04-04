%define debug_package %{nil}

Summary:	Erlang MySQL interface
Name:		erlang-mysql
Version:	0
Release:	1.20110402git%{?dist}
Group:		Development/Libraries
License:	GPL
URL:		http://github.com/dizzyd/erlang-mysql-driver
# git clone --bare http://github.com/dizzyd/erlang-mysql-driver.git erlang-mysql-0
# tar cfz erlang-mysql-0.tar.gz erlang-mysql-0
Source:		%{name}-%{version}.tar.gz
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Library that gives possibility to Erlang programs to connect MySQL databases.
This MySQL driver for Erlang is based on the Yxa driver obtained from Process One 
(at https://support.process-one.net/doc/display/CONTRIBS/Yxa).
It includes several new features such as prepared statements, transactions,
binary queries, type-converted query results, more efficient logging and a new
connection pooling mechanism.

%package devel
Summary:	Development files for Erlang MySQL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Erlang MySQL interface.

%prep
%setup -q 

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/erlang/lib/mysql-%{version}/{ebin,src,include}
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/mysql-%{version}/ebin
install -m 644 src/*.erl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/mysql-%{version}/src
install -m 644 src/*.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/mysql-%{version}/include

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING.txt README.txt
%dir %{_libdir}/erlang/lib/mysql-%{version}
%{_libdir}/erlang/lib/mysql-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/mysql-%{version}/src
%{_libdir}/erlang/lib/mysql-%{version}/include

%changelog
* Mon Apr 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 0-1.20110402git
- Update to latest git (20110402)

* Sun Jan 23 2011 Vlad V. Teterya <vlad@server-labs.ua> 0-1.20101102git
- Update to latest git (20101102)

* Mon Oct 18 2010 Vlad V. Teterya <vlad@server-labs.ua> 0-1.20100921git
- Update to latest git (20100921)

* Mon May 3 2010 Vlad V. Teterya <vlad@server-labs.ua> 0-1.20100216git
- Update to latest git (20100216) - fixed reconnection to mysqld

* Thu Mar 4 2010 Vlad V. Teterya <vlad@server-labs.ua> - 0-1.20071029svn
- Initial build for EL5
