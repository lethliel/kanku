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
package Kanku::Handler::OBSCheck;

use Moose;
use Kanku::Util::DoD;
use Try::Tiny;
use Data::Dumper;
with 'Kanku::Roles::Handler';
with 'Kanku::Roles::Logger';

has dod_object => (
  is      =>'rw',
  isa     =>'Object',
  lazy    => 1,
  default => sub  {
    my $self = shift;
    Kanku::Util::DoD->new(
      skip_all_checks     => $self->skip_all_checks,
      skip_check_project  => $self->skip_check_project,
      skip_check_package  => $self->skip_check_package,
      project             => $self->project,
      package             => $self->package,
      api_url             => $self->api_url,
      use_cache           => $self->use_cache,
    )
  },
);

has ['api_url','project','package'] => (is=>'rw',isa=>'Str',required=>1);

has '+api_url' => (default=>"https://api.opensuse.org");

has ['base_url','repository']       => (is=>'rw',isa=>'Str');

has _changed => (is=>'rw',isa=>'Bool',default=>0);

has _binary => (is=>'rw',isa=>'HashRef',lazy=>1,default=>sub { { } });

has [qw/skip_check_project skip_check_package skip_download/ ] => (is => 'ro', isa => 'Bool',default => 0 );
has [qw/offline use_cache skip_all_checks/ ] => (is => 'rw', isa => 'Bool',default => 0 );


has gui_config => (
  is => 'ro',
  isa => 'ArrayRef',
  lazy => 1,
  default => sub {
      [
        {
          param => 'api_url',
          type  => 'text',
          label => 'API URL'
        },
        {
          param => 'skip_all_checks',
          type  => 'checkbox',
          label => 'Skip all checks'
        },
        {
          param => 'project',
          type  => 'text',
          label => 'Project'
        },
        {
          param => 'package',
          type  => 'text',
          label => 'Package'
        },
        {
          param => 'repository',
          type  => 'text',
          label => 'Repository'
        },
      ];
  }
);

sub prepare {
  my $self      = shift;
  my $ctx       = $self->job()->context();

  $self->offline(1)           if ( $ctx->{offline} );
  $self->use_cache(1)         if ( $ctx->{use_cache} );
  $self->skip_all_checks(1)   if ( $ctx->{skip_all_checks} );

  return {
    state => 'succeed',
    message => "Preparation finished successfully"
  };
}

