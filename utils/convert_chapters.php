<?php
function convert_file($input_filename, $output_filename)
{
    $lines = file($input_filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    // Initialize variables for chapters
    $chapters = array();

    foreach ($lines as $line) {

        // Extract title and time
        preg_match_all('/(\d+\.\d+)\s+(\d+\.\d+)\s+(\D+)/', $line, $matches, PREG_SET_ORDER);

        foreach ($matches as $match) {

            // Add the chapter
            $chapters[] = array(
                'startTime' => floatval($match[1]),
                'title' => trim($match[3])
            );
        }
    }

    // Write the JSON data to a new file
    file_put_contents($output_filename, json_encode([
        "version" => "1.2.0",
        "chapters" => $chapters
    ]));
}

$path = dirname(__FILE__) . '/../public/chapters/';

// Convert all files in the public/chapters directory
$files = glob($path .'*.txt');
foreach ($files as $file) {

    // Output filename
    $outputFilename = $path . pathinfo($file, PATHINFO_FILENAME) . '.json';

    // If output file exists, skip
    if (file_exists($outputFilename)) {
        echo "Skipping $file\n";
        continue;
    }

    echo "Converting $file\n";

    // Convert the file
    convert_file($file, $outputFilename);
}