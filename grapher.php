<?php
/* Include all the classes */
include("/home/pi/pChart2.1.3/class/pData.class.php");
include("/home/pi/pChart2.1.3/class/pDraw.class.php");
include("/home/pi/pChart2.1.3/class/pImage.class.php");

$myData = new pData(); /* Create your dataset object */

$db = mysql_connect("localhost", "root", "plantdata"); //location of server, db username, db pass
mysql_select_db("datatest", $db);

// $Requete = "SELECT * FROM `roominfo`"; //table name
//
// this line should limit the SELECT to return the last 50 lines of the roominfo table.
$Requete = "(SELECT * FROM `roominfo` ORDER BY id DESC LIMIT 96) ORDER BY id ASC";
$Result = mysql_query($Requete, $db);

/*This fetches the data from the mysql database, and adds it to pchart as points*/
while($row = mysql_fetch_array($Result))
{
    /* $time = $row["time"];
    $myData->addPoints($time,"time"); */
    
    $coretemp = $row["coretemp"];
    $myData->addPoints($coretemp,"coretemp");
    $roomtemp = $row["roomtemp"];
    $myData->addPoints($roomtemp,"roomtemp");
    $roomhum = $row["roomhum"];
    $myData->addPoints($roomhum,"roomhum");
    $rawlight = $row["rawlight"];
    $myData->addPoints($rawlight,"rawlight");
    
}


$myData-> setSerieOnAxis("coretemp", 0); //assigns the data to the frist axis
$myData-> setSerieOnAxis("roomtemp", 0);
$myData-> setAxisName(0, "Degrees F"); //adds the label to the first axis

$myData-> setSerieOnAxis("roomhum", 1);
$myData-> setAxisName(1, "Humidity");

$myData-> setSerieOnAxis("rawlight", 2);
$myData-> setAxisName(2, "Light Level");


$myData->setAbscissa("time"); //sets the time data set as the x axis label

 
$myData-> setSerieWeight("coretemp",1); //draws the line tickness
$myData->setPalette("coretemp",array("R"=>200,"G"=>20,"B"=>200,"Alpha"=>80)); //sets the line color
    
$myData-> setSerieWeight("roomtemp",1);
$myData->setPalette("roomtemp",array("R"=>250,"G"=>10,"B"=>10,"Alpha"=>80));


$myData-> setSerieWeight("roomhum",1);
$myData->setPalette("roomhum",array("R"=>0,"G"=>200,"B"=>200,"Alpha"=>80));
/* $myData-> setSerieTicks("roomhum", 4); */

$myData-> setSerieWeight("rawlight",1);
$myData->setPalette("rawlight",array("R"=>10,"G"=>150,"B"=>250,"Alpha"=>80));
/* $myData-> setSerieTicks("rawlight", 4); */

    
    
    
$myPicture = new pImage(2000,500,$myData); /* Create a pChart object and associate your dataset */
$myPicture->setFontProperties(array("FontName"=>"/home/pi/pChart2.1.3/fonts/verdana.ttf","FontSize"=>14)); /* Choose a nice font */
$myPicture->setGraphArea(200,40,1950,390); /* Define the boundaries of the graph area */
$myPicture->drawScale(array("LabelRotation"=>320)); /* Draw the scale, keep everything automatic */
    

    
    

$Settings = array("R"=>250, "G"=>250, "B"=>250, "Dash"=>1, "DashR"=>0, "DashG"=>0, "DashB"=>0);

/*The combination makes a cool looking graph*/
$myPicture->drawPlotChart();
$myPicture->drawLineChart();
$myPicture->drawLegend(70,420); //adds the legend

//$date-> date("d-M-Y:H:i:s");

//$myPicture->autoOutput(); /* Build the PNG file and send it to the web browser */

$myPicture->render("/home/pi/renders/".date("d-M-Y_H-i-s").".png");

?>