%define _requires_exceptions \/usr\/bin\/octave

Name:           qtoctave
Version:        0.6.3
Release:        %mkrel 1
Summary:        Frontend for Octave
Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://qtoctave.wordpress.com/
Source0:        https://forja.rediris.es/frs/download.php/396/qtoctave-%{version}.tar.gz
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
Requires:	octave
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
QtOctave is a frontend for Octave based on Qt4.

%prep
%setup -q
%{__perl} -pi -e 's/\r$//g' README.txt qtoctave.nsi
%{__chmod} 0755 configure

# Desktop file
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=QtOctave
Comment=Frontend for Octave
Exec=qtoctave
Terminal=false
Type=Application
Categories=Education;Math;Science;
EOF

%build
export QTDIR=
# XXX: datadir is non-standard!
./configure --prefix=%{_prefix} --bindir=%{_bindir} --datadir=%{_datadir}/%{name} --qtdir=%{_prefix}/lib/qt4
%{__make} CXXFLAGS="%{optflags}"


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

%{__chmod} 0755 %{buildroot}%{_datadir}/%{name}/menus/Analysis/Integrate.m \
                %{buildroot}%{_datadir}/%{name}/menus/Analysis/Integrate

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
%doc LEEME.txt LICENSE_GPL.txt NEWS.txt README.txt qtoctave.nsi
%attr(0755,root,root) %{_bindir}/qtoctave
%attr(0755,root,root) %{_bindir}/widgetserver
%{_datadir}/applications/%{name}.desktop
%defattr(-,root,root,0755)
%{_datadir}/%{name}
