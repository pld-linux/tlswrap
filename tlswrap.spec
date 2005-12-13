Summary:	TLS/SSL FTP wrapper/proxy
Summary(pl):	Wrapper/proxy TLS/SSL dla FTP
Name:		tlswrap
Version:	1.02
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://tlswrap.sunsite.dk/%{name}-%{version}.tar.gz
# Source0-md5:	fa9e503a861a7519a8f485bad77e2cc7
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://tlswrap.sunsite.dk/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLSWrap is a TLS/SSL FTP wrapper/proxy for UNIX and Windows, allowing
you to use your favourite FTP client with any TLS/SSL-enabled FTP
server.

%description -l pl
TLSWrap to wrapper/proxy TLS/SSL dla FTP dla Uniksów i Windows,
pozwalaj±cy na u¿ywanie ulubionego klienta FTP z dowolnym serwerem FTP
obs³uguj±cym TLS/SSL.

%prep
%setup -q

%build
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
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tlswrap
%attr(754,root,root) /etc/rc.d/init.d/tlswrap
