#
# spec file for package kanku
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           kanku
# Version gets set by obs-service-tar_scm
Version:        0.0.0
Release:        0.0
License:        GPL-3.0
Summary:        Development and continuous integration made easy
Url:            https://github.com/M0ses/kanku
Group:          Productivity/Networking/Web/Utilities
Source:         %{name}-%{version}.tar.xz
BuildArch:      noarch
BuildRequires:  perl-macros
BuildRequires:  fdupes
BuildRequires:  systemd-rpm-macros

# perl requires for %check
BuildRequires: perl(DBIx::Class::Fixtures)
BuildRequires: perl(Test::Simple)
BuildRequires: perl(YAML)
BuildRequires: perl(Config::Tiny)
BuildRequires: perl(Path::Class)
BuildRequires: perl(Sys::Virt)
BuildRequires: perl(Moose)
BuildRequires: perl(Log::Log4perl)
BuildRequires: perl(MooseX::App::Cmd)
BuildRequires: perl(Dancer2::Plugin::REST)
BuildRequires: perl(MooseX::Singleton)
BuildRequires: perl(Expect)
BuildRequires: perl(Net::SSH2)
BuildRequires: perl(Net::IP)
BuildRequires: perl(Net::OBS::Client)
BuildRequires: perl(XML::Structured)
BuildRequires: perl(DBIx::Class::Migration)
BuildRequires: perl(Template)
BuildRequires: perl(Log::Log4perl)
BuildRequires: perl(Config::Tiny)
BuildRequires: perl(Dancer2::Plugin::DBIC)
BuildRequires: perl(Dancer2::Plugin::Auth::Extensible)
BuildRequires: perl(Dancer2::Plugin::Auth::Extensible::Provider::DBIC)
BuildRequires: perl(File::HomeDir)
BuildRequires: perl(Template::Plugin::Filter::ANSIColor)
BuildRequires: perl(JSON::XS)
BuildRequires: perl(DBIx::Class)
BuildRequires: perl(DBIx::Class::Migration)
BuildRequires: perl(Template::Plugin::Filter::ANSIColor)
BuildRequires: perl(File::LibMagic)
BuildRequires: perl(IO::Uncompress::UnXz)
BuildRequires: perl(Plack)
BuildRequires: perl(Dancer2)
BuildRequires: perl(Dancer2::Plugin::REST)
BuildRequires: perl(XML::XPath)
BuildRequires: perl(Term::ReadKey)
BuildRequires: perl(IPC::Run)
# DBD::SQLite is also provided by perl-DBD-SQLite-Amalgamation
# but perl-DBD-SQLite-Amalgamation is breaks with SQL syntax errors
# at job_histroy_sub table
BuildRequires: perl-DBD-SQLite
BuildRequires: perl(LWP::Protocol::https)
BuildRequires: perl(Mail::Sendmail)
BuildRequires: perl(Archive::Cpio)
BuildRequires: perl(Dancer2)
BuildRequires: perl(Dancer2::Plugin)
BuildRequires: perl(Dancer2::Plugin::REST)
BuildRequires: perl(Dancer2::Plugin::DBIC)
BuildRequires: perl(Dancer2::Plugin::WebSocket)
BuildRequires: perl(Dancer2::Plugin::Auth::Extensible)
BuildRequires: perl(Net::AMQP::RabbitMQ)
BuildRequires: perl(UUID)

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires: kanku-cli
Requires: kanku-web
Requires: kanku-worker
Requires: kanku-scheduler
Requires: kanku-dispatcher
Requires: kanku-triggerd

%description
TODO: add some meaningful description
 to be more verbose

%prep
%setup -q

%build
/bin/true

%install
make install DESTDIR=%{buildroot}
%fdupes %{buildroot}/opt/kanku/share
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rckanku-web
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rckanku-worker
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rckanku-dispatcher
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rckanku-scheduler
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rckanku-triggerd

%check
# FIXME
#prove -Ilib t/000_use.t

%files
%exclude /etc
%exclude /usr

