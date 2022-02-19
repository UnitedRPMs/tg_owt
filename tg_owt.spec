%global debug_package %{nil}
%global  _hardened_build     1
#define _legacy_common_support 1
%global _disable_ld_no_undefined %nil
%undefine __cmake_in_source_build


# tg_owt
%global commit0 4cba1acdd718b700bb33945c0258283689d4eac7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver git%{shortcommit0}

# libvpx
%global commit1 626ff35955c2c35b806b3e0ecf551a1a8611cdbf
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# libyuv
%global commit2 ad890067f661dc747a975bc55ba3767fe30d4452
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

#pipewire
#https://github.com/PipeWire/pipewire.git
%global commit3 bdd407fe66cc9e46d4bc4dcc989d50679000482b
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

Name: tg_owt
Version: 0
Release: 9%{?dist}

License: BSD
URL: https://github.com/desktop-app/tg_owt
Summary: WebRTC library 
Source0: https://github.com/desktop-app/tg_owt/archive/%{commit0}/tg_owt-%{shortcommit0}.tar.gz
Source1: https://chromium.googlesource.com/webm/libvpx.git/+archive/%{commit1}.tar.gz#/libvpx-%{shortcommit1}.tar.gz
Source2: https://chromium.googlesource.com/libyuv/libyuv.git/+archive/%{commit2}.tar.gz#/libyuv-%{shortcommit2}.tar.gz
Source3: https://github.com/PipeWire/pipewire/archive/%{commit3}/pipewire-%{shortcommit3}.tar.gz

Patch:	https://github.com/desktop-app/tg_owt/commit/5d6b648e5e2ef85bb8012ea42f874495823d1792.patch
Patch1:	https://github.com/desktop-app/tg_owt/commit/f1ed97b0abb5dcafc11c39ebe611fd3912dc0f9c.patch

ExclusiveArch: x86_64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5XkbCommonSupport)
BuildRequires: cmake(dbusmenu-qt5)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tl-expected)
#if 0%{?fedora} >= 34
#BuildRequires: cmake(absl)
#endif

BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavresample)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(usrsctp)
BuildRequires: pkgconfig(vpx)

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtwayland-devel
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: qt5-qtbase-static
BuildRequires: libjpeg-turbo-devel 
BuildRequires: kf5-kwayland-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: pipewire-devel
BuildRequires: rlottie-devel
BuildRequires: rnnoise-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: ffmpeg4-devel
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(webkit2gtk-4.0)
BuildRequires: extra-cmake-modules
BuildRequires: unzip
BuildRequires: libXtst-devel libXrandr-devel libXcomposite-devel libva-devel
BuildRequires: openh264-devel
BuildRequires: yasm
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libdrm)
#BuildRequires: abseil-cpp-devel

%description
WebRTC library - static linked

%package static
Summary: WebRTC library - static linked
Requires: tg_owt >= %{version}-%{release}

%description static
WebRTC library - static linked

%package devel
Summary: Development files for tg_owt
Requires: tg_owt >= %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n tg_owt-%{commit0} -p1
rm -rf $PWD/src/third_party/libvpx/source/libvpx && mkdir -p $PWD/src/third_party/libvpx/source/libvpx && tar -xf %{S:1} -C $PWD/src/third_party/libvpx/source/libvpx
tar -xf %{S:2} -C $PWD/src/third_party/libyuv
rm -rf $PWD/src/third_party/pipewire
tar -xf %{S:3} -C $PWD/src/third_party/ && mv -f $PWD/src/third_party/pipewire-%{commit3} $PWD/src/third_party/pipewire

sed -i '/include(cmake\/libvpx.cmake)/d' CMakeLists.txt
sed -i '/include(cmake\/libopenh264.cmake)/d' CMakeLists.txt

%build
cp -rf %{_builddir}/tg_owt-%{commit0}/ %{_builddir}/tg_owt-%{commit0}-shared/
DRM_CFLAGS="$(pkg-config --cflags libdrm)"

export CFLAGS="%{optflags} -fPIC $DRM_CFLAGS" CXXFLAGS="%{optflags} -fPIC $DRM_CFLAGS"

  # Static
  mkdir -p build
  cmake -B build -G Ninja \
    -DCMAKE_INSTALL_PREFIX=/usr  \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DCMAKE_BUILD_TYPE:STRING=None \
    -DTG_OWT_PACKAGED_BUILD=ON \

pushd %{_builddir}/tg_owt-%{commit0}-shared
  mkdir -p shared
    cmake -B shared -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DCMAKE_BUILD_TYPE:STRING=None \
    -DBUILD_SHARED_LIBS=ON 
    
    popd
     
#    -DCMAKE_AR=%{_bindir}/gcc-ar \
#    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
#    -DCMAKE_NM=%{_bindir}/gcc-nm \
#    -DBUILD_SHARED_LIBS=ON \
#    -DTG_OWT_SPECIAL_TARGET=linux \
#    -DTG_OWT_LIBJPEG_INCLUDE_PATH=/usr/include \
#    -DTG_OWT_OPENSSL_INCLUDE_PATH=/usr/include \
#    -DTG_OWT_OPUS_INCLUDE_PATH=/usr/include/opus \
#    -DTG_OWT_FFMPEG_INCLUDE_PATH=/usr/include/ffmpeg \
#   -DTG_OWT_USE_X11=OFF \
#    -DTG_OWT_DLOPEN_PIPEWIRE=OFF \
#    -DWEBRTC_USE_X11=OFF \
    
    
 #   -DWEBRTC_USE_PIPEWIRE 


  %ninja_build -C build -j2
  
pushd %{_builddir}/tg_owt-%{commit0}-shared
  %ninja_build -C shared -j2
popd


%install
pushd %{_builddir}/tg_owt-%{commit0}-shared    
    %ninja_install -C shared  -j2
    rm -rf %{buildroot}/%{_includedir}/tg_owt/
    rm -rf %{buildroot}/%{_libdir}/cmake/tg_owt/    
    popd
    
    %ninja_install -C build  -j2


%files
%{_libdir}/libtg_owt.so.*

%files static
%{_libdir}/lib%{name}.a

%files devel
%{_libdir}/libtg_owt.so
%{_includedir}/tg_owt/
%{_libdir}/cmake/tg_owt/
   
%changelog

* Fri Feb 11 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 0-10
- Updated to current commit

* Fri Dec 17 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 0-9
- Updated to current commit

* Fri Oct 08 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 0-8
- Updated to current commit

* Fri Jul 09 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 0-7
- Inital build
