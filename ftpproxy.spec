Summary:	ftpproxy is an application level gateway for the FTP protocol
Summary(pl):	ftpproxy jest aplikacyjn± bramk± dla protoko³u FTP
Name:		ftpproxy
Version:	1.2.3
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://ftp.daemons.de/download/%{name}-%{version}.tgz
# Source0-md5:	c2068bc452e1d7554d3bda08030aa433
Source1:	%{name}.inetd
Prereq:		rc-inetd >= 0.8.1
URL:		http://ftp.daemons.de/
BuildRequires:	ctags
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	proxytools

%description
ftp.proxy is a proxy server for a subset of the file transfer protocol
described in RFC 959. It forwards traffic between a client and a
server without looking too much if both hosts do real FTP. The FTP
server can be either given on the command line or supplied by the
client.

%description -l pl
ftp.proxy jest aplikacyjn± bramk± dla podzbioru protoko³u FTP
opisanego w RFC 959. Po¶redniczy w transferze pomiêdzy klientem a
serwerem bez specjalnego patrzenia czy oba hosty s± prawdziwymi
serwerami FTP.

%prep
%setup -q

%build
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags} -DVERSION=\\\"%{version}\\\""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/sysconfig/rc-inetd}

install src/ftp.proxy $RPM_BUILD_ROOT%{_sbindir}
install doc/ftp.proxy.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpproxy

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc doc/rfc*.txt HISTORY INSTALL
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/ftpproxy
%attr(755,root,root) %{_sbindir}/ftp.proxy
%{_mandir}/man1/*
