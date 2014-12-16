package Monitor::Main;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  shift->render;
}

sub flags {
  my $c = shift;

  $c->render(json => $c->app->flags);
}

sub debug {
  my $c = shift;

  $c->render(
    json => {
      s => $c->app->services,
      t => $c->app->teams,
      s => $c->app->scoreboard,
      x => $c->app->status,
      r => $c->app->round,
      f => $c->app->flags,
      i => $c->app->ip2team
    });
}

1;
