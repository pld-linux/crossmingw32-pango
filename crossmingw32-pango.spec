#
# TODO:
# - update arch_confdir patch
#
# Conditional build:
%bcond_with	arch_confdir	# build with arch-dependant config dir
#
%define		_realname   pango
Summary:	System for layout and rendering of internationalized text - cross Mingw32 version
Summary(pl.UTF-8):System renderowania międzynarodowego tekstu - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Sistema para layout e renderização de texto internacionalizado
Name:		crossmingw32-%{_realname}
Version:	1.14.10
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.14/%{_realname}-%{version}.tar.bz2
# Source0-md5:	e9fc2f8168e74e2fa0aa8238ee0e9c06
Patch0:		%{name}-noexamples.patch
Patch1:		%{name}-static.patch
Patch2:		%{_realname}-xfonts.patch
Patch3:		%{_realname}-arch_confdir.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.7
BuildRequires:	crossmingw32-cairo >= 1.2.4
BuildRequires:	crossmingw32-fontconfig >= 2.4.0
BuildRequires:	crossmingw32-freetype >= 2.1.7
BuildRequires:	crossmingw32-glib2 >= 2.12.9
BuildRequires:	crossmingw32-pkgconfig
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	crossmingw32-cairo >= 1.2.4
Requires:	crossmingw32-freetype >= 2.1.7
Requires:	crossmingw32-glib2 >= 2.12.9
Obsoletes:	libpango24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
System for layout and rendering of internationalized text.

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu.

%description -l pt_BR.UTF-8
Pango é um sistema para layout e renderização de texto
internacionalizado.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{?with_arch_confdir:%patch3 -p1}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target=%{target} \
	--host=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

#> $RPM_BUILD_ROOT%{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.5.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README examples/HELLO.utf8
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/libpango*.a
%{_pkgconfigdir}/*
%{_includedir}/*
