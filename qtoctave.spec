Name:           qtoctave
Version:        0.10.1
Release:        %mkrel 1
Summary:        Frontend for Octave
Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://qtoctave.wordpress.com/
Source0:        https://forja.rediris.es/frs/download.php/744/qtoctave-%{version}.tar.gz

# place qtoctave_doc and qtoctave-utils in qtoctave datadir
Patch0:         qtoctave-doc-path.patch
# fix *.m filters in file dialogs (debian#620062, patch by Sébastien Villemot)
Patch1:         qtoctave-0.10.1-filedialog-filters.patch
# fix crash when closing a dock tool within the first 5 seconds (#722986)
# (a NULL pointer dereference caused by a race condition between the user
# closing the tool and the timer setting the initial positions, prevented by
# using a QWeakPointer<QWidget> instead of a raw QWidget *)
Patch2:         qtoctave-0.10.1-initialposition.patch
# fix Octave help not working (#737297)
# (system(command, 1, "async"); is nonsense, use system(command, 0, "async");)
Patch3:         qtoctave-0.10.1-qtinfo.patch
Patch4:		no-native-menubars.patch

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	octave >= 3.2.0
Requires:	octave-doc >= 3.2.0
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Besides offering an attractive front-end to GNU Octave, an
environment for numerical computation highly compatible with MATLAB,
QtOctave currently also features matrix data entry and display and
some GUI shortcuts to frequently used Octave functions.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .doc-path
%patch1 -p1 -b .filedialog-filters
%patch2 -p1 -b .initialposition
%patch3 -p1 -b .qtinfo
%patch4 -p1

find xmlwidget/qt4/src/ -type f -exec chmod a-x {} \;
find easy_plot/src/ -type f -exec chmod a-x {} \;


%build
cmake "-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}"
%make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%defattr(-,root,root,-)
%doc readme.txt leeme.txt LICENSE_GPL.txt
%{_bindir}/*
%{_datadir}/%{name}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/64x64/apps/*
%exclude %{_datadir}/doc/octave-html
