package Monitor;
use Mojo::Base 'Mojolicious';

use Mojo::Util 'slurp';
use Mojo::Pg;
use Time::Piece;

has flags      => sub { {} };
has ip2team    => sub { {} };
has round      => sub { {} };
has scoreboard => sub { [] };
has services   => sub { {} };
has status     => sub { {} };
has teams      => sub { {} };

has lock => 0;

sub startup {
  my $app = shift;

  my $mode = $app->mode;
  $app->plugin('Config', file => "monitor.$mode.conf");
  $app->secrets(['qJ9e_d3Snf']);

  $app->helper(
    pg => sub {
      state $pg = Mojo::Pg->new($app->config->{db});
    });

  my $r = $app->routes;
  $r->get('/')->to('main#index')->name('index');
  $r->get('/flags')->to('main#flags')->name('flags');
  $r->get('/debug')->to('main#debug')->name('debug');

  my $update = sub {
    return if $app->lock;
    $app->lock(1);

    $app->log->info('Update scoreboard');
    Mojo::IOLoop->delay(
      sub {
        my $delay = shift;

        $app->pg->db->query('SELECT id, name FROM services'        => $delay->begin);
        $app->pg->db->query('SELECT id, name, vuln_box FROM teams' => $delay->begin);
        $app->pg->db->query(
          'SELECT DISTINCT ON (team_id, service_id) team_id, service_id, score
            FROM score ORDER BY team_id, service_id, time DESC'
            => $delay->begin
        );
        $app->pg->db->query(
          'SELECT DISTINCT ON (team_id, service_id) team_id, service_id, successed, failed
            FROM sla ORDER BY team_id, service_id, time DESC'
            => $delay->begin
        );
        $app->pg->db->query(
          'SELECT n, EXTRACT(EPOCH FROM time) AS time
            FROM rounds ORDER BY n DESC LIMIT 1'
            => $delay->begin
        );
        $app->pg->db->query(
          'SELECT team_id, service_id, status, fail_comment FROM service_status' => $delay->begin);
        $app->pg->db->query('SELECT * FROM services_flags_stolen' => $delay->begin);
      },
      sub {
        my (
          $delay,    $e1, $s,     $e2, $t,      $e3, $scores, $e4,
          $services, $e5, $round, $e6, $status, $e7, $flags
        ) = @_;
        $app->lock(0);
        if (my $e = $e1 || $e2 || $e3 || $e4 || $e5) {
          $app->log->error("Error while update scoreboard: $e");
          return;
        }

        $s->arrays->map(sub { $app->services->{$_->[0]} = $_->[1] });
        $t->hashes->map(
          sub {
            $app->teams->{$_->{id}}         = $_;
            $app->ip2team->{$_->{vuln_box}} = $_->{name};
          });

        my ($flag_points, $sla_points);

        $services->hashes->map(
          sub {
            my ($sla, $sum) = (1, $_->{successed} + $_->{failed});
            $sla = $_->{successed} / $sum if $sum > 0;
            $sla_points->{$_->{team_id}}{$_->{service_id}} = $sla;
          });

        $scores->hashes->map(
          sub {
            $flag_points->{$_->{team_id}}{$_->{service_id}} = $_->{score};
          });

        my @data;
        for my $tid (keys %{$app->teams}) {

          my $score = 0;
          $score += $sla_points->{$tid}{$_} * $flag_points->{$tid}{$_} for keys %{$app->services};

          push @data, {
            team => {
              id       => $tid,
              name     => $app->teams->{$tid}{name},
              vuln_box => $app->teams->{$tid}{vuln_box}
            },
            sla   => $sla_points->{$tid},
            fp    => $flag_points->{$tid},
            score => $score
            };
        }

        @data = sort { $b->{score} <=> $a->{score} } @data;
        $app->scoreboard(\@data);

        my $r = $round->hash;
        $app->round({n => $r->{n}, time => scalar localtime int $r->{time}});

        $status->hashes->map(
          sub {
            $app->status->{$_->{service_id}}{$_->{team_id}} = $_;
          });

        $flags->hashes->map(
          sub {
            $app->flags->{$_->{team_id}}{$_->{service_id}} =
              {count => $_->{flags}, name => $_->{service}};
          });
      });
  };
  $update->();

  Mojo::IOLoop->recurring(5 => $update);
}

1;
