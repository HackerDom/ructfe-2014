use FindBin '$Bin';
use IPC::Run 'start';
use Mojo::IOLoop::Server;
use Mojo::URL;
use Test::Mojo;
use Test::More;

use warnings;
use strict;

my ($port, $vws);
BEGIN {
  $port = Mojo::IOLoop::Server->generate_port;
  $vws = start ["$Bin/../vws", '-p', $port, '-i', '1', '-d', "$Bin/static"];
  sleep 1;
}
END { $vws->signal('SIGTERM') }

my $url = Mojo::URL->new("http://localhost:$port/");
my $t   = Test::Mojo->new->tap(sub { $_->ua->max_connections(0) });

$t->get_ok($url->path('/1.txt'))
  ->status_is(200)
  ->header_is(Server => 'VWS')
  ->header_is('X-Powered-By' => 'Vala 0.26.0')
  ->header_is('Content-Length' => 10)
  ->content_is("test data\n");

$t->get_ok($url->path('/-1.txt'))
  ->status_is(404)
  ->header_is(Server => 'VWS')
  ->header_is('X-Powered-By' => 'Vala 0.26.0');

$t->get_ok($url->path('/1.txt/../1.txt'))->status_is(200);
$t->get_ok($url->path('/a/b/../../1.txt'))->status_is(200);
$t->get_ok($url->path('/../../1.txt'))->status_is(200);
$t->get_ok($url->path('/a/b/c/../../1.txt'))->status_is(404);

# Test vuln
$t->get_ok($url->path('/../vws.t'))->status_is(404);
$t->get_ok($url->path('/%2E%2E/vws.t'))->status_is(200);

done_testing();
