%define _requires_exceptions \/usr\/bin\/octave

Name:           qtoctave
Version:        0.7.4
Release:        %mkrel 1
Summary:        Frontend for Octave
Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://qtoctave.wordpress.com/
Source0:        https://forja.rediris.es/frs/download.php/744/qtoctave-%{version}.tar.gz
Patch0:         qtoctave-add-path-for-cmake26.patch
Patch1:         qtoctave-build-out-of-source.patch
Patch2:         qtoctave-move-doc-under-doc.patch
Patch3:         qtoctave-use-octave-doc.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	octave
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
QtOctave is a frontend for Octave based on Qt4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__perl} -pi -e 's/\r$//g' readme.txt

# Desktop file
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=QtOctave
Comment=Frontend for Octave
Exec=qtoctave
Terminal=false
Type=Application
Categories=Education;Math;Science;
EOF

%build
%{cmake}
%{make}

%install
%{__rm} -rf %{buildroot}
pushd build
%{makeinstall_std}
popd

%{_bindir}/chrpath -d %{buildroot}%{_bindir}/qtoctave

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
%doc LICENSE_GPL.txt leeme.txt news.txt readme.txt
%attr(0755,root,root) %{_bindir}/qtoctave
%{_datadir}/applications/*%{name}.desktop
%defattr(-,root,root,0755)
%{_datadir}/%{name}
