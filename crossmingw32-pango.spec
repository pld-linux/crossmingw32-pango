Summary:	System for layout and rendering of internationalized text - cross MinGW32 version
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu - wersja skrośna dla MinGW32
%define		realname   pango
Name:		crossmingw32-%{realname}
Version:	1.44.7
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.44/%{realname}-%{version}.tar.xz
# Source0-md5:	c75cc5b833d934d98e83343832e20e5d
URL:		http://www.pango.org/
# cairo-ft cairo-pdf cairo-png cairo-ps cairo-win32
BuildRequires:	crossmingw32-cairo >= 1.12.10
BuildRequires:	crossmingw32-fontconfig >= 2.11.91
BuildRequires:	crossmingw32-freetype >= 2.1.7
BuildRequires:	crossmingw32-fribidi >= 0.19.7
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.59.2
BuildRequires:	crossmingw32-harfbuzz >= 2.0.0
BuildRequires:	crossmingw32-w32api >= 5.0.2-6
# glib-genmarshal, glib-mkenums
BuildRequires:	glib2-devel >= 1:2.59.2
BuildRequires:	meson >= 0.50.0-2
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-cairo >= 1.12.10
Requires:	crossmingw32-fontconfig >= 2.11.91
Requires:	crossmingw32-freetype >= 2.1.7
Requires:	crossmingw32-fribidi >= 0.19.7
Requires:	crossmingw32-glib2 >= 2.59.2
Requires:	crossmingw32-harfbuzz >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}
# for meson 0.50+, keep __cc/__cxx as host compiler and pass %{target}-* in meson-cross.txt

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

%package static
Summary:	Static Pango libraries (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczne biblioteki Pango (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static Pango libraries (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczne biblioteki Pango (wersja skrośna MinGW32).

%package dll
Summary:	DLL pango libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL pango dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairo-dll >= 1.12.10
Requires:	crossmingw32-fontconfig-dll >= 2.11.91
Requires:	crossmingw32-freetype-dll >= 2.1.7
Requires:	crossmingw32-fribidi-dll >= 0.19.7
Requires:	crossmingw32-glib2-dll >= 2.59.2
Requires:	crossmingw32-harfbuzz-dll >= 2.0.0
Requires:	wine

%description dll
DLL pango libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL pango dla Windows.

%prep
%setup -q -n %{realname}-%{version}

cat > meson-cross.txt <<'EOF'
[host_machine]
system = 'windows'
cpu_family = 'x86'
cpu = 'i386'
endian='little'
[binaries]
c = '%{target}-gcc'
cpp = '%{target}-g++'
ar = '%{target}-ar'
windres = '%{target}-windres'
pkgconfig = 'pkg-config'
[properties]
c_args = ['%(echo %{rpmcflags} | sed -e "s/ \+/ /g;s/ /', '/g")', '-DWINVER=0x0600']
EOF

%build
export PKG_CONFIG_LIBDIR=%{_pkgconfigdir}
%meson build \
	--cross-file meson-cross.txt \
	%{?debug:--debug} \
	-Dgtk_doc=false \
	-Dintrospection=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/pango-{list,view}.exe

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README.md README.win32 THANKS
%{_libdir}/libpango-1.0.dll.a
%{_libdir}/libpangocairo-1.0.dll.a
%{_libdir}/libpangoft2-1.0.dll.a
%{_libdir}/libpangowin32-1.0.dll.a
%{_includedir}/pango-1.0
%{_pkgconfigdir}/pango.pc
%{_pkgconfigdir}/pangocairo.pc
%{_pkgconfigdir}/pangoft2.pc
%{_pkgconfigdir}/pangowin32.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpango-1.0.a
%{_libdir}/libpangocairo-1.0.a
%{_libdir}/libpangoft2-1.0.a
%{_libdir}/libpangowin32-1.0.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpango-1.0-0.dll
%{_dlldir}/libpangocairo-1.0-0.dll
%{_dlldir}/libpangoft2-1.0-0.dll
%{_dlldir}/libpangowin32-1.0-0.dll
