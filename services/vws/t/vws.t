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
  $vws = start ["$Bin/../vws", '-p', $port, '-i', '1', '-d', "$Bin/static"]
}
END { $vws->signal('SIGTERM') }

my $url = Mojo::URL->new("http://localhost:$port/");
my $t   = Test::Mojo->new();

$t->get_ok($url->path('/1.txt'))
  ->header_is(Server => 'VWS')
  ->header_is('X-Powered-By' => 'Vala 0.26.0')
  ->header_is('Content-Length' => 10)
  ->content_is("test data\n");

done_testing();
