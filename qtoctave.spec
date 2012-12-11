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


%changelog
* Thu May 03 2012 Cristobal Lopez Silla <tobal@mandriva.org> 0.10.1-1mdv2012.0
+ Revision: 795700
- updated to new version and spec and patches.
- updated to new version and spec and patches.

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8.2-3mdv2011.0
+ Revision: 614682
- the mass rebuild of 2010.1 packages

* Wed Feb 17 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 0.8.2-2mdv2010.1
+ Revision: 506896
- Rebuild

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 0.8.2-1mdv2010.1
+ Revision: 462520
- Update to new version 0.8.2
- Sync patches with Debian
- Add patch to fix detection of QT >= 4.5

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 0.8.1-2mdv2010.0
+ Revision: 442630
- rebuild

* Mon Feb 16 2009 Frederik Himpe <fhimpe@mandriva.org> 0.8.1-1mdv2009.1
+ Revision: 341097
- Update to version 0.8.1
- Use cmake option to disable rpath instead of using chrpath
- Sync patches with Debian, disable fuz=0 as Debian's patches
  are fuzzy

* Sun Aug 10 2008 David Walluck <walluck@mandriva.org> 0.7.4-1mdv2009.0
+ Revision: 270164
- 0.7.4

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Sat May 03 2008 Funda Wang <fwang@mandriva.org> 0.6.3-2mdv2009.0
+ Revision: 200671
- drop file dependency

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 02 2007 David Walluck <walluck@mandriva.org> 0.6.3-1mdv2008.1
+ Revision: 94414
- fix whitespace in spec
- import qtoctave


* Sat Aug 11 2007 Jorge Torres <jorge@fedoraproject.org> 0.5-1.20070811svn
- Initial build