%package common
Summary: Common files for kanku

Recommends: osc 
Recommends: perl(IO::Uncompress::UnXz)
Recommends: apache2
Requires: libvirt-daemon-qemu qemu-kvm libvirt-daemon-config-network libvirt-daemon-config-nwfilter
Requires: perl(DBIx::Class::Fixtures)
Requires: perl(Test::Simple)
Requires: perl(YAML)
Requires: perl(Config::Tiny)
Requires: perl(Path::Class)
Requires: perl(Sys::Virt)
Requires: perl(Moose)
Requires: perl(Log::Log4perl)
Requires: perl(MooseX::App::Cmd)
Requires: perl(Dancer2::Plugin::REST)
Requires: perl(MooseX::Singleton)
Requires: perl(Expect)
Requires: perl(Net::SSH2)
Requires: perl(Net::IP)
Requires: perl(Net::OBS::Client)
Requires: perl(XML::Structured)
Requires: perl(DBIx::Class::Migration)
Requires: perl(Template)
Requires: perl(Log::Log4perl)
Requires: perl(Config::Tiny)
Requires: perl(Dancer2::Plugin::DBIC)
Requires: perl(Dancer2::Plugin::Auth::Extensible)
Requires: perl(Dancer2::Plugin::Auth::Extensible::Provider::DBIC)
Requires: perl(File::HomeDir)
Requires: perl(Template::Plugin::Filter::ANSIColor)
Requires: perl(JSON::XS)
Requires: perl(DBIx::Class)
Requires: perl(DBIx::Class::Migration)
Requires: perl(Template::Plugin::Filter::ANSIColor)
Requires: perl(File::LibMagic)
Requires: perl(IO::Uncompress::UnXz)
Requires: perl-Plack
Requires: perl(Dancer2)
Requires: perl(Dancer2::Plugin::REST)
Requires: perl(XML::XPath)
Requires: perl(Term::ReadKey)
Requires: perl(IPC::Run)
# DBD::SQLite is also provided by perl-DBD-SQLite-Amalgamation
# but perl-DBD-SQLite-Amalgamation is breaks with SQL syntax errors
# at job_histroy_sub table
Requires: perl-DBD-SQLite
Requires: perl(LWP::Protocol::https)
Requires: perl(Mail::Sendmail)
Requires: perl(Archive::Cpio)
Requires: logrotate

Conflicts: perl-DBD-SQLite-Amalgamation

%description common
TODO:
 add a useful description


%files common
%defattr(-,root,root)
%doc README.md TODO

%dir /opt/kanku
%dir /opt/kanku/var
%dir /opt/kanku/var/log
%dir /opt/kanku/var/cache
%dir /opt/kanku/lib
%dir /opt/kanku/lib/Kanku
%dir /opt/kanku/lib/Kanku/Daemon

# share contains database related stuff
%dir /opt/kanku/share/
/opt/kanku/share/fixtures
/opt/kanku/share/migrations

%dir /opt/kanku/bin
%attr(755,root,root) /opt/kanku/bin/kanku
%attr(755,root,root) /opt/kanku/bin/kanku-network-setup.pl

%dir /opt/kanku/etc/
%ghost /opt/kanku/etc/config.yml
%config /opt/kanku/etc/console-log.conf
%config /opt/kanku/etc/kanku-network-setup-logging.conf
%config /opt/kanku/etc/config.yml.template

%dir /opt/kanku/etc/templates
%dir /opt/kanku/etc/templates/examples-vm/
%dir /opt/kanku/etc/templates/cmd
%config /opt/kanku/etc/templates/cmd/setup.config.yml.tt2
%config /opt/kanku/etc/templates/cmd/init.tt2
%config /opt/kanku/etc/templates/examples-vm/obs-server-26.tt2
%config /opt/kanku/etc/templates/examples-vm/sles11sp3.tt2
%config /opt/kanku/etc/templates/examples-vm/obs-server.tt2

