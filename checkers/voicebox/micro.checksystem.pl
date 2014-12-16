#!/usr/bin/perl
use strict;
++$|;

my $COUNT = 100;
my @fch = ('A'..'Z','0'..'9');
my @ich = ('0'..'9','a'..'z');

my $ip = shift or die "give ip as argument\n";
my $ret;

$\=$/;

for (1..$COUNT)
{
	printf "%d of %d ...\n", $_, $COUNT;
	print system("./voicebox.checker.sh check $ip 2>>micro.checksystem.err.log") >> 8;
	my $id = id();
	my $flag = flag();
	print system("./voicebox.checker.sh put $ip $id $flag >id-$$.tmp 2>>micro.checksystem.err.log") >> 8;
	open ID, "id-$$.tmp" or die;
	chomp($id = <ID>);
	close ID;
	unlink "id-$$.tmp";
	print system("./voicebox.checker.sh get $ip $id $flag 2>>micro.checksystem.err.log") >> 8;
}

sub rs {
	my $len = shift;
	join '', map { $_[int rand @_] } 1..$len;
}

sub flag {
	rs(31,@fch)."=";
}

sub id {
	sprintf "%s-%s-%s", rs(4,@ich), rs(4,@ich), rs(4,@ich);
}

