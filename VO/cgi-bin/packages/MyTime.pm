package packages::MyTime;

# +-------------------------------+
# | Dorey Sebastien               |
# | Time.pm                       |
# | Written     on Aug 8 th 2005  |
# | Last update on Oct 13rd 2005  |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw(
	     dates_substracted  are_dates_greater  are_dates_smaller        are_dates_equal 
	     print_res          test_for_smaller   test_for_greater         test_for_equal
	     get_formated_date  is_timer_ok        get_digital_date_format
	     );
@EXPORT_OK = qw( timegm_nocheck timelocal_nocheck );

# Sat Sep 10 16:12:01 UTC 2005

@nday = ("Sun","Mon","Tues","Wed","Thu","Fri","Sat");
@nmonth = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

use Fcntl qw(:DEFAULT :flock);
use Time::Local;

=head1 ABSTRACT

This packages helps used to manipulate dates.

=head2 LIST OF FUNCTIONS

=over 4



=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:> Jun 6th 2003

- I<Starting date Nov:> Feb 2005

=back

=cut


# my $a = localtime(timelocal(01,42,15,10,8,2005));
# my $b = localtime(timelocal(42,10,16,10,6,2004));

# is laps within one time session passed (1 min(s) 2sec(s),1 min(s) 1 sec(s)) is     ok returns  0
#                                        (1 min(s) 2sec(s),1 min(s) 2 sec(s)) is not ok returns -1
#                                        (1 min(s) 2sec(s),1 min(s) 3 sec(s)) is not ok returns -1

sub is_timer_ok { # Begin sub is_timer_ok
    my ($time,$laps) = @_;
    my ($y_t,$d_t,$h_t,$m_t,$s_t) = &split_info_for_timer($time);
    my ($y_l,$d_l,$h_l,$m_l,$s_l) = &split_info_for_timer($laps);

    if ($y_t > $y_l) { # Begin if ($y_t > $y_l)
	return 0;
    }  # End if ($y_t > $y_l)
    elsif ($y_t == $y_l) { # Begin elsif ($y_t == $y_l)
	if ($d_t > $d_l) { # Begin if ($d_t > $d_l)
	    return 0;
	}  # End if ($d_t > $d_l)
	elsif ($d_t == $d_l) { # Begin elsif ($d_t == $d_l)
	    if ($h_t > $h_l) { # Begin if ($h_t > $h_l)
		return 0;
	    } # End if ($h_t > $h_l)
	    elsif ($h_t == $h_l) { # Begin elsif ($h_t == $h_l)
		if ($m_t > $m_l) {  # Begin if ($m_t > $m_l) 
		    return 0;
		} # End if ($m_t > $m_l) 
		elsif ($m_l == $m_t) { # Begin elsif ($m_l == $m_t)
		    if ($s_t > $s_l) { # Begin if ($s_t > $s_l)
			return 0;
		    } # End if ($s_t > $s_l)
		    elsif ($s_l == $s_t) { # Begin elsif ($s_l == $s_t)
			return -1;
		    }  # End elsif ($s_l == $s_t)
		    else {  # Begin else
			return -1;
		    }  # End else
		}  # End elsif ($m_l == $m_t)
		else {  # Begin else
		    return -1;
		} # End else
	    } # End elsif ($h_t == $h_l)
	    else {  # Begin else
		return -1;
	    } # End else
	} # End elsif ($d_t == $d_l)
	else {  # Begin else
	    return -1;
	} # End else
    }  # End elsif ($y_t == $y_l)
    else { # Begin else
	return -1;
    }  # End else
}  # End sub is_timer_ok

