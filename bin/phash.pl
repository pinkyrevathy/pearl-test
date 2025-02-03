#!/usr/bin/perl

use Image::PHash;

die "File expected as argument" unless $ARGV[0];

my $iph = Image::PHash->new($ARGV[0]);

print $iph->pHash()."\n";