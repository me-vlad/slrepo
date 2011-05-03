
Summary: Advanced persistent key-value store
Name: redis
Version: 2.2.5
Release: 1%{?dist}
License: BSD
Group: Applications/Databases
URL: http://code.google.com/p/redis/

Source0: http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: %{name}.logrotate
Source2: %{name}.init

Patch0: %{name}-%{version}-config.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc, make
# for /usr/sbin/useradd
Requires(pre):      shadow-utils
Requires(post):     chkconfig
# for /sbin/service
Requires(preun):    chkconfig, initscripts
Requires(postun):   initscripts
Provides: %{name} = %{version}-%{release}

%description
Redis is an advanced key-value store. It is similar to memcached but the 
dataset is not volatile, and values can be strings, exactly like in 
memcached, but also lists, sets, and ordered sets. All this data types 
can be manipulated with atomic operations to push/pop elements, add/remove 
elements, perform server side union, intersection, difference between sets,
and so forth. Redis supports different kind of sorting abilities.

In order to be very fast but at the same time persistent the whole dataset
is taken in memory, and from time to time saved on disc asynchronously
(semi persistent mode) or alternatively every change is written into an
append only file (fully persistent mode). Redis is able to rebuild the
append only file in background when it gets too big.

Redis supports trivial to setup master-slave replication, with very fast
non-blocking first synchronization, auto reconnection on net split, and so forth. 

%prep
%setup -q
%patch0 -p1 -b .conf

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -Dp -m0755 src/%{name}-server %{buildroot}%{_sbindir}/%{name}-server
%{__install} -Dp -m0755 src/%{name}-benchmark %{buildroot}%{_bindir}/%{name}-benchmark
%{__install} -Dp -m0755 src/%{name}-check-aof %{buildroot}%{_bindir}/%{name}-check-aof
%{__install} -Dp -m0755 src/%{name}-check-dump %{buildroot}%{_bindir}/%{name}-check-dump
%{__install} -Dp -m0755 src/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli

%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%{__install} -Dp -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{name}
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/%{name}

%clean
%{__rm} -rf %{buildroot}

%pre
%{_sbindir}/useradd -c 'Redis user' -s /sbin/nologin -r -d %{_localstatedir}/lib/redis %{name} 2> /dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    # make sure redis service is not running before uninstalling

    # when the preun section is run, we've got stdin attached.  If we
    # call stop() in the redis init script, it will pass stdin along to
    # the redis-cli script; this will cause redis-cli to read an extraneous
    # argument, and the redis-cli shutdown will fail due to the wrong number
    # of arguments.  So we do this little bit of magic to reconnect stdin
    # to the terminal
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec < $term

    /sbin/service %{name} stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc doc/*.html
%{_sbindir}/%{name}-server
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-dump
%{_bindir}/%{name}-cli
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0770,%{name},%{name}) %{_localstatedir}/lib/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/log/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/run/%{name}

%changelog
* Tue May 3 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.2.5-1
- updated to 2.2.5

* Mon Apr 4 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.2.2-1
- updated to 2.2.2

* Thu Feb 24 2011 Vlad V. Teterya <vlad@server-labs.ua> 2.2.1-1
- updated to 2.2.1

* Fri Nov 12 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.4-1
- updated to 2.0.4

* Fri Oct 15 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.3-1
- updated to 2.0.3

* Thu Sep 30 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.2-1
- updated to 2.0.2

* Mon Sep 13 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.1-1
- updated to 2.0.1

* Sun Sep 5 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0-1
- updated to 2.0.0

* Wed Sep 1 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0.rc4-1
- updated to 2.0.0-rc4

* Mon Jul 12 2010 Vlad V. Teterya <vlad@server-labs.ua> 2.0.0.rc2-1
- updated to 2.0.0-rc2

* Tue Apr 6 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.2.6-1
- updated to 1.2.6

* Sun Mar 14 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.2.5-1
- updated to 1.2.5

* Sun Mar 7 2010 Vlad V. Teterya <vlad@server-labs.ua> 1.2.3-1
- Initial build for EL5
