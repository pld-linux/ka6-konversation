#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		qtver		6.5.0
%define		kframever	6.13.0
%define		kaname		konversation
Summary:	Konversation
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7d5bb5b891f8369317ce8d0a83781464
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Multimedia-devel >= %{qtver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kbookmarks-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kglobalaccel-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kidletime-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kstatusnotifieritem-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-qttools >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Konversation.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

sed -i -e 's|!/usr/bin/env bash|!/bin/bash|' $RPM_BUILD_ROOT%{_datadir}/konversation/scripts/*
sed -i -e 's|!/usr/bin/env perl|!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/konversation/scripts/*
sed -i -e 's|!/usr/bin/env python|!/usr/bin/python3|' $RPM_BUILD_ROOT%{_datadir}/konversation/scripts/*

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{sr,zh_CN}

# not supported by glibc yet
%{__rm} -rf $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL NEWS README
%attr(755,root,root) %{_bindir}/konversation
%{_desktopdir}/org.kde.konversation.desktop
%{_datadir}/dbus-1/services/org.kde.konversation.service
%{_iconsdir}/hicolor/*x*/actions/konv_message.png
%{_iconsdir}/hicolor/*x*/apps/konversation.png
%{_datadir}/knotifications6/konversation.notifyrc
%{_datadir}/knsrcfiles/konversation_nicklist_theme.knsrc
%dir %{_datadir}/konversation
%{_datadir}/konversation/scripting_support
%dir %{_datadir}/konversation/scripts
%attr(755,root,root) %{_datadir}/konversation/scripts/bug
%attr(755,root,root) %{_datadir}/konversation/scripts/cmd
%attr(755,root,root) %{_datadir}/konversation/scripts/fortune
%attr(755,root,root) %{_datadir}/konversation/scripts/fortunes.dat
%attr(755,root,root) %{_datadir}/konversation/scripts/gauge
%attr(755,root,root) %{_datadir}/konversation/scripts/media
%attr(755,root,root) %{_datadir}/konversation/scripts/sayclip
%attr(755,root,root) %{_datadir}/konversation/scripts/sysinfo
%attr(755,root,root) %{_datadir}/konversation/scripts/tinyurl
%attr(755,root,root) %{_datadir}/konversation/scripts/uptime
%{_datadir}/konversation/themes
%{_datadir}/metainfo/org.kde.konversation.appdata.xml
%{_datadir}/qlogging-categories6/konversation.categories
