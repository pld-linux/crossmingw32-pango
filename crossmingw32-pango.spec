Summary:	System for layout and rendering of internationalized text - cross MinGW32 version
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu - wersja skrośna dla MinGW32
%define		realname   pango
Name:		crossmingw32-%{realname}
Version:	1.38.1
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.38/%{realname}-%{version}.tar.xz
# Source0-md5:	7fde35d4a127b55ce8bbcefe109bc80d
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	crossmingw32-cairo >= 1.12.10
BuildRequires:	crossmingw32-fontconfig >= 2.10.91
BuildRequires:	crossmingw32-freetype >= 2.1.7
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.34.0
BuildRequires:	crossmingw32-harfbuzz >= 0.9.9
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-cairo >= 1.12.10
Requires:	crossmingw32-fontconfig >= 2.10.91
Requires:	crossmingw32-freetype >= 2.1.7
Requires:	crossmingw32-glib2 >= 2.34.0
Requires:	crossmingw32-harfbuzz >= 0.9.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%define		_ssp_cflags		%{nil}
%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
System for layout and rendering of internationalized text (cross
MinGW32 version).

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu (wersja skrośna
MinGW32).

%package dll
Summary:	DLL pango libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL pango dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairo-dll >= 1.12.10
Requires:	crossmingw32-fontconfig-dll >= 2.10.91
Requires:	crossmingw32-freetype-dll >= 2.1.7
Requires:	crossmingw32-glib2-dll >= 2.34.0
Requires:	crossmingw32-harfbuzz-dll >= 0.9.9
Requires:	wine

%description dll
DLL pango libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL pango dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_pkgconfigdir}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

# omitted from make install
for f in pango pangocairo pangoft2 pangowin32 ; do
	cp -p pango/${f}.def $RPM_BUILD_ROOT%{_libdir}/${f}-1.0.def
done

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{gtk-doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/libpango-1.0.dll.a
%{_libdir}/libpangocairo-1.0.dll.a
%{_libdir}/libpangoft2-1.0.dll.a
%{_libdir}/libpangowin32-1.0.dll.a
%{_libdir}/libpango-1.0.la
%{_libdir}/libpangocairo-1.0.la
%{_libdir}/libpangoft2-1.0.la
%{_libdir}/libpangowin32-1.0.la
%{_libdir}/pango-1.0.def
%{_libdir}/pangocairo-1.0.def
%{_libdir}/pangoft2-1.0.def
%{_libdir}/pangowin32-1.0.def
%{_includedir}/pango-1.0
%{_pkgconfigdir}/pango.pc
%{_pkgconfigdir}/pangocairo.pc
%{_pkgconfigdir}/pangoft2.pc
%{_pkgconfigdir}/pangowin32.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpango-1.0-*.dll
%{_dlldir}/libpangocairo-1.0-*.dll
%{_dlldir}/libpangoft2-1.0-*.dll
%{_dlldir}/libpangowin32-1.0-*.dll
