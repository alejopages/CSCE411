<?php
    $username = "cfarmer"; 
    $password = "eKd65T";   
    $host = "cse.unl.edu";
    $database= "cfarmer";
    $query = $_POST['query'];
    $server = mysqli_connect($host, $username, $password);
    $connection = mysqli_select_db($server, $database);

    $query = mysqli_query($server, $query);
    
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
