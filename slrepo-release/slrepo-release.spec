Name:           slrepo-release       
Version:        5 
Release:        2%{?dist}
Summary:        Server Labs Packages for Enterprise Linux repository configuration

Group:          System Environment/Base 
License:        GPL 
URL:            http://rpm.server-labs.com/slrepo/centos

Source0:        http://rpm.server-labs.com/slrepo/centos/RPM-GPG-KEY-SLrepo
Source1:        sl.repo	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      redhat-release >=  %{version} 

%description
This package contains the Server Labs Packages for Enterprise Linux repository
GPG key as well as configuration for yum.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .

%build


%install
rm -rf $RPM_BUILD_ROOT

# GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-SLrepo

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Wed May 4 2011 Vlad V. Teterya <vlad@server-labs.ua> - 5-2
- Turn on gpgcheck

* Sun Mar 13 2011 Vlad V. Teterya <vlad@server-labs.ua> - 5-1
- Add GPG key

* Wed Mar 9 2011 Vlad V. Teterya <vlad@server-labs.ua> - 5-0
- Initial Package for RHEL 5
