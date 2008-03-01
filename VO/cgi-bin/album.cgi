#!/usr/bin/perl

# Written by Shark bait ###

use constant ALBUM_VERSION        => '1.2.2';       # Album version
use constant AUTHOR               => 'Flotilla Reindeer';    # Author's name
use constant TESTED_WITH_BROWSERS =>
  'Mozilla 1.7.2, Konqueror 3.3';                   # That's browsers tested
use constant COMPAGNY      => 'Shark Bait';         # That's for fun
use constant HOSTED_BY     => 'Zend URL';        # That's the host name
use constant HOSTED_BY_URL =>
  'http://www.zendurl.com';    # That's the url of host name
use constant MY_WEBSITE =>
  'http://dorey.sebastien.free.fr';    # That's author's url
use constant MAX_PAGE_PER_LINE_INDEX =>
  20;    # That's max of page in browser that shows up on one line.
use constant MAX_IMAGES_PER_PAGE => 5;    # Maximum of images per page
use constant LANGUAGES     => ( "French", "English" );    # Languages used
use constant ROOT_DESPOSIT => "../";                      # To store information
use constant PRIVATE_INFO_DIRECTORY =>
  "private/";    # that's where private info are stored
use constant AMOUNT_OF_INFO_TO_READ => ( 5 * 2096 )
  ;              # That's the amount bite read each time src files read (slot)

my $loc_margin = "        ";

# Next 3 lines are used to suffix new file name to save in the album.
@month = ( Jan, Fev, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec );
my @proc                  = gmtime;
my $suffix_for_image_file =
    ( $proc[5] + 1900 ) . "_"
  . $month[ $proc[4] ]
  . "_$proc[3]"
  . "_$proc[2]:$proc[1]:$proc[0]-";

# This is used when we want to debug and use upload bar.cgi Not in user anymore
use constant DEBUG => 1;

# This is usefull when pb occurs and file being open
use IO;

import bar . cgi;

=head1 ABSTRACT

This file creates an album on the net of different pictures that have different formats. Formats can be jpeg or jpg or gif (can be others but these format are mostly used). Size of the picture (length,width) does not matter but file size yes (look my_upload function).

=head2 LIST OF FUNCTIONS

=over 4

remove_picture
return_average_file
return_info_picture
set_language
set_link
set_upload
show_list_pictures
show_page_not_taken_yet
size_dir
split_links
switch_from_a_specified_character_to_tag
switch_from_a_specified_tag_to_characters
title_average_formating
under_construction_prompt

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:> Jan 27 2006

- I<Last modification:> Mar 03 2005

- I<Starting date Nov:> 10 2004

=back

=cut

# --------------------------------------------------------------------------
# --------- Modifications can be done in the zone below --------------------
# --------------------------------------------------------------------------

# This is directory where all be stored
my $album_directory = "album";

# That's where the file that contains info for building pages are stored
my $configuration_file = "conf.file";

# send to another site when under construction for a demo
my $url_demo = "http://storm.prohosting.com/dorey/cgi-bin/album.cgi";

# --------------------------------------------------------------------------
# --------- End of zone ----------------------------------------------------
# --------------------------------------------------------------------------

$| = 1;

use CGI;
use Fcntl qw( :DEFAULT :flock);

# We define a boolean value OK = 0
use constant OK  => 0;
use constant NOK => !(OK);

# Define values to set up upload image files
# use constant SIZE_TMP          => 16_384;
use constant MAXIMUM_SIZE_FILE => (1_048_576 * 5);    # 1 deposit = 1Mo * 5
use constant MAXIMUM_DIRECTORY_SIZE_THAT_CAN_CONTAIN_FILE => 100 * 1_048_576;
use constant MAXIMUM_FILE_OPENED                          => 100;

$CGI::DISABLE_UPLOADS = 0;
$CGI::POST_MAX        = MAXIMUM_SIZE_FILE;

# This is document which will help to deal with CGI information
my $doc = new CGI;

# Password for login
my ( $login, $password ) = &get_private_stuff_for_administrator;

# We need PID tO make a little security
my $my_pid = $doc->param('prev_pid');
chomp($my_pid);

# This is where configuration file is
my $file_conf_to_save = "$album_directory/$configuration_file";
chomp($file_conf_to_save);

# That's the service
my $service = $doc->param("service");
chomp($service);

# Upload granted or not
my $upload = $doc->param("upload");
chomp($upload);

# That's the user login from the url
my $user_login = $doc->param("login");
chomp($user_login);

# That's the user password from the url
my $user_password = $doc->param("password");
chomp($user_password);

# Modify or remove lines for album
my $an_action = $doc->param("action");
chomp($an_action);

# That's info stored when we want to modify it
my @info_on_picture = ();

=head1 FUNCTION  find_directory_to_store_image

We create a variable that stores image path for the constant DIRECTORY_DEPOSIT

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1 when no directory found for image that are already stored.

=back

=back

=head2 BUG KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 04 2006

- I<Created on:> Jan 04 2006

=back

=back



=cut

sub find_directory_to_store_images {  # Begin sub find_directory_to_store_images
    my $directory_to_store_images = ROOT_DESPOSIT;

    if ( -d "../img/" ) {             # Begin if (-d "../img/")
        return $directory_to_store_images .= "img/";
    }    # End if (-d "../img/")
    elsif ( -d "../image" ) {    # Begin elsif (-d "../image")
        return $directory_to_store_images .= "image/";
    }    # End elsif (-d "../image")
    elsif ( -d "../images" ) {    # Begin elsif (-d "../images")
        return $directory_to_store_images .= "images/";
    }    # End elsif (-d "../images")
    elsif ( -d "../Image" ) {    # Begin elsif (-d "../Image")
        return $directory_to_store_images .= "image/";
    }    # End elsif (-d "../Image")
    elsif ( -d "../IMAGE" ) {    # Begin elsif (-d "../IMAGE")
        return $directory_to_store_images .= "IMAGE/";
    }    # End elsif (-d "../IMAGE")
    elsif ( -d "../IMAGES" ) {    # Begin elsif (-d "../IMAGES")
        return $directory_to_store_images .= "IMAGES/";
    }    # End elsif (-d "../IMAGES")
    elsif ( -d "../Image" ) {    # Begin elsif (-d "../Image")
        return $directory_to_store_images .= "Image/";
    }    # End elsif (-d "../Image")
    elsif ( -d "../Images" ) {    # Begin elsif (-d "../Images")
        return $directory_to_store_images .= "Images/";
    }    # End elsif (-d "../Images")
    else {    # Begin else
           # That's the case where no directory was found under the above names.
         # Case where directory does not exist. we create a directory where all images will be stored.
         # &error_raised("can't find a directory to store images");
        $directory_to_store_images .= "images/";
        mkdir( "$directory_to_store_images", 0755 );
        return $directory_to_store_images;
    }    # End else
}    # End sub find_directory_to_store_images

# Where pictures are going to be when upload action is done
use constant DIRECTORY_DEPOSIT => &find_directory_to_store_images;

# necessary images
@images_used = (
		DIRECTORY_DEPOSIT . "under_construction10.gif",
		DIRECTORY_DEPOSIT . "my_lovely_pict.gif",
		DIRECTORY_DEPOSIT . "chair1-a.gif",
		DIRECTORY_DEPOSIT . "powered.gif"
);

print "Content-type: text/html\n";
print "Pragma: no-cache \n\n";
print
"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR//xhtml/DTD/xhtml1-transitional.dtd\">\n";
print "<html>\n";
print "    <head>\n";
print "        <meta name=\"title\"       content=\"Album of pictures\" />\n";
print
"        <meta name=\"description\" content=\"Album of pictures generated with a perl script\" />\n";
print
"        <meta name=\"keywords\"    content=\"Sebastien DOREY, album,Dorey Sebastien album,Stevens Instute of Technology, EPITA, Hoboken, New Jersey, Paris, France, album picture Sebastien Dorey, album photo Sebastien Dorey, website, site web, study, etude, biboune, ailefroide, montagne, ballade, marche � pied, hike, mountain, mere denis, le grand mechand loup, the wolf, de l'eau gnon, de l'oignon\" />\n";
print "        <meta name=\"author\"      content=\"Sebastien DOREY\" />\n";
print &cascade_style_sheet_definition;
print "    </head>\n";
print "<body onload=\"JavaScript:show()\">\n";

if ( $an_action eq "modify" ) {    # Begin if ($an_action eq "modify")
     # We print the administration menu of the album of pictures to modify a feature
    @info_on_picture = &return_info_picture;
}    # End if ($an_action eq "modify")

# We get info from URL
my (
    $modify_page_position_in_album, $modify_position_in_page,
    $modify_file_name,              $modify_valign,
    $modify_halign,                 $modify_french_comment,
    $modify_english_comment,        $modify_vertical_text,
    $modify_horizontal_text,        $modify_position_from_the_image
  )
  = @info_on_picture;

# Check login & password if ok then access to extra services
if ( (&check_password) == 0 ) {    # Begin  if ( (&check_password) == 0 )
    my $recor = $doc->param("recording");
    chomp($recor);
    &main_menu(
        "Menu pour administration. / Administration menu.",
"Choisir une page et un rang pour placer l'image. / Choose a page and a row for the image.",
        "Choisir une image. / Choose an image.",
"Entrer le(s) mot(s) (versions Fran�ais et Anglais) et � cot� son lien pour que ce dernier aparaissent dans le Cyber Album sous forme de lien dans le commentaire. / Enter words to link in message (French, English versions) in order to make links show up in message when Cyber Album is watched.",
        "Choisir les options de placement. / Choose options for positions.",
        "Mettre les commentaires. / Write comments."
    );

    # That's where info are uploaded
    if ( $an_action ne "record_modify" )
    {    # Begin if ($an_action ne "record_modify")
        if ( $upload eq "ok" ) {    # Begin if ($upload eq "ok")
            my $type_upload = $doc->param("type_of_upload");

# We use this option in order to make a difference between an image linked to a web site and an image localy uploaded
            if ( $type_upload eq "Local" )
            {                       # Begin if ($type_upload eq "Local")
                                    # When upload raised a new window with info
                open( W, ">album/dec" );
                print W ".";
                close(W);
                &raised_upload_window;
                sleep(1);
                &my_upload;
            }    # End if ($type_upload eq "Local")
        }    # End if ($upload eq "ok")
    }    # End if ($an_action ne "record_modify")

    # Record information on disk
    if (   ( $doc->param("file_name_img") ne "" )
        || ( $doc->param("file_name_img2") ne "" )
        || ( $an_action eq "record_modify" ) )
    { #  Begin if ( ($doc->param("file_name_img") ne "") || ($an_action eq "record_modify") )
        if ( $recor eq "check" ) {    #  Begin if ($recor eq "check")
            &record;
        }    # End if ($recor eq "check")
    } # End if ( ($doc->param("file_name_img") ne "") || ($an_action eq "record_modify") )

    # We remove a feature from the list
    if ( $an_action eq "remove" ) {    # Begin if ($an_action eq "remove")
        print $doc->p( "<br><br><br><br>Picture will be removed from page "
              . $doc->param("page")
              . " line "
              . $doc->param("line") );
        &remove_picture;
    }    # End if ($an_action eq "remove")

    &menu_admin_title();
    &menu_leave_admin;
    print "<table width='100\%'><tr><td bgcolor='#73B5A5'>\n";
    print
"\n<FORM ACTION='album.cgi?service=auth&upload=ok' method='post'   ENCTYPE='multipart/form-data'>\n";
    print "<input type='hidden' name='prev_pid' value='$$'>";
    print
"<table width=100% border=0><tr><td width=22% bgcolor='#CFD3F6' align=left valign=top>\n";

    # We show the list of pictures that are already taken
    &show_page_not_taken_yet;
    print "<td align=left valign=top bgcolor='#CFD3F6'>\n";

#    print "<table width=100% border=0><tr><td align=center valign=top bgcolor='#C56B4A'>Configure image position</tr></table>\n";
    print
"<table width=100% border=0><tr><td class=\"configuration\">Configure image position</tr></table>\n";
    &admin_menu( "Set position of the image in compartment",
        "Set position of the text from the image in compartment" );
    print "</br><center>\n";
    &go_back;
    print "</center>\n";

    # We show the pictures list of the album with caracteristics
    &show_list_pictures;
    print "</tr></table>\n";
    print "</tr></table>\n";
}    # End  if ( (&check_password) == 0 )
elsif ( $service eq "auth" ) {    # Begin elsif ( (&check_password) == 0 )
    &main_menu(
        "Aide pour l'authentification / Authentication menu help",
        "Entrer l'identifiant et le mot de passe. / Enter login and password."
    );

    # We print the main title of authentication menu
    &auth_menu;
}    # End elsif ( (&check_password) == 0 )
elsif ( $service eq "showPict" ) {    # Begin elsif ( (&check_password) == 0 )
    &main_help_menu_css;

    # We print the choosen picture on the screen, with comments.
    &printPict;
}    # End elsif ( (&check_password) == 0 )
else {    # Begin else ( (&check_password) == 0 )
          # We create a directory if it does not exists
    &create_dir;
    &main_help_menu_css;
    print &print_page;
}    # End else

