Summary:	System for layout and rendering of internationalized text - cross Mingw32 version
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu - wersja skrośna dla Mingw32
%define		_realname   pango
Name:		crossmingw32-%{_realname}
Version:	1.16.4
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/pango/1.16/%{_realname}-%{version}.tar.bz2
# Source0-md5:	025e2ac5e40cac163aae4653aeef559c
Patch0:		%{_realname}-xfonts.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.7
BuildRequires:	crossmingw32-cairo >= 1.4.0
BuildRequires:	crossmingw32-fontconfig >= 2.4.0
BuildRequires:	crossmingw32-freetype >= 2.1.7
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.12.11
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	crossmingw32-cairo >= 1.4.0
Requires:	crossmingw32-fontconfig >= 2.4.0
Requires:	crossmingw32-freetype >= 2.1.7
Requires:	crossmingw32-glib2 >= 2.12.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
System for layout and rendering of internationalized text (cross
mingw32 version).

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu (wersja skrośna
mingw32).

%package dll
Summary:	DLL pango libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL pango dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairo-dll >= 1.4.0
Requires:	crossmingw32-fontconfig-dll >= 2.4.0
Requires:	crossmingw32-freetype-dll >= 2.1.7
Requires:	crossmingw32-glib2-dll >= 2.12.11
Requires:	wine

%description dll
DLL pango libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL pango dla Windows.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1

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

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/{gtk-doc,man}
# useless (modules loaded through libgmodule)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/1.6.0/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/libpango*-1.0.dll.a
%{_libdir}/libpango*-1.0.la
%{_libdir}/pango*-1.0.def
%{_includedir}/pango-1.0
%{_pkgconfigdir}/pango*.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpango*-1.0-*.dll
