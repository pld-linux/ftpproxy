Summary:	ftpproxy is an application level gateway for the FTP protocol
Summary(pl):	ftpproxy jest aplikacyjn± bramk± dla protoko³u FTP.
Name:		ftpproxy
Version:	1.1.2
Release:	1
License:	GPL
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	http://ftp.daemons.de/download/%{name}-%{version}.tgz
Source1:	%{name}.inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ftp.proxy is a proxy server for a subset of the file tran­ fer
protocol described in RFC 959. It forwards traffic between a client
and a server without looking too much if both hosts do real FTP. The
FTP server can be either given on the command line or supplied by the
client.

%description -l pl
ftp.proxy jest aplikacyjn± bramk± dla protoko³u FTP.

%prep
%setup -q

%build
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}

install ftp.proxy $RPM_BUILD_ROOT%{_sbindir}/
install ftp.proxy.1 $RPM_BUILD_ROOT%{_mandir}/man1/

gzip -9nf  rfc959 HISTORY INSTALL
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpproxy

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
	    
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *gz
%attr(755,root,root) %{_sbindir}/ftp.proxy
%{_mandir}/man1/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/ftpproxy
