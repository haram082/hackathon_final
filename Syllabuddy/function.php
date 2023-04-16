<?php

$arg1 = "text_file.txt";
$arg2 = 'DEPACE';
$arg3 = 'CLASS.csv';


$command = "python Main.py \"$arg1\" \"$arg2\" \"$arg3\"";
exec($command, $output, $return_value);

$file = 'CLASS.csv';
file_put_contents($file, $output);


if ($return_value == 1){
    echo "failed";
    

} else{
    echo "Success";
    echo "<br><br><a href='CLASS.csv' download>Download CSV File</a>";
}
