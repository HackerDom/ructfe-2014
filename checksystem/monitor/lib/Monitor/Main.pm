package Monitor::Main;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  shift->render;
}

sub flags {
  my $c = shift;

  $c->render(json => $c->app->flags);
}

sub history {
  my $c = shift;

  $c->render(json => $c->app->history);
}

1;
