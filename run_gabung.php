<?php
header('Content-Type: application/json');

$command = escapeshellcmd('python3 /Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/gabung.py');
$output = shell_exec($command);
$return_var = null;
exec($command, $output, $return_var);

if ($return_var !== 0) {
    echo json_encode(['success' => false, 'message' => 'Failed to execute script', 'output' => $output, 'return_var' => $return_var]);
} else {
    echo json_encode(['success' => true, 'message' => 'Script executed successfully', 'output' => $output]);
}
?>
