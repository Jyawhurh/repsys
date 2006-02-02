%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%%d.%%d'%%v" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define maxver %(python -c "import sys; a,b=sys.version_info[:2]; print%'%%d.%%d'%%(a,b+1)" 2>/dev/null || echo PYTHON-NOT-FOUND) 
%define minver %py_ver
%define py_prefix  %(python -c "import sys; print sys.prefix" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_libdir  %{py_prefix}/%{_lib}/python%{py_ver}
%define py_sitedir %{py_libdir}/site-packages

%define repsys_version 1.5.4

Name: repsys
Version: 1.6.0
Release: 1mdk
Summary: Tools for Mandriva Linux repository access and management
Group: Development/Other
Source: %{name}-%{repsys_version}.tar.bz2
License: GPL
URL: http://qa.mandriva.com/twiki/bin/view/Main/RepositorySystem
Prefix: %{_prefix}
BuildArch: noarch
Buildrequires: python-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python 
BuildRequires: python-devel
Requires: python-cheetah

%description
Tools for Mandriva Linux repository access and management.

%prep
%setup -q -n %{name}-%{repsys_version}

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot}
# Using compile inline since niemeyer's python macros still not available on mdk rpm macros
find %{buildroot}%{py_sitedir} -name '*.pyc' -exec rm -f {} \; 
python -c "import sys, os, compileall; br='%{buildroot}'; compileall.compile_dir(sys.argv[1], ddir=br and 
(sys.argv[1][len(os.path.abspath(br)):]+'/') or None)" %{buildroot}%{py_sitedir}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_datadir}/repsys/
mkdir -p %{buildroot}%{_bindir}/
install -m 0644 repsys.conf %{buildroot}%{_sysconfdir}/repsys.conf
install -m 0755 rebrand-mdk %{buildroot}%{_datadir}/repsys/rebrand-mdk
install -m 0755 getsrpm-mdk %{buildroot}%{_bindir}/getsrpm-mdk
install -m 0755 create-srpm %{buildroot}%{_datadir}/repsys/create-srpm

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc repsys.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/repsys.conf
%defattr(0755,root,root,0755)
%{_bindir}/repsys
%{_bindir}/getsrpm-mdk
%{_datadir}/repsys/rebrand-mdk
%{_datadir}/repsys/create-srpm
%{py_sitedir}/RepSys

# MAKE THE CHANGES IN CVS: NO PATCH OR SOURCE ALLOWED

%changelog
* Thu Feb 02 2006 Andreas Hasenack <andreas@mandriva.com> 1.6.0-1mdk
- version 1.6.0, see CVS changelog

* Wed Dec  7 2005 Frederic Lepied <flepied@mandriva.com> 1.5.4-1mdk
- switch to cvs

* Fri Oct 21 2005 Frederic Lepied <flepied@mandriva.com> 1.5.3.1-4.1mdk
- add svn+ssh access method

* Fri Sep 30 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-09-30 18:25:48 (979)
- releasing 1.5.3.1-4mdk

* Fri Sep 30 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-09-30 18:10:53 (978)
- fixed author's email
- fixed mandriva logo url

* Fri Sep 30 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-09-30 17:41:45 (977)
- fixed mime-type of the repsys-mdk.patch

* Tue Jul 26 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-07-26 04:48:46 (441)
- Changes on behalf of Oden Eriksson
- update S1
- lib64 fixes
- this is no noarch package
- rpmlint fixes

* Wed Jun 29 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-06-29 04:50:47 (257)
- Upload new spec

* Wed Jun 29 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-06-29 04:44:48 (256)
- Fixed ugly type on url type svn+ssh

* Tue Jun 28 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-06-28 07:22:47 (248)
- Update repsys to match new changelog requirements ( just release keep unchanged )
- Update getsrpm-mdk to genrate srpm with changelog
- Fixed regexp for unicode/color chars in terminal ( thanks to aurelio )

* Tue Jun 14 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-06-14 05:04:31 (206)
- Start to fix builds on x86_64 archs.

* Wed Jun 08 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-06-08 04:48:55 (151)
- Fixed patch for get real changelog and version

* Sun May 29 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-29 13:08:25 (147)
- Added changelog patch to match mdk style

* Fri May 27 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-27 10:26:17 (146)
- Added rebrand script for match release number with svn
- Added wrapper script for get srpms ready for submit to cluster compilation

* Fri May 27 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-27 09:46:09 (145)
- Added suggested changes by neoclust

* Fri May 27 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-27 04:23:34 (144)
- Added initial users on default

* Wed May 25 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-25 11:10:18 (143)
- Added a initial changelog until repsys submit is working

* Wed May 25 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-25 10:28:57 (142)
- No bziped patches

* Wed May 25 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-05-25 10:22:47 (141)
- Initial import of repsys package
