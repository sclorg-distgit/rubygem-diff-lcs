%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name diff-lcs

# %%check section needs rspec-expectations, however rspec-expectations depends
# on diff-lcs.
%{!?need_bootstrap:	%global	need_bootstrap	1}

Summary: Provide a list of changes between two sequenced collections
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.2.5
Release: 6%{?dist}
Group: Development/Languages
#lib/diff/lcs.rb is Artistic or Ruby or BSD
#lib/diff/lcs/*.rb is GPLv2+ or Artistic or Ruby or BSD
#License.rdoc states GPLv2+ or Artistic or MIT
License: (GPLv2+ or Artistic or MIT) and (GPLv2+ or Artistic or Ruby or BSD) and (Artistic or Ruby or BSD)
URL: https://github.com/halostatue/diff-lcs
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Make test suite RSpec 3.x compatible.
# https://github.com/halostatue/diff-lcs/pull/32
Patch0: rubygem-diff-lcs-1.2.5-Fix-RSpec-3.x-compatibility.patch

Requires:       %{?scl_prefix_ruby}ruby(release)
Requires:       %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{?need_bootstrap} < 1
BuildRequires: %{?scl_prefix}rubygem(rspec)
%endif
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildArch: noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Diff::LCS is a port of Algorithm::Diff that uses the McIlroy-Hunt longest
common subsequence (LCS) algorithm to compute intelligent differences between
two sequenced enumerable containers. The implementation is based on Mario I.
Wolczko's Smalltalk version (1.2, 1993) and Ned Konz's Perl version
(Algorithm::Diff).

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation

Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
This package contains documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c  -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}/%{_bindir}

cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}
cp -a .%{_bindir}/* %{buildroot}/%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f |xargs chmod a+x

# Fix shebangs.
sed -i 's|^#!.*|#!/usr/bin/ruby|' %{buildroot}%{gem_instdir}/bin/{htmldiff,ldiff}

%if 0%{?need_bootstrap} < 1

%check
pushd .%{gem_instdir}
# https://github.com/halostatue/diff-lcs/issues/1
sed -i '/Diff::LCS.patch(s1, diff_s1_s2).should == s2/ s/^/#/' spec/issues_spec.rb

# https://github.com/halostatue/diff-lcs/issues/33
%{?scl:scl enable %{scl} - << \EOF}
rspec -rdiff/lcs -rdiff/lcs/hunk spec
%{?scl:EOF}
popd
%endif

%files
%{_bindir}/ldiff
%{_bindir}/htmldiff
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/License.rdoc
%doc %{gem_instdir}/docs
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Contributing.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/autotest
%{gem_instdir}/spec

%changelog
* Mon Feb 22 2016 Pavel Valena <pvalena@redhat.com> - 1.2.5-6
- Rebuilt for rh-ror42

* Fri Jan 16 2015 Josef Stribny <jstribny@redhat.com> - 1.2.5-2
- Enable tests

* Fri Jan 16 2015 Josef Stribny <jstribny@redhat.com> - 1.2.5-1
- Update to 1.2.5

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.3-5
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Thu Feb 06 2014 Josef Stribny <jstribny@redhat.com> - 1.1.3-4
- Fix licensing

* Wed Nov 20 2013 Josef Stribny <jstribny@redhat.com> - 1.1.3-3
- Allow test suite.

* Tue May 21 2013 Josef Stribny <jstribny@redhat.com> - 1.1.3-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Jul 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.3-1
- Update to Diff-lcs 1.1.3.
- Specfile cleanup.

* Fri Mar 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-8
- Rebuilt for scl.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-7
- Rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-2
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-1
- Package generated by gem2rpm
- Strip useless shebangs
- Fix up License
