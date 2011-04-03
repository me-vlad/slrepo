%define nginx_user      nginx
%define nginx_group     %{nginx_user}
%define nginx_home      %{_localstatedir}/lib/nginx
%define nginx_home_tmp  %{nginx_home}/tmp
%define nginx_logdir    %{_localstatedir}/log/nginx
%define nginx_confdir   %{_sysconfdir}/nginx
%define nginx_datadir   %{_datadir}/nginx
%define nginx_webroot   %{nginx_datadir}/html

Name:           nginx
Version:        0.8.54
Release:        7%{?dist}
Summary:        Robust, small and high performance http and reverse proxy server
Group:          System Environment/Daemons

License:        BSD
URL:            http://nginx.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      pcre-devel,zlib-devel,openssl-devel
BuildRequires:      GeoIP-devel
Requires:           pcre,zlib,openssl
Requires:           GeoIP
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig, initscripts
Requires(postun):   initscripts

Source0:        http://sysoev.ru/nginx/nginx-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}.logrotate
Source3:        virtual.conf
Source4:        ssl.conf
Source5:        nginx-upstream-fair.tar.gz
Source7:        %{name}.sysconfig
Source21:       GeoIPCountryCSV.zip
Source100:      index.html
Source101:      poweredby.png
Source102:      nginx-logo.png
Source103:      50x.html
Source104:      404.html
Source500:      simpl-ngx_devel_kit-v0.2.17-0-gbc97eea.tar.gz
Source501:      chaoslawful-lua-nginx-module-v0.1.6rc2-0-gccaf132.tar.gz
Patch0:         nginx-auto-cc-gcc.patch
Patch1:         nginx-config.patch


%description
Nginx [engine x] is an HTTP(S) server, HTTP(S) reverse proxy and IMAP/POP3
proxy server written by Igor Sysoev.

Following third party modules added:
* lua-nginx-module


%prep
%setup -q
%patch0 -p0
%patch1 -p0
%setup -T -D -a 21
%setup -T -D -a 500
%setup -T -D -a 501


%build

# Convert GeoIP
perl contrib/geo2nginx.pl < GeoIPCountryWhois.csv > geo.data

# Rename dirs
mv simpl-ngx_devel_kit-bc97eea ngx_devel_kit
mv chaoslawful-lua-nginx-module-ccaf132 lua-nginx-module

# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.  The configure script(s) have been patched (Patch1 and
# Patch2) in order to support installing into a build environment.
export LUAJIT_LIB=/usr/lib
export LUAJIT_INC=/usr/include/luajit-2.0
export DESTDIR=%{buildroot}
./configure \
    --user=%{nginx_user} \
    --group=%{nginx_group} \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{nginx_confdir}/%{name}.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --pid-path=%{_localstatedir}/run/%{name}.pid \
    --lock-path=%{_localstatedir}/lock/subsys/%{name} \
    --with-http_stub_status_module \
    --with-http_ssl_module \
    --add-module=%{_builddir}/%{name}-%{version}/ngx_devel_kit \
    --add-module=%{_builddir}/%{name}-%{version}/lua-nginx-module \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -type f -empty -exec rm -f {} \;
find %{buildroot} -type f -exec chmod 0644 {} \;
find %{buildroot} -type f -name '*.so' -exec chmod 0755 {} \;
chmod 0755 %{buildroot}%{_sbindir}/nginx
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
%{__install} -p -m 0644 %{SOURCE3} %{SOURCE4} %{buildroot}%{nginx_confdir}/conf.d
%{__install} -p -d -m 0755 %{buildroot}%{nginx_home_tmp}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_logdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_webroot}
%{__install} -p -m 0644 %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} %{buildroot}%{nginx_webroot}

# init srcipt fix
sed -i -e "s|killproc \$prog -QUIT|killproc \$prog -TERM|" %{buildroot}%{_initrddir}/%{name}

# convert to UTF-8 all files that give warnings.
for textfile in CHANGES
do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -c "Nginx user" -s /bin/false -r -d %{nginx_home} %{nginx_user} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README
%{nginx_datadir}/
%{_sbindir}/%{name}
%{_initrddir}/%{name}
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%config(noreplace) %{nginx_confdir}/conf.d/*
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/%{name}.conf.default
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/%{name}.conf
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}


%changelog
* Tue Mar 8 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-7
- Update ngx_devel_kit

* Mon Mar 7 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-6
- Update lua module
- Update ngx_devel_kit
- Spec cleanup

* Fri Feb 11 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-5
- Update lua module

* Wed Feb 9 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-4
- Update lua module

* Thu Feb 3 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-3
- Update lua module

* Wed Jan 26 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-2
- Update lua module

* Sun Jan 23 2011 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-1
- Rebuild for fc14

* Fri Dec 17 2010 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.54-1
- update to 0.8.54

* Sun Nov 14 2010 Vlad V. Teterya <vlad@server-labs.ua> - 0.8.53-5
- Rebuild for EL5