# Splits time somthing like that 1 hour(s) 2 min(s) 5sec(s) into separate fields no field for month is available only days
sub split_info_for_timer { # Begin sub split_info_for_timer
    my ($schedule) = @_;
    my ($year,$day,$hour,$min,$sec,$other) = ();

    $schedule =~ s/\(s\)//g;
    if ($schedule =~ m/year/) {  # Begin if ($schedule =~ m/year/)
	($year,$schedule) = split(/year/,$schedule);
	$year =~ s/\ *//g;
    }   # End if ($schedule =~ m/year/)
    else { # Begin else
	$year = 0;
    }  # End else
    if ($schedule =~ m/day/) { # Begin  if ($schedule =~ m/day/)
	($day,$schedule)  = split(/day/ ,$schedule);
	$day =~ s/\ *//g;
    } # End  if ($schedule =~ m/day/)
    else { # Begin else
	$day = 0;
    }  # End else
    if ($schedule =~ m/hour/) { # Begin if ($schedule =~ m/hour/)
	($hour,$schedule) = split(/hour/,$schedule);
	$hour =~ s/\ *//g;
    }  # End if ($schedule =~ m/hour/)
    else { # Begin else
	$hour = 0;
    } # End else
    if ($schedule =~ m/min/) { # if ($schedule =~ m/min/)
	($min,$schedule)  = split(/min/ ,$schedule);
	$min =~ s/\ *//g;
    } # End if ($schedule =~ m/min/)
    else { # Begin else
	$min = 0;
    }  # End else
    if ($schedule =~ m/sec/) { # Begin if ($schedule =~ m/sec/)
	($sec,$other)  = split(/sec/ ,$schedule);
	$sec =~ s/\ *//g;
    } # End if ($schedule =~ m/sec/)
    else { # Begin else
	$sec = 0;
    }  # End else
    return ($year,$day,$hour,$min,$sec);
}  # End sub split_info_for_timer

# Substract 2 dates at the format above and returns the result in the format 2 hours 3 min for instance
sub dates_substracted { # Begin sub dates_substracted
    my ($time1,$time2) = @_;
    chomp($time1);
    chomp($time2);
    my $s = &translate(&substract_date($time1,$time2));

    return $s;
} # End sub dates_substracted

# Prints dates result
sub print_res { # Begin sub print_res
    my ($d1,$d2,$res) = @_;

    return ($res == 0) ? "ok\n":"nok\n";
} # End sub print_res

# Looks if date 1 is greater than date 2
sub are_dates_greater {
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) { # Begin if (&get_year_from_string($d1) > &get_year_from_string($d2))
	return 0;
    } # End if (&get_year_from_string($d1) > &get_year_from_string($d2))
    elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) { # Begin elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) { # Begin if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2))
	    return 0;
	}  # End if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2))
	elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) { # Begin elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) { # Begin if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
		return 0;
	    }  # End if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
	    elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { # Begin elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) { # Begin if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		    return 0;
		}  # End if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) { # Begin elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { # Begin if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
			return 0;
		    } # End if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
		    elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) { # Begin  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
			if (&get_seconds_from_string($d1) > &get_seconds_from_string($d2)) { # Begin if (&get_seconds_from_string($d1) > &get_seconds_from_string($d2))
			    return 0;
			}  # End if (&get_seconds_from_string($d1) > &get_seconds_from_string($d2))
			return -1;
		    }  # End  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
		    else { # Begin else
		      return -1;
		    } # End else
		}  # End elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		else { # Begin else
		  return -1;
		} # End else
	    } # End elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
	    else { # Begin else
		return -1;
	    } # End else
	}  # End elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	else { # Begin else
	    return -1;
	}  # End else
    } # End elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
    else { # Begin else
	return -1;
    }  # End else
}

# Looks if date 1 is smaller than date 2
sub are_dates_smaller { # Begin sub are_dates_smaller
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) { # Begin if (&get_year_from_string($d1) > &get_year_from_string($d2))
	return -1;
    }  # End if (&get_year_from_string($d1) > &get_year_from_string($d2))
    elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) { # Begin elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) {
	    return -1;
	}
 elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) { # Begin  elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) { # Begin if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
		return -1;
	    }  # End if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
	    elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { # Begin elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) { # Begin if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		    return -1;
		} # End if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) { # Begin elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { # Begin if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
			return -1;
		    } # End if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
		    elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) { # Begin  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
			if (&get_seconds_from_string($d1) < &get_seconds_from_string($d2)) { # Begin if (&get_seconds_from_string($d1) < &get_seconds_from_string($d2))
			    return 0;
			}  # End if (&get_seconds_from_string($d1) < &get_seconds_from_string($d2))
			return -1;
		    } # End  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
		    else { # Begin else
		      return 0;
		    } # End else
		}  # End elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		else { # Begin else
		  return 0;
		} # End else
	    }  # End elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
	    else { # Begin else
	      return 0;
	    } # End else
	} # Begin  elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	else { # Begin else
	  return 0;
	} # End else
    } # End elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
    else { # Begin else
	return 0;
    } # End else
} # End sub are_dates_smaller