# Footer is here because it is printed from here on all pages without modifying other page structures
print &footer;
print "</body>\n";
print "</html>\n";

=head1 FUNCTION raised_upload_window

When the upload action is done, a new window is raised on the screen with info related to upload. This info now is the upload percent of the image file processing to directory.

=head2 PARAMETER(S)


=over 4


=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1

=back

=back

=head2 BUG KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Mar 04 2005

- I<Created on:> Mar 03 2005

=back

=back



=cut

sub raised_upload_window {    # Begin sub raised_upload_window
    print
"<script>\nwindow.open('bar.cgi','smallwin','bgcolor=blue,width=550,height=200,status=no,resizable=no');\n</script >\n";
}    # End sub raised_upload_window

=head1 FUNCTION menu_leave_admin

This function helps user to leave admin menu by creating a button on the screen.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 25 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub menu_leave_admin {    # Begin sub menu_leave_admin
    print "<form action='album.cgi' method='put'>\n";
    print "<input type='submit' value='Quitter ce menu / Leave this menu'>\n";
    print "<input type='hidden' name='service' value='leave'>\n";
    print "</form>\n";
}    # End sub menu_leave_admin

=head1 FUNCTION printPict

This function is used to print bigger picture.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Fev 14 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub printPict {    # Begin sub printPict
    my $img     = $doc->param('pict');
    my $comment = $doc->param('comments');
    my ( $french, $english ) = split( /SEPARATOR/, $comment );

    $french  = &switch_from_a_specified_tag_to_characters($french);
    $english = &switch_from_a_specified_tag_to_characters($english);
    print
"<br><br><br><center><img src='$img'><br><u>$french</u><br>/<br><u><i>$english</i></u></center><br><br><br>\n<a href='javaScript:history.back()'>Back</a> previous page\n<br>";
}    # End sub printPict

=head1 FUNCTION create_new_page

This function is called when a new page is asked to be created.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

New page created.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub create_new_page {    # Begin sub create_new_page
    open( R, "$file_conf_to_save" )
      or error_raised("File $file_conf_to_save does not exists");
    my @f = <R>;
    close(R);
    my $line = ();

    if ( scalar(@f) != 0 ) {    # Begin if (scalar(@f) != 0)
        my $value_not_exist = 1;

        foreach (@f) {          # Begin foreach (@f)
            $line = $_;
        }    # End foreach (@f)
        chomp($line);

        my @tmp_line = split( /\/\//, $line );
        $tmp_line[0]++;
        return "$tmp_line[0]||1";
    }    # End if (scalar(@f) != 0)
    else {    # Begin else
        return "1||1";
    }    # End else
}    # End sub create_new_page

=head1 FUNCTION number_of_pages

This function calculates number of pages to show on the screen when a user inserts, or modifies a picture.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Number of pages.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:>  Nov 10 2004

=back



=cut

sub number_of_pages {    # Begin sub number_of_pages
    open( R, "$file_conf_to_save" );
    my @all_file = <R>;
    close(R);
    my $num = ( ( split( /\|\|/, $all_file[ scalar(@all_file) - 1 ] ) )[0] );
    return ( ( "$num" eq "" ) ? 0 : $num );
}    # End sub number_of_pages

=head1 FUNCTION go_back

This function helps the user to go back on a previous page.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Feb 25 2006

- I<Last modification:>  Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub go_back {    # Begin sub go_back
    print
"<form action='album.cgi' method='POST'>\n<input type='submit' value='Menu principal / Go back to main menu'>\n</form>";
}    # End sub go_back

=head1 FUNCTION menu_page_title($title)

This function sets up the menu page title.

=head2 PARAMETER(S)


=over 4


$title: Enter title of the menu.

=back

=head2 RETURNED VALUE

=over 4

The title.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub menu_page_title {    # Begin sub menu_page_title
    my ( $title, $num_page ) = @_;

    return $doc->center( $doc->h1("$title") . $doc->h1("$num_page\n") )
      . $doc->br
      . $doc->br;
}    # End sub menu_page_title

=head1 FUNCTION menu_admin_title

This function creates menu admin.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Admin menu.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 NOTES

=over 4

Name's changed from menu_admin to menu_admin_title.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006.

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub menu_admin_title {    # Begin sub menu_admin_title
    print &menu_page_title( "MENU ADMIN" . $doc->br );
}    # End sub menu_admin_title

=head1 FUNCTION  admin_menu(@line_title)

This function manages the menu in order to insert a new page. A page must have a fixed length of image per it.

=head2 PARAMETER(S)


=over 4


@line_title: that's the line title for each pictures.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Fev 25 2006

- I<Last modification:> Jan 20 2005

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub admin_menu {    # Begin sub admin_menu
    my (@line_title) = @_;

    print "<table border=0>\n";
    &set_upload;
    &set_link;
    if ( $an_action ne "modify" ) {    # Begin  if ($an_action ne "modify")
        my $num = &number_of_pages;
        foreach my $l_title (@line_title) {    # Begin foreach @line_title
            print "<tr><td align=left valign=top>\n";
            &manage_position( (&number_of_pages), $l_title );
            print "</tr>\n";
        }    # End foreach @line_title
    }    # End  if ($an_action ne "modify")
    else {    # Begin  else of if ($an_action ne "modify")
        print
"<input type='hidden' name='page' value='$modify_page_position_in_album'>\n";
        print
"<input type='hidden' name='line' value='$modify_position_in_page'>\n";
    }    # Begin  if ($an_action ne "modify")
    &set_language(LANGUAGES);
    print "<input type=hidden name='upload' value='ok'>\n";
    print "<input type=hidden name='login' value='"
      . $doc->param("login") . "'>\n";
    print "<input type=hidden name='password' value='"
      . $doc->param("password") . "'>\n";
    print
"<input type=hidden name='Set_page_position_in_the_album' value='Page \#$modify_page_position_in_album @ row \#$modify_position_in_page'>\n";
    print "<input type=hidden name='service' value='check'>\n";
    print "<input type=hidden name='recording' value='check'>\n";
    print
"<tr><td align=right><input type=submit value='Envoyer la requete / Send query'><td><input type=reset value='Annuler / Reset'></tr>\n";
    print "</table>\n";
    print "</form>\n";
}    # End sub admin_menu

=head1 FUNCTION set_upload

This function sets upload button in menu. It manages all upload.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub set_upload {    # Begin sub set_upload
    if ( $an_action ne "modify" ) {    # Begin if ($an_action ne "modify")
        print
"<tr><td>Enter file name to upload from\n <select name='type_of_upload'>\n<option>Local</option>\n<option>http://</option>\n</select>\n<td><input TYPE=\"FILE\" name='file_name_img' size=50>\n";
        print "</tr>";

#	print "<tr><td>Enter name to save <td><input TYPE=\"text\" name='file_name_img_to' size=50>\n";
#	print "</tr>";
        print
"<tr><td>Enter URL here if http option above is choosen<td><input TYPE=\"text\" name='file_name_img2' size=50>\n";
    }    # End if ($an_action ne "modify")
}    # End sub set_upload

=head1 FUNCTION set_link

This function sets a link (optional) within French text or English text when asked in admin menu.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 2 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub set_link {    # Begin sub set_link
    chomp( $info_on_picture[10] );
    $info_on_picture[10] =~ s/[\(\)]//g;
    my ( $fr, $eng ) =
      split( /\;/, $info_on_picture[10] )
      ;           # we take last field (french and english comment and link)
    my ( $words,     $link )     = split( /\,/, $fr );
    my ( $words_eng, $link_eng ) = split( /\,/, $eng );

    print
"<tr><td valign=top aglign=left>Enter a name to link within the text for French comment <td><table><tr><td><input name='name_to_link' value='$words'><td>Enter the related link<input type=text name='link' value='$link'></tr></table></tr>\n";
    print
"<tr><td valign=top aglign=left>Enter a name to link within the text for English comment<td><table><tr><td> <input name='name_to_link_eng' value='$words_eng'><td>Enter the related link for eng<input type=text name='link_eng' value='$link_eng'></tr></table></tr>\n";
}    # End sub set_link

=head1 FUNCTION set_language( @languages)

This function sets language(s).

=head2 PARAMETER(S)


=over 4


@languages: that's the list of languages that can be set up.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub set_language {    # Begin sub set_language
    my @languages = @_;
    my $comment   = ();

    foreach $lng (@languages) {    # Begin foreach @languages
        if ( $lng =~ m/french/i ) {    # Begin if ($lng =~ m/french/i)
            $comment = $modify_french_comment;
        }    # End if ($lng =~ m/french/i)
        elsif ( $lng =~ m/english/i ) {    # Begin elsif ($lng =~ m/english/i)
            $comment = $modify_english_comment;
        }    # End elsif ($lng =~ m/english/i)
        $comment = &switch_from_a_specified_tag_to_characters($comment);
        $comment =~ s/\'/\&\#145/g;
        $comment =~ s/\"/\&\#147/g;
        print
"<tr><td>Comment of the picture in $lng <td><input type='text' name='lang_${lng}_comment' value=\"$comment\" size=50 maxlength=142></tr><br>\n";
    }    # End foreach @languages
    if ( $an_action eq "modify" ) {    # Begin if ($an_action eq "modify")
        print "<input type=hidden name='action' value='record_modify'>\n";
    }    # End if ($an_action eq "modify")
}    # End sub set_language

=head1 FUNCTION manage_position

This function manages different positions in the picture album.

=head2 PARAMETER(S)


=over 4


$number_of_page: that's the number of page.

$line: that's the line.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub manage_position {    # Begin sub manage_position
    my $number_of_page = $_[0];
    my $line           = $_[1];
    my $select_name    =
      $_[1];    # risk of error here to check because param $_[1] set twice
    $select_name =~ s/\ +/_/g;
    print "$line<td>\n";
    print "<table border=0 width=100%>\n<tr><td valign=top align=right>";

    if ( $line =~ m!text from the image! )
    {           # Begin if ($line =~ m!text from the image!)
        print "<select name='$select_name'>\n";
        print "<option>Left side of the image</option>\n";
        print "<option>Right side of the image</option>\n</select></tr>\n";
        print
"<tr><td align=left valign=top>Vertical <select name='vertical_text'>\n";
        print "<option>Top</option>\n";
        print "<option>Middle</option>\n";
        print "<option>Bottom</option>\n";
        print "</select>\n<td>\n";
        print "Horizontal <select name='horizontal_text'>\n";
        print "<option>Left</option>\n";
        print "<option>Middle</option>\n";
        print "<option>Right</option>\n";
        print "</select>\n";
    }    # End if ($line =~ m!text from the image!)
    elsif ( $line =~ m!position of the image!i )
    {    # Begin if ($select_name =~ m/aisle/i)
        print "<td valign=top align=left>Vertical <select name='vertical'>\n";
        print "<option>top</option>\n";
        print "<option>middle</option>\n";
        print "<option>bottom</option>\n";
        print "</select>\n\n";
        print
          "<td valign=top align=left>Horizontal <select name='horizontal'>\n";
        print "<option>Left</option>\n";
        print "<option>Middle</option>\n";
        print "<option>Right</option>\n";
        print "</select>\n";
    }    # End if ($line =~ m!text from the image!)
    print "</tr></table>\n";
}    # End sub manage_position

