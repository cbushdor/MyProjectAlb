package packages::Paranoiac;

# +-------------------------------+
# | Dorey Sebastien               |
# | MyDaemon.pm                   |
# | Written     on Sept 24th 2005 |
# | Last update on Sept 27th 2005 |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( starts_daemon );
@EXPORT_OK = qw(  );


BEGIN {
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/cgi-bin");
}

use Fcntl qw(:DEFAULT :flock);
use packages::MyTime;
use packages::Common;

# This starts daemon
sub starts_daemon {
    my ($log_f,$index_log_file) = @_;
    my ($val,
	$loc_time,
	@string_to_print,
	$critical_section,
	$current_date,
	$laps,
	$line) = ();
    my $last_size = 0;

    &insert_last_log_file_in_index($index_log_file,$log_f);
    $current_date = get_formated_date ;
    chomp($current_date);
    sysopen(CREATE_WRITE_FILE,"$log_f",O_WRONLY|O_CREAT) or die("Cannot open $index_log_file $!");
    flock(CREATE_WRITE_FILE,LOCK_EX);
    print CREATE_WRITE_FILE "$current_date\n";
    close(CREATE_WRITE_FILE);
    ($current_date,$laps) = &reset_laps($current_date);     
    $last_size = 1;
    while (1) { # Begin while (1)

	if (is_timer_ok("3 min(s) 42 sec(s)",$laps) == 0) { #  Begin if (is_timer_ok("1 min(s) 42 sec(s)",$laps) == 0)
	    #                                                 We check if timer is under prerequisites

	    my $size            = get_file_content("$log_f");

	    if ($size > 2) { #  Begin if ($size >= 2)
		#              We have more that two lines at least in the file that contains time measured during website visit
		my @string_to_print = get_file_content("$log_f");

		$laps = &insert_info_when_more_than_two_lines_exists_in_log_file($log_f,@string_to_print);
	    }  # End if ($size >= 2)
	    else { #  Begin if (!($size >= 2))
		#    Case that's the first page
		my @string_to_print = get_file_content("$log_f");

		sysopen(W,"$log_f",O_WRONLY) || die("$log_f does not exists $!\n");
		print W "$string_to_print[0]";
		$line = $string_to_print[0];
		$current_date = get_formated_date ;
		chomp($current_date);
		$laps = dates_substracted($current_date,$string_to_print[0]);
		print W "$current_date*X*$laps";		    
		close(W);
	    }  #  End if (!($size >= 2))
	    sleep(1); # One sec stop
	    $last_size = $size;
	} #  End if (is_timer_ok("1 min(s) 42 sec(s)",$laps) == 0)
	else { # Begin if (is_timer_ok("1 min(s) 42 sec(s)",$laps) != 0)
#	    print "end 1\n";
	    exit(-1);
	} # End if (is_timer_ok("1 min(s) 42 sec(s)",$laps) != 0)
    } # End while (1)
}

# reset laps to current date
sub reset_laps {
    my ($current_date) = @_;
    my $line = ();

    $line = &init_date;
    $laps = dates_substracted($line,$current_date);
    chomp($laps);
    return ($line,$laps);
}

# initialise a date
sub init_date {
    my $line = ();

    $line = get_formated_date;
    chomp($line);
    return $line;
}

# insert new info when a log file zlready exists (at least 2 lines)
sub insert_info_when_more_than_two_lines_exists_in_log_file {
    my ($log_f,	@string_to_print)           = @_;
    my $num_line                            = @string_to_print;
    my $line                                = ();
    my $last_date_taken_from_local_clock    = ();
    my $initial_date_taken_from_local_clock = ();
    my $laps                                = ();
    my $counter                             = 0;

    $num_line = (!($num_line % 2)) ? $num_line : ($num_line+1);
    sysopen(WRF,"$log_f",O_CREAT|O_WRONLY) || die("$log_f does not exists $!\n");
    while ($counter != $num_line) { #  Begin foreach (@string_to_print[0..(@string_to_print - 1)])
	#                          We scan file that contains info of visits
	my $to_rec = $string_to_print[$counter];
	$counter++;
	if ($counter != $num_line) {
	    chomp($to_rec);
	    print WRF "$to_rec\n";
	    $line = $to_rec;
	}
    } #  End foreach (@string_to_print[0..(@string_to_print - 1)])
    $initial_date_taken_from_local_clock  = (split(/\*/,$line))[0];
    $last_date_taken_from_local_clock     = get_formated_date;
    chomp($last_date_taken_from_local_clock);
    $laps = dates_substracted($last_date_taken_from_local_clock,$initial_date_taken_from_local_clock);
    chomp($laps);
    print WRF "$last_date_taken_from_local_clock*X*$laps\n";
    close(WRF);
    return $laps;
}

# Create or insert info in an index file in order to track users
sub insert_last_log_file_in_index {
    my ($index_log_file,$log_f) = @_;

    if (-f "$index_log_file") { # We append in index the new log book file names
	sysopen(APPEND_WRITE_INDEX,"$index_log_file",O_WRONLY|O_APPEND) or die("Cannot open $index_log_file $!");
	flock(APPEND_WRITE_INDEX,LOCK_EX);
	print APPEND_WRITE_INDEX "$log_f\n";
	close(APPEND_WRITE_INDEX);
    } else { # We create index that hold log book file name
	sysopen(O_CREATE_WRITE_INDEX,"$index_log_file",O_WRONLY|O_CREAT) or die("Cannot open $index_log_file $!");
	flock(O_CREATE_WRITE_INDEX,LOCK_EX);
	print O_CREATE_WRITE_INDEX "$log_f\n";
	close(O_CREATE_WRITE_INDEX);	
    } # end if
}

1;


