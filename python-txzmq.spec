#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define	module	txZMQ
Summary:	Twisted bindings for ZeroMQ
Name:		python-txzmq
Version:	0.7.3
Release:	2
License:	GPL v2
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/t/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	8064422e590f859bf9c5aedf94af5a5c
URL:		http://pypi.python.org/pypi/txZMQ
Patch0:		0001-Disable-epgm-test.patch
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-TwistedCore
BuildRequires:	python-devel
BuildRequires:	python-nose
BuildRequires:	python-setuptools
BuildRequires:	python-six
BuildRequires:	python-zmq >= 13.0.0
%endif
Requires:	python-TwistedCore >= 10.0
Requires:	python-six
Requires:	python-zmq >= 13.0.0
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools
BuildRequires:	python3-six
BuildRequires:	python3-twisted-core
BuildRequires:	python3-zmq >= 13.0.0
%endif
BuildArch:	noarch

%description
txZMQ allows to integrate easily ZeroMQ sockets into Twisted event
loop (reactor).

%package -n python3-txzmq
Summary:	Twisted bindings for ZeroMQ
Group:		Development/Languages
Requires:	python3-six
Requires:	python3-twisted-core
Requires:	python3-zmq >= 13.0.0

%description -n python3-txzmq
txZMQ allows to integrate easily ZeroMQ sockets into Twisted event
loop (reactor).

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

# getting this error with python-setuptools and python-distribute: http://stackoverflow.com/q/8295644
%{__sed} -i -e '/install_requires/d' setup.py

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with tests}
PYTHONPATH=$(pwd) nosetests-%{py_ver}

%if %{with python3}
PYTHONPATH=$(pwd) nosetests-%{py3_ver}
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/txzmq/test

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/txzmq/test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py_sitescriptdir}/txzmq
%{py_sitescriptdir}/txZMQ-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-txzmq
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py3_sitescriptdir}/txzmq
%{py3_sitescriptdir}/txZMQ-%{version}*.egg-info
%endif
