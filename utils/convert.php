<?php
function convertFile($filename)
{
    $lines = file($filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    // Initialize variables for chapters
    $chapters = array();

    foreach ($lines as $line) {
        // Ignore empty lines
        if (trim($line) == '') continue;

        // Extract title and time
        preg_match_all('/(\d+\.\d+)\s+(\d+\.\d+)\s+([^\d]+)/', $line, $matches, PREG_SET_ORDER);

        foreach ($matches as $match) {
            $startTime = floatval($match[1]);
            $title = trim($match[3]);

            // Add the chapter
            $chapters[] = array(
                'startTime' => $startTime,
                'title' => $title
            );
        }
    }

    $json = json_encode([
        "version" => "1.2.0",
        "chapters" => $chapters
    ]);

    // Output filename
    $outputFilename = dirname(__FILE__).'/../public/chapters/' . pathinfo($filename, PATHINFO_FILENAME) . '.json';

    // Write the JSON data to a new file
    file_put_contents($outputFilename, $json);
}

// Convert all files in the public/chapters directory
$files = glob(dirname(__FILE__).'/../public/chapters/*.txt');
foreach ($files as $file) {

    // If output file exists, skip
    if (file_exists(dirname(__FILE__).'/../public/chapters/' . pathinfo($file, PATHINFO_FILENAME) . '.json')) {
        echo "Skipping $file\n";
        continue;
    }

    echo "Converting $file\n";

    // Convert the file
    convertFile($file);
}