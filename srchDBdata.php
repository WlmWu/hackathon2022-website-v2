<?php
$GLOBALS["url"] = 'http://10.192.183.197';
$GLOBALS["port"] = '5000';

$GLOBALS["range"] = (isset($_REQUEST["range"]))? $_REQUEST["range"] : -1;
$GLOBALS["unit"] = (isset($_REQUEST["unit"]))? $_REQUEST["unit"] : '';
?>

<?php
function getDataByPost($range, $unit){
    $url = $GLOBALS["url"].':'.$GLOBALS["port"].'/data';
    $data = json_encode(['range' => $range, 'unit' => $unit]);
    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_HEADER, false);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array("Content-type: application/json"));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
    $output = curl_exec($curl);
    curl_close($curl);
    $res = json_decode($output, true);
    // $res = preg_replace_callback('/\\\\u([0-9a-fA-F]{4})/', function ($match) {
    //     return mb_convert_encoding(pack('H*', $match[1]), 'UTF-8', 'UCS-2BE');
    // }, $res);
    // echo 'Output:<br> '.$res;
    return $res;
}
?>

<?php
    echo<<<EOT
    <div class="box" data-aos="fade-up">
        <div class="inboxl"><h2>Detail</h2></div>
        <div class="inboxr"><h2>Image<h2></div>
    </div>
    EOT;
    // $res = getDataByPost(12, 'mon');
    $res = getDataByPost($GLOBALS["range"], $GLOBALS["unit"]);
    foreach($res as $r){
        echo '<div class="box" data-aos="fade-up">';
        
        echo '<div class="inboxl">';
        $msg = $r['msg'];
        $time = $r['time'];
        $ip = $r['ip'];
        $img = $r['img'];
        echo '<p>'.$msg.'</p>';
        echo '<p>'.$time.'</p>';
        echo '<p>'.$ip.'</p>';
        echo '</div>';

        echo '<div class="inboxr">';
        echo "<img src='data:image/png;base64, {$img}' alt='image error' />";
        echo '</div>';

        echo '</div>';
    }
?>