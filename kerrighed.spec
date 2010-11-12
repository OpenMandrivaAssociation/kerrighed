
Summary: The Kerrighed system (a Linux-based SSI)

%define name kerrighed
%define krgversion 2.4.3
%define linuxversion 2.6.20.21
%define	kernelrelease 1
%define kernelpkgrelease %mkrel %kernelrelease
%define extraversion -krg%{krgversion}-%{kernelrelease}%{distsuffix}
%define kernelkrgversion %{linuxversion}%{extraversion}
%define release %mkrel 2
%define libname %mklibname %name

%define all_x86 i686 x86_64

Name:		%name
Version:	%{krgversion}
Release:	%release

Group:		System/Cluster
License:	GPL
URL:		http://kerrighed.org

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	autoconf >= 2.59, automake >= 1.9, gcc, libtool, docbook-utils, hevea
BuildRequires:  xmlto
#kernel-kerrighed-source-krgversion = 2.4.2-2xos2.0
BuildRequires:  kernel-kerrighed-source-krgversion = %{krgversion}-%{kernelpkgrelease}

BuildRequires: lsb-core, docbook-dtd412-xml, rsync

ExclusiveArch:	%{ix86} x86_64
Requires:	kerrighed-kmodule = %{krgversion}-%{release}, kerrighed-utils = %{krgversion}, %{libname} = %{krgversion}
Source0:	kerrighed-%{krgversion}.tar.bz2
Source10:	compile.h
Source111:	redhat
Patch1:		krg_2.4.4-libkerrighed_libhotplug.c.patch

%description
The Kerrighed meta-package. It depends on the kernel, the module,
tools and libs. The Kerrighed system is a Linux-based SSI.

%package kernel
Summary: The kernel module for Kerrighed kernel %{kernelkrgversion}
Group:		System/Cluster
Requires: kernel-kerrighed-krgversion = %{krgversion}-%{kernelpkgrelease}, kerrighed-utils = %{krgversion}
Provides: kerrighed-kmodule = %{krgversion}

%description kernel
This package provides the kernel module kerrighed.ko needed to make a
Kerrighed cluster work. It works with the %{kernelkrgversion} kernel.

%package utils
Summary: Tools for Kerrighed cluster
Group:		System/Cluster
Requires: %{libname} = %{krgversion}-%{release}

%description utils
This package contains tools to make a fully fonctionnal Kerrighed
cluster, like init scripts. It contains the command krgadm.

%package -n %{libname}
Summary: The Kerrighed library
Group:		System/Cluster
Requires: kerrighed-kmodule = %{krgversion}-%{release}

%description -n %{libname}
This package provides the kerrighed library to use some advanced
features of the Kerrighed OS.

%package python
Summary: The Kerrighed python library
Group:          System/Cluster
Requires: kerrighed-kmodule = %{krgversion}-%{release} python

%description python
This package provides the kerrighed python files

%package -n %{libname}-devel
Summary: The Kerrighed library - development files
Group:		System/Cluster
Provides: kerrighed-devel = %{krgversion}-%{release}, libkerrighed-devel = %{krgversion}-%{release}
Requires: %{libname} = %{krgversion}-%{release}