=head1 FUNCTION auth_menu

This function manages the Authentication menu.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub auth_menu {    # Begin sub auth_menu
    my $color = 'red';
    print $doc->br
      . &menu_page_title(
        "Album of pictures",
        "Authenticate" . $doc->br . "to access admin menu",
        ALBUM_VERSION
      );

    print "<center>\n";
    print "<form action='album.cgi' method=POST>\n";
    print
      "<table class=\"main_auth\" ><tr><td align=center valign=center><br>\n";
    print "<table class=\"auth\">\n";
    print "<tr><td>Enter login <td><input type=text name='login'>\n</tr>\n";
    print
      "<tr><td>Enter password<td><input type=password name='password'></tr>\n";
    print "<input type=hidden name='service' value='check'>\n";
    print "<input type=hidden name='login' >\n";
    print "<input type=hidden name='password'>\n";
    print "</table>\n";
    print
"<br>\n<input type=submit value='Soumettre :) / Submit :)'>\n<input type='reset' value='Annuler / Reset'><br>\n";
    print "</form><br>\n";
    &go_back;
    print "</tr></table>\n";
    print "</center>\n";
    print $doc->br
      . $doc->br
      . $doc->br
      . $doc->br
      . $doc->br
      . $doc->br
      . $doc->br;
}    # End sub auth_menu

=head1 FUNCTION footer

This function standardizes footer within menus.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

New footer string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006

- I<Created on:> Jan 27 2006

=back



=cut

sub footer {    # Begin sub footer
    return $doc->table(
        {
            -class => "footer",
            -width => '100%'
        },
        $doc->Tr(
            $doc->td(
                {
                    -align  => 'left',
                    -valign => 'top'
                },
                "Designed by "
                  . $doc->a(
                    {
                        -href =>
'mailto:shark.bait@laposte.net?subject=Album of pictures'
                    },
                    COMPAGNY
                  )
                  . " and written by "
                  . $doc->a(
                    {
                        -href =>
'mailto:flotilla.reindeer@laposte.net?subject=Album of pictures'
                    },
                    AUTHOR
                  )
                  . $doc->br
                  . "<font class=\"footer\">Script version "
                  . ALBUM_VERSION . "<br>"
                  . "Tested with browsers: "
                  . TESTED_WITH_BROWSERS . "."
                  . "</font>"
            ),
            $doc->td(
                {
                    -align  => 'right',
                    -valign => 'bottom'
                },
                $doc->img( { -src => $images_used[3] } )
                  . $doc->br
                  . "Hosted by"
                  . $doc->a(
                    { -href => 'http://www.zendurl.com' }, HOSTED_BY
                  )
            )
        )
    );
}    # End sub footer

=head1 FUNCTION check_password

This function checks password for admin.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

0 if ok otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

-1 is returned and means that a problem occured.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub check_password {    # Begin sub check_password
    if ( $doc->param("service") eq "check" ) {  # Begin if ($service eq "check")

        #	print $doc->p("Check passed");
        if ( $doc->param('prev_pid') eq "" )
        {    # Begin if ( $doc->param('prev_pid') eq "")

            #	    print $doc->p("Prev pid passed");
            if ( $user_login eq "$login" )
            {    # Begin if ($user_login eq "$login")

                #		print $doc->p("Login passed");
                if ( $user_password eq "$password" )
                {    # Begin if ($user_password eq "$password")
                    print $doc->p("Password passed");
                    open( PID, ">album/pid" )
                      || die("Can't create album/pid: $!");
                    print PID $$;
                    close(PID);
                    return 0;
                }    # End if ($user_password eq "$password")
            }    # End if ($user_login eq "$login")
        }    # End if ( $doc->param('prev_pid') eq "")
        else {    # Begin else
            open( OLD_PID, "album/pid" ) || die("Can't open album/pid: $!");
            my $pid;
            foreach (<OLD_PID>) {    # Begin foreach (<OLD_PID>)
                chomp($_);
                $pid .= $_;
            }    # End foreach (<OLD_PID>)
            close(OLD_PID);

            #	    print "('$my_pid' ne '$pid')\n";
            if ( $my_pid != $pid ) {    # Begin if ($my_pid != $pid)
                return -1;
            }    # End if ($my_pid != $pid)
            open( PID, ">album/pid" ) || die("Can't create album/pid: $!");
            print PID $$;
            close(PID);
            $user_password = "";
            $user_login    = "";
            return 0;
        }    # End else
    }    # End if ($service eq "check")
    else {    # Begin else

        #	print $doc->p("Check not passed");
    }    # End else
    return -1;
}    # End sub check_password

=head1 FUNCTION numbers

This function sorts numbers when it is used with the sort function.

=head2 PARAMETER(S)


=over 4


$a: value to sort.

$b: value to sort.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

-1 if $a smaller that $b,0 is $a equals to $b, else 1

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub numbers {    # Begin sub numbers
    my @la = split( /\|\|/, $a );
    my @lb = split( /\|\|/, $b );

    if ( $a ne $b ) {    # Begin if ($a ne $b)
        ( $la[0] <=> $lb[0] ) || ( $la[1] <=> $lb[1] );
    }    # End if ($a ne $b)
}    # End sub numbers

=head1 FUNCTION record

This function records information into a file named $file_conf.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 17 2006

