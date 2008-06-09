
Summary: The Kerrighed system (a Linux-based SSI)

%define name kerrighed
%define krgversion 2.2.1
%define linuxversion 2.6.20
%define	kernelrelease 1
%define kernelpkgrelease %mkrel %kernelrelease
%define extraversion -krg%{krgversion}-%{kernelrelease}%{distsuffix}
%define kernelkrgversion %{linuxversion}%{extraversion}
%define release %mkrel 1
%define libname %mklibname %name

%define all_x86 i686

Name:		%name
Version:	%{krgversion}
Release:	%release

Group:		System/Cluster
License:	GPL
URL:		http://kerrighed.org

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	autoconf >= 2.59, automake >= 1.9, gcc, libtool, docbook-utils, hevea
BuildRequires:  xmlto
BuildRequires:  kernel-kerrighed-source-krgversion = %{krgversion}-%{kernelpkgrelease}

BuildRequires: lsb-core, docbook-dtd412-xml, rsync

ExclusiveArch:	%{ix86}
Requires:	kerrighed-kmodule = %{krgversion}-%{release}, kerrighed-utils = %{krgversion}, %{libname} = %{krgversion}
Source0:	kerrighed-%{krgversion}.tar.gz

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

%package -n %{libname}-devel
Summary: The Kerrighed library - development files
Group:		System/Cluster
Provides: kerrighed-devel = %{krgversion}-%{release}, libkerrighed-devel = %{krgversion}-%{release}
Requires: %{libname} = %{krgversion}-%{release}

%description -n %{libname}-devel
This package provides the kerrighed libraries (libkerrighed and 
libkrgthread) development files and static libraries.

%prep
%setup -q
%{__tar} --exclude=iforce-protocol.txt -C /usr/src -cf - kernel-kerrighed-%{kernelkrgversion} | %{__tar} -xf -
%{__sed} -i 's/EXTRAVERSION = .*/EXTRAVERSION = %{extraversion}/' kernel-kerrighed-%{kernelkrgversion}/Makefile

%build
%configure \
	--with-kernel=`pwd`/kernel-kerrighed-%{kernelkrgversion} \
	--enable-libkerrighed \
	--enable-tools \
	--enable-module \
	--disable-service \
	--disable-tests
%make

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/etc/init.d
%{__cp} -p tools/scripts/init.d/redhat $RPM_BUILD_ROOT%{_sysconfdir}/init.d/kerrighed
%{__mkdir} -p $RPM_BUILD_ROOT/lib/modules/%{kernelkrgversion}/extra

%clean
%{__rm} -rf $RPM_BUILD_ROOT
#rm -rf %{_builddir}/linux-%{linuxversion} %{_builddir}/%{name}-%{version}

%post kernel
/sbin/depmod %{kernelkrgversion}

%postun kernel
/sbin/depmod %{kernelkrgversion}

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%post utils
/sbin/chkconfig --add kerrighed

%preun utils
/sbin/chkconfig --del kerrighed

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog INSTALL README

%files kernel
%defattr(-,root,root)
%doc README ChangeLog modules/CHANGES modules/COPYRIGHT
/lib/modules/%{kernelkrgversion}/extra/kerrighed.ko

%files utils
%defattr(-,root,root)
%doc tools/ChangeLog tools/INSTALL tools/README
%{_bindir}/migrate
%{_bindir}/krgcapset
%{_bindir}/krgadm
%{_bindir}/checkpoint
%{_bindir}/restart
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
#%config %{_sysconfdir}/default/kerrighed
%{_sysconfdir}/init.d/kerrighed


%files -n %libname
%defattr(-,root,root)
%doc libs/ChangeLog libs/INSTALL libs/README
%{_libdir}/libkerrighed.so.1.0.0
%{_libdir}/libkerrighed.so.1


#%files libkrgthread
#%defattr(-,root,root)
#%doc libs/AUTHORS libs/ChangeLog libs/COPYING libs/INSTALL libs/README
#%{_libdir}/libkrgthread.so.1.0.0
#%{_libdir}/libkrgthread.so.1
#%{_libdir}/libkrgthread.so

%files -n %{libname}-devel
%defattr(-,root,root)
%doc libs/ChangeLog libs/INSTALL libs/README
%{_includedir}/kerrighed/kerrighed.h
%{_includedir}/kerrighed/capability.h
%{_includedir}/kerrighed/capabilities.h
%{_includedir}/kerrighed/proc.h
%{_includedir}/kerrighed/comm.h
%{_includedir}/kerrighed/types.h
%{_includedir}/kerrighed/process_group_types.h
%{_includedir}/kerrighed/checkpoint.h
%{_includedir}/kerrighed/kerrighed_tools.h
%{_includedir}/kerrighed/hotplug.h
%{_includedir}/kerrighed/krgnodemask.h
#%{_includedir}/kerrighed/krgthread.h
#%{_includedir}/kerrighed/krg_dsm.h
%{_libdir}/pkgconfig/kerrighed.pc
#%{_libdir}/pkgconfig/krgthread.pc
%{_libdir}/libkerrighed.la
%{_libdir}/libkerrighed.a
#%{_libdir}/libkrgthread.la
#%{_libdir}/libkrgthread.a
%{_libdir}/libkerrighed.so
