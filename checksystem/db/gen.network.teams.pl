$\=$/;
for $p2 (0..2)
{
	for $p3 (0..255)
	{
		next if $p2 == 0 && $p3 < 128;

		$num = $p2 * 256 + $p3;
		$o2 = 60 + $p2;
		print "INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES ($num, 'Test$num', '10.$o2.$p3.0/24', '10.$o2.$p3.0', true);";
	}
}


__END__
INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES (1, 'Test', '172.16.16.0/24', '172.16.16.2', true);