# Looks if date 1 is equal to date 2
sub are_dates_equal { # Begin sub are_dates_equal
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) { # Begin if (&get_year_from_string($d1) > &get_year_from_string($d2))
	return -1;
    } # End if (&get_year_from_string($d1) > &get_year_from_string($d2))
    elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) { # Begin elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) { # Begin if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2))
	    return -1;
	} # End if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2))
	elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) { # Begin elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) { # Begin if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
		return -1;
	    }  # End if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2))
	    elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { # Begin elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) { # Begin if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		    return -1;
		}  # End if (&get_hour_from_string($d1) > &get_hour_from_string($d2))
		elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) { # Begin elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { # Begin if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
			return -1;
		    } # End if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2))
		    elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) { # Begin if (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
			if (&get_seconds_from_string($d1) == &get_seconds_from_string($d2)) { # Begin if (&get_seconds_from_string($d1) == &get_seconds_from_string($d2))
			    return 0;
			}  # End if (&get_seconds_from_string($d1) == &get_seconds_from_string($d2))
			return -1;
		    }  # End elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2))
		    else { # Begin else
		      return -1;
		    }  # End else
		}  # End elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2))
		else { # Begin else
		    return -1;
		}  # End else
	    } # End elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2))
	    else { # Begin else
	      return -1;
	    }  # End else
	}  # End elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2))
	else { # Begin else
	  return -1;
	}  # End else
    }  # End elsif (&get_year_from_string($d1) == &get_year_from_string($d2))
    else { # Begin else
	return -1;
    }  # End else
}  # End sub are_dates_equal

# Returns as year days month year min sec format according to epoc
sub translate { # Begin sub translate
    my ($epoc) = @_;
    my ($sec,
	$min,$min_r,
	$hour,$hour_r,
	$day,$day_r,
	$year) = 0;
    my $date_to_return = ();

    ($sec,$min) = &div_time($epoc,60); # left minute(s)
    ($min_r,$hour) = &div_time($min,60); # left hour(s)
    ($hour_r,$day) = &div_time($hour,24); # left day(s)
    ($day_r,$year) = &div_time($day,365); # left year(s)
    $date_to_return = 
	&print_peace_of_date($year," year(s) ") .
	&print_peace_of_date($day_r," day(s) ") . 
	&print_peace_of_date($hour_r," hour(s) ") .
	&print_peace_of_date($min_r," min(s) ") .
	&print_peace_of_date($sec," sec(s)");
    $date_to_return =~ s/\ +/\ /g;
    $date_to_return =~ s/^[\ ]+//g;
    $date_to_return =~ s/[\ ]+$//g;
    return $date_to_return;
}  # End sub translate

# A bug showed up at 2 min with translate function: a carriage return shows up in the middle of the string formated
sub remove_carriage_return { # Begin sub remove_carriage_return
    my ($string) = @_;
    my $new_string = ();

    foreach (split(/\n/,$string)) { # Begin foreach (split(/\n/,$string))
	$new_string .= $_ . " ";
    }  # End foreach (split(/\n/,$string))
    $new_string =~ s/^\ //;
    return $new_string;
}  # End sub remove_carriage_return

# Returns if value non 0 the string 
sub print_peace_of_date { # Begin sub print_peace_of_date
    my ($value,$string) = @_;
    my $result = ($value != 0) ? "$value $string" : "";

    return $result;
} # End sub print_peace_of_date

# to crroect here
# Division for time. Returns reminder and time left after operation
sub div_time { # Begin sub div_time
    my ($epoc,$max_time) = @_;
    my $first_div = ($epoc % $max_time);

    return ($first_div,(($epoc - $first_div) / $max_time));
} # End sub div_time


