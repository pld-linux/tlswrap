Summary:	TLS/SSL FTP wrapper/proxy.
Name:		tlswrap
Version:	0.7
Release:	0.1
License:	GPL
Group:          Networking/Daemons
Source0:	http://tlswrap.sunsite.dk/%{name}%{version}.tar.gz
# Source0-md5:	6da51a7e3e7950b2b3feca77e9708314
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://tlswrap.sunsite.dk/
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:	openssl-devel
Requires(post,preun):   /sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLSWrap is a TLS/SSL FTP wrapper/proxy for UNIX and Windows, allowing
you to use your favourite FTP client with any TLS/SSL-enabled FTP
server.

%prep
%setup -q -n %{name}%{version}

%build
touch memcmp.c
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/tlswrap
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/tlswrap

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/tlswrap ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start tlswrap daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/tlswrap ]; then
		/etc/rc.d/init.d/tlswrap stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr( 644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/tlswrap
%attr( 754,root,root) /etc/rc.d/init.d/tlswrap
%attr(755,root,root) %{_bindir}/*
