//Static Slide Menu 6.5 � MaXimuS 2000-2001, All Rights Reserved.
//Site: http://www.absolutegb.com/maximus
//E-mail: maximus@nsimail.com
//Script featured on Dynamic Drive (http://www.dynamicdrive.com)
NS6 = (document.getElementById&&!document.all)
IE = (document.all)
NS = (navigator.appName=="Netscape" && navigator.appVersion.charAt(0)=="4")
tempBar='';barBuilt=0;ssmItems=new Array();
moving=setTimeout('null',1)
function moveOut() {
if ((NS6||NS)&&parseInt(ssm.left)<0 || IE && ssm.pixelLeft<0) {
clearTimeout(moving);moving = setTimeout('moveOut()',
slideSpeed);slideMenu(10)}
else {clearTimeout(moving);moving=setTimeout('null',1)}};
function moveBack() {clearTimeout(moving);moving =
setTimeout('moveBack1()', waitTime)}
function moveBack1() {
if ((NS6||NS) && parseInt(ssm.left)>(-menuWidth) || IE
&& ssm.pixelLeft>(-menuWidth)) {
clearTimeout(moving);moving = setTimeout('moveBack1()',
slideSpeed);slideMenu(-10)}
else {clearTimeout(moving);moving=setTimeout('null',1)}}
function slideMenu(num){
if (IE) {ssm.pixelLeft += num;}
if (NS||NS6) {ssm.left = parseInt(ssm.left)+num;}
if (NS) {bssm.clip.right+=num;bssm2.clip.right+=num;}}
function makeStatic() {
if (NS||NS6) {winY = window.pageYOffset;}
if (IE) {winY = document.body.scrollTop;}
if (NS6||IE||NS) {
if (winY!=lastY&&winY>YOffset-staticYOffset) {
smooth = .2 * (winY - lastY - YOffset + staticYOffset);}
else if (YOffset-staticYOffset+lastY>YOffset-staticYOffset) {
smooth = .2 * (winY - lastY - (YOffset-(YOffset-winY)));}
else {smooth=0}
if(smooth > 0) smooth = Math.ceil(smooth);
else smooth = Math.floor(smooth);
if (IE) bssm.pixelTop+=smooth;
if (NS6||NS) bssm.top=parseInt(bssm.top)+smooth
lastY = lastY+smooth;
setTimeout('makeStatic()', 1)}}
function buildBar() {
if(barText.indexOf('<IMG')>-1) {tempBar=barText}
else{for (b=0;b<barText.length;b++)
{tempBar+=barText.charAt(b)+"<BR>"}}
document.write('<td align="center" rowspan="100"
width="'+barWidth+'" bgcolor="'+barBGColor+'"
valign="'+barVAlign+'"><p align="center"><font
face="'+barFontFamily+'" Size="'+barFontSize+'"
COLOR="'+barFontColor+'"><B>'+tempBar+'</B></font></p></TD>')}
function initSlide() { if (NS6){
ssm=document.getElementById("thessm").style;
bssm=document.getElementById("basessm").style; bssm.clip="rect(0 "+document.getElementById("thessm").offsetWidth+" "+document.getElementById("thessm").offsetHeight+" 0)";ssm.visibility="visible"; }else if (IE) {
ssm=document.all("thessm").style; bssm=document.all("basessm").style;
bssm.clip="rect(0 "+thessm.offsetWidth+" "+thessm.offsetHeight+" 0)";bssm.visibility = "visible"; }else if (NS) {
bssm=document.layers["basessm1"];
bssm2=bssm.document.layers["basessm2"];ssm=bssm2.document.layers["thessm"];
bssm2.clip.left=0;ssm.visibility = "show"; } if (menuIsStatic=="yes") makeStatic();
}
function buildMenu() { if (IE||NS6) { document.write('<DIV
ID="basessm" style="visibility:hidden;Position : Absolute ;Left :
'+XOffset+' ;Top : '+YOffset+' ;Z-Index :
20;width:'+(menuWidth+barWidth+10)+'"><DIV ID="thessm"
style="Position : Absolute ;Left : '+(-menuWidth)+' ;Top : 0 ;Z-Index :
20;" onmouseover="moveOut()" onmouseout="moveBack()">'); } if (NS) {
document.write('<LAYER name="basessm1" top="'+YOffset+'" LEFT='+XOffset+' visibility="show"><ILAYER
name="basessm2"><LAYER visibility="hide" name="thessm"
bgcolor="'+menuBGColor+'" left="'+(-menuWidth)+'" onmouseover="moveOut()" onmouseout="moveBack()">'); } if (NS6){ document.write('<table border="0" cellpadding="0" cellspacing="0" width="'+(menuWidth+barWidth+2)+'" bgcolor="'+menuBGColor+'"><TR><TD>'); }
document.write('<table border="0" cellpadding="0" cellspacing="1" width="'+(menuWidth+barWidth+2)+'" bgcolor="'+menuBGColor+'">');
for(i=0;i<ssmItems.length;i++) { if(!ssmItems[i][3]){
ssmItems[i][3]=menuCols; ssmItems[i][5]=menuWidth-1; }else
if(ssmItems[i][3]!=menuCols)
ssmItems[i][5]=Math.round(menuWidth*(ssmItems[i][3]/menuCols)-1); if ( ssmItems[i-1] && ssmItems[i-1][4] != "no" ) {
document.write('<TR>'); } if(!ssmItems[i][1]){
document.write('<td bgcolor="'+hdrBGColor+'" HEIGHT="'+hdrHeight+'"
ALIGN="'+hdrAlign+'" VALIGN="'+hdrVAlign+'" WIDTH="'+ssmItems[i][5]+'"
COLSPAN="'+ssmItems[i][3]+'"><font face="'+hdrFontFamily+'"
Size="'+hdrFontSize+'" COLOR="'+hdrFontColor+'">
<b>'+ssmItems[i][0]+'</b></font></td>'); }else
{ if(!ssmItems[i][2]) ssmItems[i][2]=linkTarget; document.write('<TD
BGCOLOR="'+linkBGColor+'" onmouseover="bgColor=\''+linkOverBGColor+'\'"
onmouseout="bgColor=\''+linkBGColor+'\'" WIDTH="'+ssmItems[i][5]+'"
COLSPAN="'+ssmItems[i][3]+'"><ILAYER><LAYER
onmouseover="bgColor=\''+linkOverBGColor+'\'"
onmouseout="bgColor=\''+linkBGColor+'\'" WIDTH="100%"
ALIGN="'+linkAlign+'"><DIV ALIGN="'+linkAlign+'"><FONT
face="'+linkFontFamily+'" Size="'+linkFontSize+'"> <A
HREF="'+ssmItems[i][1]+'" target="'+ssmItems[i][2]+'"
CLASS="ssmItems">'+ssmItems[i][0]+'</DIV></LAYER></ILAYER></TD>');
} if(ssmItems[i][4]!="no"&&barBuilt==0){ buildBar();
barBuilt=1; } if(ssmItems[i][4]!="no"){ document.write('</TR>');
} } document.write('</table>'); if (NS6){
document.write('</TD></TR></TABLE>'); } if (IE||NS6)
{ document.write('</DIV></DIV>'); } if (NS) {
document.write('</LAYER></ILAYER></LAYER>'); }
theleft=-menuWidth;lastY=0;setTimeout('initSlide();', 1);
}
<!--
/*
Configure menu styles below
NOTE: To edit the link colors, go to the STYLE tags and edit the
ssm2Items colors
*/
b=(screen.width==800&&screen.height==600);
if(b) YOffset=0;
else YOffset=10; // no quotes!!
XOffset=0;
staticYOffset=6; // no quotes!!
slideSpeed=20 // no quotes!!
waitTime=100; // no quotes!! this sets the time the menu stays out for
after the mouse goes off it.
menuBGColor="RoyalBlue";
menuIsStatic="yes"; //this sets whether menu should stay static on the
screen
if(b) menuWidth=160;
else menuWidth=180; // Must be a multiple of 10! no quotes!!
menuCols=2;
hdrFontFamily="verdana";
if(b) hdrFontSize="1";
else hdrFontSize="2";
hdrFontColor="Navy";
hdrBGColor="Sandybrown";
hdrAlign="center";
hdrVAlign="center";
hdrHeight="15";
linkFontFamily="Verdana";
if(b) linkFontSize="1";
else linkFontSize="2";
linkBGColor="white";
linkOverBGColor="PaleGoldenrod";
linkTarget="_top";
linkAlign="Left";
barBGColor="Sandybrown";
barFontFamily="Verdana";
if(b) barFontSize="1";
else barFontSize="2";
barFontColor="Navy";
barVAlign="center";
barWidth=20; // no quotes!!
barText="NOM DU MENU"; // <IMG> tag supported. Put exact html for
an image to show.
///////////////////////////
// ssmItems[...]=[name, link, target, colspan, endrow?] - leave 'link'
and 'target' blank to make a header
ssmItems[0]=["1"] //create header
ssmItems[1]=["1.1", "url1.1",""] //create header
ssmItems[2]=["1.2", "url1.2",""] ssmItems[3]=["1.3", "url1.3",""]
ssmItems[4]=["2", "", ""] //create header
ssmItems[5]=["2.1", "url2.1",""] ssmItems[6]=["2.2", "url2.2", ""]
ssmItems[7]=["2.3", "url2.3", ""]
ssmItems[8]=["3"] //create header
ssmItems[9]=["3.1", "url3.1",""]
ssmItems[10]=["3.2", "url3.2",""]
ssmItems[11]=["3.3", "url3.3",""]
ssmItems[12]=["4"] //create header
ssmItems[13]=["4.1", "url4.1",""] //create header
ssmItems[14]=["4.2", "url4.2",""] ssmItems[15]=["4.3", "url4.3",""]
ssmItems[16]=["5", "", ""] //create header
ssmItems[17]=["5.1", "url5.1",""] ssmItems[18]=["5.2", "url5.2", ""]
ssmItems[19]=["5.3", "url5.3", ""]
ssmItems[20]=["6"] //create header
ssmItems[21]=["6.1", "url6.1",""]
ssmItems[22]=["6.2", "url6.2",""]
ssmItems[23]=["6.3", "url6.3",""]
buildMenu();
//-->