# Substracts two dates and return as epoc format
sub substract_date { # Begin sub substract_date
    my ($time1,$time2) = @_;
    my ($my_date_left,$my_date_right) = (&clean_dates($time1),&clean_dates($time2));
    my $result = 0;
    my ($date_left_nday ,$date_left_month ,$date_left_mday ,$date_left_hour ,$date_left_min ,$date_left_sec ,$date_left_year ) = 
	split(/\ /,$my_date_left);
    my ($date_right_nday,$date_right_month,$date_right_mday,$date_right_hour,$date_right_min,$date_right_sec,$date_right_year) =
	split(/\ /,$my_date_right);

    $result_tmloc1 = timelocal(
		  &format_number_two_on_digits($date_left_sec),
		  &format_number_two_on_digits($date_left_min) ,
		  &format_number_two_on_digits($date_left_hour) ,
		  &format_number_two_on_digits($date_left_mday) ,
		  &format_number_two_on_digits(&get_num_month($date_left_month)),
		  &format_number_two_on_digits($date_left_year));
    $result_tmloc2 = timelocal(
		     &format_number_two_on_digits($date_right_sec),
		     &format_number_two_on_digits($date_right_min),
		     &format_number_two_on_digits($date_right_hour),
		     &format_number_two_on_digits($date_right_mday),
		     &format_number_two_on_digits(&get_num_month($date_right_month)),
		     &format_number_two_on_digits($date_right_year));
    return  $result_tmloc1 -  $result_tmloc2;
} # End sub substract_date

# We clean format of 2 dates received
sub clean_dates{ # Begin sub clean_dates
    my ($my_date) = @_;

    $my_date =~ s/UTC//ig;
    $my_date =~ s/\:/\ /g; # we remove : and replace it with a space
    $my_date =~ s/^\ *//g; # we remove spaces at the first place
    $my_date =~ s/\ +/\ /g;# we remove spaces and replace them with a single space
    return ($my_date);
}  # End sub clean_dates

# from a given month return its rank in year
sub get_num_month { # Begin sub get_num_month
    my ($month) = @_;
    my $n = 0;

    while ($n != 12) { # Begin  while ($n != 12)
	if ($nmonth[$n] =~ m/$month/i ) { # Begin if ($nmonth[$n] =~ m/$month/i )
	    return $n;
	} # End if ($nmonth[$n] =~ m/$month/i )
	$n++;
    } # End while ($n != 12)
    return (11);
}  # End sub get_num_month

# Substracts 2 dates. If result < 0 then 0
sub substract { # Begin sub substract
    if (($_[0] - $_[1]) < 0 ) { # Begin if (($_[0] - $_[1]) < 0 )
	return 0;
    } # End if (($_[0] - $_[1]) < 0 )
    return ($_[0] - $_[1]);
} # End sub substract

# Returns time in second from a given date 
sub get_time_epoc { # Begin sub get_time_epoc
    return time();
} # End sub get_time_epoc

# Returns a digital date 
sub get_digital_date_format { # Begin sub get_digital_date_format
    my @my_localtime = localtime(time());

    return
	&format_number_two_on_digits($my_localtime[4]+1) . "/" .
	&format_number_two_on_digits($my_localtime[3]) . "/" .
	&format_number_two_on_digits($my_localtime[5]+1900) . " " .
	&format_number_two_on_digits($my_localtime[2]) . ":" .
	&format_number_two_on_digits($my_localtime[1]) . ":" .
	&format_number_two_on_digits($my_localtime[0]); 
}  # End sub get_digital_date_format

# Prints a formated date (s.a Sat Sep 10 16:12:01 UTC 2005) according to date function
sub get_formated_date { # Begin sub get_formated_date
    return
	&get_day_name . " " .
	&get_month_name . " " . 
	&format_number_two_on_digits(&get_num_day) . " " .
	&format_number_two_on_digits(&get_hour) . ":" . 
	&format_number_two_on_digits(&get_min) . ":" .
	&format_number_two_on_digits(&get_sec) . " UTC " .
	&get_year;
} # End sub get_formated_date

