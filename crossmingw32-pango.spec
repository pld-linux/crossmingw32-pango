#
# TODO:
# - update arch_confdir patch
#
# Conditional build:
%bcond_with	arch_confdir	# build with arch-dependant config dir
#
Summary:	System for layout and rendering of internationalized text - cross Mingw32 version
Summary(pl.UTF-8):System renderowania międzynarodowego tekstu - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Sistema para layout e renderização de texto internacionalizado
%define		_realname   pango
Name:		crossmingw32-%{_realname}
%define		_mainver 1.15
Version:	%{_mainver}.6
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/%{_mainver}/%{_realname}-%{version}.tar.bz2
# Source0-md5:	b122a41e2ba832a24013c153dd52c982
Patch0:		%{name}-noexamples.patch
Patch1:		%{name}-static.patch
Patch2:		%{_realname}-xfonts.patch
Patch3:		%{_realname}-arch_confdir.patch
Patch4:		%{name}-cairo.patch
Patch5:		%{name}-static_and_dll.patch
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
#%patch0 -p1
#%patch1 -p1
%patch2 -p1
%{?with_arch_confdir:%patch3 -p1}
%patch4 -p1
#%patch5 -p1

%build
export PKG_CONFIG_PATH=%{_pkgconfigdir}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--with-fribidi \
	--enable-static

#%{__sed} -i -e 's/^deplibs_check_method=.*/deplibs_check_method="pass_all"/' libtool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

#> $RPM_BUILD_ROOT%{_sysconfdir}/pango%{?with_arch_confdir:-%{_host_cpu}}/pango.modules

# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.6.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/lib*.la
%{_libdir}/libpango*.a
%{_bindir}/*.dll
%{_pkgconfigdir}/*
%{_includedir}/*