%dir /opt/kanku/etc/jobs
%dir /opt/kanku/etc/jobs/examples
%config /opt/kanku/etc/jobs/examples/obs-server.yml
%config /opt/kanku/etc/jobs/examples/obs-server-26.yml
%config /opt/kanku/etc/jobs/examples/sles11sp3.yml

%config(noreplace) /opt/kanku/etc/log4perl.conf

%dir /etc/sudoers.d
%config (noreplace)  /etc/sudoers.d/kanku

%exclude %dir /etc/profile.d
%config /etc/profile.d/kanku.sh

%exclude %dir /etc/logrotate.d/
%config /etc/logrotate.d/kanku-common

/opt/kanku/lib/Kanku/Handler/
/opt/kanku/lib/Kanku/Roles/
/opt/kanku/lib/Kanku/Schema/
/opt/kanku/lib/Kanku/Setup/
/opt/kanku/lib/Kanku/Util/
/opt/kanku/lib/Kanku/Task/
/opt/kanku/lib/OpenStack/
/opt/kanku/lib/Kanku/Config.pm
/opt/kanku/lib/Kanku/Handler.pod
/opt/kanku/lib/Kanku/Notifier
/opt/kanku/lib/Kanku/Job.pm
/opt/kanku/lib/Kanku/RabbitMQ.pm
/opt/kanku/lib/Kanku/Schema.pm
/opt/kanku/lib/Kanku/JobList.pm
/opt/kanku/lib/Kanku/Task.pm
/opt/kanku/lib/Kanku/Airbrake.pm
/opt/kanku/lib/Kanku/NotifyQueue.pm

%dir /opt/kanku/lib/Kanku/WebSocket
/opt/kanku/lib/Kanku/WebSocket/Notification.pm
/opt/kanku/lib/Kanku/WebSocket/Session.pm

%dir /opt/kanku/lib/Kanku/Airbrake
/opt/kanku/lib/Kanku/Airbrake/Dummy.pm

%dir /opt/kanku/lib/Kanku/LibVirt
/opt/kanku/lib/Kanku/LibVirt/HostList.pm

%dir /opt/kanku/lib/Kanku/Dispatch/
/opt/kanku/lib/Kanku/Dispatch/Local.pm


%package cli
Summary: Command line client for kanku
Requires: kanku-common
Requires: libvirt-client

%description cli
Command line client for kanku, mainly used for setup tasks
and in developer mode