%description -n %{libname}-devel
This package provides the kerrighed libraries (libkerrighed
development files and static libraries.

%prep
%setup -q
%patch1 -p0
%{__tar} --exclude=iforce-protocol.txt -C /usr/src -cf - kernel-kerrighed-%{kernelkrgversion} | %{__tar} -xf -

%build
rm -rf kernel
ln -sf kernel-kerrighed-%{kernelkrgversion} _kernel 
ln -sf kernel-kerrighed-%{kernelkrgversion} kernel
# fix missing dir
mkdir tools/tools
# kernel always has been built
perl -pi -e "s/false//" modules/Makefile.am
./autogen.sh
%configure \
	--with-kernel=`pwd`/kernel-kerrighed-%{kernelkrgversion} \
	--enable-libkerrighed \
	--enable-module \
	--enable-tools \
	--disable-service \
	--disable-tests \
	--disable-kernel
cp %{SOURCE10} kernel/include/linux/compile.h
%make


%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/etc/init.d
%{__cp} -p %{SOURCE111} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/kerrighed
%{__mkdir} -p $RPM_BUILD_ROOT/lib/modules/%{kernelkrgversion}/extra

%clean
%{__rm} -rf $RPM_BUILD_ROOT
#rm -rf %{_builddir}/linux-%{linuxversion} %{_builddir}/%{name}-%{version}

%post kernel
/sbin/depmod %{kernelkrgversion}

%postun kernel
/sbin/depmod %{kernelkrgversion}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%post utils
/sbin/chkconfig --add kerrighed

%preun utils
/sbin/chkconfig --del kerrighed

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog INSTALL README

%files kernel
%defattr(-,root,root)
%doc README ChangeLog modules/COPYRIGHT
/lib/modules/%{kernelkrgversion}/extra/kerrighed.ko
/lib/modules/%{kernelkrgversion}/extra/freq_limit_filter.ko
/lib/modules/%{kernelkrgversion}/extra/migration_probe.ko
/lib/modules/%{kernelkrgversion}/extra/mosix_load_balancer.ko
/lib/modules/%{kernelkrgversion}/extra/mosix_probe.ko
/lib/modules/%{kernelkrgversion}/extra/remote_cache_filter.ko
/lib/modules/%{kernelkrgversion}/extra/round_robin_balancer.ko
/lib/modules/%{kernelkrgversion}/extra/threshold_filter.ko


%files utils
%defattr(-,root,root)
%{_bindir}/migrate
%{_bindir}/krgcapset
%{_bindir}/krgadm
%{_bindir}/checkpoint
%{_bindir}/restart
%{_bindir}/krg_legacy_scheduler
%{_bindir}/krgcr-run
%{_mandir}/man1/krgadm.1*
%{_mandir}/man7/kerrighed.7*
%{_mandir}/man5/kerrighed_nodes.5*
%{_mandir}/man1/krgcapset.1*
%{_mandir}/man2/krgcapset.2*
%{_mandir}/man1/migrate.1*
%{_mandir}/man2/migrate.2*
%{_mandir}/man2/migrate_self.2*
%{_mandir}/man1/checkpoint.*
%{_mandir}/man1/restart.*
%{_mandir}/man7/kerrighed_capabilities.*
%{_mandir}/man1/krgcr-run.1.lzma
#%config %{_sysconfdir}/default/kerrighed
%{_sysconfdir}/init.d/kerrighed


%files -n %libname
%defattr(-,root,root)
%{_libdir}/libkerrighed.so.2.0.0
%{_libdir}/libkerrighed.so.2
%{_libdir}/libkrgcb.so.1
%{_libdir}/libkrgcb.so.1.0.0

%files python
%{py_puresitedir}/kerrighed.py
%{py_puresitedir}/kerrighed.pyc
%{py_puresitedir}/kerrighed.pyo

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/kerrighed/kerrighed.h
%{_includedir}/kerrighed/capability.h
%{_includedir}/kerrighed/capabilities.h
%{_includedir}/kerrighed/proc.h
%{_includedir}/kerrighed/types.h
%{_includedir}/kerrighed/checkpoint.h
%{_includedir}/kerrighed/kerrighed_tools.h
%{_includedir}/kerrighed/hotplug.h
%{_includedir}/kerrighed/krgnodemask.h
%{_includedir}/kerrighed/libkrgcb.h
%{_libdir}/pkgconfig/kerrighed.pc
%{_libdir}/libkerrighed.la
%{_libdir}/libkerrighed.a
%{_libdir}/libkerrighed.so
%{_libdir}/pkgconfig/krgcb.pc
%{_libdir}/libkrgcb.a
%{_libdir}/libkrgcb.la
%{_libdir}/libkrgcb.so


%changelog
