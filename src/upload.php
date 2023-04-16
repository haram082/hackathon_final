<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file_name = $_FILES['pdf_file']['name'];
    $file_tmp = $_FILES['pdf_file']['tmp_name'];
    $file_type = $_FILES['pdf_file']['type'];
    $file_size = $_FILES['pdf_file']['size'];
    $upload_dir = 'uploads/';

    if(move_uploaded_file($file_tmp, $upload_dir . $file_name)){
        echo "File Uploaded Successfully!";
    } else{
        echo "File Upload Failed...";
    }
}