sub execute {
  my $self = shift;

  if ($self->offline) {
    return $self->get_from_history();
  }

  my $last_run  = $self->last_run_result();
  my $dod       = $self->dod_object();

  if ( $self->base_url ) {
    # prevent from errors because of missing trailing slash
    if (  $self->base_url !~ q{/$} ) { $self->base_url($self->base_url.'/') }
    $dod->base_url($self->base_url);
  }
  $dod->base_url($self->base_url)     if $self->base_url;
  $dod->repository($self->repository) if $self->repository;

  my $binary    = $dod->get_image_file_from_url();

  my $ctx       = $self->job()->context();

  # check if $binary is HashRef to prevent Moose from
  # crashing the whole application with an exception
  # if value is undef
  $self->_binary($binary) if ( ref($binary) eq "HashRef");

  # Don`t check for skipping if no last run found
  # or Job was triggered instead of scheduled
  # triggered jobs coming from external
  # and have higher priority
  if (
      $last_run and
      ! $self->job->triggered and
      ! $self->skip_all_checks
  ) {
    # TODO: implement offline mode
    #
    my $prep_result = $last_run->{prepare}->{binary};
    foreach my $key (qw/mtime filename size/) {
      my $bv = $binary->{$key} || '';
      my $pv = $prep_result->{$key} || '';
      if ( $bv ne $pv ) {
        $self->logger->debug("Change detected");
        $self->_changed(1);
      }
    }
  } else {
    $self->_changed(1);
  }

  if ( ! $self->_changed ) {
    $self->logger->debug("Setting job skipped");
    $self->job->skipped(1);
    return {
      code    => 0,
      state   => 'skipped',
      message => "execution skipped because binary did not change since last run"
    };
  }

  if ( ! $self->use_cache ) {
    try {
      $dod->check_before_download();
    }
    catch {
      my $e = $_;
      if (! ref($e) && $e =~ /^(Project|Package) not ready yet$/ ) {
        $self->logger->warn($e);
        $self->job->skipped(1);
        return {
          code    => 0,
          state   => 'skipped',
          message => $e
        };
      }
      die $e;
    };
  }

  $ctx->{vm_image_url}   = $binary->{url};
  $ctx->{obs_direct_url} = $binary->{bin_url};
  $ctx->{public_api}     = $binary->{public_api};
  $ctx->{obs_filename}   = $binary->{filename};
  $self->logger->debug("obs_direct_url = '".( $ctx->{obs_direct_url} || '')."'");
  $ctx->{obs_username}   = $binary->{obs_username};
  $ctx->{obs_password}   = $binary->{obs_password};
  $ctx->{obs_project}    = $self->project;
  $ctx->{obs_package}    = $self->package;

  if (!$ctx->{vm_image_url} and !$ctx->{obs_direct_url}) {
    die "Neither vm_image_url nor obs_direct_url found\n"
      ."HINT: Try \n\nosc api /build/"
      . $dod->project ."/"
      . $dod->repository ."/"
      . $dod->arch ."/"
      . $dod->package
      . "\n\nfor further debugging\n"
    ;
  }

  $self->update_history();

  return {
    code    => 0,
    state   => 'succeed',
    message => "Sucessfully checked project ".$self->project." under url "
                 .$self->api_url ."\n"
                 ." ("
                 .    "vm_image_url: $ctx->{vm_image_url}, "
                 .    "obs_direct_url: $ctx->{obs_direct_url}"
                 .")"
  };
}

sub update_history {
  my $self = shift;

  my $rs = $self->schema->resultset('ObsCheckHistory')->update_or_create(
    {
      api_url     => $self->api_url,
      project     => $self->project,
      package     => $self->package,
      check_time  => time(),
      vm_image_url=> $self->job->context->{vm_image_url}
    },{
      unique_obscheck => [$self->api_url,$self->project,$self->package]
    }
  );

};

sub get_from_history {
  my $self = shift;
  my $ctx  = $self->job->context;
  my $rs = $self->schema->resultset('ObsCheckHistory')->find(
    {
      api_url     => $self->api_url,
      project     => $self->project,
      package     => $self->package,
    }
  );

  die "Could not found last entry in database" if (! $rs);

  $ctx->{vm_image_url} = $rs->vm_image_url;

  return {
    code    => 0,
    state   => 'succeed',
    message => "Sucessfully fetch vm_image_url '".$ctx->{vm_image_url}."' from database"
  };

};

1;
__END__

=head1 NAME

Kanku::Handler::OBSCheck

=head1 SYNOPSIS

Here is an example how to configure the module in your jobs file or KankuFile

  -
    use_module: Kanku::Handler::OBSCheck
    options:
      api_url: https://api.opensuse.org
      project: home:M0ses:kanku:images
      package: openSUSE-Leap-42.1-JeOS
      use_cache: 1


=head1 DESCRIPTION

This handler downloads a file from a given url to the local filesystem and sets vm_image_file.

=head1 OPTIONS

  api_url             : API url to OBS server

  base_url            : Url to use for download

  project             : project name in OBS

  package             : package name to search for in project

  repository          : repository name to search for in project/package

  skip_all_checks     : skip checks all checks on project/package on obs side before downloading image

  skip_check_project  : skip check of project state before downloading image

  skip_check_package  : skip check of package state before downloading image

  skip_download       : no changes detected in OBS skip downloading image file if found in cache

  offline             : proceed in offline mode ( skip download and set use_cache in context)

  use_cache           : use cached files if found in users cache directory

=head1 CONTEXT

=head2 getters

  offline

  use_cache

  skip_all_checks


=head2 setters

  vm_image_url

=head1 DEFAULTS

NONE

=cut