- I<Last modification:> Mar 29 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub record {    # Begin sub record
    my (
        $file_name,               $page_position_in_album,
        $valign,                  $halign,
        $french_comment,          $english_comment,
        $vertical_text,           $horizontal_text,
        $position_from_the_image, $link_name,
        $link,                    $link_name_eng,
        $link_eng
      )
      = (
        $doc->param("file_name_img"),
        $doc->param("Set_page_position_in_the_album"),
        $doc->param("vertical"),
        $doc->param("horizontal"),
        $doc->param("lang_French_comment"),
        $doc->param("lang_English_comment"),
        $doc->param("vertical_text"),
        $doc->param("horizontal_text"),
        $doc->param("Set_position_of_the_text_from_the_image_in_compartment"),
        $doc->param("name_to_link"),
        $doc->param("link"),
        $doc->param("name_to_link_eng"),
        $doc->param("link_eng")
      );

    $file_name = &reformat($file_name);
    my $type_upload = $doc->param("type_of_upload");
    my @save_result = ();

    print $doc->p(
        "<br><br><br><br>Information recorded." .
          #		  " Name to link:".$doc->param("name_to_link").
          #		  " Name linked with:".$doc->param("link").
          #		  " Name to link eng:".$doc->param("name_to_link_eng").
          #		  " Name linked with eng:".$doc->param("link_eng") .
          $doc->br
    );

    if ( $doc->param("Set_page_position_in_the_album") eq "" )
    {    # Begin if ($doc->param("Set_page_position_in_the_album") eq "" )
        error_raised( $doc,
                "No page position set in the previous menu here is the value ["
              . $doc->param("Set_page_position_in_the_album")
              . "]" );
    }    # End if ($doc->param("Set_page_position_in_the_album") eq "" )

# Next session deals with the file to upload (from menu where you choose the file to upload as local)
    if ( $type_upload eq "Local" ) {    # Begin if ($type_upload eq "Local")
#        if ( $doc->param("file_name_img") =~ m/([^\/\\]+)$/ )
#        {    # Begin if ($doc->param("file_name_img") =~ m/([^\/\\]+)$/)
#            $file_name = $suffix_for_image_file . $file_name ; # $doc->param("file_name_img");
#        }    # End if ($doc->param("file_name_img") =~ m/([^\/\\]+)$/)
             # if there's any space in the filename, get rid of them
# changed
#        $file_name =~ s/\s+//g;
        if ( $file_name =~ m/\\/ ) {    # Begin if ($file_name =~ m/\\/)
            my @l_file_scat = split( /\\/, $file_name );
            $file_name = $l_file_scat[ scalar(@l_file_scat) - 1 ];
        }    # End if ($file_name =~ m/\\/)
    }    # End if ($type_upload eq "Local")
#    $file_name =~ tr/A-Z/a-z/;

    # That's the end of session at the end this session will be remove

    $page_position_in_album =~ s/\ *\@\ */\|\|/g;
    $page_position_in_album =~ s/\ *(Page|[\#]|row)\ *//g;
    if ( $page_position_in_album =~ m/create/i )
    {    # Begin if ( $page_position_in_album =~ m/create/)
        $page_position_in_album = &create_new_page;
    }    # End if ( $page_position_in_album =~ m/create/i)
         # Case we want to save info but no modification is required
    if ( $an_action ne "record_modify" )
    {    # Begin if ($an_action ne "record_modify")
         #                                  Begin if record modify action not requested

       #	print $doc->p("case 1");
       # if file exists then we get its content then we sort it and then save it
        if ( -f "$file_conf_to_save" )
        { # Begin if case where all info related to files are stored and already exists
            my $pages_num = 0;

            open( CHECK, "$file_conf_to_save" );
            @save_result = <CHECK>;
            close(CHECK);
            @save_result = sort numbers @save_result;

            foreach (@save_result) {    # Begin foreach @save_result
                                        # format of BD:
                 #    page||row||img||comment pos v||comment pos h||French comment||English comment||img pos h||img pos v||comment pos to img||(french link,url french link);(english link,url english link)
                chomp($_);

                my @in_file = split( /\|\|/, $_ );
                $page_num = $in_file[0];
                if ( $position_in_page =~ /last/i )
                {    # Begin  if ($position_in_page =~ /last/i)
                    if ( $page_position_in_album == $page_num )
                    {    # Begin if ($page_position_in_album == $page_num)
                        if ( $in_file[1] == MAX_IMAGES_PER_PAGE )
                        {    # Begin if ($in_file[1] == MAX_IMAGES_PER_PAGE)
                            error_raised( $doc,
                                "Maximum of images reached per page which is "
                                  . MAX_IMAGES_PER_PAGE );
                        }    # End if ($in_file[1] == MAX_IMAGES_PER_PAGE)
                    }    # End if ($page_position_in_album == $page_num)
                }    # End if ($position_in_page =~ /last/i)
                if (   $page_position_in_album == $in_file[0]
                    && $position_in_page == $in_file[1] )
                { # Begin if ( $page_position_in_album == $in_file[0] && $position_in_page == $in_file[1] )
                    error_raised( $doc,
"This place is already taken by another picture [(pos in album=$page_position_in_album == $page_num = page number),(row in page = $in_file[1] == "
                          . MAX_IMAGES_PER_PAGE
                          . "max row(s) per page)]" );
                } # End if ( $page_position_in_album == $in_file[0] && $position_in_page == $in_file[1] )
            }    # End foreach (@save_result)
        } # End if case where all info related to files are stored and already exists
          # Code not in use anymore
        if ( $page_position_in_album =~ m/create/i )
        {    # Begin if ($page_position_in_album =~ m/create/i)
            $page_position_in_album = $page_num + 1;
        }    # End if ($page_position_in_album =~ m/create/i)
             # End of code not in use
        $french_comment  = ( $french_comment  eq "" ) ? "." : $french_comment;
        $english_comment = ( $english_comment eq "" ) ? "." : $english_comment;
        $page_position_in_album = $doc->param("Set_page_position_in_the_album");
        $page_position_in_album =~ s/\ *\@\ */\|\|/g;
        $page_position_in_album =~ s/\ *(Page|[\#]|row)\ *//g;
        if ( $page_position_in_album =~ m/create/i )
        {    # Begin if ( $page_position_in_album =~ m/create/)
            $page_position_in_album = &create_new_page;
        }    # End if ( $page_position_in_album =~ m/create/i)

        @save_result = (
            @save_result,
            $page_position_in_album . "||"
              .
              #			$doc->param("file_name_img_to") . "||" .
              $suffix_for_image_file
              . $file_name . "||" # $doc->param("file_name_img") . "||"
              . $doc->param("vertical") . "||"
              . $doc->param("horizontal") . "||"
              . &switch_from_a_specified_character_to_tag(
                $doc->param("lang_French_comment")
              )
              . "||"
              . &switch_from_a_specified_character_to_tag(
                $doc->param("lang_English_comment")
              )
              . "||"
              . $doc->param("horizontal_text") . "||"
              . $doc->param("vertical_text") . "||"
              . $doc->param(
                "Set_position_of_the_text_from_the_image_in_compartment")
              . "||" . "("
              . $doc->param("name_to_link") . ","
              . $doc->param("link") . ")" . ";" . "("
              . $doc->param("name_to_link_eng") . ","
              . $doc->param("link_eng") . ")"
        );
        @save_result = sort numbers @save_result;
    }    # End if ($an_action ne "record_modify")
    else {    # Begin else
              #    Else record modify action requested
        my $local_page = $doc->param("page");
        my $local_line = $doc->param("line");

        #	print $doc->p("case 2");
        open( R, "$file_conf_to_save" )
          || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
        my @all_file = <R>;
        close(R);
        foreach (@all_file) {    # Begin foreach (@all_file)
            chomp($_);
            my (
                $page_position_in_album, $position_in_page,
                $file_name,              $valign,
                $halign,                 $french_comment,
                $english_comment,        $vertical_text,
                $horizontal_text,        $position_from_the_image,
                $related_link
              )
              = split( /\|\|/, $_ );
            if ( $page_position_in_album eq $local_page )
            {    # Begin if ( $page_position_in_album eq $local_page)
                if ( $position_in_page eq $local_line )
                {    # Begin if ( $position_in_page eq $local_line )
                    print "position found and changed: $related_link <br>";

                    $_ =
		      "$page_position_in_album||$position_in_page||$file_name||$valign||$halign||"
                      . $doc->param("lang_French_comment") . "||"
                      . $doc->param("lang_English_comment")
                      . "||$vertical_text||$horizontal_text||$position_from_the_image||"
                      . "("
                      . $doc->param("name_to_link") . ","
                      . $doc->param("link") . ")" . ";" . "("
                      . $doc->param("name_to_link_eng") . ","
                      . $doc->param("link_eng") . ")";
                }
                else {    # Else of if ( $position_in_page eq $local_line )
                    @tmp = ( @tmp, "$_" );
                }    # End if ( $position_in_page eq $local_line )
            }
            else {    # Else if ( $page_position_in_album eq $local_page)
                @tmp = ( @tmp, "$_" );
            }    # End if ( $page_position_in_album eq $local_page)
        }    # End foreach (@all_file)
        @save_result = @all_file;
    }    # End else
         # End if Record modify action requested

    open( S_CONF, ">$file_conf_to_save" )
      or error_raised( $doc, "File [$file_conf_to_save] does not exist !!!" );
    foreach my $in (@save_result) {    # Begin foreach @save_result
        chomp($in);
        print S_CONF "$in\n";
    }    # End foreach @save_result
    close(S_CONF);
}    # End sub record

=head1 FUNCTION create_dir

This function creates a directory in order to store all information related to album info.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub create_dir {    # Begin sub create_dir
    if ( !-d "$album_directory" ) {    # Begin if (!-d "$album_directory")

#       mkdir("$album_directory",0700) || die("Cannot create $album_directory\n");
        `mkdir $album_directory`;
        `chmod 700 $album_directory`;
    }    # End if (!-d "$album_directory")
    if ( !-f "$file_conf_to_save" ) {    # Begin if (!-f "$file_conf_to_save")
        open( W, ">$file_conf_to_save" )
          || die("Cannot create $file_conf_to_save\n");
        print W "";
        close(W);
    }    # End if (!-f "$file_conf_to_save")
    open( F, "$file_conf_to_save" );
    my @local_f  = <F>;
    my $num_line = 0;
    if ( scalar(@local_f) < 2 && scalar(@local_f) > 0 )
    {    # Begin if (scalar(@local_f) < 2 && scalar(@local_f) > 0)
        foreach (@local_f) {    # Begin foreach (@local_f)
            chomp($_);
            @o = split( /\|\|/, $_ );

            $_ =~ s/\ *//;
            if ( $_ eq "" ) {    # Begin if ($_ eq "")
                &under_construction_prompt;
            }    # End if ($_ eq "")
        }    # Begin foreach (@local_f)
        close(F);
    }    # End if (scalar(@local_f) < 2 && scalar(@local_f) > 0)
    elsif ( scalar(@local_f) == 0 ) {    # Begin elsif (scalar(@local_f) == 0)
        &under_construction_prompt;
    }    # End elsif (scalar(@local_f) == 0)
}    # End sub create_dir

=head1 FUNCTION under_construction_prompt

This function prints under construction prompt (picture) on the screen.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub under_construction_prompt {    # Begin sub under_construction_prompt
    print "<br><br><br><br><center>\n";
    print "<table border=0>\n<tr>\n<td align=right>\n";
    &look_for_images_used;
    print "<td>\n<center>\n<img src='"
      . DIRECTORY_DEPOSIT
      . "under_construction10.gif'>\n<br>\n<br>\n<br>\n";
    print "<a href='album.cgi?service=auth'><img src='"
      . DIRECTORY_DEPOSIT
      . "chair1-a.gif' border=0 alt='Click me'></a><br><b><a href='album.cgi?service=auth'>Administer le Cyber Album</a></b> / <font color='gray42'><b><a href='album.cgi?service=auth'>Administrate Cyber Album</a></b></font><br>";
    print "<img src='" . DIRECTORY_DEPOSIT . "under_construction10.gif'> \n";
    print
"<br>\n<br>\nAller <a href='$url_demo'>version</a> precedente / <font color='gray42'>Go to previous <a href='$url_demo'>version</a>.\n</font><br>\n"
      . $doc->br
      . $doc->br
      . $doc->img( { -src => DIRECTORY_DEPOSIT . 'powered.gif' } )
      . $doc->br
      . "Hosted by "
      . $doc->a( { -href => HOSTED_BY_URL }, HOSTED_BY )
      . "</center>\n";
    print "</table>\n";
    exit(-1);
}    # End sub under_construction_prompt

=head1 FUNCTION size_dir($dir)

This function calculates the size of directory.

=head2 PARAMETER(S)


=over 4


$dir: directory.

=back

=head2 RETURNED VALUE

=over 4

Returns size of the directory.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub size_dir {    # Begin sub size_dir
    my $dir          = shift;
    my $size_dir_tmp = 0;

    opendir DIR, $dir or die "Impossible to open $dir: $!";
    while ( readdir DIR ) {    #  Begin  while (readdir DIR)
        $size_dir_tmp += -s "$dir/$_";
    }    # End while (readdir DIR)
    return $size_dir_tmp;
}    # End sub size_dir

=head1 FUNCTION error_raised($doc,$explaination)

This function generates an error message when a problem occurs.

=head2 PARAMETER(S)


=over 4


$doc: that's an implementation of the object CGI (new CGI to be precised).

$explaination: explaination of the error.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub error_raised {    # Begin sub error_raised
    my ($explaination) = @_;
    print $doc->header("text/html"),

      #    $doc->start_html("Error"),
      $doc->h1("Error"),
      $doc->p(
        "Your deposit was not successul because of the following error: "),
      $doc->p( $doc->i($explaination) ),
      $doc->p("<a href=\"JavaScript:history.back()\">go back</a>"),

      #    $doc->end_html;
      exit;
}    # End sub error_raised

=head1 FUNCTION error_raised_visit($doc,$explaination)

This function generates an error message when problem occurs.

=head2 PARAMETER(S)

=over 4

$doc: that's an implementation of the object CGI (new CGI to be precised).

$explaination: explaination of the error.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub error_raised_visit {    # Begin sub error_raised_visit
    my ( $doc, $explaination ) = @_;
    print $doc->header("text/html"), $doc->start_html("Error"),
      $doc->h1("Error"),
      $doc->p("Your visit was not successul because of the following error: "),
      $doc->p( $doc->i($explaination) ),
      $doc->p("<a href=\"JavaScript:history.back()\">go back</a>"),
      $doc->end_html;
    exit;
}    # End sub error_raised_visit

=head1 FUNCTION  show_page_not_taken_yet

This function shows pages that are taken.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 28 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub show_page_not_taken_yet {    # Begin sub show_page_not_taken_yet
    open( SHOW, "$file_conf_to_save" )
      or error_raised("File $file_conf_to_save does not exists");
    my @save_info = <SHOW>;
    close(SHOW);
    my $script_page_taken =
"<table width=100% border=0><tr>\n<td bgcolor='#CF6748' align=center>Nouvelles postions / New positions</tr>\n<tr><td align=center valign=center><select name='Set_page_position_in_the_album' size=12>\n"
      ;                          # Filnal script to print
    my $lmax =
      ( split( /\|\|/, $save_info[ scalar(@save_info) - 1 ] ) )[0]
      ;                          # Max of lines
    my $s =
      ()
      ; # String that store all pages in order to create option list with true missing pages and rows
    my $first_pass = 0;    # used when option need to be selected as default

# Problem solve as in this way: a matrix (page, line). Enumerate all possibilities in a list.
# read page already saved. Remove from the list page already saved. And print the matrix of page not taken.
    for ( my $l = 1 ; $l != ( $lmax + 1 ) ; $l++ )
    {                      # Begin for (my $l = 1;$l != ($lmax+1);$l++)
        for ( my $c = 1 ; $c != ( MAX_IMAGES_PER_PAGE + 1 ) ; $c++ )
        {    # Begin for ($c = 1; $c != (MAX_IMAGES_PER_PAGE+1); $c++)
            $s .= "$l $c;";
        }    # End for ($c = 1; $c != (MAX_IMAGES_PER_PAGE+1); $c++)
    }    # End for (my $l = 1;$l != ($lmax+1);$l++)

    foreach (@save_info) {    # Begin foreach (@save_info)
        @line = split( /\|\|/, $_ );              #save_info
        $add = $line[0] . " " . $line[1] . ";";
        $s =~ s/$add//;
    }    # End foreach (@save_info)

    foreach ( split( /\;/, $s ) ) {    # Begin foreach (split(/\;/,$s))
        my ( $p, $l ) = split( /\ /, $_ );

        if ( $first_pass == 0 ) {      # Begin if ($first_pass == 0)
            $script_page_taken .=
              "<option selected>Page #$p @ row #${l}</option>\n";
            $first_pass++;
        }    # End if ($first_pass == 0)
        else {    # Begin else
            $script_page_taken .= "<option>Page #$p @ row #${l}</option>\n";
        }    # End else
    }    # End foreach (split(/\;/,$s))

    $script_page_taken .=
      "<option>\nCreate a new page\n</option>\n</select></tr>\n</table>\n";

    print $script_page_taken ;
}    # End sub show_page_not_taken_yet

=head1 FUNCTION show_list_pictures

This function shows the list of pictures.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 6 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub show_list_pictures {    # Begin sub show_list_pictures
    open( SHOW, "$file_conf_to_save" )
      or error_raised("File $file_conf_to_save does not exists");
    my @save_info = <SHOW>;
    close(SHOW);
    print
      "<fieldset><legend align='Top'>\nPicture(s) already set</legend>\n<ol>\n";
    print "<table><tr><td align=center valign=center bgcolor='#D0EFE6'>\n";
    print "<table border=0><tr>\n";
    print "<td width=90% valign=Top align=left bgcolor='#9CDCCA'>\nComments\n";
    print
"<td width=90% valign=Top align=left bgcolor='#9CDCCA'>\nWhere is comment\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Page\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Line\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Text position\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Image position\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Image view\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Link on word(s)\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>URL\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Modify\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Remove\n";
    print "<td valign=Top align=center bgcolor='#9CDCCA'>Operations</tr>\n";

    foreach my $line_comment (@save_info)
    {    # Begin foreach my $line_comment (@save_info)
        @line = split( /\|\|/, $line_comment );
        ( $word, $link, $word_eng, $link_eng ) = &split_links( $line[10] );
        print "<form action='album.cgi' method=post>\n";
        print "<tr><td valign=Top align=left>\n<li>"
          . &switch_from_a_specified_tag_to_characters( $line[5] ) . "<br><font color=\#822942>"
          . &switch_from_a_specified_tag_to_characters( $line[6] )
          . "</font></li>\n";
        print "<td align=center valign=center>\n$line[9]\n";
        print
	  "<td align=center valign=center>\n$line[0]<td align=center valign=center>$line[1]\n";
        print "<td align=center valign=center>\n$line[7]/$line[8]\n";
        print "<td align=center valign=center>\n$line[3]/$line[4]\n";

        if ( $line[2] !~ m/^http\:\/\//i )
        {    # Begin if ($line[2] !~ m/^http\:\/\//i)
            print "<td align=center valign=center>\n<img src='"
              . DIRECTORY_DEPOSIT
              . "$line[2]' width='75'  height='75'>\n";
        }    # End if ($line[2] !~ m/^http\:\/\//i)
        else {    # Begin else
            print
"<td align=center valign=center>\n<img src='$line[2]' width='75'  height='75'>\n";
        }    # End else
        print
	  "<td align=center valign=center>\n$word<br><font color=\#822942>$word_eng</font>".
	    "<td align=center valign=center>$link<br><font color=\#822942>$link_eng</font>\n";
        print "<td align=center valign=center>\n";
        print "<input type='radio' name='action' value='modify'>\n";
        print "<td align=center valign=center>\n";
        print "<input type='radio' name='action' value='remove'>\n<td>\n";
        print "<input type='hidden' name='login' value='"
          . $doc->param("login") . "'>\n";
        print "<input type='hidden' name='password' value='"
          . $doc->param("password") . "'>\n";
        print "<input type='hidden' name='page' value='$line[0]'>\n";
        print "<input type='hidden' name='line' value='$line[1]'>\n";
        print "<input type='hidden' name='service' value='check'>\n";
        print "<input type='submit'  value='Soumettre :) / Submit :)'>\n";
        print "</form></tr>\n";
    }    # End foreach my $line_comment (@save_info)
    print "</table>\n\n</fieldset>\n";
    print "</table>\n";
}    # End sub show_list_pictures

=head1 FUNCTION split_links($language)

This function split links in a given string ($language). That's what it is returned from $language ($word_to_link,$link,$word_to_link_eng,$link_eng).

=head2 PARAMETER(S)


=over 4


$language: that's the list of possible languages.

=back

=head2 RETURNED VALUE

=over 4

$word_to_link: word to link in French.

$link: that's the link for French.

$word_to_link_eng: word to link in English.

$link_eng: that's the link.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub split_links {    # Begin sub split_links
    my ( $fr_l,             $en_l )     = split( /\;/, $_[0] );
    my ( $word_to_link,     $link )     = split( /\,/, $fr_l );
    my ( $word_to_link_eng, $link_eng ) = split( /\,/, $en_l );

    $word_to_link     =~ s/\(//g;
    $link             =~ s/\)//g;
    $word_to_link_eng =~ s/\(//g;
    $link_eng         =~ s/\)//g;
    return ( $word_to_link, $link, $word_to_link_eng, $link_eng );
}    # End sub split_links

=head1 FUNCTION remove_picture

This function gets a picture to be removed. A line and, a page number are necesessary to know the location of the picture. These information are taken with $doc->param('...') function that's why no parameters are used.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 23rd 2006

- I<Last modification:> Nov 10th 2004

- I<Created on:> Nov 10th 2004

=back

=cut

sub remove_picture {    # Begin sub remove_picture
    my @tmp            = ();
    my @all_file       = ();
    my $local_page     = $doc->param("page");
    my $local_line     = $doc->param("line");
    my $file_to_remove = ();

    open( R, "$file_conf_to_save" )
      || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
    @all_file = <R>;
    close(R);

    # We remove a line from a given page from the album
    foreach (@all_file) {    # Begin foreach (@all_file)
        chomp($_);
        my @line = split( /\|\|/, $_ );
        if ( $line[0] eq $local_page ) {    # Begin if ($line[0] eq $local_page)
            if ( $line[1] eq $local_line )
            {    # Begin if ( $line[1] eq $local_line )
                $file_to_remove = $line[2];
                print "---> Line <b>$_</b> removed.<br>";
            }    # End if ( $line[1] eq $local_line )
            else {    # Else of if ( $line[1] eq $local_line )
                @tmp = ( @tmp, "$_" );
            }    # End if ( $line[1] eq $local_line )
        }    # End if ($line[0] eq $local_page)
        else {    # Else of if ($line[0] eq $local_page)
            @tmp = ( @tmp, "$_" );
        }    # End if ($line[0] eq $local_page)
    }    # End foreach (@all_file) {

    if ( scalar(@all_file) > scalar(@tmp) )
    {    # Begin if (scalar(@all_file) > scalar(@tmp))
        @all_file = @tmp;
    }    # End if (scalar(@all_file) > scalar(@tmp))

    # We check if the picture to remove is not use into another comment of picture before destroying it.
    my $linked_to_other_comment = 0;
    my @list_file = ();

    foreach (@all_file) {    # Begin foreach (@all_file)
        my @line = split( /\|\|/, $_ );
	@list_file = (@list_file,DIRECTORY_DEPOSIT . $line[2]);
    }    # End foreach (@all_file)

    # We create the new file_conf
    open( W, ">$file_conf_to_save" )
      || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
    flock( W, LOCK_EX | LOCK_SH );
    foreach (@tmp) {    # Begin foreach (@tmp)
        print W "$_\n";
    }    # End foreach (@tmp)
    close(W);

    # We remove the image that goes with the associated comment if no more use than once in the album otherwise it is not removed
    my $local_dir = DIRECTORY_DEPOSIT . "$file_to_remove";
    unlink("$local_dir") || die("$local_dir cannot be removed");
    print "Picture removed from te disk<br>\n";
    &clean_pictures(@list_file);
}    # End sub remove_picture


=head1 FUNCTION clean_pictures

This function cleans pictures. The picrures removed are the pictures that are not anymore in the album.

=head2 PARAMETER(S)

=over 4

@list: that's the list of pictures that are in the album.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 22sd 2006

- I<Created on:> Aug 22sd 2006

=back

=cut

sub clean_pictures { # Begin sub clean_pictures
  my (@list) = @_;
  my $dir =  DIRECTORY_DEPOSIT . "200*";
  my @l = `ls $dir`;

  if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me") { # Begin if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me")
    print "Will clean pictures that were recorded and removed from the album but still on the disk...<br>\n";
    open(WPICT,">${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me") || 
      die("${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me cannot be created $!");
    print WPICT " ";
    close(WPICT) ||   die("${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me cannot be closed $!");
    foreach my $list_pict (@l) { # Begin foreach my $list_pict (@l)
      my $is_ok = 0;
      chomp($list_pict);
      foreach my $elem_pict (@list) { # Begin foreach my $elem_pict (@list)
	chomp($elem_pict);
	
	if ($list_pict eq $elem_pict) { # Begin if ($list_pict eq $elem_pict)
	  $is_ok = 1;
	} # End if ($list_pict eq $elem_pict)
      }  # End foreach my $elem_pict (@list)
      if (!$is_ok) { # Begin if (!$is_ok)
	unlink("$list_pict") || die("$list_pict cannot be removed");
      } # End if (!$is_ok)
    } # End foreach my $list_pict (@l)
    print "Pictures removed :)<br>";
  } # End if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me")
}  # End sub clean_pictures

=head1 FUNCTION return_info_picture

This function returns info related to picture. At this time, looks in the file where info are stored, then returns line concerned, if it exists.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub return_info_picture {    # Begin sub return_info_picture
    my @tmp            = ();
    my @all_file       = ();
    my $local_page     = $doc->param("page");
    my $local_line     = $doc->param("line");
    my $file_to_remove = ();

    open( R, "$file_conf_to_save" )
      || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
    @all_file = <R>;
    close(R);

    # We remove a line from a given page from the album
    foreach (@all_file) {    # Begin  foreach (@all_file)
        chomp($_);
        my @line = split( /\|\|/, $_ );
        if ( $line[0] eq $local_page ) {    # Begin if ($line[0] eq $local_page)
            if ( $line[1] eq $local_line )
            {    # Begin if ( $line[1] eq $local_line )
                return @line;
            }    # End if ( $line[1] eq $local_line )
            else {    # Begin else
                @tmp = ( @tmp, "$_" );
            }    # End else
        }    # End if ($line[0] eq $local_page)
        else {    # Begin else
            @tmp = ( @tmp, "$_" );
        }    # End else
    }    # End foreach (@all_file)
}    # End sub return_info_picture

=head1 FUNCTION put_url_line($word_to_link,$line,$url)

When we print info on screen we put url if there is a link.

=head2 PARAMETER(S)


=over 4


$word_to_link: that's the word to link.

$line: that's the line to look for the word(s) to link.

$url: that's the url to link to the word(s).

=back

=head2 RETURNED VALUE

=over 4

Returns the linked string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub put_url_line {    # Begin sub put_url_line
    my $word_to_link = $_[0];
    my $line         = $_[1];
    my $url          = $_[2];
    chomp($word_to_link);
    chomp($line);
    chomp($url);

    $line =~
      s/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/$1\<a href=\"$url\"\>$2\<\/a\>$3/gi;

# Had to do a second time because when ([\ \,\.\'\;\:\!\?\"\)])($word_to_link) is used then sencond occurence of that does not work
# We need to do it a sencond time
    $line =~
      s/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/$1\<a href=\"$url\"\>$2\<\/a\>$3/gi;

# Need to do it in that order otherwise does not work properly for te time being.
# Look at the end of the string
    $line =~
      s/([\ \,\.\'\;\:\!\?\"\)])($word_to_link)$/$1\<a href=\"$url\"\>$2\<\/a\>/gi;

    # Look at the begining of string
    $line =~
      s/^($word_to_link)([\ \,\.\'\;\:\!\?\"\(])/\<a href=\"$url\"\>$1\<\/a\>$2/gi;

    # Extra test if it is only a word in the sentence
    $line =~ s/^($word_to_link)$/\<a href=\"$url\"\>$1\<\/a\>$2/gi;

    return $line;
}    # End sub put_url_line

=head1 FUNCTION print_page

This function prints an HTML page for the album. There's automatic link to next page(s).

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 7 2006

- I<Last modification:> Fev 6 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub print_page {    # Begin sub print_page
    my $page_asked                = $doc->param("page");
    my $print_my_page_script_head =
      ()
      ; #"<script language='javascript'>\nfunction BigPict(i) {\n var toto = '<html><body> <img src=\"' + i + '\"><br>Go <a href=\"javascript:history.back()\">back</a><br></body>';\n document.write(toto);return 0; }\n</script>\n";
    my $print_my_page_script   = ();
    my @all_file               = ();
    my $list_page_beg          = "&nbsp;&nbsp;";
    my $list_page              = "<table border=0><tr>";
    my $prev                   = 1;
    my $prev_page              = ();
    my $next_page              = ();
    my @line                   = ();
    my @list_of_existing_pages = ();
    chomp($page_asked);
    my $div = $page_asked / MAX_IMAGES_PER_PAGE;
    my ( $word_to_link,     $my_link )     = ();
    my ( $word_to_link_eng, $my_link_eng ) = ();

    $div = ( split( /\./, $div ) )[0];

# We setup min range and max range of page number to show up on the navigator menu of the album.
    my $RANK_MIN_PICT_SHOW = (
        ( $div < 1.0 )
        ? 1
        : ( $div * MAX_IMAGES_PER_PAGE )
    );

# We set up min range and max range of page number to show up on the navigator menu of the album.
    my $RANK_MAX_PICT_SHOW =
      &rank_right_navigator_bar_range(
        $RANK_MIN_PICT_SHOW + ( MAX_IMAGES_PER_PAGE - 1 ) );

    open( R, "$file_conf_to_save" )
      || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
    @all_file = <R>;
    close(R);

# This line was added because of case empty page (no number of page). If so, page asked is the first one
    $page_asked =
      ( "$page_asked" eq "" || "$page_asked" eq "0" )
      ? &get_first_page_number
      : $page_asked;

    $print_my_page_script .= "<table border=0 width='75\%'>\n";

    foreach (@all_file) {    # Begin foreach (@all_file)
        chomp($_);
        my @line = split( /\|\|/, $_ );

# we get word to link in order to make on screen a link on other web sites. This is done for French and English version.
        ( $word_to_link, $my_link, $word_to_link_eng, $my_link_eng ) =
          &split_links( $line[10] );

        if ( $word_to_link ne "" && $word_to_link_eng ne "" )
        {    # Begin if ($word_to_link ne "" && $word_to_link_eng ne "")
            chomp($my_link);
            chomp($my_link_eng);

            $line[5] = &put_url_line( $word_to_link, $line[5], $my_link );
            $line[6] = &put_url_line( $word_to_link_eng, $line[6], $my_link_eng );
        }    # End if ($word_to_link ne "" && $word_to_link_eng ne "")
        else {    # Begin else
            $line[5] = &switch_from_a_specified_tag_to_characters( $line[5] );
            $line[6] = &switch_from_a_specified_tag_to_characters( $line[6] );
        }    # End else
        @list_of_existing_pages = ( @list_of_existing_pages, $line[0] );

# To print nicely list of images you have to modify rhez following lines. For the time being only the next line commented.
        if ( $my_prev != $line[0] ) {    # Begin if ($my_prev != $line[0])
            if ( $page_asked != $line[0] )
            {                            # Begin if ($page_asked != $line[0])
                if ( ( $my_prev != 1 ) )
                { # && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) ) { # Begin if ( ($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                    if ( ( $line[0] % MAX_PAGE_PER_LINE_INDEX ) <
                        ( $my_prev % MAX_PAGE_PER_LINE_INDEX ) )
                    {    # Begin if ($line[0] % 10 == 0)
                        $list_page .= " </tr><tr>\n";
                    }    # End if ($line[0] % 10 == 0)
                    $list_page .=
"<td align=center><a href='album.cgi?page=$line[0]'>$line[0]</a>\n";
                } # End if ( ($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                else
                { #  Begin else of if ( ($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                    if ( ( $line[0] % MAX_PAGE_PER_LINE_INDEX ) == 0 )
                    {    # Begin if ($line[0] % 10 == 0)
                        $list_page .= "<td align=center></tr><tr>\n";
                    }    # End if ($line[0] % 10 == 0)
                         #    First element in the list
                    $list_page .=
"<td align=center><a href='album.cgi?page=$line[0]'>$line[0]</a>\n";
                } # End if ( ($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                $my_prev = $line[0];
            }    # End if ($page_asked != $line[0])
            else {    # Begin else
                $my_prev = $line[0];
                if (   ( $my_prev != 1 )
                    && ( ( $line[0] % ( MAX_IMAGES_PER_PAGE + 1 ) ) != 0 ) )
                { # Begin if (($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                    if ( ( $line[0] % MAX_PAGE_PER_LINE_INDEX ) == 0 )
                    {    # Begin if ($line[0] % 10 == 0)
                        $list_page .= " </tr><tr>\n";
                    }    # End if ($line[0] % 10 == 0)
                    $list_page .=
" <td align=center><i><font color=#CE3030>$line[0]</font></i>\n";
                } # End if (($my_prev != 1) && (($line[0] % (MAX_IMAGES_PER_PAGE+1)) != 0) )
                else {    # Begin else
                    if ( ( $line[0] % MAX_PAGE_PER_LINE_INDEX ) == 0 )
                    {     # Begin if ($line[0] % 10 == 0)
                        $list_page .= " </tr><tr>\n";
                    }    # End if ($line[0] % 10 == 0)
                    $list_page .= "<td align=center><font color=#CE3030>$line[0]</font>\n";
                }    # End else
            }    # End else
        }    # End if ($my_prev != $line[0])

        if ( $page_asked eq $line[0] ) {    # Begin if ($page_asked eq $line[0])
            if ( $line[9] =~ m/left/i )
            {    # Begin if ($line[scalar(@line)-1] =~ m/left/i)
                $print_my_page_script .=
"<tr>\n<td align='$line[7]' valign='$line[8]' width='50\%'>\n$line[5]<br>\n<font color='\#822942'>$line[6]</font><td valign='$line[3]'  align='$line[4]' width='50\%'>\n<a href='album.cgi?service=showPict&pict="
                  . DIRECTORY_DEPOSIT
                  . "$line[2]&comments="
                  . &switch_from_a_specified_character_to_tag(
                    "$line[5]SEPARATOR$line[6]")
                  . "'><img src='"
                  . DIRECTORY_DEPOSIT
                  . "$line[2]' width='130' height='130' border=0\">\n</a>\n</tr>\n";
            }    # End if ($line[scalar(@line)-1] =~ m/left/i)
            else {    # Begin else
                $print_my_page_script .=
"<tr>\n<td valign='$line[3]'  align='$line[4]' width='50\%'>\n<a href='album.cgi?service=showPict&pict="
                  . DIRECTORY_DEPOSIT
                  . "$line[2]&comments="
                  . &switch_from_a_specified_character_to_tag(
                    "$line[5]SEPARATOR$line[6]")
                  . "'><img src='"
                  . DIRECTORY_DEPOSIT
                  . "$line[2]' width='130'  height='130' border=0>\n</a>\n<td align='$line[7]' valign='$line[8]' width='50\%'>\n$line[5]<br>\n<font color='\#822942'>$line[6]</font>\n</tr>\n";
            }    # End else
        }    # End if ($page_asked eq $line[0])
    }    # End foreach (@all_file)
    $print_my_page_script .= "</table>\n";

    if ( &is_ok_page_num( $page_asked, @list_of_existing_pages ) == NOK )
    {  # Begin if ( &is_ok_page_num($page_asked,@list_of_existing_pages) == NOK)
        print &error_raised( $doc,
            "Page asked [$page_asked] does not exist!!!!" );
    }    # End if ( &is_ok_page_num($page_asked,@list_of_existing_pages) == NOK)

    $list_page .= "\n</table>\n";
    my $navigator_menu =
      &create_table_for_navigator( $list_page_beg, $prev_page, $list_page,
        $next_page );

    return (
        $doc->br . $doc->br . $doc->table(
            {
                -border => 0,
                -width  => "100%"
            },
            "\n",
            $doc->Tr(
                $doc->td(
                    { -bgcolor => '#CFD3F6' },
                    "\n",
                    $doc->table(
                        {
                            -width  => "100%",
                            -border => 0
                        },
                        "\n",
                        $doc->Tr(
                            $doc->td(
                                {
                                    -valign => "top",
                                    -align  => "left",
                                    -width  => "48%",

                                    #										 -bgcolor => '#F7C5C5'
                                },
                                [$navigator_menu]
                            ),
                            "\n",
                            $doc->td(
                                {
                                    -align => 'center',

                                    #										-bgcolor => '#F7C5C5'
                                },
                            ),
                            "\n",
                            $doc->td(
                                {
                                    -align  => 'right',
                                    -valign => 'top',

                                    #										-bgcolor => '#F7C5C5'
                                },
                                $doc->a(
                                    { -href => 'album.cgi?service=auth' },
                                    "Insert pictures"
                                ),
                                "\n"
                            ),
                            "\n"
                        ),
                        "\n"
                    )
                )
            )
          )
          . "\n"
          . $doc->table(
            {
                -border => 0,
                -width  => "100%"
            },
            "\n",
            $doc->Tr(
                $doc->td(
                    {
                        -align  => 'center',
                        -valign => 'center'
                    },
                    &menu_page_title(
                        "Album of pictures",
                        "page #$page_asked"
                    )
                ),
                "\n"
            ),
            "\n",
            $doc->Tr(
                $doc->td(
                    {
                        -align  => 'center',
                        -valign => 'center'
                    },
                    $doc->br,
                    $doc->br,
                    $doc->br,
                    $print_my_page_script,
                    "\n"
                )
            ),
            "\n"
          )
          . $print_my_page_script_head
    );
}    # End sub print_page

=head1 FUNCTION rank_right_navigator_bar_range($rank_max)

This function is there to calculate right the navigator bar menu for pages (enumerates all page number(s)).

=head2 PARAMETER(S)


=over 4


$rank_max: maximum rank.

=back

=head2 RETURNED VALUE

=over 4

Returns max_rank in one page (to check better).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub rank_right_navigator_bar_range {  # Begin sub rank_right_navigator_bar_range
    my $rank_max = $_[0];

    while ( ( $rank_max % MAX_IMAGES_PER_PAGE ) != 0 )
    {    # Begin while (($rank_max % MAX_IMAGES_PER_PAGE) != 0)
        $rank_max++;
    }    # End while (($rank_max % MAX_IMAGES_PER_PAGE) != 0)
    return $rank_max;
}    # End sub rank_right_navigator_bar_range

=head1 FUNCTION is_ok_page_num($page_asked,@list_of_existing_pages)


This function checks if page asked is in the page rank.

=head2 PARAMETER(S)


=over 4


$page_asked:page asked.

@list_of_existing_pages: list of pages.

=back

=head2 RETURNED VALUE

=over 4

OK: ok.

NOK: not ok.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub is_ok_page_num {    # Begin sub is_ok_page_num
    my ( $page_asked, @list_of_existing_pages ) = @_;

    if ( $page_asked !~ m/^\d+$/ ) {    # Begin  if ($page_asked !~ m/^\d+$/)
        &error_raised_visit( $doc, "Page format number not correct!!!!" );
    }    # End  if ($page_asked !~ m/^\d+$/)
    elsif ( $page_asked <=
        $list_of_existing_pages[ scalar(@list_of_existing_pages) - 1 ] )
    { # Begin if ($page_asked <= $list_of_existing_pages[scalar(@list_of_existing_pages)-1])
        return OK;
    } # End if ($page_asked <= $list_of_existing_pages[scalar(@list_of_existing_pages)-1])
    else {    # Begin else

        #	print $doc->p("NOK value is [$page_asked]");
        return NOK;
    }    # End else
}    # End sub is_ok_page_num

=head1 FUNCTION create_table_for_navigator

We create a table for navigation menu that's it.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

String of table for navigator.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 29 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub create_table_for_navigator {    # Begin sub create_table_for_navigator
    return $doc->table(
        $doc->Tr(
            $doc->td(
                {

                    #					  -bgcolor => '#F7C5C5'
                },
                "\n",
                $doc->table(
                    { -border => 0 },
                    "\n",
                    $doc->Tr(
                        $doc->td(
                            {

                                #									 -bgcolor => '#F7C5C5',
                                -align  => 'left',
                                -valign => 'top'
                            },
                            "$_[0]"
                        ),
                        "\n",
                        $doc->td(
                            {

                                #									 -bgcolor => '#F7C5C5',
                                -align  => 'left',
                                -valign => 'top'
                            },
                            "$_[1]"
                        ),
                        "\n",
                        $doc->td(
                            {

                                #									 -bgcolor => '#F7C5C5',
                                -align  => 'left',
                                -valign => 'top'
                            },
                            "$_[2]"
                        ),
                        "\n",
                        $doc->td(
                            {

                                #									 -bgcolor => '#F7C5C5',
                                -align  => 'left',
                                -valign => 'top'
                            },
                            "$_[3]"
                        ),
                        "\n",
                    ),
                    "\n"
                ),
                "\n"
            ),
            "\n"
        )
    );
}    # End sub create_table_for_navigator

=head1 FUNCTION return_average_file($file_size,$info_read_from_begining,$size_read)

This function calculates info for upload to be printed.

=head2 PARAMETER(S)


=over 4


$file_size: That's the file size.

$info_read_from_begining: Info to print.

$size_read: That's the size read from the begining.

=back

=head2 RETURNED VALUE

=over 4

Returns string to print.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub return_average_file {    # Begin sub return_average_file
    my ( $file_size, $info_read_from_begining, $size_read ) = @_;
    my $percent_read = sprintf "%.2f",
      ( ( 100 * $info_read_from_begining ) / $file_size ) . '%';

    return (
        &title_average_formating( "Percent read", $percent_read . '%' )
          . &title_average_formating( "Info read", $size_read . " Byte(s)" )
          . &title_average_formating(
            "File size read",
            $info_read_from_begining
              . " Byte(s) over a total of $file_size Byte(s)"
          ),
        $percent_read
    );
}    # End sub return_average_file

=head1 FUNCTION title_average_formating($title1,$title2)

This function center the title of the main page.

=head2 PARAMETER(S)


=over 4


$title1: that's the title.

$title2: other info abour title.

=back

=head2 RETURNED VALUE

=over 4

Returns the title formated with the two titles concatenated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back



=cut

sub title_average_formating {    # Begin sub title_average_formating
    return "<u>$_[0]:</u> $_[1]<br>";
}    # End sub title_average_formating

=head1 FUNCTION my_upload

This function allows upload.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Aug 22sd 2006

- I<Last modification:> Mar 04 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub my_upload {    # Begin sub my_upload
    my $file_from          = ();    # file uploaded
    my $file_name_saved_at_server_side  = ();    # file that is used to save uploaded file
    my $file_to_upload = ();    # where file has to be stored: that's the "to"
    my $bytes_read     = ();    # bytes read from file uploaded
    my $buff           = ();    # buffer used to read image
    my $type_upload = $doc->param("type_of_upload");  # type of info to use mode
    my $is_image_file_need_to_be_uploaded = 1;
    my @l_file_scat = ();

    $doc->cgi_error
      and error_raised( $doc, "Transfert error of file :", $doc->cgi_error );
    $file_from = $doc->param("file_name_img");
    chomp($file_from);

    # Never ever change something in the variable $file_from above from this point, it contains the file that is uploaded from source
    @file_to_upload_info = stat $file_from;

    # We check if file has the following format
    # <drive name>:\d1\d1\f1.gif where d[num] is a directory and and f1.gif an image file name
    # then we take only the image file nam

    @l_file_scat = split( /\//, &reformat($file_from) );
    $file_name_saved_at_server_side = &reformat($l_file_scat[ scalar(@l_file_scat) - 1 ]);

    # We create a file into a path where to store new image file
    $file_to_upload = DIRECTORY_DEPOSIT . "/${suffix_for_image_file}${file_name_saved_at_server_side}";

    if ( $file_from !~ m/(jpeg|jpg|gif)$/i ) {    # Begin if ($file !~ m/^[a-zA-Z][a-zA-Z0-9\-_]*.(jpeg|jpg|gif)$/i)
      error_raised( $doc,
		    "File received [$file_from].<br>Character accepted: from <u>a to z</u> and <u>A to Z</u> as first file character. Then several occurrencies from <u>a to z</u> and <u>A to Z</u> and <u>0 to 9</u> and <u>- and _</u> can be accepted.<br>\nFormat of image different from gif, jpeg, jpg."
		  );
    }    # End if ($file !~ m/^[a-zA-Z][a-zA-Z0-9\-_]*.(jpeg|jpg|gif)$/i)
    if ( size_dir(DIRECTORY_DEPOSIT) + $ENV{CONTENT_LENGTH} > MAXIMUM_DIRECTORY_SIZE_THAT_CAN_CONTAIN_FILE ) { # Begin if (size_dir(DIRECTORY_DEPOSIT)  + $ENV{CONTENT_LENGTH} > MAXIMUM_DIRECTORY_SIZE_THAT_CAN_CONTAIN_FILE)
      error_raised( $doc, "Directory is full" );
    } # End if (size_dir(DIRECTORY_DEPOSIT)  + $ENV{CONTENT_LENGTH} > MAXIMUM_DIRECTORY_SIZE_THAT_CAN_CONTAIN_FILE)

    if ( $is_image_file_need_to_be_uploaded == 1 )
      {    # Begin  if ($is_image_file_need-to_be_uploaded == 1 )
        open( FW, ">${file_to_upload}" )
          || die("Can't create ${file_to_upload}");
        my @info          = stat $file_from;
        my $seg_file_read = 0;
        while ( $bytes_read = read( $file_from, $buff, AMOUNT_OF_INFO_TO_READ ) )
	  { # Begin while ($bytes_read=read($file_from,$buff,AMOUNT_OF_INFO_TO_READ)
            $seg_file_read += $bytes_read;
            my ( $to_print, $average ) =
              &return_average_file( $info[7], $seg_file_read, $bytes_read );
            open( W, ">album/dec" );
            flock( W, LOCK_EX | LOCK_SH );
            print W $to_print;
            close(W);
            sleep(1);
            binmode FW;
            print FW $buff;
	  }; # End while ($bytes_read=read($file_from,$buff,AMOUNT_OF_INFO_TO_READ)
        close(FW);
        open( W, ">album/dec" );
        print W End;
        close(W);
	
        #	unlink "album/dec";
        chmod( 0755, "$file_to_upload" );
      }    # End  if ($is_image_file_need-to_be_uploaded == 1 )
  }    # End sub my_upload

=head1 FUNCTION get_private_stuff_for_administrator

This function gets info related to administrator to be identified.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Returns $login, and $passwd values.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 16 2006

- I<Last modification:> Jan 04 2006

- I<Created on:> Jan 04 2006

=back



=cut

sub get_private_stuff_for_administrator
{    # Begin sub get_private_stuff_for_administrator
    my ( $login, $passwd ) = ();

    if ( $an_action ne "record_modify" )
    {    # Begin if ($an_action ne "record_modify")
        if ( -f PRIVATE_INFO_DIRECTORY . "/pswd.txt" )
        {    # Begin if (-f "private/pswd.txt")
            open( R, PRIVATE_INFO_DIRECTORY . "/pswd.txt" )
              || die( "Cannot find file "
                  . PRIVATE_INFO_DIRECTORY
                  . "/pswd.txt $!\n" );
            my @p = <R>;
            chomp( $p[0] );
            chomp( $p[1] );
            $login  = $p[0];
            $passwd = $p[1];
            close(R);
            chomp($login);
            chomp($passwd);

            if ( $login eq "" || $passwd eq "" ) {
                $login  = $doc->param("login");
                $passwd = $doc->param("password");
                open( W, ">" . PRIVATE_INFO_DIRECTORY . "/pswd.txt" )
                  || die( "Cannot find file "
                      . PRIVATE_INFO_DIRECTORY
                      . "/pswd.txt when being created $!\n" );
                print W "$login\n";
                print W "$passwd\n";
                close(W);
            }
        }    # End if (-f "private/pswd.txt")
        else {    # Begin else
            if ( !-d PRIVATE_INFO_DIRECTORY )
            {     # Begin if (!-d "$album_directory")
                mkdir( PRIVATE_INFO_DIRECTORY, 0700 )
                  || die("Cannot create $album_directory\n");
            }    # End if (!-d "$album_directory")
            open( W, ">" . PRIVATE_INFO_DIRECTORY . "/pswd.txt" )
              || die( "Cannot find file "
                  . PRIVATE_INFO_DIRECTORY
                  . "/pswd.txt when being created $!\n" );
            print W "\n";
            print W "\n";
            close(W);

#	    print "login:".$doc->param("login").";password".$doc->param("password").$doc->br ;
        }    # End else
    }    # End if ($an_action ne "record_modify")
    return ( $login, $passwd );
}    # End sub get_private_stuff_for_administrator

=head1 FUNCTION cascade_style_sheet_definition

This function creates a cascade style sheet for the whole program.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Returns String formated for style sheet.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006

- I<Created on:> Jan 27 2006

=back



=cut

sub cascade_style_sheet_definition {  # Begin sub cascade_style_sheet_definition
    return &javaScript
      . $loc_margin
      . "<style type='text/css'>\n"
      . $loc_margin
      . "<!--\n"
      . &general_css_def
      . $loc_margin . "-->\n"
      . $loc_margin
      . "</style>\n";
}    # End sub cascade_style_sheet_definition

=head1 FUNCTION javaScript

This function creates a java script section.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Returns string formated of section in Java Script code.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 10 2006

- I<Created on:> Feb 10 2006

=back



=cut

sub javaScript {

    return $loc_margin
      . "<script type=\"text/javascript\">\n"
      . $loc_margin
      . "  <!--\n"
      . $loc_margin
      . "     window.onload=show;\n"
      . $loc_margin
      . "     function go_to(url) {\n"
      . $loc_margin
      . "          location= url;\n"
      . $loc_margin
      . "     }\n"
      . $loc_margin
      . "     function show(id) {\n"
      . $loc_margin
      . "        var d = document.getElementById(id);\n"
      . $loc_margin
      . "        for (var i = 1; i<=10; i++) {\n"
      . $loc_margin
      . "                if (document.getElementById('smenu'+i)) {document.getElementById('smenu'+i).style.display='none';}\n"
      . $loc_margin
      . "        }\n"
      . $loc_margin
      . "        if (d) {d.style.display='block';}\n"
      . $loc_margin
      . "     }\n"
      . $loc_margin
      . "   //-->\n"
      . $loc_margin
      . "</script>\n";
}

=head1 FUNCTION general_css_def

This function creates a cascade style sheet definition for the 'a' html tag.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Returns String formated for style sheet for 'a' tag.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 9 2006

- I<Last modification:> Feb 1 2006

- I<Created on:> Jan 27 2006

=back



=cut

sub general_css_def {    # Begin sub general_css_def
    return "            body {\n"
      . "                color: #07396E;\n"
	. "            }\n"
	  . "            dl {\n"
	      . "                display: block;\n"
		. "                width: 100%;\n"
		  . "            }\n"
		    . "            dt {\n"
		      . "                float: left;\n"
			. "                text-align: center;\n"
			  . "                border: 1px solid;\n"
			    . "                background-color: #BEC3E5;\n"
			      . "                width: 14em;\n"
				. "                height: 2em;\n"
				  . "                padding-top: 0.25em;\n"
				    . "            }\n"
					. "            dd {\n"
					  . "                display: none;\n"
					    . "                margin: 2.0;\n"
					      . "                height: 12;\n"
						. "            }\n"
						  . "            font.footer {\n"
						    . "                font-size: 12.0px;\n"
						      . "                font-style: italic;\n"
							. "            }\n"
							  . "            P.footer {\n"
							    . "                border-width: 1;\n"
							      . "                border: double;\n"
								. "                border-color: blue;\n"
								  . "                background-color: #E5E3FF;\n"
								    . "                font-family: Times, LucidaTypewriter;\n"
								      . "            }\n"
									. "            ul.main_menu {\n"
									  . "                 text-align: left;\n"
									    . "                 background-color: #ABAFCE;\n"
									      . "                 color: black;\n"
										. "                 border-color: #807CA5;\n"
										  . "              }\n"
										    . "            li {\n"
										      . "                margin-left: 2px;\n"
											. "                display: inline;\n"
											  .
											    
											    #	"                color: red;\n".
											    "            }\n" . "            li.help_menu_content {\n" .
											      
											      #	"                margin-left: 30px;\n".
											      #	"                display: inline;\n".
											      "                color: red;\n"
												. "            }\n"
												  . "            b.taken {\n"
												    . "                color: red;\n"
												      . "            }\n"
      . "            table.footer {\n"
	. "                 font-size: 12px;\n"
	  . "                 text-align: right;\n"
	    . "                 color: black;\n"
	      . "                 background-color: #D2D2FF;\n"
		. "                 border: double;\n"
		  . "                 border-color: blue;\n"
		    . "              }\n"
		      . "            table.main_auth {\n"
			. "                 text-align: right;\n"
			  . "                 background-color: #D2D2FF;\n"
			    . "                 color: black;\n"
			      . "                 font-weight: bolder;\n"
				. "                 border: double;\n"
				  . "                 border-color: #807CA5;\n"
				    . "              }\n"
				      . "            table.auth {\n"
					. "                 text-align: right;\n"
					  . "                 background-color: #D8D7FF;\n"
					    . "                 color: black;\n"
					      . "                 font-weight: bolder;\n"
						. "              }\n"
						  . "            td.configuration {\n"
						    . "                 vertical-align: top;\n"
						      . "                 text-align: center;\n"
							. "                 background-color: #33127F;\n"
							  . "                 color: white;\n"
							    . "                 font-weight: bolder;\n"
							      . "              }\n"
								. "            img {\n"
								  . "                 border: 0;\n"
								    . "              }\n"
								      . "            h1 {\n"
									. "                 color: #000067;\n"
									  . "                 font-family: Times, LucidaTypewriter;\n"
									    . "              }\n"
									      . "            i {\n"
										. "                 color: #07396E;\n"
										  . "              }\n"
										    . "            a.toto {\n"
										    . "                 color: #822942;\n"
										      . "                 font-style: italic;\n"
											. "                 font-weight: bold;\n"
											  . "                 text-decoration: none;\n"
											    . "              }\n"

											      . "            a {\n"
										    . "                 color: black;\n"
										      . "                 font-style: italic;\n"
											. "                 font-weight: bold;\n"
											  . "                 text-decoration: none;\n"
											    . "              }\n"
										


											      . "              #help_content {\n"
												. "                  color: yellow;\n"
												  . "                  position: absolute;\n"
												    . "                  left: 242px;\n"
												      . "                  top: 130px;\n"
													. "                  width: 600px;\n"
													  . "                  height: 400px;\n"
													    . "                  border: 1.42px;\n"
													      . "                  border-color: #011438;\n"
														. "                  border-style: double;\n"
														  . "                  background: #1a1731;\n"
														    . "                 opacity: .95;\n"
      . "              }\n"
	. "              #image_help {\n"
	  . "                  background:  #7e85c1;\n"
	    . "                 opacity: .1;\n"
#	  . "                  background-image: url(\""
#	    . DIRECTORY_DEPOSIT
#	      . "/my_lovely_pict.gif\");\n"
#		. "                  background-repeat: no-repeat;\n"
		  . "                  background-position: left top;\n"
		    . "              }\n"
		      . "              #parag_help {\n"
			. "                 position: relative;\n"
			  . "                 text-indent: 40px;\n"
			    . "                 left: 10px;\n"
			      . "                 right: 10px;\n"
				. "                 width: 500px;\n"
				  . "                 margin-left: 90px;\n"
				    . "                 margin-right: 10px;\n"
				      .
					
					#	"                 text-align: justify;\n".
					"              }\n" . "              #title_help {\n" .
					  
					  #	"                  position: absolute;\n".
					  "                  text-align: center;\n"
					    . "                  top: 5px;\n"
					      . "                  width: 100%;\n"
						. "                  border-bottom: 2px solid #D9D073;\n"
						  . "              }\n"
						    . "              #my_face_help {\n"
						      . "                  position: absolute;\n"
							. "                  left: 5px;\n"
							  . "                  top: 5px;\n"
							    . "                  width: 80px;\n"
							      . "              }\n"
								.
								  
								  #	"              dl {display: block;}".
								  "              a:hover {\n" .

      #	"                 zindex: 100;".
      #	"                 color: #4E5293;\n" .
      "                 color: #C49209;\n" .

      #	"                 font-size: 20px;\n".
      #	"                 font-family: courier;\n".
      "              }\n";
}    # End sub general_css_def

=head1 FUNCTION main_menu

This function creates a general menu.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 25 2006

- I<Created on:> Feb 1 2006

=back



=cut

sub main_menu {    # Begin sub main_menu
    my ( $title, @help_feature ) = @_;

    print "<dl>\n";
    print "<dt>\n<a href='JavaScript:go_to(\""
      . MY_WEBSITE
      . "\");'>My website</a>\n</dt>\n";
    print "<dt>Other albums</dt>\n";
    print
"<dt onmouseover=\"javascript:show('smenu2');\" onmouseout=\"javascript:show();\">Help</dt>";
    print "<dd id=\"smenu2\">\n";
    &help_menu_with_css( $title, @help_feature );
    print "</dd>\n";
    print "</dl>\n";
}    # End sub main_menu

=head1 FUNCTION help_menu_with_css

This function creates a menu for help.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 8 2006

- I<Created on:> Feb 8 2006

=back



=cut

sub help_menu_with_css {
    my ( $title, @info ) = @_;
    @info = (
"Suivre attentivement les instructions dessous. / Follow carefully instructions below.",
        @info
    );
    print "<div id=\"help_content\">\n";    # b0
    print "<div id=\"title_help\">\n";      # b1
    print "$title\n";
    print "</div>\n";                       # e1
    print "<div id=\"my_face_help\">\n";    # b2
    print "<img src=\""
      . DIRECTORY_DEPOSIT
      . "/my_lovely_pict.gif\" style=\"float: right;padding-top: 25px;\">\n";
    print "</div>\n";                       # e2
    print "<div id=\"parag_help\">\n";      # b3

    foreach my $feature (@info) {           # Begin foreach my $feature (@info)
        $feature =~ s/(\/)(.*)/$1\<font color=\'orange\'\>$2\<\/font\>/g;
        print "<p>+ $feature</p>\n";
    }    # End foreach my $feature (@info)

    #    print "</p>\n";
    print "</div>\n";    # e3
    print "</div>\n";    # e0
}

=head1 FUNCTION switch_from_a_specified_character_to_tag($string)

This function changes some specified character to a tag in order not to avoid miss-understanding in local Data Base when reading it.

=head2 PARAMETER(S)


=over 4


$string: that's the string to reformat.

=back

=head2 RETURNED VALUE

=over 4

New srting formated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 6 2006

- I<Created on:> Feb 5 2006

=back



=cut

sub switch_from_a_specified_character_to_tag
{    # Begin sub switch_from_a_specified_character_to_tag
    my ($string) = @_;

    $string =~ s/\'/\_\_TAG\_COT\_\_/g;

    #    $string =~ s/\_/\_\_TAG\_UNDERSCORE\_\_/g;
    $string =~ s/\;/\_\_TAG\_SEMI\_COLUMN\_\_/g;
    return $string;
}    # End sub switch_from_a_specified_character_to_tag

=head1 FUNCTION switch_from_a_specified_tag_to_characters($string)

This function changes some specified character tag to a character in order not to avoid miss-understanding in local Data Base when reading it.

=head2 PARAMETER(S)


=over 4


$string: that's the string to reformat.

=back

=head2 RETURNED VALUE

=over 4

New srting formated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Feb 6 2006

- I<Created on:> Feb 5 2006

=back



=cut

sub switch_from_a_specified_tag_to_characters
{    # Begin sub switch_from_a_specified_tag_to_characters
    my ($string) = @_;

    $string =~ s/\_\_TAG\_COT\_\_/\'/g;

    #   $string =~ s/\_\_TAG\_UNDERSCORE\_\_/\_/g;
    $string =~ s/\_\_TAG\_SEMI\_COLUMN\_\_/\;/g;
    return $string;
}    # End sub switch_from_a_specified_tag_to_characters

=head1 FUNCTION look_for_images_used

This function check if all necessary images are stored in the path where images are stored.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 27 2006

- I<Last modification:> Feb 17 2006

- I<Created on:> Feb 17 2006

=back



=cut

sub look_for_images_used {    # Begin sub look_for_images_used
    if ( !-f "private/image_checked" )
    {                         # Begin if (!-f "private/image_checked")
        my $counter = 0;
        print "<center><b>Checks</b>\n";
        print "</center>\n";
        print "<table>\n";
        print
"	<tr><td align=left><font color=blue><b>Status</b></font><td align=right><font color=blue><b>Image</b></font></tr>\n";
        foreach (@images_used) {    # Begin foreach (@images_used)
            if ( -f "$_" ) {        # Begin if (-f DIRECTORY_DEPOSIT . "$_")
                $counter++;
                print
		  "	<tr><td align=left><b><font color=green>ok</font></b><td align=right>$_</tr>\n";
            }    # End if (-f DIRECTORY_DEPOSIT . "$_")
            else {    # Begin else
                print
"<tr><td align=left><font color=red>n'existe pas / does not exist !!!</font><b><td align=right>$_</tr>\n";
            }    # End else
        }    # End foreach (@images_used)
        print "</table>\n";
        if ( ($counter) == scalar(@images_used) )
        {    # Begin if (($counter+1) == scalar(@images_used))
            open( W, ">private/image_checked" )
              || die("Can't create private/image_checked file $!\n");
            print W "";
            close(W);
            print "All images are present in the directory "
              . DIRECTORY_DEPOSIT
              . "<br>\n";
        }    # End if (($counter+1) == scalar(@images_used))
        else {    # Begin else
            exit;
        }    # End else
    }    # End if (!-f "private/image_checked")
}    # End sub look_for_images_used

=head1 FUNCTION  get_first_page_number

We got the first page that is stored. Usefull if fake page number is given.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

Returns first page number stored in album DB file.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 09 2006

- I<Created on:> Mar 09 2006

=back



=cut

sub get_first_page_number {    # Begin sub get_first_page_number
    open( R, "$file_conf_to_save" )
      or error_raised("File $file_conf_to_save does not exists");
    my @f = <R>;
    close(R);
    my @line = split( /\|\|/, $f[0] );
    return $line[0];
}    # End sub get_first_page_number

=head1 FUNCTION  main_help_menu_css

We print help menu just for main page.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 27 2006

- I<Created on:> Mar 27 2006

=back



=cut

sub main_help_menu_css {    # Begin sub main_help_menu_css
    &main_menu(
        "Aide / Help",
"Les liens apparaissent en fonc�. Des qu'ont les survolent ils changent de couleur. Cliquez dessus pour suivre le lien. / Links show up in dark color. As soon as mouse is over, color changes hence click on it to follow the link.",
"Les images peuvent etre agrandies si on clique dessus. / Images can be enlarged if we click on it.",
"On peut changer les pages en pressant les num�ros en haut � gauche. / Pages can be switched when number at left top are clicked.",
        "Merci pour la visite :) / Thanks for the visit :)"
    );
}    # End sub main_help_menu_css


=head1 FUNCTION reformat

This function reformats path when it comes from Internet Explorer.

=head2 PARAMETER(S)

$path: that's the path to file

=back

=head2 RETURNED VALUE

=over 4

Path reformated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 22sd 2006

- I<Last modification:> Jul 18 2006

- I<Created on:> Jul 17 2006

=back

=cut

sub reformat { # Begin sub reformat
  my ($path) = @_;

  chomp($path);
  my $toto = $path;
  if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/) { # Begin if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/)
    $path = $1;
  }  # End if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/)
  $path =~ s/\ //g;
  $path =~ s/\\/\//g;
  $path =~ s/^[a-zA-Z]\://g;

  return $path;
}  # End sub reformat


=head1 AUTHOR

Current maintainer: M. Flotilla Reindeer, <flotilla.reindeer@laposte.net>


=cut



