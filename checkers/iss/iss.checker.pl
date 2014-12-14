#!/usr/bin/perl -wl

use IO::Socket::INET;
use IO::Select;

use feature ':5.10';
no warnings 'experimental::smartmatch';

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) =
  (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);
my ($mode, $ip) = splice @ARGV, 0, 2;
my @chars = qw/A T G C/;
my @alph = ('A' .. 'Z', 'a' .. 'z');

warn 'Invalid input. Empty mode or ip address.' and exit $INTERNAL_ERROR
  unless defined $mode and defined $ip;
warn 'Invalid mode.' and exit $INTERNAL_ERROR unless $mode ~~ %MODES;
exit $MODES{$mode}->(@ARGV);

sub check {
  return $SERVICE_OK;
}

sub get {
  my ($id, $flag, $line, $data) = @_;

  my $h = IO::Socket::INET->new(PeerAddr => "$ip:31337", Proto => 'tcp', Timeout => 10)
    or return $SERVICE_FAIL;
  my $s = IO::Select->new($h);

  $line .= $alph[rand @alph] for 1 .. 32;
  $h->send("$id $line\n");
  return $SERVICE_FAIL unless $s->can_read(5);
  $h->recv($data, 1024);
  chomp $data;
  return $FLAG_GET_ERROR unless $flag eq $data;

  $h->close;
  return $SERVICE_OK;
}

sub put {
  my ($id, $flag, $data, $chain) = @_;

  my $h = IO::Socket::INET->new(PeerAddr => "$ip:31337", Proto => 'tcp', Timeout => 10)
    or return $SERVICE_FAIL;
  my $s = IO::Select->new($h);

  $chain .= $chars[rand @chars] for 1 .. 12;

  $h->send("$chain $flag\n");
  return $SERVICE_FAIL unless $s->can_read(5);
  $h->recv($data, 1024);
  chomp $data;
  return $SERVICE_CORRUPT unless $flag eq $data;

  $h->close;
  print STDOUT $chain;
  return $SERVICE_OK;
}