# Reformat a number on 2 digits
sub format_number_two_on_digits { # Begin sub format_number_two_on_digits
    my ($digit) = @_;

    $digit = ($digit == 0 || $digit eq "") ? 0 : $digit;
    return ($digit  < 10) ? "0$digit" : "$digit";
}  # End sub format_number_two_on_digits

# Returns seconds from localtime() function
sub get_sec { # Begin sub get_sec
    return ((localtime(time()))[0]);
}  # End sub get_scec

# Returns minutes from localtime() function
sub get_min { # Begin sub get_min
    return ((localtime(time()))[1]);
}  # End sub get_min

# Returns seconds from localtime() function
sub get_hour { # Begin sub get_hour
    return ((localtime(time()))[2]);
}  # End sub get_hour

# Returns number of the day from localtime() function
sub get_num_day { # Begin sub get_num_day
    return ((localtime(time()))[3]);
} # End sub get_num_day

# Returns month from localtime() function
sub get_month {
    return ((localtime(time()))[4]);
}
 
# Returns month name from localtime() function
sub get_month_name { # Begin sub get_month_name
    return ($nmonth[(localtime(time()))[4]]);
}  # End sub get_month_name

# Returns year from localtime() function
sub get_year { # Begin sub get_year
    return (1900+(localtime(time()))[5]);
} # End sub get_year

# Returns day name from localtime() function
sub get_day_name { # Begin sub get_day_name
    return ($nday[(localtime(time()))[6]]);
}  # End sub get_day_name

# Returns day number from Jan 1st from current year from localtime() function
sub get_day_num_in_year { # Begin sub get_day_num_in_year
    return ((localtime(time()))[7]);
} # End sub get_day_num_in_year

# Get name of the day  from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_name_of_the_day_from_string { # Begin sub get_name_of_the_day_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[0]);
}  # End sub get_name_of_the_day_from_string

# Get month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_month_from_string { # Begin sub get_month_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[1]);
}  # End sub get_month_from_string

# Get month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_month_number_from_string { # Begin sub get_month_number_from_string
    my ($string) = &clean_dates($_[0]);
    my $counter = 0;

    foreach my $m (@nmonth) { # Begin foreach my $m (@nmonth)
	if ($string =~ m/$m/i) { # Begin if ($string =~ m/$m/i)
	    return $counter;
	}  # End if ($string =~ m/$m/i)
	$counter++;
    } # End foreach my $m (@nmonth)
    return -1;
}  # End sub get_month_number_from_string

# Get day number in month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_day_number_from_string { # Begin sub get_day_number_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[2]);
} # End sub get_day_number_from_string

# Get hour from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_hour_from_string { # Begin sub get_hour_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[3]);
} # End sub get_hour_from_string

# Get minutes from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_minutes_from_string { # Begin sub get_minutes_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[4]);
}  # End sub get_minutes_from_string

# Get seconds from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_seconds_from_string { # Begin sub get_seconds_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[5]);
}  # End sub get_seconds_from_string

# Get UTC from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_utc_from_string { # Begin sub get_utc_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[6]);
} # End sub get_utc_from_string

# Get year from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_year_from_string { # Begin sub get_year_from_string
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[7]);
}  # End sub get_year_from_string


sub test_for_equal { # Begin sub test_for_equal
    my ($d1,$d2) = @_;

    print "equal:( $d1,$d2):" . print_res("$d1","$d2", are_dates_equal( "$d1","$d2"));
}  # End sub test_for_equal

sub test_for_greater { # Begin sub test_for_greater
    my ($d1,$d2) = @_;

    print "greater:( $d1,$d2):" . print_res("$d1","$d2", are_dates_greater( "$d1","$d2"));
}  # End sub test_for_greater

sub test_for_smaller { # Begin sub test_for_smaller
    my ($d1,$d2) = @_;

    print "smaller:( $d1,$d2):" . print_res("$d1","$d2", are_dates_smaller( "$d1","$d2"));
} # End sub test_for_smaller

1;
