<?php
// Spostato in utils/chapters/ (prima era utils/convert_chapters.php)
// Converte i file txt dei capitoli in JSON per il player

function convert_file($input_filename, $output_filename)
{
    $lines = file($input_filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    // Initialize variables for chapters
    $chapters = array();

    foreach ($lines as $line) {
        // Expected format per line: start end title [optional URL]
        // Capture: start, end, and the rest of the line (title + optional URL)
        if (preg_match('/^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(.+?)\s*$/', $line, $m)) {
            $start = floatval($m[1]);
            $rest  = $m[3];

            // Find URLs in the rest of the line
            $url = null;
            $allUrls = array();
            if (preg_match_all('~https?://\S+~', $rest, $mu)) {
                $allUrls = isset($mu[0]) ? $mu[0] : array();
                if (count($allUrls) > 0) {
                    $url = $allUrls[0]; // use the first URL for url/img field
                }
                // Remove ALL URL tokens from the title chunk
                $rest = preg_replace('~https?://\S+~', '', $rest);
                // Collapse multiple whitespaces and trim
                $rest = trim(preg_replace('/\s+/', ' ', $rest));
            }

            // Prepare chapter entry
            $entry = array('startTime' => $start);

            // Only set title if there is residual non-URL text
            if (strlen($rest) > 0) {
                $entry['title'] = $rest;
            }

            // If URL present, decide whether it's an image or a normal link
            if ($url) {
                if (preg_match('~\.(jpg|jpeg|png|gif|webp|svg)(?:\?.*)?$~i', $url)) {
                    $entry['img'] = $url;
                } else {
                    $entry['url'] = $url;
                }
            }

            $chapters[] = $entry;
        }
    }

    // Sort by startTime to preserve timeline (even if input is unordered)
    usort($chapters, function ($a, $b) {
        $ta = isset($a['startTime']) ? $a['startTime'] : 0;
        $tb = isset($b['startTime']) ? $b['startTime'] : 0;
        if ($ta == $tb) return 0;
        return ($ta < $tb) ? -1 : 1;
    });

    // Write the JSON data to a new file
    file_put_contents($output_filename, json_encode([
        "version" => "1.2.0",
        "chapters" => $chapters
    ]));
}

// Aggiornati i percorsi: ora siamo in utils/chapters, quindi serve salire di due livelli
$inputPath = dirname(__FILE__) . '/../../raw/chapters/';
$outputPath = dirname(__FILE__) . '/../../public/chapters/';

// Opzione CLI: --force per sovrascrivere i JSON esistenti
$force = false;
if (isset($argv) && is_array($argv)) {
    foreach ($argv as $arg) {
        if ($arg === '--force') {
            $force = true;
        }
    }
}

// Convert all files in the raw/chapters directory
$files = glob($inputPath .'*.txt');
foreach ($files as $file) {

    // Determine episode id from input filename
    $episodeId = pathinfo($file, PATHINFO_FILENAME);

    // Output filename
    $outputFilename = $outputPath . 'PIC' . $episodeId . '.json';

    // If output file exists, skip unless --force
    if (file_exists($outputFilename) && !$force) {
        echo "Skipping $file (output exists)\n";
        continue;
    }

    echo "Converting $file" . ($force ? " (force)" : "") . "\n";

    // Convert the file (URLs are now parsed inline within chapter lines)
    convert_file($file, $outputFilename);
}
