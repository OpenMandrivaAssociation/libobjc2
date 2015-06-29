%define _disable_ld_no_undefined 1

%define major 4.6
%define libname %mklibname objc %{major}
%define libcxxname %mklibname objcxx %{major}
%define devname %mklibname objc -d

Name: libobjc2
Version: 1.7
Release: 1
Source0: http://download.gna.org/gnustep/%{name}-%{version}.txz
Patch0: libobjc2-1.7-cxx-fixes.patch
Patch1: libobjc2-fix-llvm-detection.patch
Summary: Objective-C 2.0 runtime for use with clang
URL: http://download.gna.org/gnustep/
License: GPL
Group: System/Libraries

%description
Objective-C 2.0 runtime for use with clang

%libpackage objc %{major}

%libpackage objcxx %{major}

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Requires: %{libcxxname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%apply_patches

%cmake -DLLVM_OPTS:BOOL=ON \
	-G Ninja

%build
ninja -C build

%install
DESTDIR=%{buildroot} ninja install -C build

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
