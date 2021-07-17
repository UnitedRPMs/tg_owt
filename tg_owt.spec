%global debug_package %{nil}
%global  _hardened_build     1
#define _legacy_common_support 1
%global _disable_ld_no_undefined %nil
%undefine __cmake_in_source_build


# tg_owt
%global commit0 91d836dc84a16584c6ac52b36c04c0de504d9c34
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver git%{shortcommit0}

# libvpx
%global commit1 ebefb90b75f07ea5ab06d6b2a5ea5355c843d266
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# libyuv
%global commit2 c41eabe3d4e1c30f8cb1c5f8660583bf168d426a
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

#pipewire
#https://github.com/PipeWire/pipewire.git
%global commit3 c43dabcc96e2e072cdf08e5f094bb677d9017c6b
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

Name: tg_owt
Version: 0
Release: 7%{?dist}

License: BSD
URL: https://github.com/desktop-app/tg_owt
Summary: WebRTC library - static linked
Source0: https://github.com/desktop-app/tg_owt/archive/%{commit0}/tg_owt-%{shortcommit0}.tar.gz
Source1: https://chromium.googlesource.com/webm/libvpx.git/+archive/%{commit1}.tar.gz#/libvpx-%{shortcommit1}.tar.gz
Source2: https://chromium.googlesource.com/libyuv/libyuv.git/+archive/%{commit2}.tar.gz#/libyuv-%{shortcommit2}.tar.gz
Source3: https://github.com/PipeWire/pipewire/archive/%{commit3}/pipewire-%{shortcommit3}.tar.gz

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
BuildRequires: ffmpeg-devel
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(webkit2gtk-4.0)
BuildRequires: extra-cmake-modules

BuildRequires: yasm


%description
WebRTC library - static linked

%package devel
Summary: Development files for 
Requires: tg_owt >= %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n tg_owt-%{commit0}
tar -xf %{S:1} -C $PWD/src/third_party/libvpx/source/libvpx
tar -xf %{S:2} -C $PWD/src/third_party/libyuv
rm -rf $PWD/src/third_party/pipewire
tar -xf %{S:3} -C $PWD/src/third_party/ && mv -f $PWD/src/third_party/pipewire-%{commit3} $PWD/src/third_party/pipewire

%build

  # Static
  mkdir -p build
  cmake -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DBUILD_SHARED_LIBS=OFF \
    -DTG_OWT_SPECIAL_TARGET=linux \
    -DTG_OWT_LIBJPEG_INCLUDE_PATH=/usr/include \
    -DTG_OWT_OPENSSL_INCLUDE_PATH=/usr/include \
    -DTG_OWT_OPUS_INCLUDE_PATH=/usr/include/opus \
    -DTG_OWT_FFMPEG_INCLUDE_PATH=/usr/include/ffmpeg \
    -DTG_OWT_DLOPEN_PIPEWIRE=OFF  


  %ninja_build -C build -j2



%install
    %ninja_install -C build  -j2



%files
%{_libdir}/lib%{name}.a

%files devel
%{_includedir}/tg_owt/
%{_libdir}/cmake/tg_owt/
   
%changelog

* Fri Jul 09 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 0-7
- Inital build
