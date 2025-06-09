%define		major	0
%define		libname	%mklibname openmpt %{major}
%define		devname	%mklibname openmpt -d

Summary:	A C/C++ library to decode tracker music module (MOD) files
Name:		libopenmpt
Version:	0.8.0
Release:	1
License:	BSD
Group:	Sound
Url:		https://lib.openmpt.org/libopenmpt/
Source0:	https://lib.openmpt.org/files/libopenmpt/src/%{name}-%{version}+release.autotools.tar.gz
Source100:	libopenmpt.rpmlintrc
# This one needs to be rediffed at every version update
Patch0:		llibopenmpt-0.8.0-drop-release.autotools-from-package-version.patch
BuildRequires:		chrpath
BuildRequires:		doxygen
BuildRequires:		graphviz
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(flac) >= 1.3.0
BuildRequires:		pkgconfig(libmpg123) >= 1.14.0
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(ogg)
BuildRequires:		pkgconfig(portaudio-2.0)
BuildRequires:		pkgconfig(portaudiocpp)
BuildRequires:		pkgconfig(sdl2) >= 2.0.4
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(vorbis)
BuildRequires:		pkgconfig(vorbisfile)
BuildRequires:		pkgconfig(zlib)

%description
This is a cross-platform C++ and C library to decode tracked music (MOD) files
into a raw PCM audio stream. It is based on the player code of the OpenMPT
project (Open ModPlug Tracker). In order to avoid code base fragmentation, the
library is developed in the same source code repository as OpenMPT.

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A C/C++ library to decode tracker music module (MOD) files
Group:	System/Libraries

%description -n %{libname}
A cross-platform C++ and C library to decode tracked music (MOD) files into a
raw PCM audio stream. This package contains the actual library.

%files -n %{libname}
%doc LICENSE README.md
%{_libdir}/%{name}.so.%{major}*

#-----------------------------------------------------------------------------

%package -n openmpt123
Summary:	Command-line tracker music player based on %{libname}
Group:	Sound

%description -n openmpt123
This is a cross-platform command-line based player for tracker music (MOD)
module files. It uses %{libname}.

%files -n openmpt123
%doc LICENSE
%{_bindir}/openmpt123
%{_mandir}/man1/openmpt123.1*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for the %{name} library
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	openmpt-devel = %{EVRD}

%description -n %{devname}
Files needed when building software using %{libname}.

%files -n %{devname}
%doc LICENSE examples
%doc doxygen-doc/html
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}+release.autotools

sed -i 's/\r$//' LICENSE

# Drop useless hidden file
rm -f examples/.clang-format


%build
%configure	--disable-static \
			--with-sdl2 \
			--enable-doxygen-dot \
			--enable-doxygen-man
%make_build

# Build docs
doxygen -u Doxyfile
doxygen Doxyfile


%install
%make_install

chrpath --delete %{buildroot}%{_bindir}/openmpt123

# We pick up docs with our macro
rm -rf %{buildroot}%{_docdir}/%{name}/*
