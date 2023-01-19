# Workaround for
# https://github.com/llvm/llvm-project/issues/60137
%define _disable_lto 1

%define major 4.6
%define libname %mklibname objc %{major}
%define libcxxname %mklibname objcxx %{major}
%define devname %mklibname objc -d

Name: libobjc2
# Outnumber gcc's libobjc (which has gcc's version number,
# but not the feature set of libobjc2)
Epoch: 1
Version: 2.1
Release: 2
Source0: https://github.com/gnustep/libobjc2/archive/refs/tags/v%{version}.tar.gz
Source1: https://github.com/Tessil/robin-map/archive/757de829927489bee55ab02147484850c687b620.tar.gz
Patch0: libobjc2-2.1-workaround-clang-bug.patch
Patch1: libobjc2-fix-eh_trampoline.patch
Summary: Objective-C 2.0 runtime for use with clang
URL: http://download.gna.org/gnustep/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: llvm-devel
BuildRequires: llvm-polly

%description
Objective-C 2.0 runtime for use with clang

%libpackage objc %{major}

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%autosetup -p1 -a 1
rmdir third_party/robin-map
mv robin-map-* third_party/robin-map

%cmake -DLLVM_OPTS:BOOL=ON \
	-DGNUSTEP_INSTALL_TYPE=SYSTEM \
	-G Ninja

%build
ninja -C build

%install
DESTDIR=%{buildroot} ninja install -C build

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
