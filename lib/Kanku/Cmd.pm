# Copyright (c) 2016 SUSE LLC
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
#
package Kanku::Cmd;

use Moose;

extends qw(MooseX::App::Cmd);

use Log::Log4perl;
use Kanku::Config;

Log::Log4perl->init("$FindBin::Bin/../etc/console-log.conf");
Kanku::Config->initialize(class => "KankuFile");

__PACKAGE__->meta->make_immutable();

1;
