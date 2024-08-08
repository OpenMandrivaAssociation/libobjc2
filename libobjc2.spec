# Workaround for
# https://github.com/llvm/llvm-project/issues/60137
%define _disable_lto 1

%define major 4.6
# Versioned libname is intentional here to avoid
# clash with gcc's internal libobjc
%define libname %mklibname objc %{major}
%define libcxxname %mklibname objcxx %{major}
%define devname %mklibname objc -d

Name: libobjc2
# Outnumber gcc's libobjc (which has gcc's version number,
# but not the feature set of libobjc2)
Epoch: 1
Version: 2.2.1
Release: 1
Source0: https://github.com/gnustep/libobjc2/archive/v2.2.1.tar.gz
Summary: Objective-C 2.0 runtime for use with clang
URL: https://github.com/gnustep/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: llvm-devel
BuildRequires: llvm-polly
BuildRequires: cmake(tsl-robin-map)

%description
Objective-C 2.0 runtime for use with clang

%package -n %{libname}
Summary: Objective-C 2.0 runtime library for use with clang
Group: System/Libraries

%description -n %{libname}
Objective-C 2.0 runtime library for use with clang

%files -n %{libname}
%{_libdir}/libobjc.so.*

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%autosetup -p1
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
