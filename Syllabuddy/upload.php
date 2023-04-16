<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file_name = $_FILES['pdf_file']['name'];
    $file_tmp = $_FILES['pdf_file']['tmp_name'];
    $file_type = $_FILES['pdf_file']['type'];
    $file_size = $_FILES['pdf_file']['size'];
    $upload_dir = 'uploads/';

    if(move_uploaded_file($file_tmp, $upload_dir . $file_name)){
        echo "File Uploaded Successfully!\n";   

        // Call PDF_TO_TXT with the uploaded PDF file's path as an argument
        $pdf_path = $upload_dir.$file_name;
        $command = "python Pdf_to_text.py \"$pdf_path\"";
        $output = shell_exec($command);
    

        $file = 'text_file.txt';
        file_put_contents($file, $output);

        echo "<br><br><a href='text_file.txt' download>Download Text File</a>";

        // Redirect back to original page after 5 seconds
        header("Refresh: 3; url=Syllabuddy_2.html");

    } else{
        echo "File Upload Failed...";
        header("Refresh: 3; url=Syllabuddy.html");
    }
}
