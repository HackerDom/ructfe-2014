#!/usr/bin/perl
print "DELETE FROM users;\n";
for $f (<users.db/*>) {
	open F, $f or die;
	$f =~ s|.*/||;
	chomp($id=<F>);
	printf "INSERT INTO users(key, value) VALUES ('%s', '%s');\n", $f, $id;
}

