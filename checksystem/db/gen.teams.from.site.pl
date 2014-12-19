$\=$/;

@teams = split /\],\[/, `curl http://ructf.org/e/2014/teams/info`;
for(@teams)
{
	next unless /^(\d+),"(.*)"$/,
	$id = $1;
	$name = $2;
	$name =~ s/\'/\'\'/;
	$oc1 = 60 + int $id / 256;
	$oc2 = $id % 256;
	print "INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES ($id, '$name', '10.$oc1.$oc2.0/24', '10.$oc1.$oc2.2', true);";
}



__END__
[["Id","Name"],[1,"#misec"],[30,"Squareroots"],[21,"ANeSeC"],[35,"Honeypot"],[28,"Peterpen"],[27,"UFOlogists"],[12,"xnosuchteam"],[10,"vodkamatreshka"],[4,"KQCQ"],[24,"Noobs1337"],[25,"0x0x"],[39,"Borscha.net"],[3
7,"BAD_Magic"],[20,"Lobotomy"],[15,"FAUST"],[2,"dcua"],[11,"SiBears"],[121,"unnamed"],[13,"OjeteTeam"],[14,"SlientMan"],[123,"Samurai"],[33,"Singularity"],[19,"TeamTHS"],[17,"SlashDotDash"],[18,"Knightsec"],[125,"

INSERT INTO teams (id,name,network,vuln_box,enabled) VALUES (1, '#misec', '10.60.1.0/24', '10.60.1.2', true);
