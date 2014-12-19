#!/usr/bin/perl -wl

use IO::Socket::INET;
use IO::Select;

use feature ':5.10';
no warnings 'experimental::smartmatch';
my $port = 1013;

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) =
  (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);
my ($mode, $ip) = splice @ARGV, 0, 2;
my @chars = qw/A T G C/;
my @alph = ('A' .. 'F', '0' .. '9');

warn 'Invalid input. Empty mode or ip address.' and exit $INTERNAL_ERROR
  unless defined $mode and defined $ip;
warn 'Invalid mode.' and exit $INTERNAL_ERROR unless $mode ~~ %MODES;
exit $MODES{$mode}->(@ARGV);

sub check {
  my $h = IO::Socket::INET->new(PeerAddr => "$ip:$port", Proto => 'tcp', Timeout => 10)
    or return $SERVICE_FAIL;
  my $s = IO::Select->new($h);

  $chain .= $chars[rand @chars] for 1 .. 14;
  $fake .= $alph[rand @alph] for 1 .. 31;
  $fake .= "=";

  $h->send("$chain $fake\n");
  do {
    return $SERVICE_FAIL unless $s->can_read(5);
    $h->recv($data, 1024);
    $buf .= $data;
  } while ($buf !~ /\n/ and length $buf < 1024);

  chomp $buf;
  return $SERVICE_CORRUPT unless $fake eq $buf;

  undef $buf;
  my $check = $chain;
  substr($check, rand length $check, 1, $chars[rand @chars]);
  $check .= $chars[rand @chars] if rand(2) > 1;

  $h->send("$check\n");
  do {
    return $SERVICE_FAIL unless $s->can_read(5);
    $h->recv($data, 1024);
    $buf .= $data;
  } while ($buf !~ /\n/ and length $buf < 1024);

  return $SERVICE_CORRUPT if $buf !~ /PATTERN MATCHED : (.*?) (.*?)\n/ or $2 ne $fake;

  return $SERVICE_OK;
}

sub put {
  my ($id, $flag, $data, $chain) = @_;

  my $h = IO::Socket::INET->new(PeerAddr => "$ip:$port", Proto => 'tcp', Timeout => 10)
    or return $SERVICE_FAIL;
  my $s = IO::Select->new($h);

  $chain .= $chars[rand @chars] for 1 .. 14;

  $h->send("$chain $flag\n");
  do {
    return $SERVICE_FAIL unless $s->can_read(5);
    $h->recv($data, 1024);
    $buf .= $data;
  } while ($buf !~ /\n/ and length $buf < 1024);

  chomp $buf;
  return $SERVICE_CORRUPT unless $flag eq $buf;

  $h->close;
  print STDOUT $chain;
  return $SERVICE_OK;
}

sub get {
  my ($id, $flag, $fake, $data) = @_;

  my $h = IO::Socket::INET->new(PeerAddr => "$ip:$port", Proto => 'tcp', Timeout => 10)
    or return $SERVICE_FAIL;
  my $s = IO::Select->new($h);

  $fake .= $alph[rand @alph] for 1 .. 31;
  $fake .= "=";
  $h->send("$id $fake\n");
  my $buf;
  do {
    return $SERVICE_FAIL unless $s->can_read(5);
    $h->recv($data, 1024);
    $buf .= $data;
  } while ($buf !~ /\n/ and length $buf < 1024);
  chomp $buf;
  return $FLAG_GET_ERROR unless $flag eq $buf;

  $h->close;
  return $SERVICE_OK;
}
