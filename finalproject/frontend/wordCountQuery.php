<?php
/**
 * Created by PhpStorm.
 * User: Matt
 * Date: 10/20/2018
 * Time: 11:43 AM
 */
$username = "cfarmer";
$password = "eKd65T";
$host = "cse.unl.edu";
$database= "cfarmer";

$server = mysqli_connect($host, $username, $password);
$connection = mysqli_select_db($server, $database);

$myquery = "SELECT date, word, count FROM RawWordCount
            JOIN WordDate ON WordDate.id = RawWordCount.dateId";
$query = mysqli_query($server, $myquery);

if ( ! $query ) {
    echo mysqli_error();
    die;
}

$data = array();

for ($x = 0; $x < mysqli_num_rows($query); $x++) {
    $data[] = mysqli_fetch_assoc($query);
}

echo json_encode($data);

mysqli_close($server);
?>