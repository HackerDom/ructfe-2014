#!/usr/bin/perl -wl

use Digest::SHA 'hmac_sha1_hex';
use HTTP::Tiny;
use POSIX 'strftime';
use Time::Piece;
use Time::Seconds;

use feature ':5.10';
no warnings 'experimental::smartmatch';

use constant HMAC_KEY => 'RuCTFE_2014';

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) =
  (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);
my ($mode, $ip) = splice @ARGV, 0, 2;
my @chars = ('A' .. 'Z', 'a' .. 'z', '_', '0' .. '9');

warn 'Invalid input. Empty mode or ip address.' and exit $INTERNAL_ERROR
  unless defined $mode and defined $ip;
warn 'Invalid mode.' and exit $INTERNAL_ERROR unless $mode ~~ %MODES;
exit $MODES{$mode}->(@ARGV);

sub check {
  my $data;
  $data .= $chars[rand @chars] for 1 .. 10;

  my $ua = HTTP::Tiny->new(timeout => 10);
  my $response = $ua->head("http://$ip:2014/$data");
  return $SERVICE_FAIL if $response->{status} >= 500;
  return $SERVICE_CORRUPT unless defined $response->{headers}{'date'};

  my $backup_file = eval {
    my $t = Time::Piece->strptime($response->{headers}{'date'} => '%Y-%m-%dT%H:%M:%S%z');
    $t -= 2 * ONE_MINUTE;
    $t->strftime('%Y-%m-%dT%H:%M+0000');
  };
  return $SERVICE_CORRUPT if $@;

  my $url = "http://$ip:2014/b/$backup_file.tar.bz2";
  $response = $ua->head($url, {headers => {'X-RuCTFE' => $data}});

  return $SERVICE_FAIL if $response->{status} >= 500;
  return $SERVICE_CORRUPT
    if ($response->{headers}{'x-ructfe'} // '') ne hmac_sha1_hex($data, HMAC_KEY);
  return $SERVICE_CORRUPT unless $response->{success};
  return $SERVICE_OK;
}

sub get {
  my ($id, $flag) = @_;
  my $data;
  $data .= $chars[rand @chars] for 1 .. 10;

  my $ua = HTTP::Tiny->new(timeout => 10);
  my $response = $ua->get("http://$ip:2014/$id", {headers => {'X-RuCTFE' => $data}});

  return $SERVICE_FAIL if $response->{status} >= 500;
  return $SERVICE_CORRUPT unless $response->{success};
  return $SERVICE_CORRUPT
    if ($response->{headers}{'x-ructfe'} // '') ne hmac_sha1_hex($data, HMAC_KEY);
  return $response->{content} eq $flag ? $SERVICE_OK : $FLAG_GET_ERROR;
}

sub put {
  my ($id, $flag) = @_;
  my $data;
  $data .= $chars[rand @chars] for 1 .. 10;

  my $ua = HTTP::Tiny->new(timeout => 10);
  my $response =
    $ua->put("http://$ip:2014/$id", {content => $flag, headers => {'X-RuCTFE' => $data}});

  return $SERVICE_FAIL if $response->{status} >= 500;
  return $SERVICE_CORRUPT unless $response->{success};
  return $SERVICE_CORRUPT
    if ($response->{headers}{'x-ructfe'} // '') ne hmac_sha1_hex($data, HMAC_KEY);
  return $SERVICE_OK;
}
