#!/usr/bin/env perl
$\=$/;
for(1..10)
{
	$num = 100 + $_;
	print "INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES ($num, 'Fake $_', '10.60.13.0/24', '10.60.13.0', true);";
}


__END__
INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES (6, 'Team157', '10.60.157.0/24', '10.60.157.0', true);