%files cli
%dir /opt/kanku/views/cli/
%dir /opt/kanku/views/cli/rjob
/opt/kanku/views/cli/*.tt
/opt/kanku/views/cli/rjob/*.tt
/opt/kanku/lib/Kanku/Cmd/
/opt/kanku/lib/Kanku/Cmd.pm

%package web
Summary: WebUI for kanku
Requires: kanku-common
Requires: perl(Dancer2::Plugin::WebSocket)
Requires: perl(Twiggy)
Requires: perl(Mail::Message::Body::String)
Requires: perl(Mail::Transport::Send)
Requires: perl(Net::AMQP::RabbitMQ)
Requires: perl(UUID)
#Requires: %{?systemd_requires}

%description web
TODO:
 add a useful description

%pre web
%service_add_pre kanku-web.service

%post web
%service_add_post kanku-web.service

%preun web
%service_del_preun kanku-web.service

%postun web
%service_del_postun kanku-web.service

%files web
%attr(755,root,root) /opt/kanku/bin/kanku-app.psgi
%dir /opt/kanku/views/
%{_unitdir}/kanku-web.service
%{_sbindir}/rckanku-web
/opt/kanku/views/admin.tt
/opt/kanku/views/guest.tt
/opt/kanku/views/index.tt
/opt/kanku/views/job.tt
/opt/kanku/views/notify.tt
/opt/kanku/views/notify_disabled.tt
/opt/kanku/views/job_history.tt
/opt/kanku/views/job_result.tt
%dir /opt/kanku/views/layouts
/opt/kanku/views/layouts/main.tt
/opt/kanku/views/login.tt
%dir /opt/kanku/views/login
/opt/kanku/views/login/denied.tt
/opt/kanku/views/admin.tt
/opt/kanku/views/settings.tt
/opt/kanku/views/signup.tt
/opt/kanku/views/pwreset.tt
/opt/kanku/views/reset_password.tt

%dir /etc/apache2
%dir /etc/apache2/conf.d
%config (noreplace) /etc/apache2/conf.d/kanku.conf

# public contains css/js/bootstrap/jquery etc
/opt/kanku/public/
/opt/kanku/lib/Kanku.pm
/opt/kanku/lib/Kanku/REST.pm

%package worker
Summary: Worker daemon for kanku

Requires: kanku-common
#Requires: %{?systemd_requires}
Requires: perl(Net::AMQP::RabbitMQ)
Requires: perl(UUID)
Requires: perl(Sys::CPU)
Requires: perl(Sys::LoadAvg)
Requires: perl(Sys::MemInfo)

%description worker
A simple remote worker for kanku based on RabbitMQ

%pre worker
%service_add_pre kanku-worker.service

%post worker
%service_add_post kanku-worker.service

%preun worker
%service_del_preun kanku-worker.service

%postun worker
%service_del_postun kanku-worker.service

%files worker
%{_unitdir}/kanku-worker.service
%{_sbindir}/rckanku-worker
/opt/kanku/bin/kanku-worker
/opt/kanku/lib/Kanku/Daemon/Worker.pm

%package dispatcher
Summary: Dispatcher daemon for kanku

Requires: kanku-common
#Requires: %{?systemd_requires}
Requires: perl(Net::AMQP::RabbitMQ)
Recommends: rabbitmq-server

%description dispatcher
A simple dispatcher for kanku based on RabbitMQ

%pre dispatcher
%service_add_pre kanku-dispatcher.service

%post dispatcher
%service_add_post kanku-dispatcher.service

%preun dispatcher
%service_del_preun kanku-dispatcher.service

%postun dispatcher
%service_del_postun kanku-dispatcher.service

%files dispatcher
%{_unitdir}/kanku-dispatcher.service
%{_sbindir}/rckanku-dispatcher
/opt/kanku/bin/kanku-dispatcher
/opt/kanku/lib/Kanku/Daemon/Dispatcher.pm
/opt/kanku/lib/Kanku/Dispatch/RabbitMQ.pm

%package scheduler
Summary: Scheduler daemon for kanku
Requires: kanku-common
#Requires: %{?systemd_requires}

%description scheduler
A simple scheduler for kanku based on RabbitMQ

%pre scheduler
%service_add_pre kanku-scheduler.service

%post scheduler
%service_add_post kanku-scheduler.service

%preun scheduler
%service_del_preun kanku-scheduler.service

%postun scheduler
%service_del_postun kanku-scheduler.service

%files scheduler
%attr(755,root,root) /opt/kanku/bin/kanku-scheduler
/opt/kanku/lib/Kanku/Daemon/Scheduler.pm
%{_unitdir}/kanku-scheduler.service
%{_sbindir}/rckanku-scheduler

%package triggerd
Summary: Trigger daemon for kanku
Requires: kanku-common
#Requires: %{?systemd_requires}

%description triggerd
A simple triggerd for kanku based on RabbitMQ

%pre triggerd
%service_add_pre kanku-triggerd.service

%post triggerd
%service_add_post kanku-triggerd.service

%preun triggerd
%service_del_preun kanku-triggerd.service

%postun triggerd
%service_del_postun kanku-triggerd.service

%files triggerd
%attr(755,root,root) /opt/kanku/bin/kanku-triggerd
%dir /opt/kanku/lib/Kanku/Listener
/opt/kanku/lib/Kanku/Daemon/TriggerD.pm
/opt/kanku/lib/Kanku/Listener/RabbitMQ.pm
%{_unitdir}/kanku-triggerd.service
%{_sbindir}/rckanku-triggerd


%package doc
Summary: Documentation files for kanku

%description doc
This package contains the documentation files for kanku

%files doc
%{_defaultdocdir}/kanku/



%changelog
