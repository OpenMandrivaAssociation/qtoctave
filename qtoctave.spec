%define _requires_exceptions \/usr\/bin\/octave
%define _default_patch_fuzz 3

Name:           qtoctave
Version:        0.8.2
Release:        %mkrel 3
Summary:        Frontend for Octave
Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://qtoctave.wordpress.com/
Source0:        https://forja.rediris.es/frs/download.php/744/qtoctave-%{version}.tar.gz
# Debian patches
Patch0:		qtoctave-add_missing_includes.patch
Patch1:		qtoctave-build-out-of-source.patch
Patch2:		qtoctave-font-option-in-png-export.patch
Patch3:		qtoctave-install_easyplot_as_target.patch
Patch4:		qtoctave-move_doc_under_doc.patch
Patch5:		qtoctave-use_cstdio_header.patch
Patch6:		qtoctave-use_octave_htmldoc.patch
# fhimpe: fix detection of QT versions > 4.5
Patch7:		qtoctave-fix-qt4.6-detection.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	octave
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
QtOctave is a frontend for Octave based on Qt4.

%prep
%setup -q -n %{name}-%{version}/
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1 

%{__perl} -pi -e 's/\r$//g' readme.txt

# Desktop file
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=QtOctave
Comment=Frontend for Octave
Exec=qtoctave
Terminal=false
Icon=qtoctave
Type=Application
Categories=Education;Math;Science;
EOF

%build
%{cmake} -DCMAKE_SKIP_RPATH:STRING="ON"  
make

%install
%{__rm} -rf %{buildroot}
pushd build
%{makeinstall_std}
popd

%if 0
%{__chmod} 0755 %{buildroot}%{_datadir}/%{name}/menus/Analysis/Integrate.m \
                %{buildroot}%{_datadir}/%{name}/menus/Analysis/Integrate
%endif

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{_bindir}/desktop-file-install --dir %{buildroot}%{_datadir}/applications %{name}.desktop

%clean
%{__rm} -rf %{buildroot}

%post
%{update_desktop_database}
#%%update_icon_cache hicolor

%postun
%{clean_desktop_database}
#%%clean_icon_cache hicolor

%files
%defattr(0644,root,root,0755)
%doc LICENSE_GPL.txt leeme.txt readme.txt
%attr(0755,root,root) %{_bindir}/qtoctave
%attr(0755,root,root) %{_bindir}/easy_plot
%attr(0755,root,root) %{_bindir}/qtjs
%attr(0755,root,root) %{_bindir}/qtoctave_pkg
%attr(0755,root,root) %{_bindir}/simplercs
%attr(0755,root,root) %{_bindir}/xmlwidget
%{_iconsdir}/hicolor/64x64/apps/qtoctave.png
%{_datadir}/applications/*%{name}.desktop
%defattr(-,root,root,0755)
%{_datadir}/%{name}
